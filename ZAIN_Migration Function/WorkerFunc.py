import sys
import cmd
import os
import re
import time

def worker(sta, current_time, last_timestamp, current_ssid, history):
    # time.sleep(0.15)
    vehicle_id = sta.params['wlan'][0]
    # vehicle_position = sta.position
    # essids = sta.cmd("iwconfig")
    try:
        essids = sta.cmd("iwconfig")
        time.sleep(0.15)
        # print("essids:::::____",essids)
        essids1 = re.findall(r'ESSID:"([^"]+)"', essids)
        essid = essids1[0] if essids1 else "Unknown"
        # print("essid___INSIDE WorkerFunc", essid)
    except Exception as e:
        print("Error executing command:", e)
        # Handle the error appropriately
    # time.sleep(0.15)
    # essids1 = re.findall(r'ESSID:"([^"]+)"', essids)
    # time.sleep(0.15)
    # print('ESSIDs:', essids1)
    # essid = essids1[0] if essids1 else "Unknown"

    timestamp_spent = 0

    if not history:  # new entry
        history[(vehicle_id, current_ssid)] = last_timestamp
        # time.sleep(0.15)
    else:  # not new entry but old key and new value
        # time.sleep(0.15)
        if (vehicle_id, current_ssid) in history:
            last_timestamp = history[(vehicle_id, current_ssid)]
            timestamp_spent = current_time - last_timestamp
            history[(vehicle_id, current_ssid)] = last_timestamp + 1
        else:  # not new entry but new key
            history[(vehicle_id, current_ssid)] = last_timestamp


    try:
        current_ssid = essid
        # print("current_ssid__INSIDE WORKERFUNC1", current_ssid)
    except Exception as e1:
        print("Error executing command:", e1)
        # print('(in-side worker fn) vehicle '+vehicle_id+' with current_ssid:'+ current_ssid+'at current_time '+str(current_time))
    # time.sleep(0.15)
    return timestamp_spent, current_ssid, vehicle_id, history, current_time

