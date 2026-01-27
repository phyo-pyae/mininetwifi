# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import time


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.last_timestamp_dict={}
        #My Six Vehicle MAC Addresses
        self.last_timestamp_dict = { "d6:76:e0:ab:36:71": [], "d6:76:e0:ab:36:72": [], "d6:76:e0:ab:36:73": [],
                                     "d6:76:e0:ab:36:74": [], "d6:76:e0:ab:36:75": [], "d6:76:e0:ab:36:76": [],
                                     "d6:76:e0:ab:36:77": []}
            # "d6:76:e0:ab:36:74",
            # "d6:76:e0:ab:36:75",
            # "d6:76:e0:ab:36:76",
            # "d6:76:e0:ab:36:77"}
        self.allowed_mac_addresses = {
            "d6:76:e0:ab:36:71",
            "d6:76:e0:ab:36:72",
            "d6:76:e0:ab:36:73",
            "d6:76:e0:ab:36:74",
            "d6:76:e0:ab:36:75",
            "d6:76:e0:ab:36:76",
            "d6:76:e0:ab:36:77"
        }
        self.allowed_DPIDs={
            1152921504606846979,
            1152921504606846982,
            1152921504606846985}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        print('_switch_features_handler ===========================')
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath,0, match, actions, 0, 0)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None, hard_timeout=None):
        print('_add_flow ===========================')
        print("datapath:", datapath)#, "priority", priority, "match", match, "", actions)
        print("priority",priority)
        print("match", match)
        print("actions", actions)
        print("hard_timeout", hard_timeout)
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
                                    match=match, instructions=inst, hard_timeout=hard_timeout)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        print('_packet_in_handler ===========================')
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:

            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth.dst
        src = eth.src

        dpid1 = datapath.id
        # self.logger.info("DRPIDs Before : %s", dpid1)
        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        # self.logger.info(('\n'))

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]
        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                print('_packet_in_handler ===========================1')
                self.add_flow(datapath, 1, match, actions, msg.buffer_id, 1)
                return
            else:
                print('_packet_in_handler ===========================1')
                self.add_flow(datapath, 1, match, actions, 0, 1)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        self.logger.info("dpid in Packet_in_handler before IF Condition: %s", dpid1)

        new = False
        self.logger.info('before %s',new)

        self.logger.info('before checking %s')
        if (dpid1 in self.allowed_DPIDs and src in self.allowed_mac_addresses and dst in self.allowed_mac_addresses):

            # here c see the veh
            current_timestamp = time.time()
            self.last_timestamp_dict[src].append(current_timestamp)
            self.logger.info(self.last_timestamp_dict[src][-1])
            # self.logger.info(type(self.last_timestamp_dict[src][-1]))
            # self.logger.info(len(self.last_timestamp_dict))
            print("self.last_timestamp_dict", self.last_timestamp_dict[src])
        #
            # new one
            if len(self.last_timestamp_dict[src]) > 2:
                print(' ')

                self.logger.info('yes: %s')

                last_time_stamp = self.last_timestamp_dict[src][-1]
                current_timestamp_1 = time.time()
                self.logger.info('last_time_stamp: %s', last_time_stamp)
                print('last_time_stamp: %s', last_time_stamp)
                # self.logger.info('current_timestamp:%s', current_timestamp_1)
                # print('current_timestamp:%s', current_timestamp_1)
                time_difference = self.last_timestamp_dict[src][-1] - self.last_timestamp_dict[src][-2]
                self.logger.info('time_difference : %s', time_difference)
                print('time_difference : %s', time_difference)

                # print(f"Old customer at time {current_timestamp_1}")
                # self.logger.info((f"OLD customer at time {current_timestamp_1}, OLD Customer MAC Address {src}"))
                # self.logger.info(self.last_timestamp_dict[src])
                # self.last_timestamp_dict[src].pop()

            #old one
            # if len(self.last_timestamp_dict[src]) > 1:
            #     print(' ')
            #
            #     self.logger.info('yes: %s')
            #
            #     last_time_stamp = self.last_timestamp_dict[src][-1]
            #     current_timestamp_1 = time.time()
            #     self.logger.info('last_time_stamp: %s', last_time_stamp)
            #     print('last_time_stamp: %s', last_time_stamp)
            #     self.logger.info('current_timestamp:%s', current_timestamp_1)
            #     print('current_timestamp:%s', current_timestamp_1)
            #     time_difference = current_timestamp_1 - last_time_stamp
            #     self.logger.info('time_difference : %s', time_difference)
            #     print('time_difference : %s', time_difference)
            #
            #     print(f"Old customer at time {current_timestamp_1}")
            #     self.logger.info((f"OLD customer at time {current_timestamp_1}, OLD Customer MAC Address {src}"))
            #     self.logger.info(self.last_timestamp_dict[src])
            #     # self.last_timestamp_dict[src].pop()

            if len(self.last_timestamp_dict[src]) == 1:
                new = True
                self.logger.info("NEW CUSTOMER: because of 0 %s")
                print("£££££££££££££££££££££££££££******NEW CUSTOMER----1st*********££££££££££££££££££££££££££££££££££££££: because of 0 %s")
                self.logger.info("£££££££££££££££££££££££££££******NEW CUSTOMER*********££££££££££££££££££££££££££££££££££££££: because of 0 %s")

            if len(self.last_timestamp_dict[src]) > 1:
                if time_difference > 8.3:
                    new = True
                    self.logger.info("NEW CUSTOMER: because of time difference %s")
                    self.logger.info(time_difference)
                    print("------------------------**NEW CUSTOMER**: because of time difference--------------------- %s")
                    self.logger.info("------------------------**NEW CUSTOMER**: because of time difference--------------------- %s")
                    print(time_difference)

                if time_difference <= 8.3:
                    new = False
                    self.logger.info("OLD CUSTOMER: because of time difference %s")
                    self.logger.info(time_difference)
                    print("^^^^^^^^^^^^^^^^^^^^^^^^&&&&&&&OLD CUSTOMER&&&&&&&: because of time difference^^^^^^^^^^^^^^^^^^^^^^^^^^ %s")
                    self.logger.info("^^^^^^^^^^^^^^^^^^^^^^^^&&&&&&&OLD CUSTOMER&&&&&&&: because of time difference^^^^^^^^^^^^^^^^^^^^^^^^^^ %s")
                    print(time_difference)

            if len(self.last_timestamp_dict[src]) > 3:
                self.last_timestamp_dict[src].pop(0)


        self.logger.info('after %s', new)
        if new:

        # if dpid1 in self.allowed_DPIDs and src in self.allowed_mac_addresses and dst in self.allowed_mac_addresses:
        #     self.logger.info("SRC Inside IF Condition: %s", src)
            self.logger.info("Before Sleep: ________________ %s")
            time.sleep(1)
            self.logger.info("After Sleep:------ now try to send msg: 1 %s ")
            # time.sleep(1)
            self.logger.info("After Sleep:------ now try to send msg: 2 %s ")
            # time.sleep(1)
            self.logger.info("After Sleep:------ now try to send msg: 3 %s ")

        datapath.send_msg(out)


        # self.logger.info("Before DP_IF of C3: %s", type(dpid))
        # if dpid in self.allowed_DPIDs:
        #     self.logger.info("YES: in dpid%s")
        #     dst = eth.dst
        #     src = eth.src
        #     mac_address = src
        #     current_timestamp = time.time()
        #
        #     self.logger.info("SRC: %s", src)
        #     self.logger.info("SRC: %s", type(src))
        #     self.logger.info("DST: %s", dst)
        #     self.logger.info("DST: %s", type(dst))
        #     # if dst == 'd6:76:e0:ab:36:71' or src == 'd6:76:e0:ab:36:71':
        #     if src in self.allowed_mac_addresses or dst in self.allowed_mac_addresses:


                # self.logger.info("YES IN MAC ADDRESS: %s")
                # if len(self.last_timestamp_dict) == 0:
                #     self.last_timestamp_dict[mac_address] = current_timestamp
                #     print(f"New customer at time {current_timestamp}")
                #     self.logger.info((f"New customer at time {current_timestamp}, New Customer MAC Address {mac_address}"))
                #     self.logger.info(('before sleep'))
                #     self.logger.info(('      '))
                #     time.sleep(1)
                #     self.logger.info(('after sleep'))
                #
                #     dpid = format(datapath.id, "d").zfill(16)
                #     self.mac_to_port.setdefault(dpid, {})
                #
                #     # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
                #     self.logger.info(('\n'))
                #
                #     # learn a mac address to avoid FLOOD next time.
                #     self.mac_to_port[dpid][src] = in_port
                #
                #     if dst in self.mac_to_port[dpid]:
                #         out_port = self.mac_to_port[dpid][dst]
                #     else:
                #         out_port = ofproto.OFPP_FLOOD
                #
                #     actions = [parser.OFPActionOutput(out_port)]
                #
                #     # install a flow to avoid packet_in next time
                #     if out_port != ofproto.OFPP_FLOOD:
                #         match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
                #         # verify if we have a valid buffer_id, if yes avoid to send both
                #         # flow_mod & packet_out
                #         if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                #             self.add_flow(datapath, 1, match, actions, msg.buffer_id, 0, 1)
                #             return
                #         else:
                #             self.add_flow(datapath, 1, match, actions, 0, 0, 1)
                #     data = None
                #     if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                #         data = msg.data
                #
                #     out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                #                               in_port=in_port, actions=actions, data=data)
                #     datapath.send_msg(out)
                #
                # else:
                #     if mac_address in self.last_timestamp_dict:
                #         last_time_stamp = self.last_timestamp_dict.get(mac_address)
                #         self.logger.info('last_time_stamp: %s', last_time_stamp)
                #         print('last_time_stamp: %s', last_time_stamp)
                #         self.logger.info('current_timestamp:%s', current_timestamp)
                #         print('current_timestamp:%s', current_timestamp)
                #         time_difference = current_timestamp - last_time_stamp
                #         self.logger.info('time_difference : %s', time_difference)
                #         print('time_difference : %s', time_difference)
                #
                #         if time_difference <= 4:  # or 2<time_difference<=5:
                #             self.last_timestamp_dict[mac_address] = current_timestamp
                #             print(f"Old customer at time {current_timestamp}")
                #             self.logger.info(
                #                 (f"OLD customer at time {current_timestamp}, OLD Customer MAC Address {mac_address}"))
                #             dpid = format(datapath.id, "d").zfill(16)
                #             self.mac_to_port.setdefault(dpid, {})
                #
                #             # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
                #             self.logger.info(('\n'))
                #
                #             # learn a mac address to avoid FLOOD next time.
                #             self.mac_to_port[dpid][src] = in_port
                #
                #             if dst in self.mac_to_port[dpid]:
                #                 out_port = self.mac_to_port[dpid][dst]
                #             else:
                #                 out_port = ofproto.OFPP_FLOOD
                #
                #             actions = [parser.OFPActionOutput(out_port)]
                #
                #             # install a flow to avoid packet_in next time
                #             if out_port != ofproto.OFPP_FLOOD:
                #                 match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
                #                 # verify if we have a valid buffer_id, if yes avoid to send both
                #                 # flow_mod & packet_out
                #                 if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                #                     self.add_flow(datapath, 1, match, actions, msg.buffer_id, 0, 1)
                #                     return
                #                 else:
                #                     self.add_flow(datapath, 1, match, actions, 0, 0, 1)
                #             data = None
                #             if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                #                 data = msg.data
                #
                #             out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                #                                       in_port=in_port, actions=actions, data=data)
                #             datapath.send_msg(out)
                #
                #         else:
                #             self.last_timestamp_dict[mac_address] = current_timestamp
                #             print("^^^*****ELSE CONDITION__NEW CUSTOMER^^^*****")
                #             self.logger.info("^^^*****ELSE CONDITION__NEW CUSTOMER^^^*****: %s")
                #             print(f"New customer at time {current_timestamp}")
                #             self.logger.info(
                #                 (f"New customer at time {current_timestamp}, New Customer MAC Address {mac_address}"))
                #             self.logger.info(('before sleep'))
                #             self.logger.info(('      '))
                #             time.sleep(1)
                #             self.logger.info(('after sleep'))
                #
                #             dpid = format(datapath.id, "d").zfill(16)
                #             self.mac_to_port.setdefault(dpid, {})
                #
                #             # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
                #             self.logger.info(('\n'))
                #
                #             # learn a mac address to avoid FLOOD next time.
                #             self.mac_to_port[dpid][src] = in_port
                #
                #             if dst in self.mac_to_port[dpid]:
                #                 out_port = self.mac_to_port[dpid][dst]
                #             else:
                #                 out_port = ofproto.OFPP_FLOOD
                #
                #             actions = [parser.OFPActionOutput(out_port)]
                #
                #             # install a flow to avoid packet_in next time
                #             if out_port != ofproto.OFPP_FLOOD:
                #                 match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
                #                 # verify if we have a valid buffer_id, if yes avoid to send both
                #                 # flow_mod & packet_out
                #                 if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                #                     self.add_flow(datapath, 1, match, actions, msg.buffer_id, 0, 1)
                #                     return
                #                 else:
                #                     self.add_flow(datapath, 1, match, actions, 0, 0, 1)
                #             data = None
                #             if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                #                 data = msg.data
                #
                #             out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                #                                       in_port=in_port, actions=actions, data=data)
                #             datapath.send_msg(out)
                #
                #
                #
                #
                #
                #
                #



















