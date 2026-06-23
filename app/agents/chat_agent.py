from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from app.services.llm_factory import get_llm
from app.prompts.chat_prompt import CHAT_PROMPT
from app.utils.text_utils import truncate_text


class ChatAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", CHAT_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])
        self.chain = self.prompt | self.llm

    def run(self, paper_text: str, question: str, chat_history: list) -> str:
        """
        Answers a question based on the paper text and conversation history.
        """
        # Truncate text to a safe size for the LLM context window 
        # (Using a slightly larger window for chat to capture more context)
        truncated_text = truncate_text(paper_text, max_chars=40000)
        
        # Convert simple history dicts to Langchain Message objects
        formatted_history = []
        for msg in chat_history:
            if msg["role"] == "user":
                formatted_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(AIMessage(content=msg["content"]))

        result = self.chain.invoke({
            "paper_text": truncated_text,
            "question": question,
            "history": formatted_history
        })
        
        return result.content
