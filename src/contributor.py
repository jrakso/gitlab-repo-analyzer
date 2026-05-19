from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from branch import Branch

from commit import CommitNode


class Contributor:
    email: str
    name: str
    commits: dict[str, CommitNode]
    merge_commits: dict[str, CommitNode]

    def __init__(self, email, name) -> None:
        self.email = email
        self.name = name
        self.commits = {}
        self.merge_commits = {}

    def add_commit(self, commit: CommitNode) -> None:
        if commit.hexsha not in self.commits:
            self.commits[commit.hexsha] = commit
            if commit.is_merge_commit:
                self.merge_commits[commit.hexsha] = commit

    def get_commits_in_branch(self, branch: Branch) -> dict[str, CommitNode]:
        commits_in_branch = {}
        for commit in branch.commits.values():
            if commit.hexsha in self.commits and commit.hexsha not in commits_in_branch:
                commits_in_branch[commit.hexsha] = commit
        return commits_in_branch
