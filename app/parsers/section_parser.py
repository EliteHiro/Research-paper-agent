import re


class SectionParser:

    POSSIBLE_SECTIONS = [
        "abstract",
        "introduction",
        "related work",
        "background",
        "methodology",
        "methods",
        "approach",
        "experiments",
        "results",
        "discussion",
        "conclusion",
        "references"
    ]

    def extract_sections(self, text: str):

        sections = {}

        current_section = "unknown"

        lines = text.split("\n")

        for line in lines:

            cleaned = line.strip().lower()

            if cleaned in self.POSSIBLE_SECTIONS:

                current_section = cleaned

                sections[current_section] = []

            sections.setdefault(current_section, [])

            sections[current_section].append(line)

        return {
            key: "\n".join(value)
            for key, value in sections.items()
        }
