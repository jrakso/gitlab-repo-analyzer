from commit import CommitNode
from datetime import datetime
from datetime import timedelta


class Branch:
    name: str
    branch_tip: CommitNode
    parent_branch: Branch | None
    commits: dict[str, CommitNode]
    merge_commits: dict[str, CommitNode]

    def __init__(self, name: str, branch_tip: CommitNode) -> None:
        self.name = name
        self.branch_tip = branch_tip
        self.parent_branch = None
        self.commits = {}
        self.merge_commits = {}

    def add_commit(self, commit: CommitNode) -> None:
        if commit.hexsha not in self.commits:
            self.commits[commit.hexsha] = commit
            if commit.is_merge_commit:
                self.merge_commits[commit.hexsha] = commit

    def get_number_of_commits(self) -> int:
        return len(self.commits)

    def get_number_of_merge_commits(self) -> int:
        return len(self.merge_commits)

    def get_start_date(self) -> datetime:
        return min(commit.created_at for commit in self.commits.values())

    def get_end_date(self) -> datetime:
        return max(commit.created_at for commit in self.commits.values())

    def get_lifetime(self) -> timedelta:
        return self.get_end_date() - self.get_start_date()

    def has_been_integrated(self) -> bool:
        return bool(self.branch_tip.children)

