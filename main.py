import subprocess

version = (
    subprocess.run(["git", "tag"], text=True, capture_output=True)
    .stdout.strip()
    .splitlines()[0]
)

print("version is", version)

print("hello world lol")
