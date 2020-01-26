import re

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

class Duplicates(object):
    """Find all existing skils, for duplicates."""

    def __init__(self):
        self.name_re=re.compile('name.?:\s*"(?P<name>[A-z/ ]* \d)"')
        self.skill_re=re.compile('{ skill: "(?P<name>[A-z/ ]*)",')

        self.jewels_names = self.findnames("base/decos.js")
        self.skills= self.findskills("base/skills.js")
        self.duplicate_skills_f=open("output/duplicate_skills.js","w")
        self.already_pending_skills=[]
    def findnames(self,path):
        "Apply a regex to return all 'name' in the file"
        with open(path) as f:
            return self.name_re.findall(f.read())

    def findskills(self,path):
        with open(path) as f:
            ret= self.skill_re.findall(f.read())
            return ret

    def checknewskill(self,skill):
        if skill in self.skills:
            print(skill,"is already in",self.skills)

    def checkskills(self,*skills):
        for skill in skills:
            if not skill.dummy and skill.name not in self.already_pending_skills and skill.name not in self.skills:
                self.already_pending_skills+=[skill.name]
                self.add_skill(skill)

    def add_skill(self,skill):
        # { skill: "Peak Performance", points: 3, type: 1, name: "Peak Performance Lv3" },
        self.duplicate_skills_f.write("""                {{ skill: "{skill}", points: 1, type: 1, name: "{skill} Lv1" }},\n""".format(skill=skill.name))

def name_level(text):
    name,level=text[:-2],text[-1:]
    return name,level
