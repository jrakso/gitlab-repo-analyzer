import os
from dotenv import load_dotenv
from gitlab_client import GitlabClient
from repo_cloner import RepoCloner
from repo_analyzer import RepoAnalyzer
import json

load_dotenv()

TOKEN = os.getenv("GITLAB_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

# if TOKEN is None:
#     raise ValueError("GITLAB_TOKEN not set")

# if GROUP_ID is None:
#     raise ValueError("GROUP_ID not set")

# client = GitlabClient(TOKEN)
# projects = client.get_group_projects(GROUP_ID)

OUTPUT_DIR = "repos/anon"

# cloner = RepoCloner()
# cloner.clone_repos(projects, OUTPUT_DIR)

analyzer = RepoAnalyzer()
results = {}
for repo_name in os.listdir(OUTPUT_DIR):
    repo_path = os.path.join(OUTPUT_DIR, repo_name)

    if not os.path.isdir(repo_path):
        continue

    print(f"analyzing {repo_path}...")
    results[repo_name] = analyzer.analyze_repo(repo_path)

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
