import os
import re
import subprocess

import semver

VERSION_FILE = "version.txt"

env = {
    "THE_GITHUB_PAT": os.getenv("THE_GITHUB_PAT"),
    "REPO": os.getenv("REPO"),
    "BRANCH": os.getenv("BRANCH"),
}

missing_env = [key for key, value in env.items() if value is None]
if len(missing_env) > 0:
    print("Missing environment variables:")
    for key in missing_env:
        print(f"  {key}")

    print("Exiting with status 1...")
    exit(1)


def determine_bump_type(commit_message: str) -> str:
    """
    Determines the type of version bump (increment) based on the commit message.

    Args:
        commit_message (str): The commit message.

    Returns:
        str: The type of version bump ('major', 'minor', or 'patch').
    """

    print(f"Commit message: {commit_message}")

    if re.match(r"^(?:chore|docs|style|refactor|build|ci|test):", commit_message):
        return None
    elif re.match(r"^feat:", commit_message):
        return "minor"
    if re.search(r"^major:", commit_message):
        return "major"
    # elif re.match(r"^fix:", commit_message):
    #     return "patch"
    else:
        return "patch"


def main():
    commit_message = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    print(f"Commit message: {commit_message}")

    with open(VERSION_FILE, "r+") as f:
        current_version = f.read().strip()
        print(f"Current version: {current_version}")

        bump_type = determine_bump_type(commit_message)
        print(f"Bump type: {bump_type}")

        if bump_type is None:
            print("No version bump detected.")
            return

        new_version = semver.VersionInfo.parse(current_version).next_version(
            part=bump_type
        )
        new_version = str(new_version).strip()
        if new_version == current_version:
            print("No change detected.")
            return

        print("New version:", new_version)

        # write new version to the file
        f.seek(0)
        f.write(new_version)

    # configure git
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])

    # add, commit and push
    subprocess.run(["git", "add", VERSION_FILE])
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"])
    subprocess.run(
        [
            "git",
            "remote",
            "add",
            "action-origin",
            "https://x-access-token:"
            + env["THE_GITHUB_PAT"]
            + "@github.com/"
            + env["REPO"],
        ]
    )
    subprocess.run(["git", "push", "origin", f"HEAD:{env['BRANCH']}"])


if __name__ == "__main__":
    main()
