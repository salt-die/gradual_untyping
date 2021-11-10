"""
Temp file for testing purposes.
"""

from pathlib import Path
from .untyping import untype

EXAMPLES_PATH = Path("code_examples")
CODE_PATH = EXAMPLES_PATH / "example_1.py"
CLEANED_CODE_PATH = EXAMPLES_PATH / "cleaned_example_1.py"

CODE = CODE_PATH.read_text()

CLEANED_CODE_PATH.write_text(untype(CODE))
