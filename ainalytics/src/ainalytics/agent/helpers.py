import re


def extract_raw_code(code_block: str) -> str:
    """
    Extracts raw code from a Markdown-style code block.
    Removes triple backticks and optional language specifier.

    Args:
        code_block (str): A string containing a Markdown code block.

    Returns:
        str: The raw code without the code block markers.
    """
    # Use regex to remove the code block markers
    raw_code = re.sub(r"^```[a-z]*\n", "", code_block, flags=re.MULTILINE)
    raw_code = re.sub(r"\n```$", "", raw_code, flags=re.MULTILINE)
    return raw_code
