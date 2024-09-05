import subprocess

version = subprocess.run(["git", "tag"], text=True, capture_output=True).stdout.strip()

print("version is", version)

print("hello world lol")
