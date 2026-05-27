import pandas as pd
import matplotlib.pyplot as plt
import os
import statistics


def plot_commit_overview(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metrics = [
        "total_regular_commits",
        "total_commits",
        "total_merge_commits"
    ]
    labels = [
        "Regular commits",
        "Total commits",
        "Merge commits",
    ]

    x_positions = list(range(len(df)))
    bar_width = 0.25

    plt.figure(figsize=(12, 6))

    for index, metric in enumerate(metrics):
        bar_positions = [
            position + index * bar_width
            for position in x_positions
        ]

        plt.bar(
            bar_positions,
            df[metric].fillna(0).tolist(),
            width=bar_width,
            label=labels[index],
        )

    center_positions = [
        position + bar_width
        for position in x_positions
    ]

    repo_labels = df["repo_name"].astype(str).tolist()

    plt.xticks(
        center_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Number of commits")
    plt.title("Commit overview per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_contributor_count(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "total_contributors"
    label = "Contributor count"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()

    bars = plt.bar(
        x_positions,
        df[metric].fillna(0).tolist(),
        label=label,
    )

    plt.bar_label(bars, fmt="%.0f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Number of contributors")
    plt.title("Contributor count per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_branch_count(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "branch_count"
    label = "Branch count"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()

    bars = plt.bar(
        x_positions,
        df[metric].fillna(0).tolist(),
        label=label,
    )

    plt.bar_label(bars, fmt="%.0f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Number of branches")
    plt.title("Branch count per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_branches_per_100_commits(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "branches_per_100_commits"
    label = "Branches per 100 commits"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()
    values = df[metric].fillna(0).tolist()

    bars = plt.bar(
        x_positions,
        values,
        label=label,
    )

    plt.bar_label(bars, fmt="%.2f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Branches per 100 commits")
    plt.title("Branches per 100 commits per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_merge_overview(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metrics = [
        "total_merge_commit_ratio",
        "main_branch_merge_commits_share_of_total",
        "branches_merge_commits_share_of_total",
    ]

    labels = [
        "All merge commits / all commits",
        "Merge commits on main / all merge commits",
        "Merge commits on branches / all merge commits",
    ]

    x_positions = list(range(len(df)))
    bar_width = 0.25

    plt.figure(figsize=(12, 6))

    for index, metric in enumerate(metrics):
        bar_positions = [
            position + index * bar_width
            for position in x_positions
        ]

        values = (df[metric].fillna(0) * 100).tolist()

        bars = plt.bar(
            bar_positions,
            values,
            width=bar_width,
            label=labels[index],
        )

        # plt.bar_label(bars, fmt="%.1f", padding=3)

    center_positions = [
        position + bar_width
        for position in x_positions
    ]

    repo_labels = df["repo_name"].astype(str).tolist()

    plt.xticks(
        center_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Percent (%)")
    plt.title("Merge overview per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_regular_commits_overview(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metrics = [
        "total_regular_commit_ratio",
        "main_branch_regular_commits_share_of_total",
        "branches_regular_commits_share_of_total",
    ]

    labels = [
        "All regular commits / all commits",
        "Regular commits on main / all regular commits",
        "Regular commits on branches / all regular commits",
    ]

    x_positions = list(range(len(df)))
    bar_width = 0.25

    plt.figure(figsize=(12, 6))

    for index, metric in enumerate(metrics):
        bar_positions = [
            position + index * bar_width
            for position in x_positions
        ]

        values = (df[metric].fillna(0) * 100).tolist()

        bars = plt.bar(
            bar_positions,
            values,
            width=bar_width,
            label=labels[index],
        )

        # plt.bar_label(bars, fmt="%.1f", padding=3)

    center_positions = [
        position + bar_width
        for position in x_positions
    ]

    repo_labels = df["repo_name"].astype(str).tolist()

    plt.xticks(
        center_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Percent (%)")
    plt.title("Direct work overview per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_median_branch_lifetime(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "median_lifetime_hours_per_branch"
    label = "Median branch lifetime"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()
    values = df[metric].fillna(0).tolist()

    bars = plt.bar(
        x_positions,
        values,
        label=label,
    )

    plt.bar_label(bars, fmt="%.1f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Hours")
    plt.title("Median branch lifetime per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_median_contributors_per_branch(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "median_contributors_per_branch"
    label = "Median contributors per branch"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()
    values = df[metric].fillna(0).tolist()

    bars = plt.bar(
        x_positions,
        values,
        label=label,
    )

    plt.bar_label(bars, fmt="%.1f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Contributors")
    plt.title("Median contributors per branch")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_single_author_branch_ratio(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "single_author_branch_ratio"
    label = "Single-author branches"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()
    values = (df[metric].fillna(0) * 100).tolist()

    bars = plt.bar(
        x_positions,
        values,
        label=label,
    )

    plt.bar_label(bars, fmt="%.1f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Percent (%)")
    plt.title("Single-author branch ratio per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_merged_to_main_ratio(output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    metric = "merged_to_main_branch_ratio"
    label = "Branches merged to main"

    plt.figure(figsize=(12, 6))

    x_positions = list(range(len(df)))
    repo_labels = df["repo_name"].astype(str).tolist()
    values = (df[metric].fillna(0) * 100).tolist()

    bars = plt.bar(
        x_positions,
        values,
        label=label,
    )

    plt.bar_label(bars, fmt="%.1f", padding=3)

    plt.xticks(
        x_positions,
        repo_labels,
        rotation=45,
        ha="right",
    )

    plt.ylabel("Percent (%)")
    plt.title("Branches merged to main per repository")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def print_stats() -> None:
    total_repositories = len(df)

    def print_category_stats(title: str, counts: dict[str, int], denominator: int) -> None:
        print(f"\n{title}")
        print("-" * len(title))

        for label, count in counts.items():
            percentage = (count / denominator * 100) if denominator > 0 else 0
            print(f"{label}: {count}/{denominator} repositories ({percentage:.1f}%)")

    # Branches per 100 commits
    few_branches = len(df[df["branches_per_100_commits"] < 5])
    moderate_branches = len(
        df[
            (df["branches_per_100_commits"] >= 5)
            & (df["branches_per_100_commits"] <= 15)
        ]
    )
    high_branches = len(df[df["branches_per_100_commits"] > 15])

    print_category_stats(
        "Branches per 100 commits",
        {
            "Few branches (< 5)": few_branches,
            "Moderate branches (5–15)": moderate_branches,
            "High branches (> 15)": high_branches,
        },
        total_repositories,
    )

    # Regular commit location
    regular_df = df[df["total_regular_commits"] > 0]

    majority_regular_on_branches = len(
        regular_df[
            regular_df["branches_regular_commits_share_of_total"]
            > regular_df["main_branch_regular_commits_share_of_total"]
        ]
    )

    majority_regular_on_main = len(
        regular_df[
            regular_df["main_branch_regular_commits_share_of_total"]
            > regular_df["branches_regular_commits_share_of_total"]
        ]
    )

    equal_regular_work = len(
        regular_df[
            regular_df["main_branch_regular_commits_share_of_total"]
            == regular_df["branches_regular_commits_share_of_total"]
        ]
    )

    print_category_stats(
        "Regular commit location",
        {
            "Majority regular commits on branches": majority_regular_on_branches,
            "Majority regular commits on main": majority_regular_on_main,
            "Equal regular commits on main and branches": equal_regular_work,
        },
        len(regular_df),
    )

    # Merge commit location
    merge_df = df[df["total_merge_commits"] > 0]

    majority_merges_on_branches = len(
        merge_df[
            merge_df["branches_merge_commits_share_of_total"]
            > merge_df["main_branch_merge_commits_share_of_total"]
        ]
    )

    majority_merges_on_main = len(
        merge_df[
            merge_df["main_branch_merge_commits_share_of_total"]
            > merge_df["branches_merge_commits_share_of_total"]
        ]
    )

    equal_merges = len(
        merge_df[
            merge_df["main_branch_merge_commits_share_of_total"]
            == merge_df["branches_merge_commits_share_of_total"]
        ]
    )

    print_category_stats(
        "Merge commit location",
        {
            "Majority merge commits on branches": majority_merges_on_branches,
            "Majority merge commits on main": majority_merges_on_main,
            "Equal merge commits on main and branches": equal_merges,
        },
        len(merge_df),
    )

    # Branches merged to main
    merged_df = df[
        (df["branch_count"] > 0)
        & (df["merged_to_main_branch_ratio"].notna())
    ]

    low_merged_to_main = len(
        merged_df[merged_df["merged_to_main_branch_ratio"] < 0.5]
    )

    moderate_merged_to_main = len(
        merged_df[
            (merged_df["merged_to_main_branch_ratio"] >= 0.5)
            & (merged_df["merged_to_main_branch_ratio"] <= 0.8)
        ]
    )

    high_merged_to_main = len(
        merged_df[merged_df["merged_to_main_branch_ratio"] > 0.8]
    )

    print_category_stats(
        "Branches merged to main",
        {
            "Low merged-to-main ratio (< 50%)": low_merged_to_main,
            "Moderate merged-to-main ratio (50–80%)": moderate_merged_to_main,
            "High merged-to-main ratio (> 80%)": high_merged_to_main,
        },
        len(merged_df),
    )

    # Branch lifetime
    lifetime_df = df[df["branch_count"] > 0]

    short_lifetime = len(
        lifetime_df[lifetime_df["median_lifetime_hours_per_branch"] < 24]
    )

    medium_lifetime = len(
        lifetime_df[
            (lifetime_df["median_lifetime_hours_per_branch"] >= 24)
            & (lifetime_df["median_lifetime_hours_per_branch"] <= 168)
        ]
    )

    long_lifetime = len(
        lifetime_df[lifetime_df["median_lifetime_hours_per_branch"] > 168]
    )

    print_category_stats(
        "Median branch lifetime",
        {
            "Short-lived branches (< 24h)": short_lifetime,
            "Medium-lived branches (24h–168h)": medium_lifetime,
            "Long-lived branches (> 168h)": long_lifetime,
        },
        len(lifetime_df),
    )

    # Single-author branch ratio
    single_author_df = df[df["branch_count"] > 0]

    low_single_author = len(
        single_author_df[single_author_df["single_author_branch_ratio"] < 0.5]
    )

    moderate_single_author = len(
        single_author_df[
            (single_author_df["single_author_branch_ratio"] >= 0.5)
            & (single_author_df["single_author_branch_ratio"] <= 0.8)
        ]
    )

    high_single_author = len(
        single_author_df[single_author_df["single_author_branch_ratio"] > 0.8]
    )

    print_category_stats(
        "Single-author branch ratio",
        {
            "Low single-author ratio (< 50%)": low_single_author,
            "Moderate single-author ratio (50–80%)": moderate_single_author,
            "High single-author ratio (> 80%)": high_single_author,
        },
        len(single_author_df),
    )


df = pd.read_csv("results/results.csv")
df = df.sort_values("repo_name")

plot_commit_overview("results/charts/commit_overview.png")
plot_contributor_count("results/charts/contributor_count.png")
plot_branch_count("results/charts/branch_count.png")
plot_branches_per_100_commits("results/charts/branches_per_100_commits.png")
plot_merge_overview("results/charts/merge_overview.png")
plot_merged_to_main_ratio("results/charts/merged_to_main_ratio.png")
plot_regular_commits_overview("results/charts/regular_commits_overview.png")
plot_median_branch_lifetime("results/charts/median_branch_lifetime.png")
plot_median_contributors_per_branch("results/charts/median_contributors_per_branch.png")
plot_single_author_branch_ratio("results/charts/single_author_branch_ratio.png")
print_stats()
