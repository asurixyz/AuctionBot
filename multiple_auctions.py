import subprocess
import re
from collections import defaultdict
import os

def run_auction():
    result = subprocess.run(['python3', 'Variant_2.py', '-log'], capture_output=True, text=True)
    output = result.stdout
    final_capitals = {}
    for line in output.split('\n'):
        if 'capital left' in line:
            parts = line.split(':')
            bot_name = parts[0].split('/')[-1].split('.')[0]
            capital = float(parts[-1].split('-')[-1].strip())
            final_capitals[bot_name] = capital
    sorted_bots = sorted(final_capitals.items(), key=lambda x: x[1], reverse=True)
    winner = sorted_bots[0][0] if sorted_bots else None
    runner_up = sorted_bots[1][0] if len(sorted_bots) > 1 else None
    
    return winner, runner_up

def main():
    #change as per your wish
    num_runs = 50                   
    winners = defaultdict(int)
    runner_ups = defaultdict(int)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    for i in range(num_runs):
        print(f"Running auction {i+1}/{num_runs}")
        winner, runner_up = run_auction()
        if winner:
            winners[winner] += 1
        if runner_up:
            runner_ups[runner_up] += 1

    print("\nWinners (in descending order of auction wins):")
    for bot, wins in sorted(winners.items(), key=lambda x: x[1], reverse=True):
        print(f"{bot}: {wins}/{num_runs}")

    print("\nRunner-ups (in descending order of second-place finishes):")
    for bot, seconds in sorted(runner_ups.items(), key=lambda x: x[1], reverse=True):
        print(f"{bot}: {seconds}/{num_runs}")

if __name__ == "__main__":
    main()
