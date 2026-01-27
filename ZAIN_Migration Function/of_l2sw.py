#OpenFlow Rules for L2SW:
#sudo ifconfig rsu1-wlan1 10.0.2.4/24
ovs-vsctl set-fail-mode l2sw standalone

#for AP1
# ovs-ofctl add-flow l2sw in_port=1,dl_src=00:00:00:00:02:10,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:10,priority=100,actions=output:1
ovs-ofctl add-flow l2sw arp,in_port=1,priority=100,arp_spa=10.0.2.10,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=1,priority=100,dl_src=00:00:00:00:02:10,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.10,actions=output:1
ovs-ofctl add-flow l2sw arp,in_port=1,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.10,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=1,priority=100,nw_src=10.0.2.10,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.10,actions=output:1
#ovs-ofctl add-flow l2sw in_port=1,dl_type=0x0806,dl_src=00:00:00:00:02:10,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
#ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:10,priority=100,actions=output:1
#ovs-ofctl add-flow l2sw in_port=1,dl_type=0x0800,dl_src=00:00:00:00:02:10,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
#ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:10,priority=100,actions=output:1
#sudo ovs-ofctl add-flow l2sw in_port=1,priority=100,actions=output:10
#sudo ovs-ofctl add-flow l2sw in_port=10,priority=100,actions=output:1
#sudo ovs-ofctl add-flow l2sw in_port=1,dl_src=00:00:00:00:02:10,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
#sudo ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:10,priority=100,actions=output:1

