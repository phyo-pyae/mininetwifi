import sys
import time
import os
import re
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np 
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import OVSKernelAP
from mininet.term import makeTerm
from time import sleep
from datetime import datetime
from collections import defaultdict
from WorkerFunc import worker  # Import the worker function from WorkerFunc.py
import csv
import CSVFunc  # Import the CSV functions from CSVFunc .py
import SwMigrationFunc
from subprocess import Popen, PIPE
from  pythonping import ping
import random

'''
def measure_speed(vehicle, start_time, end_time):
    # Calculate and return the speed of the vehicle based on position change
    start_position = [float(coord) for coord in vehicle.params['position'].split(',')]
    end_position = [float(coord) for coord in vehicle.params['position'].split(',')]

    time_difference = end_time - start_time
    distance_travelled = ((end_position[0] - start_position[0])**2 + (end_position[1] $
    speed = distance_travelled / time_difference

    return speed
'''

def mininet_thread_function():
    global linked_previous_ssids
    setLogLevel('info')

    "Create a network."
    net = Mininet_wifi(controller=RemoteController, link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3, switch=OVSKernelAP)
    info("*** Creating nodes\n")

    Max_v=33.333
    Min_v=0.001
    number_of_vehicle=2
    # net.setMobilityModel(time=0, model='RandomWayPoint', seed=20)#,max_x=1000, max_y=1000, seed=20)
    net.setMobilityModel(time=0, model='RandomDirection', min_x=-47, max_x=247, min_y=-47, max_y=247, min_v = 0.001, max_v = Max_v, seed=20)


    # Add stations
    stations = []
    for i in range(1, number_of_vehicle+1):
        mac_address = f'd6:76:e0:ab:36:{i:02x}'  # Format i as a two-digit hexadecimal number
        if i < 256:  # Ensure the range is limited to 'd6:76:e0:ab:36:fe'
            station = net.addStation(f'veh{i}', mac=mac_address, ip=f'10.0.2.{i}/24', min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, range=1)
            stations.append(station)
    dest = net.addHost('dest', mac='d6:76:e0:ab:36:ff', ip='10.0.2.254/24', range=10)

    ap_position_list = [
        '0,200,0', '100,200,0', '200,200,0',
        '0,100,0', '100,100,0', '200,100,0',
        '0,0,0', '100,0,0', '200,0,0'
    ]

    ap_list = []

    for i in range(1, 10):
        ap_name = f'rsu{i}'
        ap_mac = f'00:00:00:00:02:{10 * i:02d}'
        ap_ip = f'10.0.2.{10 * i}/24'
        ap_position = ap_position_list[i - 1]
        ap_dpid = str(1000000000000000 + i)
    
        ap = net.addAccessPoint(ap_name, ssid=f'new-ssid-{i}', mac=ap_mac, ip=ap_ip, mode='g',
                            channel='1', position=ap_position, dpid=ap_dpid,
                            range=75, failmode='secure', datapath='user')
        ap_list.append(ap)

    sw1 = net.addSwitch('l2sw',cls=OVSSwitch, failmode='standalone')#, protocols="OPenFlow13")

    controller_ports = [6651, 6652, 6653]
    controllers = [net.addController(f'c{i}', controller=RemoteController, port=port) for i, port in enumerate(controller_ports)]

    info("*** Configuring wifi nodes\n")
    net.setPropagationModel(model="friis", exp=4)
    net.configureWifiNodes()

    nodes = net.stations

    info("*** Associating and Creating links\n")

    for ap in ap_list:
        net.addLink(ap, sw1)

    net.addLink(sw1, dest)
    start_time = 10
    end_time = 2400
    net.plotGraph(min_x=-100, max_x=300, min_y=-100, max_y=300)

    # Define a flag to indicate if the code has been executed
    code_executed = False

    info("*** Starting network\n")
    net.build()
    for i in controllers:
        i.start()

    for ap in ap_list:
        ap.start(controllers)

    sw1.start([])

    for i, controller in enumerate(controllers, start=1):
        time.sleep(2)
        makeTerm(controller, cmd=f"bash -c 'ryu-manager simple_switch_13_B_C{i}.py --ofp-tcp-listen-port 665{i} --verbose > H{i}.txt'")

    time.sleep(2)
    makeTerm(dest, cmd="sudo tcpdump -i dest-wlan0")

    time.sleep(60)
    makeTerm(sw1, cmd="bash -c './of_l2sw.py'")

    for i, ap in enumerate(ap_list):
        time.sleep(1)
        makeTerm(ap, cmd=f"bash -c './ovstest_rsu{i + 1}.py'")


    time.sleep(1)
    ###############################################################################################################

    makeTerm(dest)#, cmd="sudo tcpdump -i dest-eth1")

    for i, station in enumerate(stations):
        time.sleep(2)
        ping_log_file = f'veh{i+1}_log1610.txt'
        pcap_file = f'veh{i+1}_log1610.pcap'

        ping_cmd = f"ping 10.0.2.254 -i 0.2 > {ping_log_file}"
        # tcpdump_cmd = f"sudo tcpdump -i {station}-wlan0 -w {pcap_file}"

        makeTerm(station, cmd=ping_cmd)
        # makeTerm(station, cmd=tcpdump_cmd)

    ###############################################################################################################

    #for ap in ap_list:
    #    time.sleep(1)
    #    makeTerm(ap)

    ###############################################################################################################
    
    #print('I want to open IWCONFIG')
    now = start_time
    is_moving = False
    print('start_time', start_time, 'now', now, 'end_time', end_time)
    # Define a flag to indicate if the code has been executed
    code_executed = False
    current_time = now
    vehicle_list = stations
    # vehicle_list = [stations[0], stations[1],stations[2],stations[3],stations[4],stations[5]]
    # Create a dictionary to store session times for each vehicle
    session_times = {}

    #===============================================================
    essid_info = {}
    # essid_info = {(i, j): [] for i in range(1, 10) for j in range(1, 10)}
    futures = []
    current_ssid = 'new-ssid-0'
    last_timestamp = start_time
    history ={}
    avg_session_time = {}

    ######################################################################

    previous_ssid_for_vehs = {station.name + '-wlan0': 'new-ssid-0' for station in stations}

    next_ssid_for_vehs = {};
    entry_time_previous_ssid_for_vehs = {station.name + '-wlan0': 0 for station in stations} 

    history_sessiontime_from_to = {};
    avg_sessiontime_from_to = {};
    ssid_vals = ["new-ssid-0", "new-ssid-1", "new-ssid-2", "new-ssid-3", "new-ssid-4", "new-ssid-5", "new-ssid-6", "new-ssid-7", "new-ssid-8", "new-ssid-9"]
    for temp_previous_ssid in ssid_vals:
        for temp_next_ssid in ssid_vals:
            history_sessiontime_from_to[(temp_previous_ssid, temp_next_ssid)] = []
            avg_sessiontime_from_to[(temp_previous_ssid, temp_next_ssid)] = []
    ########################################################################
    # Learning rate (alpha)
    alpha = 0.2
    ewma_result = {}
    # Set the interval for monitoring completion (5 minutes)
    monitoring_interval = 5  # seconds
    # latest_monitoring_data = {}
    monitoring_data = {}
    # Initialize a flag to control the execution
    execute_flag = True
    # Initialize last_sweeping_printed to a time before the start_time
    # last_sweeping_printed = current_time - sweeping_timeperiod
    ssid_to_ap = {
                    'new-ssid-1': ap_list[0],
                    'new-ssid-2': ap_list[1],
                    'new-ssid-3': ap_list[2],
                    'new-ssid-4': ap_list[3],
                    'new-ssid-5': ap_list[4],
                    'new-ssid-6': ap_list[5],
                    'new-ssid-7': ap_list[6],
                    'new-ssid-8': ap_list[7],
                    'new-ssid-9': ap_list[8],
                    'rsu9': ap_list[8],
                }
    #########################################################################
    while current_time <= end_time:
        #print("current_ssid:::::", current_ssid)
        # print("previous_ssid::::ASASAS", previous_ssid)
        # print("current_time", current_time, "end_time", end_time, flush=True)
        for sta in vehicle_list:
            # time.sleep(0.1)

            veh_id = sta.params['wlan'][0]
            # print(sta, flush=True)
            # print('++++++ current_time: ' + str(current_time) + ', vehicle:' + veh_id +'+++++++++++++++', flush=True)
            result = worker(sta, current_time, last_timestamp, current_ssid, history)
            current_ssid = result[1]
            vehicle_id = result[2]
            # history = result[3]
            current_time = result[4]
            ###############################
            # to be removed #
            if (len(essid_info)) == 0: # new entry
                essid_info[(result[1],result[2])] = result[0]
            else:  # not new entry but old key and new value
                if (essid_info.__contains__((result[1],result[2]))):
                    essid_info[(result[1],result[2])] += result[0]
                else:  # not new entry but new key and value
                    essid_info[(result[1],result[2])] = result[0]
            next_ssid = current_ssid
