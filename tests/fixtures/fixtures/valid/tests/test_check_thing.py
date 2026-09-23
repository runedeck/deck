import subprocess


def test_thing():
    subprocess.run(["python3", "scripts/check-thing"], check=True)
