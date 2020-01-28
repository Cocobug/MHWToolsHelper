from bs4 import BeautifulSoup
import requests
import re,os

class Armor(object):
    """Armor object, contains all parts"""

    def __init__(self, path,partpath):
        allparts=[partpath+p.split('/')[-1] for p in path]
        self.helm=None
        self.chest=None
        self.arms=None
        self.waist=None
        self.legs=None
        self.loadfrompath(allparts)

    def loadfrompath(self,allpaths):
        for path in allpaths:
            with open(path) as f:
                soup=BeautifulSoup(f.read(),"lxml")

class Part(object):
    """Part of an armor, contain all data needed to output a skill."""

    def __init__(self, arg):
        super(Part, self).__init__()
        self.arg = arg

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
    name=prettyname(url)
    with open(fullpath,"wb") as f:
        f.write(r.content)
    return 1

def prettyname(url):
    return url.split("/")[-1].replace(" ","")#.replace("+++"," ").replace("+","").replace(" ","+")

def download_all(listurl,folder,verbose=True,context=""):
    if verbose:
        print("Started download in",folder)
    nb_new=0
    nb_done=0
    nb_error=0
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
    for file in os.listdir(folder):
        try:
            make_from_armor(folder+file)
        except FileNotFoundError:
            print("   No armor {} was found, skipping".format(file))

def make_from_armor(path):
    with open(path,encoding="utf-8") as f:
        soup=BeautifulSoup(f.read(),"lxml")
    name=path.split("/")[-1]
    tables=(soup.find_all("table","wiki_table"))
    armor_skills=tables[0]
    armor_specs=tables[1]
    first_skill=armor_skills.find(string="Skills").find_parent("tr")
    first_skill=first_skill.next_sibling.next_sibling
    if first_skill.find(string="BNS")!=None:
        # print(first_skill.find(string=re.compile(".*piece")))
        set_skill=findsetskill(first_skill.find_all("td")[1])
    else:
        # print(first_skill.find(string=re.compile(".*piece")))
        set_skill=None
    print("  ",name,"set:",set_skill)

def findsetskill(tag):
    try:
        set_skill=tag.contents
        if set_skill==['no bonus'] or set_skill == ['none']:
            print("nope")
            return None
    except:
        set_skill="NOPE"
    return set_skill
_BASEURL="https://monsterhunterworld.wiki.fextralife.com"
if __name__ == '__main__':
    armors=findallarmors("data/MasterRankArmor")
    download_all(armors,"data/Armors/")
    make_all_from_armor("data/Armors/")
    make_from_armor("data/Armors/Lunastra+Beta+++Armor+Set")
    # parts=findallparts("data/Armors/","data/Parts/")