# #for AP2
ovs-ofctl add-flow l2sw arp,in_port=2,priority=100,arp_spa=10.0.2.40,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=2,priority=100,dl_src=00:00:00:00:02:40,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.40,actions=output:2
ovs-ofctl add-flow l2sw arp,in_port=2,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.40,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=2,priority=100,nw_src=10.0.2.40,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.40,actions=output:2
# ovs-ofctl add-flow l2sw in_port=2,dl_src=00:00:00:00:02:40,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:40,priority=100,actions=output:2
# ovs-ofctl add-flow l2sw in_port=2,dl_type=0x0806,dl_src=00:00:00:00:02:40,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:40,priority=100,actions=output:2
# ovs-ofctl add-flow l2sw in_port=2,dl_type=0x0800,dl_src=00:00:00:00:02:40,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:40,priority=100,actions=output:2
# ovs-ofctl add-flow l2sw in_port=2,priority=50,actions=output:10
#
# #for AP3
ovs-ofctl add-flow l2sw arp,in_port=3,priority=100,arp_spa=10.0.2.80,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=3,priority=100,dl_src=00:00:00:00:02:80,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.80,actions=output:3
ovs-ofctl add-flow l2sw arp,in_port=3,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.80,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=3,priority=100,nw_src=10.0.2.80,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.80,actions=output:3
# ovs-ofctl add-flow l2sw in_port=3,dl_src=00:00:00:00:02:80,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:80,priority=100,actions=output:3
# ovs-ofctl add-flow l2sw in_port=3,dl_type=0x0806,dl_src=00:00:00:00:02:80,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:80,priority=100,actions=output:3
# ovs-ofctl add-flow l2sw in_port=3,dl_type=0x0800,dl_src=00:00:00:00:02:80,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:80,priority=100,actions=output:3
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
# #for AP4
ovs-ofctl add-flow l2sw arp,in_port=4,priority=100,arp_spa=10.0.2.11,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=4,priority=100,dl_src=00:00:00:00:02:11,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.11,actions=output:4
ovs-ofctl add-flow l2sw arp,in_port=4,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.11,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=4,priority=100,nw_src=10.0.2.11,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.11,actions=output:4
# ovs-ofctl add-flow l2sw in_port=4,dl_src=00:00:00:00:02:11,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:11,priority=100,actions=output:4
# ovs-ofctl add-flow l2sw in_port=4,dl_type=0x0806,dl_src=00:00:00:00:02:11,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:11,priority=100,actions=output:4
# ovs-ofctl add-flow l2sw in_port=4,dl_type=0x0800,dl_src=00:00:00:00:02:11,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:11,priority=100,actions=output:4
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
# #for AP5
ovs-ofctl add-flow l2sw arp,in_port=5,priority=100,arp_spa=10.0.2.41,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=5,priority=100,dl_src=00:00:00:00:02:41,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.41,actions=output:5
ovs-ofctl add-flow l2sw arp,in_port=5,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.41,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=5,priority=100,nw_src=10.0.2.41,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.41,actions=output:5
# ovs-ofctl add-flow l2sw in_port=5,dl_src=00:00:00:00:02:41,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:41,priority=100,actions=output:5
# ovs-ofctl add-flow l2sw in_port=5,dl_type=0x0806,dl_src=00:00:00:00:02:41,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:41,priority=100,actions=output:5
# ovs-ofctl add-flow l2sw in_port=5,dl_type=0x0800,dl_src=00:00:00:00:02:41,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:41,priority=100,actions=output:5
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
# #for AP6
ovs-ofctl add-flow l2sw arp,in_port=6,priority=100,arp_spa=10.0.2.81,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=6,priority=100,dl_src=00:00:00:00:02:81,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.81,actions=output:6
ovs-ofctl add-flow l2sw arp,in_port=6,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.81,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=6,priority=100,nw_src=10.0.2.81,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.81,actions=output:6
# ovs-ofctl add-flow l2sw in_port=6,dl_src=00:00:00:00:02:81,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:81,priority=100,actions=output:6
# ovs-ofctl add-flow l2sw in_port=6,dl_type=0x0806,dl_src=00:00:00:00:02:81,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:81,priority=100,actions=output:6
# ovs-ofctl add-flow l2sw in_port=6,dl_type=0x0800,dl_src=00:00:00:00:02:81,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:81,priority=100,actions=output:6
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
# #for AP7
ovs-ofctl add-flow l2sw arp,in_port=7,priority=100,arp_spa=10.0.2.12,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=7,priority=100,dl_src=00:00:00:00:02:12,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.12,actions=output:7
ovs-ofctl add-flow l2sw arp,in_port=7,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.12,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=7,priority=100,nw_src=10.0.2.12,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.12,actions=output:7
# ovs-ofctl add-flow l2sw in_port=7,dl_src=00:00:00:00:02:12,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:12,priority=100,actions=output:7
# ovs-ofctl add-flow l2sw in_port=7,dl_type=0x0806,dl_src=00:00:00:00:02:12,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:12,priority=100,actions=output:7
# ovs-ofctl add-flow l2sw in_port=7,dl_type=0x0800,dl_src=00:00:00:00:02:12,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:12,priority=100,actions=output:7
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
# #for AP8
ovs-ofctl add-flow l2sw arp,in_port=8,priority=100,arp_spa=10.0.2.42,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=8,priority=100,dl_src=00:00:00:00:02:42,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.42,actions=output:8
ovs-ofctl add-flow l2sw arp,in_port=8,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.42,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=8,priority=100,nw_src=10.0.2.42,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.42,actions=output:8
# ovs-ofctl add-flow l2sw in_port=8,dl_src=00:00:00:00:02:42,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:42,priority=100,actions=output:8
# ovs-ofctl add-flow l2sw in_port=8,dl_type=0x0806,dl_src=00:00:00:00:02:42,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:42,priority=100,actions=output:8
# ovs-ofctl add-flow l2sw in_port=8,dl_type=0x0800,dl_src=00:00:00:00:02:42,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:42,priority=100,actions=output:8
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
# #for AP9
ovs-ofctl add-flow l2sw arp,in_port=9,priority=100,arp_spa=10.0.2.82,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=9,priority=100,dl_src=00:00:00:00:02:82,arp_tpa=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw arp,in_port=10,priority=100,arp_spa=10.0.2.7,arp_tpa=10.0.2.82,actions=output:9
ovs-ofctl add-flow l2sw arp,in_port=9,priority=100,dl_src=00:00:00:00:00:07,arp_tpa=10.0.2.82,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=9,priority=100,nw_src=10.0.2.82,nw_dst=10.0.2.7,actions=output:10
ovs-ofctl add-flow l2sw ip,in_port=10,priority=100,nw_src=10.0.2.7,nw_dst=10.0.2.82,actions=output:9
# ovs-ofctl add-flow l2sw in_port=9,dl_src=00:00:00:00:02:82,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:82,priority=100,actions=output:9
# ovs-ofctl add-flow l2sw in_port=9,dl_type=0x0806,dl_src=00:00:00:00:02:82,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0806,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:82,priority=100,actions=output:9
# ovs-ofctl add-flow l2sw in_port=9,dl_type=0x0800,dl_src=00:00:00:00:02:82,dl_dst=00:00:00:00:00:07,priority=100,actions=output:10
# ovs-ofctl add-flow l2sw in_port=10,dl_type=0x0800,dl_src=00:00:00:00:00:07,dl_dst=00:00:00:00:02:82,priority=100,actions=output:9
# #sudo ovs-ofctl add-flow l2sw in_port=1,priority=50,actions=output:4
#
#






