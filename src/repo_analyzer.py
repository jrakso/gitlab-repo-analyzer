from typing import Any
from git import Repo
import os
import json
from commit import CommitNode
from branch import Branch
from contributor import Contributor
from branch_tree import BranchTree

UNKNOWN = "unknown"


class RepoAnalyzer:

    def analyze_repo(self, repo_path: str) -> dict[str, Any]:
        repo = Repo(repo_path)

        commits = self.create_commit_nodes(repo)
        contributors = self.create_contributors(repo, commits)
        branches = self.create_branches(repo, commits)

        self.populate_branches(repo, branches, commits, contributors)

        for branch in branches.values():
            print(f"-------------- {branch.name} ------------------")
            print(f"parent: {branch.parent.name if branch.parent else "none"}")
        trees = self.create_branch_trees(branches)
        for tree in trees:
            tree.print_tree()

        return {
            "total_commits": len(commits),
            "total_merge_commits": sum(
                1
                for commit in commits.values()
                if commit.is_merge_commit
            ),
            "total_branches": len(branches),
            # "branch_names": [branch.name for branch in branches.values()],
            "branches": [branch.to_dict() for branch in branches.values()],
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

    def assign_parent_branch(self, child: Branch, parents: dict[str, Branch], merge_base: CommitNode) -> None:
        for parent in parents.values():
            if parent == child:
                continue
            if merge_base.hexsha in parent.commits:
                child.add_parent(parent)
                parent.add_child(child)
                return

    def populate_branches(self,
                          repo: Repo,
                          branches: dict[str, Branch],
                          commits: dict[str, CommitNode],
                          contributors: dict[str, Contributor],
                          root: str = "main") -> None:
        # Used as merge bases
        assigned_nodes = {}

        # Assign to main first
        if root in branches:
            mainline = branches[root]
            for commit in repo.iter_commits(root, first_parent=True):
                mainline.add_commit(commits[commit.hexsha])
                mainline.add_contributor(contributors[commit.author.email or UNKNOWN])
                assigned_nodes[commit.hexsha] = commit

        # Assign to feature branches
        for branch in branches.values():
            if branch.name == root:  # Already populated
                continue

            # Traverse branch, first parent only
            for commit in repo.iter_commits(branch.name, first_parent=True):
                if commit.hexsha in assigned_nodes:  # Merge base reached
                    # Assign parent and stop adding commits to branch
                    self.assign_parent_branch(branch, branches, commits[commit.hexsha])
                    break

                # Add commit and contributor to branch
                branch.add_commit(commits[commit.hexsha])
                branch.add_contributor(contributors[commit.author.email or UNKNOWN])
                assigned_nodes[commit.hexsha] = commit

    def create_branch_trees(self, branches: dict[str, Branch]) -> list[BranchTree]:
        trees = []
        for branch in branches.values():
            if not branch.parent:
                tree = BranchTree(branch)
                trees.append(tree)
        return trees


analyzer = RepoAnalyzer()
result = analyzer.analyze_repo(os.path.join("repos/anon", "repo_09"))
# trees = analyzer.create_branch_trees(self, )
# print(json.dumps(result, indent=4))
