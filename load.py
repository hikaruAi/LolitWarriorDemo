
#name_00, name_00_LOD0, name_collision_00

test="arena_03"

def format_name_num(s,eggFolder="3d"):
    sep="_"
    name=""
    num=""
    d={}
    folder=eggFolder+"/"
    try:
        ind=s.index(sep)
        name=s[:ind]
        num=s[ind+1:]
        d={"name":s,
           "egg":folder+s,
            "LOD1":folder+name+sep+num+sep+"LOD1",
            "collision":folder+name+sep+"collision"+sep+num}
        #print d
        return d
    except:
        pass

def readFile(f):
    file=open(f,"rt")
    lines=file.readlines()
    superList=[]
    for l in lines:
        tup=eval(l)
        superList.append(tup)
    return superList

if __name__=="__main__":
    print readFile("lolitaWarrior_level.txt")