#OVS-CONNECTION for RSU1Test with C1:
ovs-vsctl set-controller rsu1 tcp:127.0.0.1:6651
#ovs-vsctl set controller rsu1 connection-mode=out-of-band
#ovs-vsctl set-fail-mode rsu1 secure
ifconfig rsu1-wlan1 10.0.2.10/24
#sleep(4)
#python Listener_testpythontest_SAVED.py




#sudo ovs-ofctl add-flow rsu1 arp,in_port=1,priority=100,dl_src=00:00:00:00:00:02,arp_tpa=10.0.2.8,actions=output:4
#sudo ovs-ofctl add-flow rsu2 arp,in_port=4,priority=100,dl_src=00:00:00:00:00:04,arp_tpa=10.0.2.5,actions=output:1
#sudo ovs-ofctl add-flow rsu1 arp,in_port=4,priority=100,dl_src=00:00:00:00:00:04,arp_tpa=10.0.2.5,actions=output:1

#sudo ovs-ofctl add-flow rsu1 ip,in_port=1,priority=100,dl_dst=00:00:00:00:00:04,nw_dst=10.0.2.8,actions=output:4
#sudo ovs-ofctl add-flow rsu1 ip,in_port=4,priority=100,dl_dst=00:00:00:00:00:02,nw_dst=10.0.2.5,actions=output:1
