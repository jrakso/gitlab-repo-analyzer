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
