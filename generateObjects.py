import load,time

final="""
from HPanda.HGameObject import HLodDynamicObject

###Automatic generated file at time """+time.strftime("%d-%m-%y- %H:%M:%S")+"""

def setup(scene):
"""

text="lolitaWarrior_level.txt"
superlist=load.readFile(text)
scene="scene"
coma=", "
comilla="\""
LODDistance=50
margin=0.02
fileName="StaticObjects"

for l in superlist:
    dic=load.format_name_num(l[0])
    ts="    scene."+dic["name"]+"="
    ts+="HLodDynamicObject("
    ts+=comilla+dic["name"]+comilla +coma
    ts+=scene+coma
    ts+="visibleLODsDict="+str({dic["egg"]:(0,LODDistance),
                               dic["LOD1"]:(LODDistance,1000)} )+coma
    ts+="collisionEgg="+comilla+dic["collision"]+comilla+coma
    ts+="x0="+str(l[1])+coma
    ts+="y0="+str(l[2])+coma
    ts+="z0="+str(l[3])+coma
    ts+="parent=None"+coma
    ts+="margin="+str(margin)+coma
    ts+="directRender=True"+coma
    ts+="convex=False"+")\n"
    final+=ts

fileOb=open(fileName+".py","wt")
fileOb.write(final)
fileOb.close()
print "DONE!"