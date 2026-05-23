from branch import Branch


class BranchTree:
    root: Branch

    def __init__(self, root: Branch) -> None:
        self.root = root

    def print_tree(self) -> None:
        self._print_branch(self.root, 0)

    def _print_branch(self, branch: Branch, depth: int) -> None:
        indent = "  " * depth
        print(f"{indent}{branch.name}")

        for child in branch.children.values():
            self._print_branch(child, depth + 1)