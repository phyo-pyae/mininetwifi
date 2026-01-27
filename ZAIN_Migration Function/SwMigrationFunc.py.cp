import csv
import os
import subprocess
import time
from mininet.term import makeTerm

def check_migration(next_ssid, min_previous_ssid, c1, c2, c3, sta1, sta2, sta3, sta4, sta5, sta6):
    veh_ips = ["10.0.2.1", "10.0.2.2", "10.0.2.3", "10.0.2.4", "10.0.2.5", "10.0.2.6"]
    ips_to_controller = {
                    'tcp:127.0.0.1:6651': c1,
                    'tcp:127.0.0.1:6652': c2,
                    'tcp:127.0.0.1:6653': c3,
                }
    print("INSIDE SW MIGRATION FUNC")
    # Print the incoming next_ssid
    print(f"__^^Incoming next_ssid: {next_ssid}")
    # Command to execute
    command_template = "ovs-vsctl get-controller {}"
    command_template1= "ovs-vsctl show"
    command_del_port="ovs-vsctl del-port {}"

    # Execute the command for next_ssid
    next_ssid_command = command_template.format(next_ssid)
    next_ssid_output = os.popen(next_ssid_command).read().strip()
    next_ssid_controller_ip = next_ssid_output
    print(f"Inside__^^Controller IP for {next_ssid}: {next_ssid_controller_ip}")
    # Execute the command for min_previous_ssid
    min_previous_ssid_command = command_template.format(min_previous_ssid)
    min_previous_ssid_output = os.popen(min_previous_ssid_command).read().strip()
    min_previous_ssid_controller_ip = min_previous_ssid_output
    # print(f"Inside__^^Controller IP for {min_previous_ssid}: {min_previous_ssid_controller_ip}")
    # Check for the presence of duplicates and correct the format
    if "tcp:tcp:" in min_previous_ssid_controller_ip and ":6653:6653" in min_previous_ssid_controller_ip:
        # Correct the format by removing duplicates
        min_previous_ssid_controller_ip = min_previous_ssid_controller_ip.replace("tcp:tcp:", "tcp:").replace(":6653:6653", ":6653")
    print(f"Inside__^^Controller IP for {min_previous_ssid}: {min_previous_ssid_controller_ip}")
    # Get the Mininet-WiFi controller objects using the IPs
    next_ssid_controller = ips_to_controller.get(next_ssid_controller_ip, None)
    print("next_ssid_controller__^^::", next_ssid_controller)
    min_previous_ssid_controller = ips_to_controller.get(min_previous_ssid_controller_ip, None)
    print("min_previous_ssid_controller__^^::", min_previous_ssid_controller)

    if next_ssid_controller != min_previous_ssid_controller and next_ssid_controller != "connection-mode=out-of-band" and min_previous_ssid_controller != "connection-mode=out-of-band" and min_previous_ssid_controller != None and next_ssid_controller!=None:
        time.sleep(1)  # East/West Bound Delay
        print("Apply Migration")
        migrate_controller(min_previous_ssid_controller, next_ssid, min_previous_ssid_controller_ip, sta1, sta2, sta3, sta4, sta5, sta6)  # , min_previous_ssid)
    else:
        print("No Migration Required")

def migrate_controller(min_previous_ssid_controller, next_ssid, min_previous_ssid_controller_ip, sta1, sta2, sta3, sta4, sta5, sta6):#, min_previous_ssid):
    veh_ips = ["10.0.2.1", "10.0.2.2", "10.0.2.3", "10.0.2.4", "10.0.2.5", "10.0.2.6"]
    ips_to_veh = {
                    # 'new-ssid-0': None,
                    '10.0.2.1': sta1,
                    '10.0.2.2': sta2,
                    '10.0.2.3': sta3,
                    '10.0.2.4': sta4,
                    '10.0.2.5': sta5,
                    '10.0.2.6': sta6,
                }

    # Execute migration commands
    for veh_ip in veh_ips:
        print("Vehicle IP:::&^&^&^BF_MIG", veh_ip)
        if min_previous_ssid_controller != None and min_previous_ssid_controller_ip != None and next_ssid != None:
            migration_command = f"bash -c './gen_fr_rsu.py {next_ssid} {min_previous_ssid_controller_ip} {veh_ip}'"
            makeTerm(min_previous_ssid_controller, cmd=migration_command)
            print("Vehicle IP:::&^&^&^AF_MIG", veh_ip)
            ofr=f"ovs-ofctl dump-flows {next_ssid}" #ofr = "open flow rules" which are executed in each next_SSID
            os.system(ofr)
        print("OUTSIDE of the IF LOOP, Now lets check the status of each RSU")

        ofr1 = f"ovs-ofctl dump-flows {next_ssid}"  # ofr = "open flow rules" which are executed in each next_SSID
        os.system(ofr1)

    # Update the controller for next_ssid
    set_controller_command = f"ovs-vsctl set-controller {next_ssid} {min_previous_ssid_controller_ip}"
    os.system(set_controller_command)
