from pydriller import Repository


class RepoAnalyzer:
    def analyze_repo(self, repo_path: str) -> dict:
        authors = {}

        for commit in Repository(repo_path).traverse_commits():
            name = commit.author.name

            if name not in authors:
                authors[name] = {
                    "commits": 0,
                    "insertions": 0,
                    "deletions": 0
                }

            authors[name]["commits"] += 1
            authors[name]["insertions"] += commit.insertions
            authors[name]["deletions"] += commit.deletions

        return authors
