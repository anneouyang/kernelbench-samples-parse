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


if __name__ == "__main__":
    level = 1
    get_kernels_for_level(level)
