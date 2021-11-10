import ast

from .replacement import Replacement

__all__ = "untype",

def untype(code):
    return _replace_annotations(
        _find_annotations(code),
        code,
    )

def _add_pass_if_only_AnnAssign(node):
    """
    Check for the case of a node body being only `AnnAssign` and, if found,
    add an instruction for the last replacement to replace with `"pass"`
    instead of `""`.
    """
    for child in node.body:
        if not isinstance(child, ast.AnnAssign):
            break
    else:
        child.replace_with = "pass"

def _find_annotations(code):
    """
    Find all annotations (excepting AnnAssigns in NamedTuples and dataclasses).
    """
    tree = ast.parse(code)

    annotations = [ ]

    for node in ast.walk(tree):
        match node:
            case ast.ClassDef():
                ignore_ann_assign = False

                for decorator in node.decorator_list:
                    if decorator.id == "dataclass":
                        ignore_ann_assign = True
                        break
                else:
                    for base in node.bases:
                        if base.id == "NamedTuple":
                            ignore_ann_assign = True
                        break

                if ignore_ann_assign:
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, ast.AnnAssign):
                            child.ignore_me = True
                else:
                    _add_pass_if_only_AnnAssign(node)

            case ast.AnnAssign():
                if not getattr(node, "ignore_me", False):
                    annotations.append( Replacement.from_node(node, ast.AnnAssign, code) )

            case ast.FunctionDef():
                _add_pass_if_only_AnnAssign(node)

                if anno := node.returns:
                    annotations.append( Replacement.from_node(anno, ast.FunctionDef, code) )

            case ast.arg():
                if anno := node.annotation:
                    annotations.append( Replacement.from_node(anno, ast.arg, code) )

    return sorted(annotations, reverse=True)

def _replace_annotations(replacements, code):
    """
    Delete or replace annotations in code.
    """
    code_lines = code.splitlines()

    for lineno, col_offset, end_lineno, end_col_offset, _, type, replace_with in replacements:
        match type:
            case ast.FunctionDef:
                reverse = code_lines[lineno][:col_offset][::-1]
                where_close_parens = reverse.find(")")
                offset_adjust = len(reverse[:where_close_parens])
                col_offset -= offset_adjust
            case ast.arg:
                reverse = code_lines[lineno][:col_offset][::-1]
                where_colon = reverse.find(":")
                offset_adjust = len(reverse[:where_colon + 1])
                col_offset -= offset_adjust

        if lineno == end_lineno:
            line = code_lines[lineno]
            code_lines[lineno] = f"{line[:col_offset]}{replace_with}{line[end_col_offset:]}"
        else:
            code_lines[lineno] = f"{code_lines[lineno][:col_offset]}{replace_with}"
            code_lines[i: end_lineno] = []
            code_lines[end_lineno] = code_lines[end_lineno][end_col_offset:]

            if code_lines[end_lineno].ispace():
                del code_lines[end_lineno]

        if not code_lines[lineno] or code_lines[lineno].isspace():
            del code_lines[lineno]

    # EOF Newline.
    if code_lines[-1]:
        code_lines.append("")

    return "\n".join(code_lines)
