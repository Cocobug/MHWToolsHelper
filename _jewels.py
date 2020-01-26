import re
from _skillmanager import Skill,Duplicates

def parse_jewels(reg,dupes):
    item=Skill(reg[0])
    if item.fulln() in dupes.jewels_names:
        return ""
    skill1=Skill(reg[1])
    if len(reg)>3:
        skill2=Skill(reg[2])
    else:
        skill2=Skill("")
    dupes.checkskills(skill1,skill2)
    skills='  skills: {{{}}},\n'.format(skill1.s(skill2))
    slots="  slots: 1,\n"
    name= '  name: "{s.name} {s.level}",\n'.format(s=item)
    public_name='  public_name: "{s.name}",\n'.format(s=item)
    level="  level: {s.level}\n".format(s=item)
    return "{\n"+skills+slots+name+public_name+level+'},\n'

def generate_jewels(dupes):
    jewels_out="output/jewels_gen.js"
    jewel_nb=0
    jewel_path="data/Jewels.txt"
    jewel_re=re.compile("""^(?P<name>[A-z/ ]* \d)\n(?P<skill1>[A-z/ ]* \d)\n(?P<skill2>[A-z/ ]* \d)?\n?([ \t\d.%]*)""",re.MULTILINE)
    with open(jewel_path) as f:
        text=f.read()
        matches=jewel_re.findall(text)
    with open(jewels_out,"w") as f:
        for mat in matches:
            jewel_nb+=1
            f.write(parse_jewels(mat,dupes))
    print("Finished Jewels {} done. Saved in {}".format(jewel_nb,jewels_out))
