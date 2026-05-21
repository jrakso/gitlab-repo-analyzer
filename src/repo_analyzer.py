from typing import Any
from git import Repo
import os
import json
from commit import CommitNode
from branch import Branch
from contributor import Contributor

UNKNOWN = "unknown"


class RepoAnalyzer:

    def analyze_repo(self, repo_path: str) -> dict[str, Any]:
        repo = Repo(repo_path)

        commits = self.create_commit_nodes(repo)
        contributors = self.create_contributors(repo, commits)
        branches = self.create_branches(repo, commits)

        # self.assign_parent_branches(repo, branches)
        # self.populate_branches(repo, branches, commits, contributors)

        return {
            "total_commits": len(commits),
            "total_merge_commits": sum(
                1
                for commit in commits.values()
                if commit.is_merge_commit
            ),
            "total_branches": len(branches),
            # "branch_names": [branch.name for branch in branches.values()],
            # "branches": [branch.to_dict() for branch in branches.values()],
            "total_contributors": len(contributors),
            # "contributors": [contributor.email for contributor in contributors.values()]
        }

    def create_commit_nodes(self, repo: Repo) -> dict[str, CommitNode]:
        nodes = {}
        # Create nodes
        for commit in repo.iter_commits("--all"):
            if commit.hexsha not in nodes:
                nodes[commit.hexsha] = CommitNode(
                    commit.hexsha, str(commit.message.strip()),
                    commit.author.email or UNKNOWN,
                    commit.committed_datetime
                )
        # Connect parents
        for commit in repo.iter_commits("--all"):
            node = nodes[commit.hexsha]
            for parent in commit.parents:
                node.add_parent(nodes[parent.hexsha])
                nodes[parent.hexsha].add_child(node)
        return nodes

    def create_contributors(self, repo: Repo, nodes: dict[str, CommitNode]) -> dict[str, Contributor]:
        contributors = {}
        for commit in repo.iter_commits("--all"):
            email = commit.author.email or UNKNOWN
            name = commit.author.name or UNKNOWN
            if email not in contributors:
                contributors[email] = Contributor(email, name)
            contributors[email].add_commit(nodes[commit.hexsha])
        return contributors

    def create_branches(self, repo: Repo, commit_nodes: dict[str, CommitNode]) -> dict[str, Branch]:
        branches = {}
        for branch in repo.branches:
            branch_tip = repo.commit(branch.name)
            branches[branch.name] = Branch(branch.name, commit_nodes[branch_tip.hexsha])
        return branches

    def assign_parent_branches(self, repo: Repo, branches: dict[str, Branch], root: str = "main") -> None:
        # Iterate over each branch
        for branch in branches.values():
            if branch.name == root:
                continue

            # Parent branch candidates
            candidates = []

            # Iterate over all the possible parent branches
            for parent_branch in branches.values():
                if parent_branch == branch:
                    continue

                # Find merge base between current branch and current parent branch
                merge_bases = repo.merge_base(parent_branch.name, branch.name)

                # If no merge base exists cant be parent, on to next possible parent branch
                if not merge_bases:
                    continue

                # Merge base
                base = merge_bases[0]

                # Number of commits on current branch not reachable from merge base
                dist = sum(1 for _ in repo.iter_commits(f"{base.hexsha}..{branch.name}"))

                # First parent penalty
                fp_penalty = 1
                for commit in repo.iter_commits(parent_branch.name, first_parent=True):
                    if commit.hexsha == base.hexsha:
                        fp_penalty = 0
                        break

                # Root penalty (prefer main as parent if multiple parent branches equally good)
                root_penalty = 1
                if parent_branch.name == root:
                    root_penalty = 0

                candidates.append((dist, fp_penalty, root_penalty, parent_branch))

            if candidates:
                # 1. Prioritize lowest distance
                # 2. If distance equal prioritize parent with no first parent penalty
                # 3. If all else equal choose root (main)
                candidates.sort(key=lambda item: (item[0], item[1], item[2]))
                for i in range(len(candidates)):
                    best_parent = candidates[i][3]
                    if len(candidates) > 1:
                        if best_parent.parent_branch and best_parent.parent_branch == branch:
                            pass
                    else:
                        if best_parent.parent_branch:
                            pass
                        break

                branch.parent_branch = best_parent

    def populate_branches(self,
                          repo: Repo,
                          branches: dict[str, Branch],
                          commits: dict[str, CommitNode],
                          contributors: dict[str, Contributor]) -> None:

        for branch in branches.values():

            # Mainline
            if branch.parent_branch is None:
                for commit in repo.iter_commits(branch.name, first_parent=True):
                    branch.add_commit(commits[commit.hexsha])
                    branch.add_contributor(contributors[commits[commit.hexsha].author_email])

            # Feature branches
            else:
                parent_first_parent_commits = {
                    commit.hexsha
                    for commit in repo.iter_commits(branch.parent_branch.name, first_parent=True)
                }

                for commit in repo.iter_commits(branch.name, first_parent=True):
                    if commit.hexsha not in parent_first_parent_commits:
                        branch.add_commit(commits[commit.hexsha])
                        branch.add_contributor(contributors[commits[commit.hexsha].author_email])


# analyzer = RepoAnalyzer()
# result = analyzer.analyze_repo(os.path.join("repos", "anon4"))
# print(json.dumps(result, indent=4))
