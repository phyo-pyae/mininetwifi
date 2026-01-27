import csv
import os
import subprocess
import time
from mininet.term import makeTerm

def check_migration(next_ssid, min_previous_ssid, controllers, stations):
    # Assuming the range for IPs is from 10.0.2.1 to 10.0.2.254
    veh_ips = [f"10.0.2.{i}" for i in range(1, 255)]

    ips_to_controller = {f'tcp:127.0.0.1:{6650 + i}': controllers[i] for i in range(len(controllers))}

    def get_controller_ip(ssid):
        command_template = "ovs-vsctl get-controller {}"
        return os.popen(command_template.format(ssid)).read().strip()

    def migrate_controller(min_previous_ssid_controller, next_ssid, min_previous_ssid_controller_ip, *stations):
        ips_to_veh = {f'10.0.2.{i}': stations[i] for i in range(len(stations))}

        for veh_ip in veh_ips:
            if min_previous_ssid_controller and min_previous_ssid_controller_ip and next_ssid:
                migration_command = f"bash -c './gen_fr_rsu.py {next_ssid} {min_previous_ssid_controller_ip} {veh_ip}'"
                makeTerm(min_previous_ssid_controller, cmd=migration_command)
                ofr = f"ovs-ofctl dump-flows {next_ssid}"
                os.system(ofr)

        set_controller_command = f"ovs-vsctl set-controller {next_ssid} {min_previous_ssid_controller_ip}"
        os.system(set_controller_command)

    next_ssid_controller_ip = get_controller_ip(next_ssid)
    min_previous_ssid_controller_ip = get_controller_ip(min_previous_ssid)

    if "tcp:tcp:" in min_previous_ssid_controller_ip and ":6653:6653" in min_previous_ssid_controller_ip:
        min_previous_ssid_controller_ip = min_previous_ssid_controller_ip.replace("tcp:tcp:", "tcp:").replace(":6653:6653", ":6653")

    next_ssid_controller = ips_to_controller.get(next_ssid_controller_ip, None)
    min_previous_ssid_controller = ips_to_controller.get(min_previous_ssid_controller_ip, None)

    if next_ssid_controller != min_previous_ssid_controller and next_ssid_controller != "connection-mode=out-of-band" and min_previous_ssid_controller != "connection-mode=out-of-band" and min_previous_ssid_controller and next_ssid_controller:
        time.sleep(1)
        print("Apply Migration")
        migrate_controller(min_previous_ssid_controller, next_ssid, min_previous_ssid_controller_ip, *stations)
    else:
        print("No Migration Required")

# Example usage:
num_controllers = 3
num_stations = 6
controllers_list = [f'c{i}' for i in range(1, num_controllers + 1)]
stations_list = [f'sta{i}' for i in range(1, num_stations + 1)]
check_migration("next_ssid_value", "min_previous_ssid_value", controllers_list, stations_list)

