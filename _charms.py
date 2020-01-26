import re
from _skillmanager import Skill,Duplicates,SkillList

def parse_charms(reg,dupes):
    item=Skill(reg[0],reg[1])
    if item.fulln() in dupes.charms_names:
        return ""
    skills=SkillList()
    skills.add((reg[2],reg[3]))
    skills.add((reg[4],reg[5]))
    dupes.checkskills(skills)
    return charm_out.format(s=item,skills=str(skills))

def generate_charms(dupes):
    charms_out="output/charms_gen.js"
    charms_nb=0
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
    with open(charms_out,"w") as f:
        for mat in matches:
            charms_nb+=1
            f.write(parse_charms(mat,dupes))
    print("Finished Charms {} done. Saved in {}".format(charms_nb,charms_out))

charm_out="""[
    {{
        maxdef: 0,
        slotlevels: [0, 0, 0],
        sex: 3,
        resist: [0, 0, 0, 0, 0],
        part: 5,
        mindef: 0,
        slots: 0,
        name: "{s.name}",
        skills: {{ {skills} }},
        type: 3
    }}
]"""

if __name__ == '__main__':
    generate_charms(Duplicates())
