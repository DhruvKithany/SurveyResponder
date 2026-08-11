import time
import sys
import os
import re

def parse_log(log_file):
    if not os.path.exists(log_file):
        return 0, ""
    
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Find all tqdm progress lines
    matches = re.findall(r'Generating responses:\s*\d+%\|.*?\|\s*(\d+)/50\s*\[(.*?)\]', content)
    if matches:
        last_match = matches[-1]
        completed = int(last_match[0])
        stats = last_match[1] # e.g., "00:15<02:15,  3.00s/response"
        return completed, stats
    return 0, ""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
        
    log_file = sys.argv[1]
    target = int(sys.argv[2])
    
    while True:
        completed, stats = parse_log(log_file)
        if completed >= target:
            print(f"MILESTONE_REACHED: {completed} responses. Stats: {stats}")
            sys.exit(0)
        time.sleep(2)
