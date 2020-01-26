# -*- coding: utf-8 -*-

import re,os,sys
import time


from _jewels import generate_jewels
from _charms import generate_charms
from _skillmanager import Duplicates
# def generate_
if __name__ == '__main__':
    start_time = time.time()
    duplicates=Duplicates()
    generate_jewels(duplicates)
    # generate_charms(duplicates)
    print("All generations done. Time elapsed {}".format(time.time()-start_time))
