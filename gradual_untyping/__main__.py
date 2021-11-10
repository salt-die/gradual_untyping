"""
Temp file for testing purposes.
"""

from pathlib import Path
from .untyping import _find_annotations

CODE_PATH = Path("code_examples") / "example_1.py"
CODE = CODE_PATH.read_text()

replacements = _find_annotations(CODE)

for replacement in replacements:
    print(replacement)
