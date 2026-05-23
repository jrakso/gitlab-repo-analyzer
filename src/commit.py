from __future__ import annotations
from datetime import datetime


class CommitNode:
    hexsha: str
    message: str
    author_email: str
    parents: list[CommitNode]
    children: dict[str, CommitNode]
    is_merge_commit: bool

    def __init__(self, hexsha: str, message: str, author_email: str, created_at: datetime) -> None:
        self.hexsha = hexsha
        self.message = message
        self.author_email = author_email
        self.created_at = created_at
        self.parents = []
        self.children = {}
        self.is_merge_commit = False

    def add_parent(self, parent: CommitNode) -> None:
        for p in self.parents:
            if parent.hexsha == p.hexsha:
                return
        self.parents.append(parent)
        if len(self.parents) > 1:
            self.is_merge_commit = True

    def add_child(self, child: CommitNode) -> None:
        if child.hexsha not in self.children:
            self.children[child.hexsha] = child

    def to_dict(self):
        return {
            "hash": self.hexsha,
            "message": self.message,
            "author_email": self.author_email,
            # "parents": [parent.hexsha for parent in self.parents.values()],
            "is_merge_commit": self.is_merge_commit
        }
