from git import Repo
from pydriller import Repository


class RepoAnalyzer:
    def analyze_repo(self, repo_path: str) -> dict:
        return self.analyze_branches(repo_path)

    def analyze_branches(self, repo_path: str) -> dict:
        repo = Repo(repo_path)

        branches = [branch.name for branch in repo.branches]

        is_single_branch = len(branches) == 1

        total_commits = 0
        merge_commits = 0

        for commit in Repository(repo_path).traverse_commits():
            total_commits += 1

            # Merge commit has at least two parent commits
            # [Branch A] commit 1 -> MERGE_COMMIT
            # [Branch B] commit 1 -> MERGE_COMMIT
            if len(commit.parents) > 1:
                merge_commits += 1

        has_branching_activity = merge_commits > 0 or len(branches) > 1

        branch_commit_counts = {}

        for branch in branches:
            commits = list(repo.iter_commits(branch))
            branch_commit_counts[branch] = len(commits)

        avg_commits_per_branch = 0

        if len(branch_commit_counts) > 0:
            avg_commits_per_branch = (
                sum(branch_commit_counts.values()) / len(branch_commit_counts)
            )

        merge_ratio = 0

        if total_commits > 0:
            merge_ratio = merge_commits / total_commits

        if is_single_branch and merge_commits == 0:
            strategy = "no_branching"
        elif len(branches) > 1:
            strategy = "multi_branch"
        elif merge_commits > 0:
            strategy = "merged_branches"
        else:
            strategy = "unknown"

        return {
            "count": len(branches),
            "names": branches,
            "is_single_branch": is_single_branch,
            "has_branching_activity": has_branching_activity,
            "strategy": strategy,
            "total_commits": total_commits,
            "merge_commits": merge_commits,
            "merge_ratio": merge_ratio,
            "commits_per_branch": branch_commit_counts,
            "avg_commits_per_branch": avg_commits_per_branch
        }
