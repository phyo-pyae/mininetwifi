# !/bin/bash
import time

next_ssid=$1
min_previous_ssid_controller_ip=$2
veh_ip=$3

echo "Next SSID: $next_ssid" >> hey.txt
echo "Min Previous SSID Controller IP: $min_previous_ssid_controller_ip"  >> hey.txt
echo "Vehicle IP: $veh_ip"  >> hey.txt

# print("Inside Gen_Fr_RSU.PY")
# sudo ovs-vsctl show
# veh_ips = ["10.0.2.1", "10.0.2.2", "10.0.2.3", "10.0.2.4", "10.0.2.5", "10.0.2.6"]
# sudo ovs-vsctl del-port $1-eth2  >> hey.txt


# Set the new OVS controller for the next SSID
sudo ovs-vsctl set-controller $1 $2
# sudo ovs-vsctl set-controller $1 connection-mode=out-of-band
# sudo ovs-vsctl set-fail-mode $1 secure
# time.sleep(0.2)
# for veh_ip in veh_ips:
# sudo ovs-ofctl del-flows $1  >> hey.txt
# Assign the Flow Rules to the Respective Migrated Switch (Next SSID)
#sudo ovs-ofctl add-flow $1 arp,in_port=1,priority=100,arp_spa=$3,arp_tpa=10.0.2.7,hard_timeout=15,actions=output:3  >> hey.txt
# time.sleep(0.2)
#sudo ovs-ofctl add-flow $1 arp,in_port=3,priority=100,arp_spa=10.0.2.7,arp_tpa=$3,hard_timeout=15,actions=output:1  >> hey.txt
# time.sleep(0.2)
#sudo ovs-ofctl add-flow $1 ip,in_port=1,priority=100,nw_src=$3,nw_dst=10.0.2.7,hard_timeout=15,actions=output:3  >> hey.txt
# time.sleep(0.2)
#sudo ovs-ofctl add-flow $1 ip,in_port=3,priority=100,nw_src=10.0.2.7,nw_dst=$3,hard_timeout=15,actions=output:1  >> hey.txt
# time.sleep(0.2)

# sudo ovs-vsctl show
# # print("Inside Gen_Fr_RSU.PY")
# os.system("sudo +=====+++ovs-vsctl show")
# veh_ips = ["10.0.2.1", "10.0.2.2", "10.0.2.3", "10.0.2.4", "10.0.2.5", "10.0.2.6"]
# os.system("sudo ovs-vsctl del-port {next_ssid}-eth2")
# os.system("sudo ovs-vsctl del-flow {next_ssid}")
#
# # Set the new OVS controller for the next SSID
# os.system("sudo ovs-vsctl set-controller {next_ssid} tcp:{min_previous_ssid_controller_ip}:6653")
# os.system("sudo ovs-vsctl set controller {next_ssid} connection-mode=out-of-band")
# os.system("sudo ovs-vsctl set-fail-mode {next_ssid} secure")
#
# for veh_ip in veh_ips:
#     # Assign the Flow Rules to the Respective Migrated Switch (Next SSID)
#     os.system("sudo ovs-ofctl add-flow {next_ssid} arp,in_port=1,priority=100,arp_spa={veh_ip},arp_tpa=10.0.2.7,actions=output:3,hard_timeout=5")
#     os.system("sudo ovs-ofctl add-flow {next_ssid} arp,in_port=3,priority=0,arp_spa=10.0.2.7,arp_tpa={veh_ip},actions=output:1,hard_timeout=5")
#     os.system("sudo ovs-ofctl add-flow {next_ssid} ip,in_port=1,priority=10,nw_src={veh_ip},nw_dst=10.0.2.7,actions=output:3,hard_timeout=5")
#     os.system("sudo ovs-ofctl add-flow {next_ssid} ip,in_port=3,priority=10,nw_src=10.0.2.7,nw_dst={veh_ip}s,actions=output:1,hard_timeout=5")
#
# os.system("sudo ovs-vsctl show")