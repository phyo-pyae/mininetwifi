#OVS-CONNECTION for RSU2 with C3_H3:
#sleep(4)
ovs-vsctl set-controller rsu6 tcp:127.0.0.1:6653
#ovs-vsctl set controller rsu6 connection-mode=out-of-band
#ovs-vsctl set-fail-mode rsu6 secure
ifconfig rsu6-wlan1 10.0.2.81/24



#sudo ovs-ofctl add-flow rsu1 arp,in_port=1,priority=100,dl_src=00:00:00:00:00:02,arp_tpa=10.0.2.8,actions=output:4
#sudo ovs-ofctl add-flow rsu2 arp,in_port=4,priority=100,dl_src=00:00:00:00:00:04,arp_tpa=10.0.2.5,actions=output:1
#sudo ovs-ofctl add-flow rsu1 arp,in_port=4,priority=100,dl_src=00:00:00:00:00:04,arp_tpa=10.0.2.5,actions=output:1

#sudo ovs-ofctl add-flow rsu1 ip,in_port=1,priority=100,dl_dst=00:00:00:00:00:04,nw_dst=10.0.2.8,actions=output:4
#sudo ovs-ofctl add-flow rsu1 ip,in_port=4,priority=100,dl_dst=00:00:00:00:00:02,nw_dst=10.0.2.5,actions=output:1
