import json
import pandas as pd

def get_torch_time(level, path):
    with open(path, "r") as f:
        data = json.load(f)

    data = data[f"level{level}"]
    problem_id_to_time = {}

    for k, v in data.items():
        problem_id = k.split('_')[0]
        time = v["mean"]
        problem_id_to_time[problem_id] = time

    return problem_id_to_time

def make_L40S_path(level, model):
    return f"./times/baseline_{model}_level_{level}_L40S.json"

def make_mi250_path(level, model):
    return f"./times/baseline_{model}_level_{level}_mi250.json"

def get_L40S_time(level, path):
    with open(path, "r") as f:
        data = json.load(f)

    problem_id_to_time = {}

    for k, v in data.items():
        problem_id = k
        if not v["compiled"]:
            time = -2
        elif not v["correct"]:
            time = -1
        else:
            time = v["avg_runtime"]
        problem_id_to_time[problem_id] = time

    return problem_id_to_time

def get_mi250_time(level, path):
    with open(path, "r") as f:
        data = json.load(f)

    problem_id_to_time = {}

    for k, v in data.items():
        problem_id = k
        if not v["compiled"]:
            time = -2
        elif not v["correctness"]:
            time = -1
        else:
            time = v["runtime"]
        problem_id_to_time[problem_id] = time

    return problem_id_to_time

if __name__ == "__main__":
    models = ["claude-3.5-sonnet","deepseek-r1","deepseek-v3","gpt-4o","llama-3.1-405b","llama-3.1-70b","openai-o1"]

    results = {}

    results["torch_L40S"] = get_torch_time(1, "./times/baseline_time_torch_L40S.json")
    results["torch_mi250"] = get_torch_time(1, "./times/baseline_time_torch_mi250.json")
    
    for model in models:
        level = 1
        L40S_path = make_L40S_path(level, model)
        mi250_path = make_mi250_path(level, model)

        L40S_times = get_L40S_time(level, L40S_path)
        mi250_times = get_mi250_time(level, mi250_path)

        results[f"{model}_L40S"] = L40S_times
        results[f"{model}_mi250"] = mi250_times


    # Convert results to a pandas DataFrame and transpose it
    results_df = pd.DataFrame.from_dict(results, orient='index').transpose()

    # Print the transposed DataFrame to verify
    print(results_df)

    results_df.to_csv("results.csv", index=True)

    # with open("results.json", "w") as f:
    #     json.dump(results, f)

