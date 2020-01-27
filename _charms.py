import re
import os
import shutil
from _skillmanager import Skill,Duplicates,SkillList

def parse_charms(reg,dupes):
    # Naming is weird here because names got to be readable, and charms tend not to be
    if reg[4]=="" and reg[2]!="":
        name=reg[2]+" Charm"
    else:
        name=reg[0]
    item=Skill(name,reg[1])
    if item.fulln() in dupes.charms_names:
        return "",""
    skills=SkillList()
    skills.add((reg[2],reg[3]))
    skills.add((reg[4],reg[5]))

    dupes.checkskills(skills)
    return charm_text.format(name=item.fulln(),skills=str(skills)),item.savename().replace("Charm","")

def generate_charms(dupes):
    charms_out="output/charms"
    charms_nb=0
    new_charms_nb=0
    charms_path="data/Charms.txt"
    charms_re=re.compile("^([A-z/ ']*) ([IV]{0,4}) ; ([A-z/\- ']*) \+(\d)(?: ; ([A-z/ ']*) \+(\d))?")
    with open(charms_path) as f:
        text=f.readlines()
        matches=[]
        for l in text:
            mat=charms_re.findall(l)
            if mat!=[]:
                matches+=mat
            else:
                print("Error on line",l)
    if not os.path.isdir(charms_out):
        os.mkdir(charms_out)
    else:
        for c in os.listdir(charms_out):
            os.remove(charms_out+"/"+c)

    with open(charms_out+"/"+"index.js","w") as index:
        for mat in matches:
            charms_nb+=1
            text,savename=parse_charms(mat,dupes)
            if text!="":
                new_charms_nb+=1
                # print(charms_out+"/"+savename+".js")
                with open(charms_out+"/"+savename+".js","w") as f:
                    f.write(text)
                index.write('    "{}",\n'.format(savename))
    print("Finished Charms {} done, {} new. Saved in {}".format(charms_nb,new_charms_nb,charms_out))

charm_text="""[
    {{
        maxdef: 0,
        slotlevels: [0, 0, 0],
        sex: 3,
        resist: [0, 0, 0, 0, 0],
        part: 5,
        mindef: 0,
        slots: 0,
        name: "{name}",
        skills: {{ {skills} }},
        type: 3
    }}
]"""

if __name__ == '__main__':
    generate_charms(Duplicates())
