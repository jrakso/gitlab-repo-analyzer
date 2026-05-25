from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from commit import CommitNode

if TYPE_CHECKING:
    from contributor import Contributor


class Branch:
    name: str
    branch_tip: CommitNode
    parent_branch: Branch | None
    child_branches: dict[str, Branch]
    commits: dict[str, CommitNode]
    merge_commits: dict[str, CommitNode]
    contributors: dict[str, Contributor]

    def __init__(self, name: str, branch_tip: CommitNode) -> None:
        self.name = name
        self.branch_tip = branch_tip
        self.parent = None
        self.children = {}
        self.commits = {}
        self.merge_commits = {}
        self.contributors = {}

    def add_commit(self, commit: CommitNode) -> None:
        if commit.hexsha not in self.commits:
            self.commits[commit.hexsha] = commit
            if commit.is_merge_commit:
                self.merge_commits[commit.hexsha] = commit

    def add_contributor(self, contributor: Contributor) -> None:
        if contributor.email not in self.contributors:
            self.contributors[contributor.email] = contributor

    def add_parent(self, parent: Branch) -> None:
        if not self.parent:
            self.parent = parent

    def add_child(self, child: Branch) -> None:
        if child.name not in self.children:
            self.children[child.name] = child

    def get_number_of_commits(self) -> int:
        return len(self.commits)

    def get_number_of_merge_commits(self) -> int:
        return len(self.merge_commits)

    def get_number_of_contributors(self) -> int:
        return len(self.contributors)

    def get_number_of_commits_per_contributor(self, contributor: Contributor) -> int:
        return len(contributor.get_commits_in_branch(self))

    def get_number_of_merge_commits_per_contributor(self, contributor: Contributor) -> int:
        return sum(
            1
            for commit in contributor.get_commits_in_branch(self).values()
            if commit.is_merge_commit
        )

    def get_work_ratio_per_contributor(self, contributor: Contributor) -> float:
        return self.get_number_of_commits_per_contributor(contributor) / self.get_number_of_commits()

    def get_start_date(self) -> datetime | None:
        if not self.commits:
            return None
        return min(commit.created_at for commit in self.commits.values())

    def get_end_date(self) -> datetime | None:
        if not self.commits:
            return None
        return max(commit.created_at for commit in self.commits.values())

    def get_lifetime(self) -> timedelta | None:
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        if start_date is None or end_date is None:
            return None
        return end_date - start_date

    def get_lifetime_in_minutes(self) -> float | None:
        lifetime = self.get_lifetime()
        if lifetime is None:
            return None
        return lifetime.total_seconds() / 60

    def get_lifetime_in_hours(self) -> float | None:
        lifetime = self.get_lifetime()
        if lifetime is None:
            return None
        return lifetime.total_seconds() / 3600

    def get_lifetime_in_days(self) -> float | None:
        lifetime = self.get_lifetime()
        if lifetime is None:
            return None
        return lifetime.total_seconds() / 86400
