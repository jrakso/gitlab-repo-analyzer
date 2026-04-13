import os
from git import Repo


class RepoCloner:
    def clone_repos(self, projects: list[dict], output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)

        for project in projects:
            name = project["name"]
            repo_url = project["ssh_url_to_repo"]

            path = os.path.join(output_dir, name)

            if os.path.exists(path):
                print(f"[SKIP] {name} already exists")
                continue

            print(f"[CLONE] {name} → {path}")

            Repo.clone_from(repo_url, path)
