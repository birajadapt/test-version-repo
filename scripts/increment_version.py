import sys
import semver
import re


def determine_increment_type(commit_message: str) -> str:
    """
    Determines the type of version increment based on the commit message.

    Args:
        commit_message (str): The commit message.

    Returns:
        str: The type of version increment ('major', 'minor', or 'patch').
    """

    if re.match(r"^(?:chore|docs|style|refactor|build|ci|test):", commit_message):
        return None
    elif re.match(r"^feat:", commit_message):
        return "minor"
    if re.search(r"\bBREAKING CHANGE\b", commit_message):
        return "major"
    # elif re.match(r"^fix:", commit_message):
    #     return "patch"
    else:
        return "patch"


def main():
    if len(sys.argv) != 2:
        print("Usage: python increment_version.py <commit_message>")
        sys.exit(1)

    commit_message = sys.argv[1]

    print(f"Commit message: {commit_message}")

    with open("version.txt", "r+") as f:
        current_version = f.read().strip()

        print(f"Current version: {current_version}")

        increment_type = determine_increment_type(commit_message)
        print(f"Increment type: {increment_type}")
        if increment_type is None:
            return

        new_version = semver.VersionInfo.parse(current_version).next_version(
            part=increment_type
        )

        print("New version:", new_version)

        f.seek(0)
        f.write(f"{str(new_version)}\n")


if __name__ == "__main__":
    main()
