import ast

from .replacement import Replacement

__all__ = "untype",

def untype(code):
    replacements = sorted(_find_annotations(code), reverse=True)

    code_lines = code.splitlines()

    for lineno, col_offset, end_lineno, end_col_offset, replace_with, mark, delete_mark in replacements:
        if mark:
            col_offset -= code_lines[lineno][:col_offset][::-1].find(mark) + delete_mark

        code_lines[lineno] = (
            f"{code_lines[lineno][:col_offset]}"
            f"{replace_with}"
            f"{code_lines[end_lineno][end_col_offset:].strip()}"
        ).rstrip()

        code_lines[lineno + bool(code_lines[lineno]): end_lineno + 1] = [ ]

    # EOF Newline.
    if code_lines[-1]:
        code_lines.append("")

    return "\n".join(code_lines)

def _add_pass_if_only_AnnAssigns(node):
    """
    Check for the case of a node body being only `AnnAssign`s. If
    case found, the last `AnnAssign` will be flagged to be replaced with
    `"pass"` instead of `""`.
    """
    for child in node.body:
        if not isinstance(child, ast.AnnAssign):
            break
    else:
        child.replace_with = "pass"

def _find_annotations(code):
    """
    Yield all annotations from code (excepting `AnnAssign`s in `NamedTuple`s and `dataclass`es).
    """
    tree = ast.parse(code)

    for node in ast.walk(tree):
        match node:
            case ast.ClassDef():
                if (
                    any(decorator.id == "dataclass" for decorator in node.decorator_list)
                    or any(base.id == "NamedTuple" for base in node.bases)
                ):
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, ast.AnnAssign):
                            child.is_meta_annotation = True
                else:
                    _add_pass_if_only_AnnAssigns(node)

            case ast.AnnAssign():
                if not getattr(node, "is_meta_annotation", False):
                    yield Replacement.from_node(node)

            case ast.FunctionDef():
                _add_pass_if_only_AnnAssigns(node)

                if annotation := node.returns:
                    yield Replacement.from_node(annotation, mark=")", delete_mark=False)

            case ast.arg():
                if annotation := node.annotation:
                    yield Replacement.from_node(annotation, mark=":", delete_mark=True)
