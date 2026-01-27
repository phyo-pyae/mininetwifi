from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_4
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import time
import socket
import os


class SimpleSwitch14(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_4.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch14, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.target_dpid = 1000000000000001#[1000000000000001, 1000000000000002]
        self.datapath = 1000000000000001
        # self.controller_ip = "10.0.3.200"
        # self.controller_port = 49155
        # self.threshold = -28
        # self.old_controller="10.0.4.200"
        # self.new_controller="10.0.3.200"
        # self.SRC_IP='10.0.2.4'
        # self.DST_IP='10.0.2.7'
        # self.SRC_MAC='00:00:00:00:00:02'
        # self.DST_MAC='00:00:00:00:00:07'
        # self.hard_timeout = 10
        self.last_packet_timestamps = {}
        print('HELLO Step-1_INITIAL Step')
        counter = 0
        #socket_rec=self.check_rssi_threshold(threshold, controller_ip, controller_port)
        #socket_rec is None
        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        #start_time = time.time()
        print('Installing flow rules...._switch_features_handler')
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        print(self.datapath)
        #print(self.target_dpid)
        # if self.datapath == self.target_dpid:
            # Add flow rules for switch port 1
        match = parser.OFPMatch(in_port=1, eth_type=ether_types.ETH_TYPE_IP)#, ipv4_src=self.SRC_IP)
        #match = parser.OFPMatch(in_port=1, eth_type=ether_types.ETH_TYPE_IP)#, ipv4_src=self.SRC_IP)
        #actions = [parser.OFPActionSetField(eth_src=self.SRC_MAC), parser.OFPActionSetField(eth_dst=self.DST_MAC), parser.OFPActionOutput(3)]
        actions = [parser.OFPActionOutput(3)]
        self.add_flow(datapath,100, match, actions, hard_timeout=1)#, self.hard_timeout)

        # Add flow rule for switch port L2S-eth4
        match = parser.OFPMatch(in_port=3, eth_type=ether_types.ETH_TYPE_IP)#, ipv4_src=self.DST_IP)
        #match = parser.OFPMatch(in_port=3, eth_type=ether_types.ETH_TYPE_IP)#, ipv4_dst=self.DST_IP)
        #actions = [parser.OFPActionSetField(eth_src=self.DST_MAC), parser.OFPActionSetField(eth_dst=self.SRC_MAC), parser.OFPActionOutput(1)]
        actions = [parser.OFPActionOutput(1)]
        self.add_flow(datapath,100, match, actions, hard_timeout=1)#, self.hard_timeout)

        # Add flow rule for ARP packets on switch port S1-wlan1
        match = parser.OFPMatch(in_port=1, eth_type=ether_types.ETH_TYPE_ARP)#, arp_spa=self.SRC_IP, arp_tpa=self.DST_IP)
        #actions = [parser.OFPActionSetField(eth_src=self.SRC_MAC), parser.OFPActionSetField(eth_dst=self.DST_MAC), parser.OFPActionOutput(3)]
        actions = [parser.OFPActionOutput(3)]
        self.add_flow(datapath,100, match, actions, hard_timeout=1)#, self.hard_timeout)

        # Add flow rule for ARP packets on switch port L2S-eth4
        match = parser.OFPMatch(in_port=3, eth_type=ether_types.ETH_TYPE_ARP)#, arp_spa=self.DST_IP, arp_tpa=self.SRC_IP)
        #actions = [parser.OFPActionSetField(eth_src=self.DST_MAC), parser.OFPActionSetField(eth_dst=self.SRC_MAC), parser.OFPActionOutput(1)]
        actions = [parser.OFPActionOutput(1)]
        self.add_flow(datapath,100, match, actions, hard_timeout=1)#, self.hard_timeout)

        print('HELLO Step-2-A_switch_features_handler')
        #socket_rec = self.check_rssi_threshold(self.controller_ip, self.controller_port)
        #time.sleep(10)
        #chg_con = self.change_controller(self.old_controller, self.new_controller)
        # else:
        #     print('No Flow Rules will be assigned')
        #     return
        #end_time=time.time()
        #elapsed_time=end_time-start_time
        #print(f'Flow rules installed in {elapsed_time:.2f} seconds')
        #with open("flow_rules_install_time.txt", "a") as file:
            #file.write(f'flow rules installed in {elapsed_time:.2f} seconds\n')

    def add_flow(self, datapath, priority, match, actions, buffer_id=None, hard_timeout=1):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, hard_timeout=hard_timeout)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, hard_timeout= hard_timeout)
        datapath.send_msg(mod)
        print('HELLO Step-3_add_flow')
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        # eth = pkt.get_protocols(ethernet.ethernet)[0]
        eth = pkt.get_protocol(ethernet.ethernet)
        print('1st HELLO Step-4_packet_in_handler')
        # print("packet_in_handler_ETH:", eth)
        # print("packet_in_handler_PKT:", pkt)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
##########################################################################
        # Get the current timestamp
        # current_time = time()
        #
        # # Checking IF MAC address is in the last_packet_timestamps dictionary
        # if src not in last_packet_timestamps:
        #     # If the MAC address NOT in Dict
        #     print("Delaying packet processing for MAC address:", src)
        #     sleep(1)
        #
        #     # Updating the last timestamp
        #     last_packet_timestamps[src] = current_time
        #     print("last_packet_timestamps", last_packet_timestamps)
        # print("src ___IF_LOOP", src)
###################################################################################
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        # print("packet_in_handler_DatapathID:", dpid)

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        # print("INSIDE  packet_in_handler_DatapathID:", dpid)
        # print("INSIDE   src",src )
        # print("INSIDE   dst",dst)
        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
        print('2nd HELLO Step-4_packet_in_handler')
        # Install a flow to avoid packet_in next time
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            actions = [parser.OFPActionOutput(out_port)]
            if in_port == 1 and eth.ethertype == ether_types.ETH_TYPE_IP:
                match = parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP)
                self.add_flow(datapath, 100, match, actions, hard_timeout=1)
            elif in_port == 3 and eth.ethertype == ether_types.ETH_TYPE_IP:
                match = parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP)
                self.add_flow(datapath, 100, match, actions, hard_timeout=1)
            elif in_port == 1 and eth.ethertype == ether_types.ETH_TYPE_ARP:
                match = parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_ARP)
                self.add_flow(datapath, 100, match, actions, hard_timeout=1)
            elif in_port == 3 and eth.ethertype == ether_types.ETH_TYPE_ARP:
                match = parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_ARP)
                self.add_flow(datapath, 100, match, actions, hard_timeout=1)
            print('3rdIF HELLO Step-4_packet_in_handler')

        out_port = self.mac_to_port[dpid].get(dst, ofproto.OFPP_FLOOD)
        actions = [parser.OFPActionOutput(out_port)]
        print('4th HELLO Step-4_packet_in_handler')
        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            self.add_flow(datapath,100, match, actions, hard_timeout=1)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
        print('5th HELLO Step-4_packet_in_handler')
        