######################################################################################
            # next_ssid = ssid_to_ap.get(next_ssid)
            previous_ssid = previous_ssid_for_vehs[veh_id]
            # print("previous_ssid:::::ASASAAS___B", previous_ssid)
            # print("veh_id:::::ASASAAS___B", veh_id)
            # previous_ssid = ssid_to_ap.get(previous_ssid)
#####################################################################################
###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$###
            # Define the rsu_to_ssid dictionary
            rsu_to_ssid = {ap_list[8]: 'new-ssid-9'}#, ...}  # Add more entries as needed
            # Assuming veh_id contains the identifier for the vehicle
            if veh_id in previous_ssid_for_vehs:
                if previous_ssid in rsu_to_ssid:
                    # Convert previous_ssid to the corresponding SSID value from the dictionary
                    previous_ssid = rsu_to_ssid[previous_ssid]
                    # print("previous_ssid:::::ASASAAS___A", previous_ssid)
                # print("previous_ssid:::::ASASAAS___A", previous_ssid)
                # print("veh_id:::::ASASAAS___A", veh_id)
            # Now you can use previous_ssid with the converted value
###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$######If No MIGRATION REQUIRED FROM BELOW COMMENT THE CODE#####################################

            # print("next_SSID::::", next_ssid, flush=True)
            # print("previous_SSID::::", previous_ssid, flush=True)
            ######################################################################################
            if next_ssid != previous_ssid and next_ssid != "Unknown" and previous_ssid != "Unknown":
                # compute for new value of session time for that vehicle movement #
                # print("previous_ssid::::HISTORY_SESS_01", previous_ssid)
                session_time = current_time - entry_time_previous_ssid_for_vehs[veh_id]
                if (previous_ssid, next_ssid) not in history_sessiontime_from_to:
                    history_sessiontime_from_to[(previous_ssid, next_ssid)] = []
                if current_time not in history_sessiontime_from_to[(previous_ssid, next_ssid)]:
                    history_sessiontime_from_to[(previous_ssid, next_ssid)].append({'time': current_time, 'session_time': session_time})
                # update new entry time value into dictionary entry_time_previous_ssid_for_vehs
                entry_time_previous_ssid_for_vehs[veh_id] = current_time

                temp = history_sessiontime_from_to[(previous_ssid, next_ssid)]
                # print("temp::::", temp)
                #################################################__PANDAS_DataFrame_EWMA__#################################
                # Flatten the dictionary into a list of dictionaries
                flattened_data = []
                for key, value in history_sessiontime_from_to.items():
                    for item in value:
                        flattened_data.append({'previous_SSID': key[0], 'next_SSID': key[1], **item})

                # Create a DataFrame from the flattened data
                df = pd.DataFrame(flattened_data)
                # print("DF::::___:::",df)
                columns_to_display = ['previous_SSID' , 'next_SSID', 'time', 'session_time']#, 'time', 'session_time']
                partial_df = df[columns_to_display]
                # print("partial_DF::::___:::",partial_df, flush=True)
                # Group by 'next_ssid' and 'previous_ssid', aggregating 'time' and 'session_time'
                grouped_df = partial_df.astype(str).groupby(['previous_SSID', 'next_SSID']).agg({
                    'time': ', '.join,
                    'session_time': ', '.join
                }).reset_index()

                # print("Grouped DataFrame:::__\n", grouped_df, flush=True)

                # Specify the alpha value for weighted moving average
                alpha = 0.1  # Example alpha value
                # Convert 'time' and 'session_time' columns to lists of numbers
                grouped_df['time'] = grouped_df['time'].str.split(', ').apply(lambda x: list(map(float, x)))
                grouped_df['session_time'] = grouped_df['session_time'].str.split(', ').apply(lambda x: list(map(float, x)))

                # Calculate the weighted moving average for each group of previous_SSID and next_SSID
                grouped_df['WMA'] = grouped_df.apply(lambda row: pd.Series(row['session_time']).ewm(alpha=alpha, adjust=False).mean().values.tolist(), axis=1)
                # print("HELO Before DF")
                #print("grouped_df_EWMA::::___",grouped_df, flush=True)
                ###############################################__PANDAS_DataFrame_EWMA__##########################
                ################################################__CONTROLLER_LOGIC__##############################
                # Check if 3 minutes have passed
                # Get the IP addresses of next_ssid and min_previous_ssid
                next_ssid_ip = None
                min_previous_ssid_ip = None
                # Mapping between SSID names in your code and Mininet-WiFi definitions
                # ssid_to_ip dictionary mapping SSID to IP address
                # print("HELO Before M.Interval")
                min_previous_ssid = None
                # Initialize a dictionary to store the linked previous_ssids for each next_ssid within each monitoring interval
                linked_previous_ssids = {}
                # time.sleep(0.01)
                #print("current_time Before Monitoring Interval", current_time % monitoring_interval)
                if current_time % monitoring_interval == 0:
                    print("current_time", current_time, "end_time", end_time, flush=True)
                    minutes_passed = current_time // 60
                    #print(f"{minutes_passed} minutes completed")
                    monitoring_data[minutes_passed] = []
                    # time.sleep(0.15)
                    wma_data={}
                    # Create a list to store the data for this interval
                    interval_data = []
                    # print("previous_ssid_CHECKCHECK", previous_ssid)
                    for index, row in grouped_df.iterrows():
                        next_ssid = row['next_SSID']
                        # previous_ssid = row['previous_SSID']
                        # wma_values = row['WMA']
                        time_values = row['time']
                        wma_values = row['WMA']
                        wma_data[previous_ssid] = wma_values
                        monitoring_data[minutes_passed].append({'previous_ssid': previous_ssid, 'next_ssid': next_ssid, 'wma_values': wma_values, 'time_values': time_values})
                        # Group the DataFrame by 'next_ssid' and iterate through each group
                        for next_ssid, group_df in grouped_df.groupby('next_SSID'):
                            # Extract the unique 'previous_ssid' values for this 'next_ssid'
                            previous_ssids = group_df['previous_SSID'].unique()
                            # Extract the 'WMA' arrays for each (previous_ssid, next_ssid) pair
                            wma_data = {}
                            # Create an empty list to store data
                            data_list = []
                            for index, row in group_df.iterrows():
                                previous_ssid = row['previous_SSID']
                                wma_values = row['WMA']
                                wma_data[previous_ssid] = wma_values
                            # # Store the linked previous_ssids in the dictionary
                            # # linked_previous_ssids[next_ssid] = previous_ssids
                            ########################################################################################################################
                            # Store the linked previous_ssids and their WMA arrays in the dictionary
                            linked_previous_ssids[next_ssid] = {'previous_ssids': previous_ssids.tolist(),'wma_data': wma_data}
                            # Compare WMA arrays for each (previous_ssid, next_ssid) pair and find the smallest WMA
                            min_wma = float('inf')  # Initialize with a large value
                            # min_previous_ssid = None
                            for previous_ssid, wma_values in wma_data.items():
                                # Calculate the average of the WMA array
                                avg_wma = sum(wma_values) / len(wma_values)
                                # Check if this WMA array is smaller than the current minimum
                                if avg_wma < min_wma:
                                    min_wma = avg_wma
                                    min_previous_ssid = previous_ssid
                                min_previous_ssid1 = min_previous_ssid
                            min_previous_ssid1
                            # linked_previous_ssids[next_ssid]['smallest_previous_ssid'] = ssid_to_ap.get(min_previous_ssid1)
                            linked_previous_ssids[next_ssid]['smallest_previous_ssid'] = min_previous_ssid1
                            linked_previous_ssids[next_ssid]['smallest_wma_value'] = min_wma
                            CSVFunc.LinkedPreviousSSID_Dict_to_csv(linked_previous_ssids, 'LinkedPreviousoutput.csv')
                    if execute_flag:
                        #print('inside the execute flag', flush=True)
                        #for interval, data in monitoring_data.items():
                            #print(f"~~~~~~~~~~~__________________^^^^^^^^^^Monitoring Interval___________^^^^^^^^^^~~~~~~: {interval} minutes")
                            #for item in data:
                                #print(f"Previous SSID: {item['previous_ssid']}")
                                #print(f"Next SSID: {item['next_ssid']}")
                                #print(f"WMA Values: {item['wma_values']}")
                                #print(f"Time Values: {item['time_values']}")
                        # Check if the flag is set to execute
                        # if execute_flag:
                            # Your execution code here
                        for next_ssid, data in linked_previous_ssids.items():
                            #print(f"Next SSID: {next_ssid}")
                            #print(f"Linked Previous SSIDs: {', '.join(data['previous_ssids'])}")
                            # Compare WMA arrays for each (previous_ssid, next_ssid) pair
                            #for previous_ssid, wma_values in data['wma_data'].items():
                            #    print(f"Previous SSID: {previous_ssid}, WMA Values: {wma_values}")
                            #print(f"Smallest Previous SSID: {data['smallest_previous_ssid']}")
                            min_previous_ssid1 = data['smallest_previous_ssid']
                            #print(f"Smallest WMA Value: {data['smallest_wma_value']}")
                            # Get the AP objects for next_ssid and smallest_previous_ssid
                            # next_ssid_ap = ssid_to_ap.get(next_ssid)
                            # print("next_ssid_ap", next_ssid_ap)
                            ###############%^%^%^^^%^%^%^#######################################
                            min_previous_ssid = ssid_to_ap.get(min_previous_ssid1)
                            #print("min_previous_ssid__END::", min_previous_ssid)
                            next_ssid = ssid_to_ap.get(next_ssid)
                            #print("next_ssid__END::", next_ssid)
                            
                            SwMigrationFunc.check_migration(next_ssid, min_previous_ssid, controllers, stations)
                            # SwMigrationFunc.check_migration(next_ssid, min_previous_ssid, c1, c2, c3, stations[0], stations[1], stations[2], stations[3], stations[4], stations[5])
                            #print("FLAG:::::TRUE^^^^^^")

                        exe_comm = f'sudo ovs-vsctl show'
                        command = os.system(exe_comm)
                        # Set the flag to False, in order to prevent multiple executions
                        execute_flag = False
                        #print("FLAG:::::FALSE^^^^^^")
                        #print()
                # If it hasn't been 180 seconds, reset the flag to True
                elif not execute_flag:
                    execute_flag = True

            ##else:
                  ##print('-----------' + veh_id + ' does NOT change its ssid and remains at '+ next_ssid +'-------------')#, flush=True)
            # update new ssid value into dictionary previous_ssid_for_vehs
            previous_ssid_for_vehs[veh_id] = next_ssid
            # previous_ssid_for_vehs[veh_id] = ssid_to_ap.get(previous_ssid_for_vehs[veh_id])
            # print("next_ssid__ENDENDEND", next_ssid)
            # print("previous_ssid_for_vehs[veh_id]__ENDENDEND",previous_ssid_for_vehs[veh_id])
