import os
import subprocess
import sys

def main():
    base_dir = "Qwen_3.5_9B_Runs"
    temperatures = [1.65, 1.75, 1.85, 2.00]
    model_name = "qwen2.5:7b"
    num_responses = 50

    os.makedirs(base_dir, exist_ok=True)

    print(f"Starting sequential sweep for {len(temperatures)} temperatures with {num_responses} responses each...")

    failed = False
    for temp in temperatures:
        temp_dir = os.path.join(base_dir, f"temp_{temp:.2f}")
        os.makedirs(temp_dir, exist_ok=True)
        
        output_file = os.path.join(temp_dir, "results.csv")
        log_file_path = os.path.join(temp_dir, "run_log.txt")
        
        cmd = [
            sys.executable, "cli.py", "run",
            "--questions", "prca_questions.json",
            "--persona", "persona.json",
            "--model", model_name,
            "--num-responses", str(num_responses), 
            "--output", output_file,
            "--temperature", str(temp)
        ]
        
        print(f"Running for temperature {temp:.2f}...")
        with open(log_file_path, "w") as log_file:
            # We use sequential execution to avoid overloading a laptop and hitting Ollama timeouts
            result = subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT)
            
            if result.returncode == 0:
                print(f"Completed run for temperature {temp:.2f}.")
            else:
                print(f"Error running for temperature {temp:.2f}. Check temp_{temp:.2f}/run_log.txt for details.", file=sys.stderr)
                failed = True
                break # Stop the sweep if Ollama fails

    if failed:
        sys.exit(1)
    else:
        print("All runs completed successfully!")

if __name__ == "__main__":
    main()
