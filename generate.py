# -*- coding: utf-8 -*-

import re,os,sys
import time


class Skill(object):
    """docstring for Skill."""

    def __init__(self, text):
        if text=="":
            self.name,self.level="",""
            self.dummy=True
        else:
            self.name,self.level=name_level(text)
            self.dummy=False

    def __str__(self):
        if self.dummy:
            return ""
        return '"{self.name}": {self.level}'.format(self=self)

    def s(self,text=""):
        if str(text)!="":
            return str(self)+', '+str(text)
        return str(self)

    def fulln(self):
        return "{s.name} {s.level}".format(s=self)


def findnames(path):
    "Apply a regex to return all 'name' in the file"
    reg=re.compile('name.?:\s*"(?P<name>[A-z/ ]* \d)"')
    # reg=re.compile('name: "(?P<name>[A-z/ ]*) \d"')
    with open(path) as f:
        ret=reg.findall(f.read())
    return ret

def name_level(text):
    name,level=text[:-2],text[-1:]
    # assert(int(level) in range(1,9))
    return name,level

def parse_jewels(reg,jewel_presents):
    item=Skill(reg[0])
    if item.fulln() in jewel_presents:
        return ""
    skill1=Skill(reg[1])
    if len(reg)>3:
        skill2=Skill(reg[2])
    else:
        skill2=Skill("")
    skills='  skills: {{{}}},\n'.format(skill1.s(skill2))
    slots="  slots: 1,\n"
    name= '  name: "{s.name} {s.level}",\n'.format(s=item)
    public_name='  public_name: "{s.name}",\n'.format(s=item)
    level="  level: {s.level}\n".format(s=item)
    return "{\n"+skills+slots+name+public_name+level+'},\n'

def generate_jewels():
    jewels_out="output/jewels_gen.js"
    jewel_nb=0
    jewel_path="data/Jewels.txt"
    jewel_presents=findnames("base/decos.js")
    jewel_re=re.compile("""^(?P<name>[A-z/ ]* \d)\n(?P<skill1>[A-z/ ]* \d)\n(?P<skill2>[A-z/ ]* \d)?\n?([ \t\d.%]*)""",re.MULTILINE)
    with open(jewel_path) as f:
        text=f.read()
        matches=jewel_re.findall(text)
    with open(jewels_out,"w") as f:
        for mat in matches:
            jewel_nb+=1
            f.write(parse_jewels(mat,jewel_presents))
    print("Finished Jewels {} done. Saved in {}".format(jewel_nb,jewels_out))

if __name__ == '__main__':
    start_time = time.time()
    generate_jewels()
    print("All generations done. Time elapsed {}".format(time.time()-start_time))
