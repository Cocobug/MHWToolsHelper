from bs4 import BeautifulSoup
import requests
import re,os
from _skillmanager import SkillList,Skill

class Armor(object):
    """Armor object, contains all parts"""
    def __init__(self, name):
        self.name=name
        self.savename=prettyname(name)
        self.set_skill=None
        self.parts={"helm":None,"torso":None,"arm":None,"waist":None,"feet":None}

    def addpart(self,part_name,partobj):
        self.parts[part_name]=partobj

    def __str__(self):
        return '{\n'+',\n'.join([str(self.parts[p]) for p in _nb_to_part])+'\n}'

    def save(self,path):
        with open(path+self.savename+".js","w") as f:
            f.write(str(self))

_nb_to_part=["helm","torso","arm","waist","feet"]
_part_to_nb={"helm":0,"torso":1,"arm":2,"waist":3,"feet":4}
class Part(object):
    """Part of an armor, contain all data needed to output a skill."""
    def __init__(self, part_name):
        self.name=''
        self.part_name=part_name
        self.nb=_part_to_nb[part_name]
        self.skills=""
        self.resists=[]
        self.mindef=0
        self.maxdef=0
        self.slotlevels=[]
        self.nbslots=0

    def setname(self,path):
        self.name=path.split("/")[-1].replace("Armor","").replace("Set","").replace("++","").replace("+"," ")
        if self.name[-5:]=="Alpha":
            self.name=self.name[:-6]+" "+self.part_name.capitalize()+" Alpha +"
            self.type="Alpha"
        else:
            self.name=self.name[:-5]+" "+self.part_name.capitalize()+" Beta +"
            self.type="Beta"

    def __str__(self):
        return """    {{\n        maxdef: {self.maxdef},\n        slotlevels: {self.slotlevels},\n        sex: 3,\n        resist: {self.resists},\n        part: {self.nb},
        mindef: {self.mindef},\n        slots: {self.nbslots},\n        name: "{self.name}",\n        skills: {{ {self.skills} }},\n        type: 3\n    }}""".format(self=self)

def download_armor(url,folder):
    "Take an url and prepare to make an armor Object"
    name=url.split("/")[-1].replace(" ","")#.replace("+++"," ").replace("+","").replace(" ","+")
    fullpath=folder+name
    if os.path.exists(fullpath):
        return 0
    try:
        r = requests.get(url)
        if r.status_code!=200:
            return -1
    except requests.exceptions.MissingSchema:
        print("Couldn't download",url)
        return -1
    name=url.split("/")[-1].replace(" ","")
    with open(fullpath,"wb") as f:
        f.write(r.content)
    return 1

def prettyname(url):
    return url.split("/")[-1].replace(" ","").replace("+","").replace("Armor","").replace("Set","")

def partname(url):
    return url.split("/")[-1].replace(" ","").replace("+","").replace("Armor","").replace("Set","")

def download_all(listurl,folder,verbose=True,context=""):
    if verbose:
        print("Started download in",folder)
    nb_new,nb_done,nb_error=0,0,0
    errors=[]
    for url in listurl:
        r=download_armor(url,folder)
        if r==1:
            nb_new+=1
        elif r==0:
            nb_done+=1
        elif r==-1:
            errors+=[url]
            nb_error+=1
    if verbose:
        print("Finished processing {} elements\n   [{}] new downloads\n   [{}] already downloaded\n   [{}] errors".format(len(listurl),nb_new,nb_done,nb_error))
    elif nb_error!=0:
        print("Print {} errors in {} (called from {})".format(nb_error,url,context))
        for e in errors:
            print("    "+e)
        print("")
    return nb_error

def findallarmors(path):
    "Takes the base page of fextralife and output a list of everything to be downloaded"
    with open(path,encoding="utf-8") as f:
        html_doc=f.read()
    soup = BeautifulSoup(html_doc,'lxml')
    tab=soup.find("div","col-sm-2").find_all("a")
    list=[_BASEURL+u["href"] for u in tab]
    return(list)

