#!/usr/bin/env python

'Setting the position of nodes and providing mobility'

import sys
import time
import os
import re
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use('TkAgg')
import threading
import concurrent.futures
import pandas as pd
import numpy as np 
# import pyp
# from core import *
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
import csv
import CSVFunc  # Import the CSV functions from CSVFunc .py
#import tkinter as tk
#import pandas as pd
import tkinter as tk
from pythonping import ping
# from mininet_thread_function import mininet_thread_function
from mininet_thread_function import mininet_thread_function

def main(args):
    mininet_thread_function()


##############################################
if __name__ == '__main__':
    main(sys.argv)
