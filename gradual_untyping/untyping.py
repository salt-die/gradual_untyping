import ast

from .replacement import Replacement

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

# Remove unused imports

# Clear whitespace

