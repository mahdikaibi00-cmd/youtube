import os
import sys
import datetime
import random
import subprocess
import requests

# GitHub API setup
GH_PAT = os.environ.get('GH_PAT')
REPO_OWNER = 'mahdikaibi00-cmd'
REPO_NAME = 'youtube'

# Windows
# Grid Hardened: hours 0, 1, 2, 3
# Brew-Fi: hours 14, 15, 16

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(result.stderr)
    return result

def check_already_run(channel):
    rclone_path = f"data:Colab_AutoVideoCreator/channels/{channel}/last_run.txt"
    run_cmd(f"rclone copy '{rclone_path}' . || true")
    if os.path.exists('last_run.txt'):
        with open('last_run.txt', 'r') as f:
            last_date = f.read().strip()
        os.remove('last_run.txt')
        if last_date == datetime.datetime.utcnow().strftime('%Y-%m-%d'):
            return True
    return False

def mark_run(channel):
    with open('last_run.txt', 'w') as f:
        f.write(datetime.datetime.utcnow().strftime('%Y-%m-%d'))
    rclone_path = f"data:Colab_AutoVideoCreator/channels/{channel}"
    run_cmd(f"rclone copy 'last_run.txt' '{rclone_path}'")
    os.remove('last_run.txt')

def pop_topic(channel):
    rclone_path = f"data:Colab_AutoVideoCreator/channels/{channel}/topics.txt"
    run_cmd(f"rclone copy '{rclone_path}' . || true")
    if not os.path.exists('topics.txt'):
        print(f"Error: topics.txt not found for {channel}")
        return None
        
    with open('topics.txt', 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        
    if not lines:
        print(f"Error: topics.txt is empty for {channel}")
        return None
        
    topic = lines.pop(0)
    
    with open('topics.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        
    run_cmd(f"rclone copyto 'topics.txt' '{rclone_path}'")
    os.remove('topics.txt')
    return topic

def trigger_workflow(channel, topic):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/render.yml/dispatches"
    headers = {
        'Authorization': f"Bearer {GH_PAT}",
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        'ref': 'main',
        'inputs': {
            'action_type': 'CREATE_FRESH',
            'channel_name': channel,
            'topic': topic
        }
    }
    print(f"Triggering workflow for {channel} with topic: {topic}")
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 204:
        print("Workflow triggered successfully!")
    else:
        print(f"Failed to trigger workflow: {resp.status_code} {resp.text}")

def main():
    now = datetime.datetime.utcnow()
    hour = now.hour
    
    channel = None
    prob = 0
    
    if hour in [0, 1, 2, 3]:
        channel = "Grid Hardened"
        if hour == 0: prob = 0.25
        elif hour == 1: prob = 0.33
        elif hour == 2: prob = 0.50
        elif hour == 3: prob = 1.00
    elif hour in [14, 15, 16]:
        channel = "Brew-Fi"
        if hour == 14: prob = 0.33
        elif hour == 15: prob = 0.50
        elif hour == 16: prob = 1.00
    else:
        print(f"Hour {hour} is outside scheduling windows. Exiting.")
        sys.exit(0)
        
    print(f"Current hour: {hour}. Channel: {channel}. Probability to run: {prob*100}%")
    
    if check_already_run(channel):
        print(f"Channel {channel} already ran today. Exiting.")
        sys.exit(0)
        
    if random.random() <= prob:
        print("Dice roll SUCCESS. Executing run...")
        topic = pop_topic(channel)
        if topic:
            trigger_workflow(channel, topic)
            mark_run(channel)
    else:
        print("Dice roll FAILED. Will retry next hour.")

if __name__ == '__main__':
    main()
