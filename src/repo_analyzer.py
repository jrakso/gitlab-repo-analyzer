from typing import Any
from git import Repo
import os
import json
from commit import CommitNode
from branch import Branch
from contributor import Contributor
from branch_tree import BranchTree
import statistics

UNKNOWN = "unknown"


class RepoAnalyzer:

    def analyze_repo(self, repo_path: str) -> dict[str, Any]:
        repo = Repo(repo_path)

        commits = self.create_commit_nodes(repo)
        contributors = self.create_contributors(repo, commits)
        branches = self.create_branches(repo, commits)

        self.populate_branches(repo, branches, commits, contributors, self.get_main_branch_name(branches))

        for branch in branches.values():
            print(f"-------------- {branch.name} ------------------")
            print(f"parent: {branch.parent.name if branch.parent else "none"}")
        trees = self.create_branch_trees(branches)
        for tree in trees:
            tree.print_tree()

        repo_name = os.path.basename(repo_path)
        return self.get_results(repo, repo_name, branches, commits, contributors, self.get_main_branch_name(branches))

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

    def get_main_branch_name(self, branches: dict[str, Branch]) -> str | None:
        return "main" if "main" in branches else "master" if "master" in branches else None

    def populate_branches(self,
                          repo: Repo,
                          branches: dict[str, Branch],
                          commits: dict[str, CommitNode],
                          contributors: dict[str, Contributor],
                          root: None | str = "main") -> None:
        # Used as merge bases
        assigned_nodes = {}

        # Assign to main first
        if root and root in branches:
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

    def is_merged_to_main(self, repo: Repo, branch: Branch, main_branch: Branch) -> bool:
        return repo.is_ancestor(repo.commit(branch.name), repo.commit(main_branch.name))

    def is_directly_merged_to_main(self, branch: Branch, main_branch: Branch) -> bool:
        for merge_commit in main_branch.merge_commits.values():
            for parent in merge_commit.parents[1:]:
                if parent.hexsha == branch.branch_tip.hexsha:
                    return True
        return False

    def is_directly_merged_to_other_branch(self,
                                           branch: Branch,
                                           branches: dict[str, Branch],
                                           main_branch: Branch | None) -> bool:
        for other_branch in branches.values():
            if other_branch is main_branch or other_branch is branch:
                continue
            for merge_commit in other_branch.merge_commits.values():
                for parent in merge_commit.parents[1:]:
                    if parent.hexsha == branch.branch_tip.hexsha:
                        return True
        return False

    def get_results(self,
                    repo: Repo,
                    repo_name: str,
                    branches: dict[str, Branch],
                    commits: dict[str, CommitNode],
                    contributors: dict[str, Contributor],
                    root: None | str = "main") -> dict[str, Any]:

        total_commits = len(commits)
        total_merge_commits = sum(1 for commit in commits.values() if commit.is_merge_commit)
        total_regular_commits = total_commits - total_merge_commits

        main_branch_name = root
        total_detected_branches = len(branches)
        has_main_branch = bool(main_branch_name)

        main_branch = None
        if main_branch_name:
            main_branch = branches[main_branch_name]

        # In this code, "branch" means a branch excluding main/master.
        # If no main/master exists, all detected branches are treated as regular branches.
        branch_count = total_detected_branches - 1 if main_branch else total_detected_branches

        total_contributors = len(contributors)

        commits_on_main_branch = None
        regular_commits_on_main_branch = None
        merge_commits_on_main_branch = None

        if main_branch:
            commits_on_main_branch = len(main_branch.commits)
            regular_commits_on_main_branch = len(main_branch.commits) - len(main_branch.merge_commits)
            merge_commits_on_main_branch = len(main_branch.merge_commits)

        commits_on_branches = 0
        regular_commits_on_branches = 0
        merge_commits_on_branches = 0

        commits_per_branch = []
        regular_commits_per_branch = []
        merge_commits_per_branch = []
        contributors_per_branch = []
        lifetime_per_branch = []

        branches_with_parent_main = 0
        branches_with_parent_other = 0
        branches_with_no_parent = 0

        directly_merged_to_main_count = 0
        indirectly_merged_to_main_count = 0
        merged_to_main_count = 0
        not_merged_to_main_count = 0

        directly_merged_to_other_branch_count = 0

        for branch in branches.values():
            if branch == main_branch:
                continue

            branch_commits = len(branch.commits)
            branch_merge_commits = len(branch.merge_commits)
            branch_regular_commits = branch_commits - branch_merge_commits

            commits_on_branches += branch_commits
            merge_commits_on_branches += branch_merge_commits
            regular_commits_on_branches += branch_regular_commits

            commits_per_branch.append(branch_commits)
            merge_commits_per_branch.append(branch_merge_commits)
            regular_commits_per_branch.append(branch_regular_commits)
            contributors_per_branch.append(len(branch.contributors))

            lifetime = branch.get_lifetime_in_hours()
            if lifetime is not None:
                lifetime_per_branch.append(lifetime)

            if main_branch:
                if branch.parent == main_branch:
                    branches_with_parent_main += 1
                elif branch.parent is not None:
                    branches_with_parent_other += 1
                else:
                    branches_with_no_parent += 1
            else:
                if branch.parent is not None:
                    branches_with_parent_other += 1
                else:
                    branches_with_no_parent += 1

            if main_branch:
                if self.is_merged_to_main(repo, branch, main_branch):
                    if self.is_directly_merged_to_main(branch, main_branch):
                        directly_merged_to_main_count += 1
                    else:
                        indirectly_merged_to_main_count += 1

                    merged_to_main_count += 1
                else:
                    not_merged_to_main_count += 1

            if self.is_directly_merged_to_other_branch(branch, branches, main_branch):
                directly_merged_to_other_branch_count += 1

        median_commits_per_branch = (
            statistics.median(commits_per_branch) if commits_per_branch else 0
        )
        min_commits_on_a_branch = min(commits_per_branch) if commits_per_branch else 0
        max_commits_on_a_branch = max(commits_per_branch) if commits_per_branch else 0

        median_regular_commits_per_branch = (
            statistics.median(regular_commits_per_branch) if regular_commits_per_branch else 0
        )
        min_regular_commits_on_a_branch = (
            min(regular_commits_per_branch) if regular_commits_per_branch else 0
        )
        max_regular_commits_on_a_branch = (
            max(regular_commits_per_branch) if regular_commits_per_branch else 0
        )

        median_merge_commits_per_branch = (
            statistics.median(merge_commits_per_branch) if merge_commits_per_branch else 0
        )
        min_merge_commits_on_a_branch = (
            min(merge_commits_per_branch) if merge_commits_per_branch else 0
        )
        max_merge_commits_on_a_branch = (
            max(merge_commits_per_branch) if merge_commits_per_branch else 0
        )

        median_lifetime_hours_per_branch = (
            statistics.median(lifetime_per_branch) if lifetime_per_branch else 0
        )

        median_contributors_per_branch = (
            statistics.median(contributors_per_branch) if contributors_per_branch else 0
        )

        single_author_branches = sum(
            1
            for contributor_count in contributors_per_branch
            if contributor_count == 1
        )

        return {
            "repo_name": repo_name,

            "total_commits": total_commits,
            "total_regular_commits": total_regular_commits,
            "total_merge_commits": total_merge_commits,
            "total_merge_commit_ratio": (
                total_merge_commits / total_commits
                if total_commits > 0
                else 0
            ),

            "total_contributors": total_contributors,

            # All detected Git branches, including main/master if present.
            "total_detected_branches": total_detected_branches,

            # Main/default branch metrics.
            "has_main_branch": has_main_branch,
            "main_branch_name": main_branch_name,
            "commits_on_main_branch": commits_on_main_branch,
            "regular_commits_on_main_branch": regular_commits_on_main_branch,
            "merge_commits_on_main_branch": merge_commits_on_main_branch,
            "main_branch_regular_commit_ratio": (
                regular_commits_on_main_branch / commits_on_main_branch
                if regular_commits_on_main_branch is not None
                and commits_on_main_branch is not None
                and commits_on_main_branch > 0
                else None
            ),
            "main_branch_regular_commits_share_of_total": (
                regular_commits_on_main_branch / total_commits
                if regular_commits_on_main_branch is not None
                and total_commits > 0
                else None
            ),
            "main_branch_merge_commits_share_of_total": (
                merge_commits_on_main_branch / total_merge_commits
                if merge_commits_on_main_branch is not None
                and total_merge_commits > 0
                else None
            ),

            # Branch metrics.
            # Here, "branch" means non-main/default branch.
            # If no main/master branch exists, this includes all detected branches.
            "branch_count": branch_count,
            "branch_metrics_include_all_detected_branches": not has_main_branch,

            "branches_per_100_commits": (
                branch_count / total_commits * 100
                if total_commits > 0
                else 0
            ),

            "commits_on_branches": commits_on_branches,
            "regular_commits_on_branches": regular_commits_on_branches,
            "merge_commits_on_branches": merge_commits_on_branches,

            "branches_merge_commits_share_of_total": (
                merge_commits_on_branches / total_merge_commits if total_merge_commits > 0 else 0
            ),

            "branches_commits_share_of_total": (
                commits_on_branches / total_commits
                if total_commits > 0
                else 0
            ),
            "branches_regular_commits_share_of_total": (
                regular_commits_on_branches / total_regular_commits
                if total_regular_commits > 0
                else 0
            ),

            "median_commits_per_branch": median_commits_per_branch,
            "min_commits_on_a_branch": min_commits_on_a_branch,
            "max_commits_on_a_branch": max_commits_on_a_branch,

            "median_regular_commits_per_branch": median_regular_commits_per_branch,
            "min_regular_commits_on_a_branch": min_regular_commits_on_a_branch,
            "max_regular_commits_on_a_branch": max_regular_commits_on_a_branch,

            "median_merge_commits_per_branch": median_merge_commits_per_branch,
            "min_merge_commits_on_a_branch": min_merge_commits_on_a_branch,
            "max_merge_commits_on_a_branch": max_merge_commits_on_a_branch,

            "median_lifetime_hours_per_branch": median_lifetime_hours_per_branch,

            "median_contributors_per_branch": median_contributors_per_branch,

            "single_author_branches": single_author_branches,
            "single_author_branch_ratio": (
                single_author_branches / branch_count
                if branch_count > 0
                else 0
            ),

            # Merge-to-main metrics.
            # These are None if no main/master branch exists.
            "branches_directly_merged_to_main": (
                directly_merged_to_main_count
                if main_branch
                else None
            ),
            "branches_indirectly_merged_to_main": (
                indirectly_merged_to_main_count
                if main_branch
                else None
            ),
            "branches_merged_to_main": (
                merged_to_main_count
                if main_branch
                else None
            ),
            "branches_not_merged_to_main": (
                not_merged_to_main_count
                if main_branch
                else None
            ),
            "merged_to_main_branch_ratio": (
                merged_to_main_count / branch_count
                if main_branch and branch_count > 0
                else None
            ),
            "directly_merged_to_main_branch_ratio": (
                directly_merged_to_main_count / branch_count
                if main_branch and branch_count > 0
                else None
            ),
            "indirectly_merged_to_main_branch_ratio": (
                indirectly_merged_to_main_count / branch_count
                if main_branch and branch_count > 0
                else None
            ),

            # Inferred branch structure metrics.
            "inferred_branches_from_main": (
                branches_with_parent_main
                if main_branch
                else None
            ),
            "inferred_branches_with_no_parent": branches_with_no_parent,
            "inferred_nested_branches": branches_with_parent_other,
            "inferred_nested_branch_ratio": (
                branches_with_parent_other / branch_count
                if branch_count > 0
                else 0
            )
        }


analyzer = RepoAnalyzer()
result = analyzer.analyze_repo(os.path.join("repos/anon", "repo_09"))
# trees = analyzer.create_branch_trees(self, )
print(json.dumps(result, indent=4))
