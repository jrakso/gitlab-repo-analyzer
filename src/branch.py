from git import Commit
from typing import Any


class Branch:
    name: str
    isDefaultBranch: bool
    merge_base: Commit | None
    branch_tip: Commit | None
    commits: dict[str, Commit]
    merge_commits: dict[str, Commit]
    contributors: set[str]
    commit_count: int
    merge_commit_count: int
    first_commit_time: Any  # datetime.datetime
    last_commit_time: Any   # datetime.datetime
    lifetime: Any

    def __init__(self, branch_name: str, is_default_branch: bool = False) -> None:
        self.name = branch_name
        self.is_default_branch = is_default_branch
        self.merge_base = None
        self.branch_tip = None
        self.commits = {}
        self.merge_commits = {}
        self.contributors = set()
        self.commit_count = 0
        self.merge_commit_count = 0
        self.first_commit_time = None
        self.last_commit_time = None
        self.lifetime = None

    def populate_metrics(self) -> None:
        self.populate_contributors()
        self.populate_merge_commits()
        self.populate_commit_count()
        self.populate_merge_commit_count()
        self.populate_lifetime()

    def populate_contributors(self) -> None:
        for commit in self.commits.values():
            author_name = str(commit.author.name) if commit.author and commit.author.name else "unknown"
            self.contributors.add(author_name)

    def populate_merge_commits(self) -> None:
        for commit in self.commits.values():
            if len(commit.parents) > 1:
                self.merge_commits[commit.hexsha] = commit

    def populate_commit_count(self) -> None:
        self.commit_count = len(self.commits)

    def populate_merge_commit_count(self) -> None:
        self.merge_commit_count = len(self.merge_commits)

    def populate_lifetime(self) -> None:
        times = [commit.committed_datetime for commit in self.commits.values()]
        if times:
            self.first_commit_time = min(times)
            self.last_commit_time = max(times)
            self.lifetime = self.last_commit_time - self.first_commit_time

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "is_default_branch": self.is_default_branch,
            "commit_count": self.commit_count,
            "merge_commit_count": self.merge_commit_count,
            "contributors": list(self.contributors),
            "first_commit_time": self.first_commit_time.isoformat() if self.first_commit_time else None,
            "last_commit_time": self.last_commit_time.isoformat() if self.last_commit_time else None,
            "lifetime": str(self.lifetime) if self.lifetime is not None else None
        }
