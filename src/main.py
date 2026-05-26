import os
import json
import csv

from dotenv import load_dotenv

# from gitlab_client import GitlabClient
# from repo_cloner import RepoCloner
from repo_analyzer import RepoAnalyzer

# load_dotenv()

# TOKEN = os.getenv("GITLAB_TOKEN")
# GROUP_ID = os.getenv("GROUP_ID")

# if TOKEN is None:
#     raise ValueError("GITLAB_TOKEN not set")

# if GROUP_ID is None:
#     raise ValueError("GROUP_ID not set")

# client = GitlabClient(TOKEN)
# projects = client.get_group_projects(GROUP_ID)

# OUTPUT_DIR = "repos/anon"

# cloner = RepoCloner()
# cloner.clone_repos(projects, OUTPUT_DIR)

RELEVANT_METRICS = [
    "repo_name",
    "total_commits",
    "total_merge_commits",
    "total_regular_commits",
    "total_contributors",
    "total_detected_branches",
    "has_main_branch",

    "main_branch_commits_share_of_total",
    "main_branch_merge_commit_ratio",

    "branch_count",
    "branches_per_100_commits",
    "branches_commits_share_of_total",
    "median_commits_per_branch",
    "min_commits_on_a_branch",
    "max_commits_on_a_branch",
    "median_lifetime_hours_per_branch",

    "median_contributors_per_branch",
    "single_author_branch_ratio",

    "total_merge_commit_ratio",
    "main_branch_merge_commits_share_of_total",
    "branches_merge_commits_share_of_total",

    "total_regular_commit_ratio",
    "main_branch_regular_commits_share_of_total",
    "branches_regular_commits_share_of_total",

    "merged_to_main_branch_ratio",
    "directly_merged_to_main_branch_ratio",
]


def write_results_to_csv(results: dict[str, dict], output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=RELEVANT_METRICS)
        writer.writeheader()

        for repo_result in results.values():
            row = {}
            for metric in RELEVANT_METRICS:
                row[metric] = repo_result.get(metric)
            writer.writerow(row)

    print(f"Results written to {output_path}")


def main(repos_dir: str) -> None:
    analyzer = RepoAnalyzer()
    results = {}
    for repo_name in os.listdir(repos_dir):
        repo_path = os.path.join(repos_dir, repo_name)

        if not os.path.isdir(repo_path):
            continue

        print(f"analyzing {repo_path}...")
        results[repo_name] = analyzer.analyze_repo(repo_path)

    write_results_to_csv(results, "results/results.csv")


main("repos/anon")
