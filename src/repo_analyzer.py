from git import Repo, Commit
from branch import Branch
from typing import Any


class RepoAnalyzer:

    def analyze_repo(self, repo_path: str) -> dict[str, Any]:
        repo = Repo(repo_path)

        branch_names = self.get_branch_names(repo)
        default_branch_name = self.get_default_branch_name(repo)

        branches = self.create_branch_objects(branch_names, default_branch_name)

        self.build_branches(repo, branches, default_branch_name)

        total_commits = self.get_all_commits(repo, branches)

        total_merge_commits = self.get_all_merge_commits(repo, branches)

        return {
            "total_commits": len(total_commits),
            "total_merge_commits": len(total_merge_commits),
            "total_branches": len(branches),
            "default_branch": default_branch_name,
            "branches": [
                [name, branch.to_dict()]
                for name, branch in branches.items()
            ]
        }

    def get_branch_names(self, repo: Repo) -> list[str]:
        return [branch.name for branch in repo.branches]

    def get_default_branch_name(self, repo: Repo) -> str:
        return repo.active_branch.name

    def create_branch_objects(self, branch_names: list[str], default_branch_name: str) -> dict[str, Branch]:
        branches = {}
        for branch_name in branch_names:
            branches[branch_name] = Branch(branch_name, branch_name == default_branch_name)
        return branches

    def populate_mainline_commits(self, repo: Repo, branch: Branch) -> None:
        branch.branch_tip = repo.commit(branch.name)
        for commit in repo.iter_commits(branch.name, first_parent=True):
            branch.commits[commit.hexsha] = commit

    def populate_branch_commits(self, repo: Repo, branch: Branch, mainline: Branch) -> None:
        branch.branch_tip = repo.commit(branch.name)
        for commit in repo.iter_commits(branch.name, first_parent=True):
            if commit.hexsha in mainline.commits:
                branch.merge_base = commit
                break
            branch.commits[commit.hexsha] = commit

    def build_branches(self, repo: Repo, branches: dict[str, Branch], default_branch_name: str) -> None:
        default_branch = branches[default_branch_name]

        # Populate Branch objects with commits.
        # We populate mainline first since populate_branch_commits
        # uses mainline commits as merge base
        self.populate_mainline_commits(repo, default_branch)
        for branch in branches.values():
            if not branch.is_default_branch:
                self.populate_branch_commits(repo, branch, default_branch)
            branch.populate_metrics()

    def get_all_commits(self, repo: Repo, branches: dict[str, Branch]) -> dict[str, Commit]:
        commits = {}
        for branch in branches.values():
            for hexsha, commit in branch.commits.items():
                commits[hexsha] = commit
        return commits

    def get_all_merge_commits(self, repo: Repo, branches: dict[str, Branch]) -> dict[str, Commit]:
        merge_commits = {}
        for branch in branches.values():
            for hexsha, merge_commit in branch.merge_commits.items():
                merge_commits[hexsha] = merge_commit
        return merge_commits
