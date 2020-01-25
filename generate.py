# -*- coding: utf-8 -*-

import re,os,sys
import time

def parse_jewels(reg):
    base="""{
skills: {skills},
slots: 1,
name: "{name}",
public_name: "{name}",
level: {level}
}"""
    name,level=reg.name.split(":")
    re=""

def generate_jewels(jewel_path):
    jewel_re=re.compile("""^(?P<name>[A-z/ ]* \d)\n(?P<skill1>[A-z/ ]* \d)\n(?P<skill2>[A-z/ ]* \d)?\n?([ \t\d.%]*)""",re.MULTILINE)
    with open(jewel_path) as f:
        text=f.read()
        matches=jewel_re.findall(text)

if __name__ == '__main__':
    start_time = time.time()
    jewel_path="Jewels.txt"
    generate_jewels(jewel_path)
    print("All generations done. Time elapsed {}".format(time.time()-start_time))
