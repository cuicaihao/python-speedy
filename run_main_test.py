import subprocess
import os
import pandas as pd

TEST_IMAGES = [
    {"name": "Python 3.5", "image": "python:3.5-slim"},
    {"name": "Python 3.6", "image": "python:3.6-slim"},
    {"name": "Python 3.7", "image": "python:3.7-slim"},
    {"name": "Python 3.8", "image": "python:3.8-slim"},
    {"name": "Python 3.9", "image": "python:3.9-slim"},
    {"name": "Python 3.10", "image": "python:3.10-slim"},
    {"name": "Python 3.11", "image": "python:3.11-slim"},
    {"name": "Python 3.12", "image": "python:3.12-slim"}
]

K_MER = 13
SCRIPT = "single_test_run.py"

########
# Main #
########
cwd = os.getcwd()


def test_version(image: str) -> float:
    """
    Run single_test on Python Docker image.

    Parameter
    ---------
    image
        full name of the the docker hub Python image.

    Returns
    -------
    run_time
        runtime in seconds per test loop.
    """
    output = subprocess.run(
        [
            "docker",
            "run",
            "-it",
            "--rm",
            "-v",
            f"{cwd}/{SCRIPT}:/{SCRIPT}",
            image,
            "python3",
            f"/{SCRIPT}",
            "--k_mer",
            str(K_MER),
        ],
        capture_output=True,
        text=True,
    )

    print(output)
    avg_time = float(output.stdout[output.stdout.strip().rfind('\n')+1:-2])
    return avg_time


run_time = []
exp_name: list[str] = [x['name'] for x in TEST_IMAGES]

# Compare to previous Python versions
for item in TEST_IMAGES:
    ttime = test_version(item["image"])
    print(
        f"{item['name']} 花费了 {ttime} 秒."
    )
    run_time.append(ttime)

# save exp_name and run_time to a pandas DataFrame then export to csv
df = pd.DataFrame({'exp_name': exp_name, 'run_time': run_time})
df.to_csv('run_main_results.csv', index=False)
