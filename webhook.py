'''
Autor: Lockly
Date: 2024-01-06 11:04:13
LastEditors: Lockly
LastEditTime: 2024-01-06 11:15:26
'''

import subprocess
import requests

# 将机器人的webhook粘贴至此
webhook = ""

def send_messages(message):
    session = requests.Session()

    send = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }

    req = session.post(webhook, json=send, timeout=7)
    if req.json()["errcode"] != 0:
        print(f"Error occurred in sending messages to wechat bot: {req.text}")
        print(f"message: {message}")


def monitor_output():
    process = subprocess.Popen(['./havoc', 'server', '--profile', './profiles/havoc.yaotl', '-v', '--debug'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT,
                               text=True)
    
    capture = False
    captured_text = ""
    line_count = 0

    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        print(line)
        if "[DBUG] [agent.ParseDemonRegisterRequest:382]" in line:
            capture = True
            captured_text = ""
            line_count = 0
            continue

        if capture:
            if line_count < 5:  
                captured_text += line + '\n'
                line_count += 1
            else: # 
                send_messages('Got a new connection Sir!\n'+captured_text.strip())
                capture = False


monitor_output()