def findparts(file):
    with open(file,encoding="utf-8") as f:
        html_doc=f.read()
    soup=BeautifulSoup(html_doc,"lxml")
    wiki=soup.find_all("table","wiki_table")[1] # Should use a custom check, idc, fight me
    return([_BASEURL+"/"+l["href"].split("/")[-1] for l in wiki.find_all("a") if l["href"] not in "/n/a"] ) # Very twitchy

def findallparts(folder,savefolder):
    ge=0
    armors=[]
    for file in os.listdir(folder):
        parts=findparts(folder+file)
        try:
            r=download_all(parts,savefolder,verbose=False,context=file)
        except:
            print("Couldn't download",file)
            r=1

def make_all_from_armor(folder):
    ret=[]
    for file in os.listdir(folder):
        try:
            armor=make_from_armor(folder+file)
            if armor!=None:
                ret+=[armor]
            else:
                print(file,"coulnd't be processed")
        except FileNotFoundError:
            print("   No armor {} was found, skipping".format(file))
    return ret

def make_from_armor(path):
    convertion={}
    set_skill=None
    with open(path,encoding="utf-8") as f:
        soup=BeautifulSoup(f.read(),"lxml")
    name=path.split("/")[-1]

    ### Ading the set skill
    arm=Armor(name)
    tables=(soup.find_all("table","wiki_table"))
    armor_skills=tables[0]
    armor_specs=tables[1]
    first_skill=armor_skills.find(string="Skills").find_parent("tr")
    first_skill=first_skill.next_sibling.next_sibling
    if first_skill.find(string="BNS")!=None:
        set_skill=findsetskill(first_skill.find_all("td")[1],name)
        arm.set_skill=set_skill

    ### Adding all skills
    for tr in first_skill.find_next_siblings("tr"):
        part_name=tr.td.a.img["alt"].replace("mhw-","").replace("-wiki","").split("-")[0]
        part=Part(part_name)
        all_skills=[s for s in (tr.td.next_sibling.next_sibling.stripped_strings)]

        if len(all_skills)==1:
            continue
        if len(all_skills)%2!=0:
            continue
            print("Error in",all_skills,path)

        skills=SkillList()
        for i in range (int(len(all_skills)/2)):
            skills.add((all_skills[i*2],all_skills[i*2+1].replace("x","")))
        if set_skill!=None:
            skills.add((set_skill,'1'))
        part.skills=skills
        part.setname(name)

        arm.addpart(part_name,part)

    # print(arm)

        # skills=tr.td.next_sibling.next_sibling.find_all("a")
        # # print(skills)
        # values=tr.td.next_sibling.next_sibling.find_all(string=re.compile("x?(\d)x?"))
        # if len(skills)!=len(values):
        #     print (path,len(skills),len(values),skills,values)
        # all_parts=first_skill.find_siblings(string=re.compile(".*wiki"))
    # print(all_parts)
    # print("  ",name,"set:",set_skill)
    return arm

def findsetskill(tag,context):
    try:
        set_skill=tag.contents
        if str(set_skill[0]).lower() in ['no bonus','none',"n/a","--","??"]:
            return None
        lnk=tag.find("a")
        if lnk==None:
            raise Exception
        return(lnk.contents[-1])

    except:
        print("Error in",context,set_skill)
        return None

_BASEURL="https://monsterhunterworld.wiki.fextralife.com"
if __name__ == '__main__':
    armors=findallarmors("data/MasterRankArmor")
    download_all(armors,"data/Armors/")
    armors=make_all_from_armor("data/Armors/")
    for a in armors:
        a.save("data/HR/")
    make_from_armor("data/Armors/Lunastra+Beta+++Armor+Set")
    # parts=findallparts("data/Armors/","data/Parts/")
