import re
from bs4 import BeautifulSoup
import requests
existing=re.compile('.*public_name: "(?P<name>.*)"')


with open("C:/MAMP/htdocs/MHWTools/armorcalc/decos.js") as f:
    alls=existing.findall(f.read())
with open("MHWTools.html") as f:
    soup=BeautifulSoup(f.read(),"lxml")
# r=requests.get("http://localhost/MHWTools/")
# soup=BeautifulSoup(str(r),"lxml")

existing=soup.find_all("span",{"traslation-section":"skills"})

skill_existing=[e.contents[0] for e in existing]
skill_transl=[e["translation-key"] for e in existing]


# for s in skill_existing:
#     if s not in skill_transl:
#         print(s)
# print(skill_transl)
for skill in alls:
     if skill not in skill_existing:
            if skill not in skill_transl:
                print("Nowhere: ",skill)
            # else:
            #     print(skill,skill_transl)
            #     print("Ill translated",skill)
