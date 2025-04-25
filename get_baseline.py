import os
import glob

KERNEL_SAMPLES_REPO = "/work1/mirhoseini/aco/kernelbench-samples/"
KERNELBENCH_REPO = "/work1/mirhoseini/aco/KernelBench/"

import json

def get_kernels_for_level(level):
    """
    Retrieve the 'kernel' field from all JSON files for a given level and all models from the baseline evaluations
    and save each corresponding problem in the specified directory.

    :param level: The level number (1, 2, or 3).
    :return: A dictionary where keys are model names and values are lists of 'kernel' field contents from the JSON files.
    """
    base_path = os.path.join(KERNEL_SAMPLES_REPO, f"baseline_eval/level{level}")
    model_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    all_kernels = {}
    for model_name in model_dirs:
        pattern = os.path.join(base_path, model_name, "problem_*/sample_0/kernel.json")
        json_files = glob.glob(pattern)
        
        kernels = []
        for json_file in json_files:
            with open(json_file, 'r') as file:
                data = json.load(file)
                kernel_code = data.get("kernel", None)
                kernels.append(kernel_code)
                
                # Extract problem_id from the file path
                problem_id = os.path.basename(os.path.dirname(os.path.dirname(json_file))).split('_')[-1]
                
                # Define the output path
                output_dir = os.path.join(KERNELBENCH_REPO, f"runs/baseline/{model_name}/")
                if not os.path.exists(output_dir):
                    os.makedirs(os.path.dirname(output_dir), exist_ok=True)
                output_filename = f"level_{level}_problem_{problem_id}_sample_0_kernel.py"
                output_filename = os.path.join(output_dir, output_filename)
                
                # Save the kernel code to the specified path
                with open(output_filename, 'w') as output_file:
                    print(f"Saving kernel to {output_filename}")
                    output_file.write(kernel_code)
        
        all_kernels[model_name] = kernels
    
    return all_kernels


def get_avg_runtime_for_level(level):
    """
    Retrieve the 'avg_runtime' field from all JSON files for a given level and all models from the baseline evaluations
    and save the results in a single JSON file for each model.

    :param level: The level number (1, 2, or 3).
    :return: A dictionary where keys are model names and values are lists of dictionaries with 'problem_id' and 'avg_runtime'.
    """
    base_path = os.path.join(KERNEL_SAMPLES_REPO, f"baseline_eval/level{level}")
    model_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    all_runtimes = {}
    for model_name in model_dirs:
        pattern = os.path.join(base_path, model_name, "problem_*/sample_0/kernel.json")
        json_files = glob.glob(pattern)
        
        runtimes = {}
        for json_file in json_files:
            with open(json_file, 'r') as file:
                data = json.load(file)
                eval_result = data["eval_result"]["eval_0"]
                
                # Extract problem_id from the file path
                problem_id = os.path.basename(os.path.dirname(os.path.dirname(json_file))).split('_')[-1]
                
                # Append the result to the list
                runtimes[str(problem_id)] = eval_result
        
        # Define the output path
        output_filename = os.path.join("./times/", f"baseline_{model_name}_level_{level}_L40S.json")
        
        # Save the runtimes to the specified path
        with open(output_filename, 'w') as output_file:
            print(f"Saving runtimes to {output_filename}")
            json.dump(runtimes, output_file, indent=4)
        
        all_runtimes[model_name] = runtimes

def copy_eval_results_to_times():
    """
    Copy eval_results_mi250.json files from the specified source directory to the ./times directory
    with a new naming convention.
    """
    source_base_path = "/work1/mirhoseini/aco/KernelBench/runs/baseline"
    destination_base_path = "./times"
    model_dirs = [d for d in os.listdir(source_base_path) if os.path.isdir(os.path.join(source_base_path, d))]

    for model_name in model_dirs:
        source_file = os.path.join(source_base_path, model_name, "eval_results_mi250.json")
        if os.path.exists(source_file):
            destination_file = os.path.join(destination_base_path, f"baseline_{model_name}_level_1_mi250.json")
            with open(source_file, 'r') as src, open(destination_file, 'w') as dst:
                print(f"Copying {source_file} to {destination_file}")
                dst.write(src.read())


if __name__ == "__main__":
    # level = 1
    # get_kernels_for_level(level)
    # get_kernels_for_level(2)
    # get_kernels_for_level(3)

    # get_avg_runtime_for_level(1)
    # copy_eval_results_to_times()
    pass