###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$######If No MIGRATION REQUIRED Till Here COMMENT THE CODE#####################################
        current_time = current_time + 1
        if current_time >= end_time:
            time.sleep(0.5)
            break
        # print("All workers finished", flush=True)
    ##### # dict_to_csv(history_sessiontime_from_to)
    CSVFunc.dict_to_csv(history_sessiontime_from_to)
    print("previous_ssid___AFTER CSV FUNC", previous_ssid)
    # df_to_csv1(grouped_df)
    filename = 'output_dataframe.csv'
    # dataframe_to_csv(grouped_df, 'output_dataframe.csv')
    CSVFunc.dataframe_to_csv(grouped_df, filename)
    # dict_to_csv(avg_session_time, essid_info)
    # CSVFunc.LinkedPreviousSSID_Dict_to_csv(linked_previous_ssids, 'LinkedPreviousoutput.csv')
    # Call the function to save the output data to a CSV file
    CSVFunc.monitoring_output_to_csv(linked_previous_ssids, 'NextSSIDlinkedPrevSSID.csv')
    info("*** Running CLI\n")
    CLI(net)
    # # Stop RYU controllers when the CLI is excited
    # for process in ryu_processes:
    #     process.terminate()
    #info("*** Stopping network\n")
    net.stop()
    pass
