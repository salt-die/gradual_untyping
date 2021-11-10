"""
Temp file for testing purposes.
"""
from pathlib import Path
from .untype import untype

NEXAMPLES = 3
EXAMPLES_PATH = Path("code_examples")

for n in range(1, NEXAMPLES + 1):
    code_path = EXAMPLES_PATH / f"example_{n}.py"
    code = code_path.read_text()

    cleaned_code_path = EXAMPLES_PATH / f"example_{n}(cleaned).py"
    cleaned_code_path.write_text(untype(code))
