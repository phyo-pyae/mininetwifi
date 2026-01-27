import sys
import time
import os
import re
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use('TkAgg')
# import threading
# import concurrent.futures
import pandas as pd
import numpy as np 
#import pyp ing
#from core import *
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import OVSKernelAP
from mininet.term import makeTerm
# from threading import Timer
from time import sleep
from datetime import datetime
from collections import defaultdict
# from multiprocessing import Process
#rom mn_wifi.net import Mininet_wifi
from WorkerFunc import worker  # Import the worker function from WorkerFunc.py
# from CSVFunc import ssids_data_saved
import csv
import CSVFunc  # Import the CSV functions from CSVFunc .py
import SwMigrationFunc
# from CSVFunc import monitoring_output_to_csv
#import tkinter as tk
#import pandas as pd
# import tkinter as tk
from subprocess import Popen, PIPE
from  pythonping import ping
# def start_ryu_controller(controller_name, ryu_script):
#     log_file = open('ryu-{}.log'.format(controller_name), 'w')
#     return Popen(['ryu-manager', ryu_script, '--ofp-tcp-listen-port', '6633'], stdout=log_file, stderr=log_file)

def mininet_thread_function():
    global linked_previous_ssids
    setLogLevel('info')
    # if len(args) != 2:
    #     print("Usage: python solution.py < test-input.txt")
    #     exit(1)

    # maze = read_maze(argv[1])
    # start_row, start_col = 0, 0

    "Create a network."
    net = Mininet_wifi(controller=RemoteController, link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3, switch=OVSKernelAP)
    info("*** Creating nodes\n")
    ip_c1='127.0.0.1'
    # h1 = net.addHost('h1',ip=ip_c1)
    ip_c2='127.0.0.2'
    # h2 = net.addHost('h2',ip=ip_c2)
    ip_c3='127.0.0.3'
    # h3 = net.addHost('h3',ip=ip_c3)
    net.setMobilityModel(time=0, model='RandomWayPoint', seed=20)#,max_x=1000, max_y=1000, seed=20)

    #sta1 = net.addStation('veh1', mac='00:00:00:00:00:02', ip='10.0.2.5/24', min_x=5, max_x=80, min_y=50, max_y=51, min_v=0.5, max_v=1)# speed=1)
    Max_v=30#0.000000001
    Min_v=0.000000001
    # sta1=net.addStation('veh1', mac='00:00:00:00:00:01', ip='10.0.2.1/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # sta2=net.addStation('veh2', mac='00:00:00:00:00:02', ip='10.0.2.2/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # sta3=net.addStation('veh3', mac='00:00:00:00:00:03', ip='10.0.2.3/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # sta4=net.addStation('veh4', mac='00:00:00:00:00:04', ip='10.0.2.4/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # sta5=net.addStation('veh5', mac='00:00:00:00:00:05', ip='10.0.2.5/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # sta6=net.addStation('veh6', mac='00:00:00:00:00:06', ip='10.0.2.6/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # # # #rsu1 = net.addAccessPoint('rsu1', ssid='new-ssid',mac='00:00:00:00:00:03', ip='10.0.2.5/24',  mode='g', channel='1', position='75,100,0', range=25, failmode='secure',datapath='user') #, inNamespace=TRUE)
    # sta7 = net.addHost('veh7', mac='00:00:00:00:00:07', ip='10.0.2.7/24', range=10)
    sta1=net.addStation('veh1', mac='d6:76:e0:ab:36:71', ip='10.0.2.1/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    sta2=net.addStation('veh2', mac='d6:76:e0:ab:36:72', ip='10.0.2.2/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    sta3=net.addStation('veh3', mac='d6:76:e0:ab:36:73', ip='10.0.2.3/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    sta4=net.addStation('veh4', mac='d6:76:e0:ab:36:74', ip='10.0.2.4/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    sta5=net.addStation('veh5', mac='d6:76:e0:ab:36:75', ip='10.0.2.5/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    sta6=net.addStation('veh6', mac='d6:76:e0:ab:36:76', ip='10.0.2.6/24',min_x=-47, max_x=247, min_y=-47, max_y=247, min_v=Min_v, max_v=Max_v, min_wt=0, max_wt=0, range=1)
    # # #rsu1 = net.addAccessPoint('rsu1', ssid='new-ssid',mac='00:00:00:00:00:03', ip='10.0.2.5/24',  mode='g', channel='1', position='75,100,0', range=25, failmode='secure',datapath='user') #, inNamespace=TRUE)
    sta7 = net.addHost('veh7', mac='d6:76:e0:ab:36:77', ip='10.0.2.7/24', range=10)
    ap1 = net.addAccessPoint('rsu1', ssid='new-ssid-1',mac='00:00:00:00:02:10', ip='10.0.2.10/24',  mode='g', channel='1', position='0,200,0', dpid=str(1000000000000001), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap2 = net.addAccessPoint('rsu2', ssid='new-ssid-2',mac='00:00:00:00:02:40', ip='10.0.2.40/24',  mode='g', channel='1', position='100,200,0', dpid=str(1000000000000002), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap3 = net.addAccessPoint('rsu3', ssid='new-ssid-3',mac='00:00:00:00:02:80', ip='10.0.2.80/24',  mode='g', channel='1', position='200,200,0', dpid=str(1000000000000003), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap4 = net.addAccessPoint('rsu4', ssid='new-ssid-4',mac='00:00:00:00:02:11', ip='10.0.2.11/24',  mode='g', channel='1', position='0,100,0', dpid=str(1000000000000004), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap5 = net.addAccessPoint('rsu5', ssid='new-ssid-5',mac='00:00:00:00:02:41', ip='10.0.2.41/24',  mode='g', channel='1', position='100,100,0', dpid=str(1000000000000005), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap6 = net.addAccessPoint('rsu6', ssid='new-ssid-6',mac='00:00:00:00:02:81', ip='10.0.2.81/24',  mode='g', channel='1', position='200,100,0', dpid=str(1000000000000006), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap7 = net.addAccessPoint('rsu7', ssid='new-ssid-7',mac='00:00:00:00:02:12', ip='10.0.2.12/24',  mode='g', channel='1', position='0,0,0', dpid=str(1000000000000007), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap8 = net.addAccessPoint('rsu8', ssid='new-ssid-8',mac='00:00:00:00:02:42', ip='10.0.2.42/24',  mode='g', channel='1', position='100,0,0', dpid=str(1000000000000008), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')
    ap9 = net.addAccessPoint('rsu9', ssid='new-ssid-9',mac='00:00:00:00:02:82', ip='10.0.2.82/24',  mode='g', channel='1', position='200,0,0',dpid=str(1000000000000009), range=75, failmode='secure',datapath='user')#,cls=OVSKernelAP,protocols='OpenFlow13')

    sw1 = net.addSwitch('l2sw',cls=OVSSwitch, failmode='standalone')#, protocols="OPenFlow13")
    #sw1 = net.addAccessPoint('l2sw', ssid='new-ssid-4',mac='00:00:00:00:02:90',  mode='g', channel='1', position='75,50,0', range=20, failmode='secure',datapath='user', cls=OVSSwitch) 
    
	#'s2', ip='10.2.2.12/24',failMode='secure',datapath='user'
    c1 = net.addController('c1', controller=RemoteController,port = 6651)#,ip=ip_c1)
    c2 = net.addController('c2', controller=RemoteController,port = 6652)#,ip=ip_c2)
    c3 = net.addController('c3', controller=RemoteController,port = 6653)#,ip=ip_c3)
    # ryu_processes = [
    #     start_ryu_controller('c1', 'simple_switch_13.py'),
    #     start_ryu_controller('c2', 'simple_switch_13.py'),
    #     start_ryu_controller('c3', 'simple_switch_13.py')
    # ]
    info("*** Configuring wifi nodes\n")
    net.setPropagationModel(model="friis", exp=4)
    net.configureWifiNodes()

    nodes = net.stations
    # plt.switch_backend('agg')
    #net.telemetry(nodes=nodes, single=True, data_type='rssi')
    # net.plotGraph(min_x=-100, max_x=300, min_y=-100, max_y=300)

    info("*** Associating and Creating links\n")
    net.addLink(ap1, sw1)
    net.addLink(ap2, sw1)
    net.addLink(ap3, sw1)
    net.addLink(ap4, sw1)
    net.addLink(ap5, sw1)
    net.addLink(ap6, sw1)
    net.addLink(ap7, sw1)
    net.addLink(ap8, sw1)
    net.addLink(ap9, sw1)
    net.addLink(sw1, sta7)
    start_time = 10
    end_time = 2400
    net.plotGraph(min_x=-100, max_x=300, min_y=-100, max_y=300)
    # Define a flag to indicate if the code has been executed
    code_executed = False
    info("*** Starting network\n")
    net.build()
    c1.start()
    c2.start()
    c3.start()
    ap1.start([c1,c2,c3])
    ap4.start([c1,c2,c3])
    ap7.start([c1,c2,c3])
    ap2.start([c1,c2,c3])
    ap5.start([c1,c2,c3])
    ap8.start([c1,c2,c3])
    ap3.start([c1,c2,c3])
    ap6.start([c1,c2,c3])
    ap9.start([c1,c2,c3])
    sw1.start([])
#
    time.sleep(2)
    makeTerm(c1, cmd="bash -c 'ryu-manager simple_switch_13_B_C1.py --ofp-tcp-listen-port 6651 --verbose > H1.txt'")#, cmd="bash -c 'ryu-manager'")
    time.sleep(2)
    makeTerm(c2, cmd="bash -c 'ryu-manager simple_switch_13_B_C2.py --ofp-tcp-listen-port 6652 --verbose > H2.txt'")#, cmd="bash -c 'ryu-manager'")
    time.sleep(2)
    makeTerm(c3, cmd="bash -c 'ryu-manager simple_switch_13_B_C3.py --ofp-tcp-listen-port 6653 --verbose > H3.txt'")#, cmd="bash -c 'ryu-manager'")
    time.sleep(2)
    makeTerm(sta7, cmd="sudo tcpdump -i veh7-wlan0")
    time.sleep(60)
#   makeTerm(ap2, cmd="sudo ovs-vsctl show")
    makeTerm(sw1, cmd="bash -c './of_l2sw.py'")
    time.sleep(2)
    #time.sleep(3)
    makeTerm(ap1, cmd="bash -c './ovstest_rsu1.py'")
    time.sleep(1)
# ###############################################################################################################
#     # # makeTerm(ap1, cmd="bash -c './of_rsu1.py'")
#     time.sleep(1)
    makeTerm(ap2, cmd="bash -c './ovstest_rsu2.py'")
    time.sleep(1)
#     # # makeTerm(ap2, cmd="bash -c './of_rsu2.py'")
#     # # time.sleep(1)
#     # #makeTerm(ap2, cmd="bash -c './of_rsu2.py'")
#     time.sleep(1)
    makeTerm(ap3, cmd="bash -c './ovstest_rsu3.py'")
    time.sleep(1)
#     # # makeTerm(ap3, cmd="bash -c './of_rsu3.py'")
#     # time.sleep(1)
    makeTerm(ap4, cmd="bash -c './ovstest_rsu4.py'")
    time.sleep(1)
#     # # makeTerm(ap4, cmd="bash -c './of_rsu4.py'")
#     # time.sleep(1)
    makeTerm(ap5, cmd="bash -c './ovstest_rsu5.py'")
    time.sleep(1)
#     # # makeTerm(ap5, cmd="bash -c './of_rsu5.py'")
#     # time.sleep(1)
    makeTerm(ap6, cmd="bash -c './ovstest_rsu6.py'")
    time.sleep(1)
#     # # makeTerm(ap6, cmd="bash -c './of_rsu6.py'")
#     # time.sleep(1)
    makeTerm(ap7, cmd="bash -c './ovstest_rsu7.py'")
    time.sleep(1)
#     # # makeTerm(ap7, cmd="bash -c './of_rsu7.py'")
#     # # time.sleep(1)
    makeTerm(ap8, cmd="bash -c './ovstest_rsu8.py'")
    time.sleep(1)
    # # makeTerm(ap8, cmd="bash -c './of_rsu8.py'")
    # # time.sleep(1)
    makeTerm(ap9, cmd="bash -c './ovstest_rsu9.py'")
    time.sleep(1)
    ###############################################################################################################
    # makeTerm(ap9, cmd="bash -c './of_rsu9.py'")
#     # time.sleep(3)
#     # makeTerm(h1, cmd="bash -c 'sudo ip route add 10.0.4.0/24 via 10.0.3.10'")
#     # time.sleep(1)
#     # makeTerm(h2, cmd="bash -c 'sudo ip route add 10.0.3.0/24 via 10.0.4.10'")
#     # time.sleep(1)
#     # makeTerm(h2, cmd="bash -c 'sudo ip route add 10.0.5.0/24 via 10.0.4.10'")
#     # time.sleep(1)
#     time.sleep(2)
    makeTerm(sta7)#, cmd="sudo tcpdump -i veh7-eth1")
    # makeTerm(h3, cmd="bash -c 'sudo ip route add 10.0.4.0/24 via 10.0.5.10'")
    time.sleep(2)
    makeTerm(sta1, cmd = "ping 10.0.2.7 -i 0.2 -t 10 -c 15000 > veh1_log1610.txt") # -i 0.2 -c 6100 > s10.64.1.txt")
    # makeTerm(sta1, cmd='python veh_ping.py > veh1_log1610.txt')
    makeTerm(sta1, cmd="sudo tcpdump -i veh1-wlan0 -w veh1_log1610.pcap")
    # time.sleep(1)
    # makeTerm(sta1, cmd = "sudo tcpdump -i veh1-wlan0")# -w s10.64.1.pcap")
    time.sleep(1)
##########################################################################################################
    makeTerm(sta2, cmd = "ping 10.0.2.7 -i 0.2 -t 10 -c 15000 > veh2_log1610.txt")# -i 0.2 -c 6100 > s10.64.2.txt")
    # makeTerm(sta2, cmd="python veh_ping.py > veh2_log1610.txt")
    makeTerm(sta2, cmd="sudo tcpdump -i veh2-wlan0 -w veh2_log1610.pcap")
    # # time.sleep(1)
    # # makeTerm(sta2, cmd = "sudo tcpdump -i veh2-wlan0")# -w s10.64.2.pcap")
    time.sleep(1)
    makeTerm(sta3, cmd = "ping 10.0.2.7 -i 0.2 -t 10 -c 15000 > veh3_log1610.txt")# -i 0.2 -c 6100 > s10.64.3.txt")
    # makeTerm(sta3, cmd="python veh_ping.py > veh3_log1610.txt &")
    makeTerm(sta3, cmd="sudo tcpdump -i veh3-wlan0 -w veh3_log1610.pcap")
    # # time.sleep(1)
    # # makeTerm(sta3, cmd = "sudo tcpdump -i veh3-wlan0")# -w s10.64.3.pcap")
    time.sleep(1)
    makeTerm(sta4, cmd = "ping 10.0.2.7 -i 0.2 -t 10 -c 15000 > veh4_log1610.txt")# -i 0.2 -c 6100 > s10.64.4.txt")
    # makeTerm(sta4, cmd="python veh_ping.py > veh4_log1610.txt")
    makeTerm(sta4, cmd="sudo tcpdump -i veh4-wlan0 -w veh4_log1610.pcap")
    # # time.sleep(1)
    # # makeTerm(sta4, cmd = "sudo tcpdump -i veh4-wlan0 -w s10.64.4.pcap")
    time.sleep(1)
    makeTerm(sta5, cmd = "ping 10.0.2.7 -i 0.2 -t 10 -c 15000 > veh5_log1610.txt")# -i 0.2 -c 6100 > s10.64.5.txt")
    # makeTerm(sta5, cmd = "python veh1_ping.py > veh5_log1610.txt")# -i 0.2 -c 6100 > s10.64.5.txt")
    # makeTerm(sta5, cmd="python veh_ping.py > veh5_log1610.txt")
    makeTerm(sta5, cmd="sudo tcpdump -i veh5-wlan0 -w veh5_log1610.pcap")
    # # time.sleep(1)
    # # makeTerm(sta5, cmd = "sudo tcpdump -i veh5-wlan0")# -w s10.64.5.pcap")
    time.sleep(1)
    makeTerm(sta6, cmd = "ping 10.0.2.7 -i 0.2 -t 10 -c 15000 > veh6_log1610.txt")# -i 0.2 -c 6100 > s10.64.6.txt")
    # makeTerm(sta6, cmd="python veh_ping.py > veh6_log1610.txt")
    makeTerm(sta6, cmd="sudo tcpdump -i veh6-wlan0 -w veh6_log1610.pcap")
# ###########################################################################################
    # time.sleep(1)
    # makeTerm(sta6, cmd = "sudo tcpdump -i veh6-wlan0")# -w s10.64.6.pcap")
    # makeTerm(sta1, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sta2, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sta2, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sta3, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sta4, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sta5, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sta6, cmd="bash -c 'ping 10.0.2.7'")
    # time.sleep(1)
    # makeTerm(sw1)#, cmd="bash -c 'sudo tcpdump -i l2sw-eth10'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth1'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth2'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth3'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth4'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth5'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth6'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth7'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth8'")
    # time.sleep(1)
    # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth9'")
    # # makeTerm(sw1, cmd="bash -c 'sudo tcpdump -i l2sw-eth10'")
##################################################################################
    time.sleep(1)
    makeTerm(ap1)#, cmd="bash -c 'sudo tcpdump -i rsu1-wlan1'")
    time.sleep(1)
    makeTerm(ap2)#, cmd="bash -c 'sudo tcpdump -i rsu2-wlan1'")
    time.sleep(1)
    makeTerm(ap3)#, cmd="bash -c 'sudo tcpdump -i rsu3-wlan1'")
    time.sleep(1)
    makeTerm(ap4)#, cmd="bash -c 'sudo tcpdump -i rsu4-wlan1'")
    time.sleep(1)
    makeTerm(ap5)#, cmd="bash -c 'sudo tcpdump -i rsu5-wlan1'")
    time.sleep(1)
    makeTerm(ap6)#, cmd="bash -c 'sudo tcpdump -i rsu6-wlan1'")
    time.sleep(1)
    makeTerm(ap7)#, cmd="bash -c 'sudo tcpdump -i rsu7-wlan1'")
    time.sleep(1)
    makeTerm(ap8)#, cmd="bash -c 'sudo tcpdump -i rsu8-wlan1'")
    time.sleep(1)
    makeTerm(ap9)#, cmd="bash -c 'sudo tcpdump -i rsu9-wlan1'")
    time.sleep(1)
    # # makeTerm(sta7, cmd="bash -c 'sudo tcpdump -i sta7-wlan0'")
    # time.sleep(1)
    # makeTerm(sta7)#, cmd="bash -c 'sudo ovs-vsctl show'")
    # time.sleep(1)
#######################################################################################

    # net.plotGraph(min_x=-100, max_x=300, min_y=-100, max_y=300)

    print('I want to open IWCONFIG')
    #ap1.cmd("sudo ovs-vsctl show")

    now = start_time
    is_moving = False
    print('start_time', start_time, 'now', now, 'end_time', end_time)
    # Define a flag to indicate if the code has been executed
    code_executed = False
    current_time = now
    #current_time = time.time()#start_time#datetime.now().second
    #time.sleep(4)
    vehicle_list = [sta1, sta2, sta3, sta4, sta5, sta6]
    # Create a dictionary to store session times for each vehicle
    session_times = {}
    #command = sta1.cmd("iwconfig")

    #===============================================================
    essid_info = {}
    # essid_info = {(i, j): [] for i in range(1, 10) for j in range(1, 10)}
    futures = []
    current_ssid = 'new-ssid-0'
    last_timestamp = start_time
    history ={}
    avg_session_time = {}

    ######################################################################
    # previous_ssid_for_vehs = {'veh1-wlan0': 'rsu0', 'veh2-wlan0': 'rsu0', 'veh3-wlan0': 'rsu0', 'veh4-wlan0': 'rsu0', 'veh5-wlan0': 'rsu0', 'veh6-wlan0': 'rsu0'}# ssid0 is just null starting ssid
    previous_ssid_for_vehs = {'veh1-wlan0': 'new-ssid-0', 'veh2-wlan0': 'new-ssid-0', 'veh3-wlan0': 'new-ssid-0', 'veh4-wlan0': 'new-ssid-0', 'veh5-wlan0': 'new-ssid-0', 'veh6-wlan0': 'new-ssid-0'}; # ssid0 is just null starting ssid

    next_ssid_for_vehs = {};
    entry_time_previous_ssid_for_vehs = {'veh1-wlan0': 0, 'veh2-wlan0': 0, 'veh3-wlan0': 0, 'veh4-wlan0': 0, 'veh5-wlan0': 0, 'veh6-wlan0': 0} # 0 is just null starting ssid

    history_sessiontime_from_to = {};
    avg_sessiontime_from_to = {};
    ssid_vals = ["new-ssid-0", "new-ssid-1", "new-ssid-2", "new-ssid-3", "new-ssid-4", "new-ssid-5", "new-ssid-6", "new-ssid-7", "new-ssid-8", "new-ssid-9"]
    # ssid_vals = ["rsu0", "rsu1", "rsu2", "rsu3", "rsu4", "rsu5", "rsu6", "ap7", "rsu8", "rsu9"]
    for temp_previous_ssid in ssid_vals:
        for temp_next_ssid in ssid_vals:
            history_sessiontime_from_to[(temp_previous_ssid, temp_next_ssid)] = []
            avg_sessiontime_from_to[(temp_previous_ssid, temp_next_ssid)] = []
    ########################################################################
    # Learning rate (alpha)
    alpha = 0.2
    ewma_result = {}
    # Set the interval for monitoring completion (5 minutes)
    monitoring_interval = 120  # seconds
    # latest_monitoring_data = {}
    monitoring_data = {}
    # Initialize a flag to control the execution
    execute_flag = True
    # Initialize last_sweeping_printed to a time before the start_time
    # last_sweeping_printed = current_time - sweeping_timeperiod
    ssid_to_ap = {
                    # 'new-ssid-0': None,
                    'new-ssid-1': ap1,
                    'new-ssid-2': ap2,
                    'new-ssid-3': ap3,
                    'new-ssid-4': ap4,
                    'new-ssid-5': ap5,
                    'new-ssid-6': ap6,
                    'new-ssid-7': ap7,
                    'new-ssid-8': ap8,
                    # 'rsu9': 'new-ssid-9',
                    'new-ssid-9': ap9,
                    'rsu9':ap9,
                }
    #########################################################################
    while current_time <= end_time:
        print("current_ssid:::::ASASAS", current_ssid)
        # print("previous_ssid::::ASASAS", previous_ssid)
        print("current_time", current_time, "end_time", end_time, flush=True)
        for sta in vehicle_list:
            # time.sleep(0.1)

            veh_id = sta.params['wlan'][0]
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', flush=True)
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
            rsu_to_ssid = {ap9: 'new-ssid-9'}#, ...}  # Add more entries as needed
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

            print("next_SSID::::", next_ssid, flush=True)
            print("previous_SSID::::^^^AASASSSAA", previous_ssid, flush=True)
            ######################################################################################
            if next_ssid != previous_ssid and next_ssid != "Unknown" and previous_ssid != "Unknown":
                # compute for new value of session time for that vehicle movement #
                print("previous_ssid::::HISTORY_SESS_01", previous_ssid)
                session_time = current_time - entry_time_previous_ssid_for_vehs[veh_id]
                # print("session_time111:::__", session_time, flush=True)
                # print("current_time111:::__", current_time, flush=True)
                if (previous_ssid, next_ssid) not in history_sessiontime_from_to:
                    print("HELLOWWW")
                    # print("previous_ssid::::HISTORY_SESS_02", previous_ssid)
                    history_sessiontime_from_to[(previous_ssid, next_ssid)] = []
                    # print("history_sessiontime_from_to::::::", history_sessiontime_from_to, flush=True)
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
                print("HELO Before DF")
                print("grouped_df_EWMA::::___",grouped_df, flush=True)
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
                print("current_time Before Monitoring Interval", current_time % monitoring_interval)
                if current_time % monitoring_interval == 0:
                    minutes_passed = current_time // 60
                    print(f"{minutes_passed} minutes completed")
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
                        for interval, data in monitoring_data.items():
                            print(f"~~~~~~~~~~~__________________^^^^^^^^^^Monitoring Interval___________^^^^^^^^^^~~~~~~: {interval} minutes")
                            for item in data:
                                print(f"Previous SSID: {item['previous_ssid']}")
                                print(f"Next SSID: {item['next_ssid']}")
                                print(f"WMA Values: {item['wma_values']}")
                                print(f"Time Values: {item['time_values']}")
                        # Check if the flag is set to execute
                        # if execute_flag:
                            # Your execution code here
                        for next_ssid, data in linked_previous_ssids.items():
                            print(f"Next SSID: {next_ssid}")
                            print(f"Linked Previous SSIDs: {', '.join(data['previous_ssids'])}")
                            # Compare WMA arrays for each (previous_ssid, next_ssid) pair
                            for previous_ssid, wma_values in data['wma_data'].items():
                                print(f"Previous SSID: {previous_ssid}, WMA Values: {wma_values}")
                            print(f"Smallest Previous SSID: {data['smallest_previous_ssid']}")
                            min_previous_ssid1 = data['smallest_previous_ssid']
                            print(f"Smallest WMA Value: {data['smallest_wma_value']}")
                            # Get the AP objects for next_ssid and smallest_previous_ssid
                            # next_ssid_ap = ssid_to_ap.get(next_ssid)
                            # print("next_ssid_ap", next_ssid_ap)
                            ###############%^%^%^^^%^%^%^#######################################
                            min_previous_ssid = ssid_to_ap.get(min_previous_ssid1)
                            print("min_previous_ssid__END::", min_previous_ssid)
                            next_ssid = ssid_to_ap.get(next_ssid)
                            print("next_ssid__END::", next_ssid)

                            SwMigrationFunc.check_migration(next_ssid, min_previous_ssid, c1, c2, c3, sta1, sta2, sta3, sta4, sta5, sta6)
                            print("FLAG:::::TRUE^^^^^^")

                        exe_comm = f'sudo ovs-vsctl show'
                        command = os.system(exe_comm)
                        # Set the flag to False, in order to prevent multiple executions
                        execute_flag = False
                        print("FLAG:::::FALSE^^^^^^")
                        print()
                # If it hasn't been 180 seconds, reset the flag to True
                elif not execute_flag:
                    execute_flag = True
                        ###############%^%^%^^^%^%^%^#######################################
                        # next_ssid_Controller = f'ovs-vsctl get-controller {next_ssid}'
                        # NextSSID_Cont = os.system(next_ssid_Controller)
                        # # print("Controller IP For Next_SSID:::^^^", NextSSID_Cont)
                        # min_previous_ssid = ssid_to_ap.get(min_previous_ssid)
                        # print("min_previous_ssid:::BFLOP", min_previous_ssid)
                        # min_previous_ssid_Controller = f'ovs-vsctl get-controller {min_previous_ssid}'
                        # MinPreviousSSID_Cont = os.system(min_previous_ssid_Controller)
                        # SwMigrationFunc.check_migration(next_ssid_Controller, min_previous_ssid_Controller, next_ssid)
                        # SwMigrationFunc.check_migration(next_ssid, min_previous_ssid, h1, h2, h3)
                    # next_ssid=next_ssid
                    # min_previous_ssid=min_previous_ssid
                    # print("next_ssid___OUTSIDE_MIN_^_^", next_ssid)
                    # min_previous_ssid1 = data['smallest_previous_ssid']
                    # print("min_previous_ssid1___OUTSIDE_MIN_^_^",min_previous_ssid)
            else:
                  print('-----------' + veh_id + ' does NOT change its ssid and remains at '+ next_ssid +'-------------')#, flush=True)
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
        print("All workers finished", flush=True)
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
