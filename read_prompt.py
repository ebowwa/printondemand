from pydantic import BaseModel, FilePath
from typing import Any

class ReadPromptRequest(BaseModel):
    file_path: FilePath

def read_prompt_from_markdown(request: ReadPromptRequest) -> str:
    """
    Read and return the content of a markdown file using Pydantic for input validation.

    Parameters:
    - request: An instance of ReadPromptRequest containing the file path.

    Returns:
    - The content of the file.
    """
    with open(request.file_path, 'r') as file:
        return file.read().strip()