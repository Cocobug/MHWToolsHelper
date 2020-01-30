from bs4 import BeautifulSoup
import requests
import re,os
from _skillmanager import SkillList,Skill,Duplicates

class Armor(object):
    """Armor object, contains all parts"""
    def __init__(self, name):
        self.name=name
        self.savename=prettyname(name)
        self.set_skill=None
        self.parts={"helm":None,"torso":None,"arm":None,"waist":None,"feet":None}
        self.empty=True

    def addpart(self,part_name,partobj):
        self.parts[part_name]=partobj
        if partobj!=None:
            self.empty=False

    def getpart(self,nb):
        if type(nb)==int:
            return self.parts[_nb_to_part[nb]]
        else:
            return self.parts[nb]
    def __str__(self):
        return '[\n'+',\n'.join([str(self.parts[p]) for p in _nb_to_part if self.parts[p] != None])+'\n]'

    def check(self):
        self.empty=True
        for part in self.parts:
            if self.parts[part]!=None:
                if self.parts[part].check():
                    self.empty=False

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
        self.slotlevels=[0, 0, 0]
        self.nbslots=0

    def check(self):
        if self.name=='':
            print("Part",self.part_name,"has no name")
        if self.skills=="":
            print("  ",self.name,"has no skills")
        if self.resists==[]:
            print("  ",self.name,"has no resists")
        if self.mindef==0:
            print("  ",self.name,"has no def")
        if self.maxdef==0:
            print("  ",self.name,"has no max def")

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
    return url.split("/")[-1].replace(" ","").replace("+","").replace("Armor","").replace("Set","").replace("Alpha","A").replace("Beta","B")+"P"

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
    dupes=Duplicates()
    for file in os.listdir(folder):
        try:
            armor=make_from_armor(folder+file,dupes)
            if armor!=None:
                ret+=[armor]
                #armor.check()
            else:
                print(file,"coulnd't be processed")
        except FileNotFoundError:
            print("   No armor {} was found, skipping".format(file))
    return ret

_just_that_int=re.compile(".*(\d).*")
def make_from_armor(path,dupes):
    convertion={}
    set_skill=None
    with open(path,encoding="utf-8") as f:
        soup=BeautifulSoup(f.read(),"lxml")
    name=path.split("/")[-1]

    ### Ading the set skill
    arm=Armor(name)
    tables=soup.find_all("table","wiki_table")
    armor_skills=tables[0]
    armor_specs=tables[1]
    first_skill=armor_skills.find(string="Skills").find_parent("tr")
    first_skill=first_skill.next_sibling.next_sibling
    if first_skill.find(string="BNS")!=None:
        set_skill=findsetskill(first_skill.find_all("td")[1],name)
        arm.set_skill=set_skill

    ### Max armor value
    augmented_armor=soup.find(string=re.compile(".*Augmented"))
    if augmented_armor==None or "__augmented" in augmented_armor or "??" in augmented_armor:
        augmented_armor=0 # BIG ERROR YOU NEED TO ADD IT BY HAND
    else:
        augmented_armor=int(augmented_armor.split("with ")[-1][:3])

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
        dupes.checkskills(skills)
        arm.addpart(part_name,part)

    ### Updating all values and gems:
    all_lines=armor_specs.tbody.find_all("tr")
    part_i=0
    if len(all_lines)!=5:
        print("No info was retreived in",name)
        return arm# returning armor as is, as it can't be finished
    for line in all_lines:
        row=line.find_all('td')
        if len(row)!=8:
            print("Can't find rows in",name)
            return arm # returning armor as is, as it can't be finished
        else:
            gems=row[2]
            part=arm.getpart(part_i)
            if part!=None: # This part doen't exists, move along
                part.maxdef=augmented_armor
                part.mindef=row[1].contents[0]
                part.resists=[int(i.contents[0]) for i in row[3:]] # Yeah, n/a will make this crash
                if '??' in part.resists:
                    print(part.resists,"in",name)
                # else:
                #     print("No part",_nb_to_part[i],"in",name)
                if "??" in gems.contents:
                    print("Gems unknown in",name)
                list_gems=gems.find_all("img")
                if(len(list_gems)!=0): # That's normal
                #     print("No gems in",part.name,name)
                    jewels=[int(_just_that_int.findall(g["src"].split("/")[-1])[0]) for g in list_gems] # Very unsafe, I love it
                    nb_jewels=len(jewels)
                    for unnamedvarsarebad in range(3-nb_jewels):
                         jewels+=[0]
                    part.slotlevels=jewels
                    part.nbslots=nb_jewels
        part_i+=1

    return arm

def findsetskill(tag,context):
    try:
        set_skill=tag.contents
        if str(set_skill[0]).lower() in ['no bonus','none',"n/a","--"]:
            return None
        if str(set_skill[0]).lower()=="??":
            print("Skill unknown in armor",context)
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
        # a.save("data/MR/")
        a.save("C:/MAMP/htdocs/MHWTools/armorcalc/armors/MR/")
    with open("data/MR/index.js","w") as f:
        f.write('[\n{}\n]'.format(",\n".join(['   "{}"'.format(a.savename) for a in armors])))
    # make_from_armor("data/Armors/Shara+Ishvalda+Alpha+++Armor+Set",Duplicates()).save("data/")
