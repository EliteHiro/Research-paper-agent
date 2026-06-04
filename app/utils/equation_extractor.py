import re


def extract_equations(text: str):

    patterns = [

        r"[A-Za-z]+\s*=\s*.*",

        r".*\\sum.*",

        r".*\\frac.*",

        r".*\\log.*",

        r".*\\theta.*"
    ]

    equations = []

    lines = text.split("\n")

    for line in lines:

        for pattern in patterns:

            if re.search(pattern, line):

                equations.append(line.strip())

                break

    return list(set(equations))
