import subprocess
import os
import concurrent.futures
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


def run_command(image: str) -> float:
    try:
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

        if output.returncode != 0:
            print(f"Error running Docker image {image}: {output.stderr}")
            return 0
        
        avg_time = float(output.stdout[output.stdout.strip().rfind('\n')+1:-2])
        return avg_time
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def run_command_parallel(image, num_runs=5) -> float :
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_command, image) for _ in range(num_runs)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # Filter out None results and calculate the average
    valid_results = [r for r in results if r is not None]
    if valid_results:
        median_runtime = sorted(valid_results)[len(valid_results) // 2]
        return median_runtime
    else:
        return 0


run_time: list[float] = []
exp_name: list[str] = [x['name'] for x in TEST_IMAGES]

# Compare to previous Python versions
for item in TEST_IMAGES:
    ttime = run_command_parallel(item['image'])
    print(
        f"{item['name']} 花费了 {ttime} 秒."
    )
    run_time.append(ttime)

# save exp_name and run_time to a pandas DataFrame then export to csv
df = pd.DataFrame({'Version': exp_name, 'Runtime': run_time})
df.to_csv('run_main_results.csv', index=False)
