import sqlite3
import json
import os
import uuid
from typing import Dict, List, Any


class DBService:
    def __init__(self, db_path: str = "papers.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database and creates the necessary tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create papers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                pdf_text TEXT,
                summary TEXT,
                key_points TEXT,
                contributions TEXT,
                limitations TEXT,
                equation_explanations TEXT,
                journal_notes TEXT,
                diagram_xml TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_paper(self, filename: str, pdf_text: str, analysis_result: Dict[str, Any]) -> str:
        """Saves a paper analysis into the database. Returns the unique paper ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        paper_id = str(uuid.uuid4())
        
        # Convert lists and dicts to JSON strings for storage
        key_points = json.dumps(analysis_result.get("key_points", []))
        contributions = json.dumps(analysis_result.get("contributions", []))
        limitations = json.dumps(analysis_result.get("limitations", []))
        equation_explanations = json.dumps(analysis_result.get("equation_explanations", []))
        
        summary = analysis_result.get("summary", "")
        journal_notes = analysis_result.get("journal_notes", "")
        diagram_xml = analysis_result.get("diagram_xml", "")
        
        cursor.execute('''
            INSERT INTO papers (
                id, filename, pdf_text, summary, key_points, contributions, 
                limitations, equation_explanations, journal_notes, diagram_xml
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            paper_id, filename, pdf_text, summary, key_points, contributions,
            limitations, equation_explanations, journal_notes, diagram_xml
        ))
        
        conn.commit()
        conn.close()
        
        return paper_id

    def get_all_papers(self) -> List[Dict[str, Any]]:
        """Retrieves a list of all saved papers (basic metadata)."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, filename, created_at FROM papers ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        papers = []
        for row in rows:
            papers.append({
                "id": row["id"],
                "filename": row["filename"],
                "created_at": row["created_at"]
            })
            
        conn.close()
        return papers

    def get_paper(self, paper_id: str) -> Dict[str, Any]:
        """Retrieves the full analysis result and text for a specific paper."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM papers WHERE id = ?', (paper_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        # Reconstruct the analysis_result dictionary
        result = {
            "summary": row["summary"],
            "key_points": json.loads(row["key_points"]) if row["key_points"] else [],
            "contributions": json.loads(row["contributions"]) if row["contributions"] else [],
            "limitations": json.loads(row["limitations"]) if row["limitations"] else [],
            "equation_explanations": json.loads(row["equation_explanations"]) if row["equation_explanations"] else [],
            "journal_notes": row["journal_notes"],
            "diagram_xml": row["diagram_xml"]
        }
        
        return {
            "id": row["id"],
            "filename": row["filename"],
            "pdf_text": row["pdf_text"],
            "created_at": row["created_at"],
            "analysis_result": result
        }

    def delete_paper(self, paper_id: str) -> bool:
        """Deletes a paper from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM papers WHERE id = ?', (paper_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return deleted

# Create a singleton instance
db = DBService()
