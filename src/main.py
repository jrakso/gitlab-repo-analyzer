import os
from dotenv import load_dotenv
from gitlab_client import GitlabClient
from repo_cloner import RepoCloner
from pydriller import Repository

load_dotenv()

TOKEN = os.getenv("GITLAB_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if TOKEN is None:
    raise ValueError("GITLAB_TOKEN not set")

if GROUP_ID is None:
    raise ValueError("GROUP_ID not set")

client = GitlabClient(TOKEN)
projects = client.get_group_projects(GROUP_ID)

OUTPUT_DIR = "repos"

cloner = RepoCloner()
cloner.clone_repos(projects, OUTPUT_DIR)