#########################################################################################################################################################################
#         if eth.ethertype == ether_types.ETH_TYPE_LLDP:
#             # ignore lldp packet
#             return
#         dst = eth.dst
#         src = eth.src
#         print("BEFORE Blocking Un-Necessary Packets_In:***src***", src)
# ####################################################################################################
#         #For Blocking Un-Necessary Packets_In to my Controllers
#         if src not in self.allowed_mac_addresses and dst not in self.allowed_mac_addresses:
#             # Ignoring packet_in messages for other MAC addresses
#             print("Blocking Un-Necessary Packets_In:***src***", src)
#             return
#
# ####################################################################################################
#         dpid = format(datapath.id, "d").zfill(16)
#         self.mac_to_port.setdefault(dpid, {})
#
#         self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
#
#         # learn a mac address to avoid FLOOD next time.
#         self.mac_to_port[dpid][src] = in_port
#
#         if dst in self.mac_to_port[dpid]:
#             out_port = self.mac_to_port[dpid][dst]
#         else:
#             out_port = ofproto.OFPP_FLOOD
#
#         actions = [parser.OFPActionOutput(out_port)]
#
#         # install a flow to avoid packet_in next time
#         if out_port != ofproto.OFPP_FLOOD:
#             match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
#             # verify if we have a valid buffer_id, if yes avoid to send both
#             # flow_mod & packet_out
#             if msg.buffer_id != ofproto.OFP_NO_BUFFER:
#                 print('_packet_in_handler ===========================1')
#                 self.add_flow(datapath, 1, match, actions, msg.buffer_id, 1)
#                 return
#             else:
#                 print('_packet_in_handler ===========================1')
#                 self.add_flow(datapath, 1, match, actions, 0, 1)
#         data = None
#
#         if msg.buffer_id == ofproto.OFP_NO_BUFFER:
#             data = msg.data
#
#         out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
#                                   in_port=in_port, actions=actions, data=data)
#         datapath.send_msg(out)
