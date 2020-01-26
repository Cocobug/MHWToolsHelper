import re,os

class SkillList(object):
    "A list of skills"
    def __init__(self):
        self._list=[]

    def add(self,obj):
        if obj[0]!="":
            self._list+=[Skill(obj[0],obj[1])]

    def __str__(self):
        if len(self._list)==0:
            return ""
        elif len(self._list)==1:
            return str(self._list[0])
        else:
            return ','.join([str(e) for e in self._list])

    def __iter__(self):
        for i in self._list:
            yield i

class Skill(object):
    """docstring for Skill."""

    def __init__(self, text,level):
        self.name,self.level=text,level
        self.dummy=False
        if text=="":
            self.name,self.level="",""
            self.dummy=True
    def __str__(self):
        if self.dummy:
            return ""
        return '"{self.name}": {self.level}'.format(self=self)

    def fulln(self):
        return "{s.name} {s.level}".format(s=self)

# class Charm(object):
#     pass

class Duplicates(object):
    """Find all existing skils, for duplicates."""

    def __init__(self):
        self.name_re=re.compile('name.?:\s*"(?P<name>[A-z/ ]* \d)"')
        self.charm_name_re=re.compile('name.?:\s*"(?P<name>[A-z/ ]* [IV]+)"')
        self.skill_re=re.compile('{ skill: "(?P<name>[A-z/ \-]*)",')

        self.jewels_names = self.findnames("base/decos.js")
        self.charms_names = self.findnamesinfolder("C:/MAMP/htdocs/MHWTools/armorcalc/armors/CH")
        self.skills= self.findskills("base/skills.js")
        self.duplicate_skills_f=open("output/new_skills.js","w")
        self.already_pending_skills=[]

    def findnames(self,path):
        "Apply a regex to return all 'name' in the file"
        with open(path) as f:
            return self.name_re.findall(f.read())

    def findnamesinfolder(self,path):
        fullnames=[]
        for file in os.listdir(path):
            file=path+"/"+file
            with open(file) as f:
                # print(self.name_re.findall(f.read()))
                fullnames+=self.charm_name_re.findall(f.read())
        return fullnames

    def findskills(self,path):
        with open(path) as f:
            ret= self.skill_re.findall(f.read())
            return ret

    def checknewskill(self,skill):
        if skill in self.skills:
            print(skill,"is already in",self.skills)

    def checkskills(self,slist):
        for skill in slist:
            if not skill.dummy and skill.name not in self.already_pending_skills and skill.name not in self.skills:
                self.already_pending_skills+=[skill.name]
                self.add_skill(skill)

    def add_skill(self,skill,lvl=1):
        for i in range(lvl):
            self.duplicate_skills_f.write("""                {{ skill: "{skill}", points: {i}, type: 1, name: "{skill} Lv{i}" }},\n""".format(skill=skill.name,i=i+1))


if __name__ == '__main__':
    Duplicates()
