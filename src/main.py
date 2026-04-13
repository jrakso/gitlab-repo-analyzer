import os
from dotenv import load_dotenv
from gitlab_client import GitLabClient

load_dotenv()

TOKEN = os.getenv("GITLAB_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if TOKEN is None or GROUP_ID is None:
    raise ValueError("GITLAB_TOKEN is not set")

client = GitLabClient(TOKEN)
projects = client.get_group_projects(GROUP_ID)

for project in projects:
    print(project["name"])
