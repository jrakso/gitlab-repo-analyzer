from git import Repo
from pydriller import Repository


class RepoAnalyzer:
    def analyze_repo(self, repo_path: str) -> dict:
        repo = Repo(repo_path)

        branches = self.get_branch_names(repo)

        total_commits = self.get_total_commits(repo_path)
        merge_commits = self.get_merge_commits(repo_path)

        branch_commit_counts = self.get_commits_per_branch(repo, branches)

        return {
            "count": self.get_branch_count(branches),
            "names": branches,
            "is_single_branch": self.is_single_branch(branches),
            "has_branching_activity": self.has_branching_activity(
                branches,
                merge_commits
            ),
            "strategy": self.get_branching_strategy(
                branches,
                merge_commits
            ),
            "total_commits": total_commits,
            "merge_commits": merge_commits,
            "merge_ratio": self.get_merge_ratio(
                merge_commits,
                total_commits
            ),
            "commits_per_branch": branch_commit_counts,
            "avg_commits_per_branch": self.get_avg_commits_per_branch(
                branch_commit_counts
            )
        }

    def get_branch_names(self, repo: Repo) -> list[str]:
        return [branch.name for branch in repo.branches]

    def get_branch_count(self, branches: list[str]) -> int:
        return len(branches)

    def is_single_branch(self, branches: list[str]) -> bool:
        return len(branches) == 1

    def has_branching_activity(self, branches: list[str], merge_commits: int) -> bool:
        return len(branches) > 1 or merge_commits > 0

    def get_branching_strategy(self, branches: list[str], merge_commits: int) -> str:
        if len(branches) == 1 and merge_commits == 0:
            return "no_branching"
        if len(branches) > 1:
            return "multi_branch"
        if merge_commits > 0:
            return "merged_branches"
        return "unknown"

    def get_total_commits(self, repo_path: str) -> int:
        total_commits = 0
        for _ in Repository(repo_path).traverse_commits():
            total_commits += 1
        return total_commits

    def get_merge_commits(self, repo_path: str) -> int:
        merge_commits = 0
        for commit in Repository(repo_path).traverse_commits():
            # Merge commit has multiple parents
            if len(commit.parents) > 1:
                merge_commits += 1
        return merge_commits

    def get_merge_ratio(self, merge_commits: int, total_commits: int) -> float:
        if total_commits == 0:
            return 0
        return merge_commits / total_commits

    def get_commits_per_branch(self, repo: Repo, branches: list[str]) -> dict:
        branch_commit_counts = {}
        for branch in branches:
            commits = list(repo.iter_commits(branch))
            branch_commit_counts[branch] = len(commits)
        return branch_commit_counts

    def get_avg_commits_per_branch(self, branch_commit_counts: dict) -> float:
        if len(branch_commit_counts) == 0:
            return 0
        total = sum(branch_commit_counts.values())
        return total / len(branch_commit_counts)

    def get_contributors_per_branch(self, repo: Repo, branches: list[str]) -> dict:
        contributors_per_branch = {}
        for branch in branches:
            contributors = set()
            for commit in repo.iter_commits(branch):
                contributors.add(commit.author.name)
            contributors_per_branch[branch] = list(contributors)
        return contributors_per_branch
