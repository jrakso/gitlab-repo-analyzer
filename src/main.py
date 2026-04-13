import os
from dotenv import load_dotenv
from gitlab_client import GitLabClient
from git import Repo

load_dotenv()

TOKEN = os.getenv("GITLAB_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if TOKEN is None:
    raise ValueError("GITLAB_TOKEN not set")

if GROUP_ID is None:
    raise ValueError("GROUP_ID not set")

client = GitLabClient(TOKEN)
projects = client.get_group_projects(GROUP_ID)

OUTPUT_DIR = "repos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for project in projects:
    name = project["name"]
    repo_url = project["ssh_url_to_repo"]

    path = os.path.join(OUTPUT_DIR, name)

    if os.path.exists(path):
        print(f"[SKIP] {name} already exists")
        continue

    print(f"[CLONE] {name}...")

    Repo.clone_from(repo_url, path)

print(repo_url)
