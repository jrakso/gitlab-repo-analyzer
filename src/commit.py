from datetime import datetime


class CommitNode:
    hexsha: str
    message: str
    parents: dict[str, CommitNode]
    children: dict[str, CommitNode]
    is_merge_commit: bool

    def __init__(self, hexsha: str, message: str, created_at: datetime) -> None:
        self.hexsha = hexsha
        self.message = message
        self.created_at = created_at
        self.parents = {}
        self.children = {}
        self.is_merge_commit = False

    def add_parent(self, parent: CommitNode) -> None:
        if parent.hexsha not in self.parents:
            self.parents[parent.hexsha] = parent
            if len(self.parents) > 1:
                self.is_merge_commit = True

    def add_child(self, child: CommitNode) -> None:
        if child.hexsha not in self.children:
            self.children[child.hexsha] = child
