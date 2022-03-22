import bpy
from math import radians
import random
import math

# Global Variables

finaloutput = ""
numberpics = 10
imgstartnum = 51
kactive = True
#Senario Uno: When NumberPics = 2 and ImgStarNum = 18, then Images #18-19 will be outputs

xyBG = 99 #includes cushion space from 101.9
xymidBG = 85
xycloseBG = 75
goldenRatio = 0.618033988749
global objxcords
global objycords
global objsize
objxcords = []
objycords = []
objsize =  []
            

#Probabilities Vars & Debuging Methods


BGOPscaler = 1.07169
BGEScaler = 1.4146
BEPScaler = 1.0412

BGOPden = 10000
BGEden = 8000
BEPden = 9000

'''7 Bear Effects'''
BEP = [math.trunc(164*3.5*BEPScaler),math.trunc(130*3*BEPScaler),math.trunc(98*2.25*BEPScaler),math.trunc(65*2*BEPScaler),math.trunc(32*1.350*BEPScaler),math.trunc(16*1.125*BEPScaler)]
'''6 Background Effects'''
BGE = [math.trunc(267*3.5*BGEScaler), math.trunc(213*3*BGEScaler), math.trunc(160*2.5*BGEScaler), math.trunc(107*2*BGEScaler), math.trunc(53*1.5*BGEScaler), math.trunc(27*1*BGEScaler)]
'''10 Background Objects'''
BGOP = [math.trunc(454*7*BGOPscaler), math.trunc(409*6.5*BGOPscaler), math.trunc(363*6*BGOPscaler), math.trunc(318*4.5*BGOPscaler), math.trunc(272*3*BGOPscaler), math.trunc(227*3*BGOPscaler), math.trunc(188*BGOPscaler), math.trunc(83*BGOPscaler), math.trunc(45*BGOPscaler), math.trunc(15*BGOPscaler)]
'''7 Bear Types'''

def backObjectsProbs():
    probsum = 1
    for x in range(len(BGOP)):
        probsum *= 1-((BGOP[x])/BGOPden)
    return str((1-probsum)*100) + "%"

def backEffectsProbs():
    probsum = 1
    for x in range(len(BEP)):
        probsum *= 1-((BEP[x])/BEPden)
    return str((1-probsum)*100) + "%"

def bearEffectsProbs():
    probsum = 1
    for x in range(len(BGE)):
        probsum *= 1-((BGE[x])/BGEden)
    return str((1-probsum)*100) + "%"

def backTypesProbs():
    return str(100) + "%"


# Common Functions


def rand(max, min): # Output is a decimal with "rounded" number of decimals  EX: ~~~.~~~
    return random.randint(min, max)

def randD(max, min, rounded): # Output is a decimal with "rounded" number of decimals  EX: ~~~.~~~
    return round(random.uniform(min, max), rounded)

def mulRand(count, max, min, round):# Output is in array  EX: [0] = ~~~, [1] = ~~~ ...
    output = []
    for x in range(count):
        output.append(randD(max, min, round))
    return output

def hsvrgb(bright): # Output is int RGB(0.0-1.0)
    if(bright == True):
        h = ((randD(1,0,5)+goldenRatio)%1)
        s = randD(.99,.879,6)
        v = randD(.95,.875,6)
    else:
        h = (randD(1,0,5)+goldenRatio)%1
        s = randD(1,.85,6)
        v = randD(.205,.111,6)
    i = round(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-(f*s))
    t = v * (1-((1-f)*s))

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
        ][int(i%6)]

    return (r), (g), (b), 1

def cordD(xymax, size, kscale):#size is "s" in a s-length cube
    cleared = False
    while(cleared==False):#Loops until obj is away from other objs and bear
        kx = randD(xymax, -xymax,4)# Generates possiable x point
        ky = randD(xymax, -xymax,4)# Generates possiable y point
        index = len(objxcords)
        numcleared = 0
        if(currentbet==5):
            bearxsize = 27*5
            bearysize = 24*2
        else:
            bearxsize = 27*2
            bearysize = 24*2
        #Below Checks if Obj is in bear
        if((round(bearxsize/2,3)<(kx-round(kscale*size/2,3))) or ((-round(bearxsize/2,3)>(kx+round(kscale*size/2,3)))) or ((round(bearysize/2,3)<(ky-round(kscale*size/2,3))) or ((-round(bearysize/2,3))>(ky+round(kscale*size/2,3))))):
            if(index>0):
                for count in range(index):# Loops through all current cords
                    if(((objxcords[count]+round(objsize[count]/2,3)<(kx-(round(size/2,3)))) or (objycords[count]+round(objsize[count]/2,3)<(ky-(round(size/2,3))))) or ((objxcords[count]-round(objsize[count]/2,3)>(kx+(round(size/2,3)))) or (objycords[count]-round(objsize[count]/2,3)>(ky+(round(size/2,3)))))):
                        numcleared += 1
                    else:
                        print(kx)
                        print(ky)
                        print("This point didn't work. Touched another Object")
            else:
                objxcords.append(kx)
                objycords.append(ky)
                objsize.append(size*kscale)
                cleared = True
        else:
            print(kx)
            print(ky)
            print("This point didn't work. Touched Bear")
        if((numcleared == index) and (index!=0)):
            cleared = True
            objxcords.append(kx)
            objycords.append(ky)
            objsize.append(size*kscale)
    return (kx,ky)
        

# Decider Methods


def bgoDecider(): # Output is an array of objects' index in probs, or a -1 representing no objects.
    presentobj = [] 
    for x in range(len(BGOP)):
        if(rand(BGOPden,1) <= BGOP[x]):
            presentobj.append(x)
    if(len(presentobj)>0):
        return presentobj
    return -1

def bgeDecider(): # Output is the background effect's index in probs, or a -1 representing no background effects.
    presentobj = []
    for x in range(len(BGE)):
        if(rand(BGEden,1) <= BGE[x]):
            presentobj.append(x)
    if(len(presentobj)>0):
        return presentobj[len(presentobj)-1]
    return -1

def beeDecider(): # Output is the bear effect's index in probs, or a -1 representing no bear effects.
    presentobj = []
    for x in range(len(BEP)):
        if(rand(BEPden,1) <= BEP[x]):
            presentobj.append(x)
    if(len(presentobj)>0):
        return presentobj[len(presentobj)-1]
    return -1

def betDecider(): # Output is the bear type's index in probs, or a -1 representing error.
    num = rand(10000,1)
    if (num <= 5):                    # Chaos Bear
        output = 7
    elif (6<=num and num<=104):         # King Bear
        output = 6
    elif (105<=num and num<=304):       # Hydra Bear
        output = 5
    elif (305<=num and num<=602):       # Black Bear Change Alpha to 0
        output = 4
    elif (603<=num and num<=1000):      # Polar Bear
        output = 3
    elif (1001<=num and num<=2500):     # Bruin Bear
        output = 2
    elif (2501<=num and num<=10000):    # Random Bear
        output = 1
    else:
        print("Error Overflow: No Bear Type ")
    return output


#Changer Args
#------------------------------------
D = bpy.data
for x in range(numberpics):
    namelowres = 'cb' + str(imgstartnum + x) + 'lowres.jpg'
    addresslowres = 'C:/Users/Isean/OneDrive/Documents/Bears/FinalBearsNDA/' + namelowres
        
    namehighres = 'cb' + str(imgstartnum + x) + '.jpg'
    addresshighres = 'C:/Users/Isean/OneDrive/Documents/Bears/FinalBears/' + namehighres
    #------------------------------
    print("====================================================")
    print("Bear Number " + str(x + imgstartnum))
        #Color Refereneces
    kBearSkin = bpy.data.materials['BearColor']
    kRightEye = bpy.data.materials['RightEye']
    kLeftEye = bpy.data.materials['LeftEye']
    kEyeShadowR = bpy.data.materials['Eyeshadow.001']
    kEyeShadowL = bpy.data.materials['LeftEye.008']
            #MainObjects
    mainBear = bpy.data.objects["TheBearOne"]
    bearLight = bpy.data.objects["BearLight"]
    hydraHead = bpy.data.objects["CenterHydraHead"]
    hydraLight = bpy.data.objects["CenterHydraLight"]
    chaosHead = bpy.data.objects["ChaosRightEye"]
            #Backgrounds/Lights
    bgs = bpy.data.objects["StarryNight"]
    bgsl = bpy.data.objects["Starslight"]
    bge = bpy.data.objects["StarryNight.002"]
    bgal = bpy.data.objects["Starslight.003"]
    bga = bpy.data.objects["StarryNight.003"]
    bgc = bpy.data.objects["StarryNight.004"]
    bgcl = bpy.data.objects["Starslight.002"]
            #Objects
    t1 = bpy.data.objects["TestingIcosphere5meters"]
    ss1 = bpy.data.objects["ShootingStar1"]
    ss2 = bpy.data.objects["ShootingStar2"]
    ss3 = bpy.data.objects["ShootingStar3"]
    ss4 = bpy.data.objects["ShootingStar4"]
    ss5 = bpy.data.objects["ShootingStar5"]
    p1 = bpy.data.objects["Planet1"]
    p2 = bpy.data.objects["Planet2"]
    p3 = bpy.data.objects["Planet3"]
    b1 = bpy.data.objects["Black Hole.002"]
    b2 = bpy.data.objects["Black Hole.003"]
    b3 = bpy.data.objects["Black Hole.004"]
    cs = bpy.data.objects["CloseStar"]
    ufo = bpy.data.objects["UFO"]
    sl = bpy.data.objects["ShuttleLight"]
    sh = bpy.data.objects["SpaceShuttle"]
    smbh = bpy.data.objects["BlackHoleSuperMassive"]
    r1 = bpy.data.objects["Rings1"]
    r2 = bpy.data.objects["Rings2"]
    ses = bpy.data.objects["SolarEclispseShadow"]
    seshydra = bpy.data.objects["SolarEclispseShadow.002"]
    schaos = bpy.data.objects["ChaosShadow"]
    cr1 = bpy.data.objects["ChaosDisk2"]
    cr2 = bpy.data.objects["ChaosDisk1"]
    g1a = bpy.data.objects["GammaRay1_Inner"]
    g1b = bpy.data.objects["GammaRay1_Mid"]
    g1c = bpy.data.objects["GammaRay1_Out"]
    g2a = bpy.data.objects["GammaRay1_Inner.001"]
    g2b = bpy.data.objects["GammaRay1_Mid.001"]
    g2c = bpy.data.objects["GammaRay1_Out.001"]
    g3a = bpy.data.objects["GammaRay1_Inner.002"]
    g3b = bpy.data.objects["GammaRay1_Mid.002"]
    g3c = bpy.data.objects["GammaRay1_Out.002"]
            #Earth Collection
    er = bpy.data.objects["EarthRock"]
    eatm = bpy.data.objects["EarthAtmosphere"]
    erl = bpy.data.objects["EarthLight"]
    moon = bpy.data.objects["Moon"]
    moonl = bpy.data.objects["MoonLight"]
            #Crown Collection
    c1 = bpy.data.objects["CircleCrown"]
    c2 = bpy.data.objects["CrownPart"]
    c3 = bpy.data.objects["CrownRedGems"]
    c4 = bpy.data.objects["CrownBlueGem"]
            #Gas Clouds
    gc = bpy.data.objects["GasCloud"]
    gcl = bpy.data.objects["GasCloudLight3"]
    gcl1 = bpy.data.objects["GasCloudLight1"]
    gcl2 = bpy.data.objects["GasCloudLight2"]

    # START RENDERING HERE -------------------------------------------------------------------------------
        #Reset Actions
    print("Reset In Progress...")
    kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,1,1,1);
    kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,1,1,1);
    kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,1,1,1);
    kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,1,1,1);
    kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,1,1,1);
    bgs.location.x = 0
    bgs.location.y = 0
    bgsl.location.x = 0
    bgsl.location.y = 0
    bgc.location.x = 0
    bgc.location.y = 0
    bgcl.location.x = 0
    bgcl.location.y = 0
    mainBear.location.x = 0
    mainBear.location.y = 0
    bearLight.location.x = 0
    bearLight.location.y = 0
    hydraHead.location.y = 200
    hydraLight.location.y = 200
    bge.location.x = 0
    bge.location.y = 0
    bgal.location.x = 0
    bgal.location.y = 0
    bga.location.x = 0
    bga.location.y = 0
    ss1.location.x = -200
    ss1.location.y = 200
    ss2.location.x = -175
    ss2.location.y = 200
    ss3.location.x = -150
    ss3.location.y = 200
    ss4.location.x = -125
    ss4.location.y = 200
    ss5.location.x = -100
    ss5.location.y = 200 
    ss1.rotation_euler[2] = 0
    ss2.rotation_euler[2] = 0
    ss3.rotation_euler[2] = 0
    ss4.rotation_euler[2] = 0
    ss5.rotation_euler[2] = 0
    p1.location.x = -200
    p1.location.y = 175
    p2.location.x = -150
    p2.location.y = 175
    p3.location.x = -100
    p3.location.y = 175
    b1.location.x = -200
    b1.location.y = 150
    b2.location.x = -150
    b2.location.y = 150
    b3.location.x = -100
    b3.location.y = 150
    cs.location.x = -250
    cs.location.y = 200
    earthlocx = -250
    earthlocy = 150
    er.location.x = earthlocx
    er.location.y = earthlocy
    eatm.location.x = earthlocx
    eatm.location.y = earthlocy
    erl.location.x = earthlocx
    erl.location.y = earthlocy
    ufo.location.x = -245
    ufo.location.y = 100
    sl.location.x = -200 
    sl.location.y = 100
    sh.location.x = -200
    sh.location.y = 100
    smbh.location.x = -350
    smbh.location.y = 200
    r1.location.x = -450
    r1.location.y = 200
    r2.location.x = -450
    r2.location.y = 100
    angle = randD(360,0,4)
    tempx = (er.location.x) + 25*math.cos(angle)
    tempy = (er.location.y) + 25*math.sin(angle)
    moon.location.x = tempx
    moon.location.y = tempy
    moonl.location.x = tempx
    moonl.location.y = tempy
    crownlocx = -350
    crownlocy = 100
    c1.location.x = crownlocx
    c1.location.y = crownlocy
    c2.location.x = crownlocx
    c2.location.y = crownlocy
    c3.location.x = crownlocx
    c3.location.y = crownlocy
    c4.location.x = crownlocx
    c4.location.y = crownlocy
    ses.location.x = -450
    ses.location.y = 0
    gaslocx = -400
    gaslocy = -100
    gc.location.x = gaslocx
    gc.location.y = gaslocy
    gcl.location.x = gaslocx
    gcl.location.y = gaslocy
    gcl1.location.x = gaslocx - 75
    gcl1.location.y = gaslocy + 35
    gcl2.location.x = gaslocx + 75
    gcl2.location.y = gaslocy - 35
    cr1.location.x = 300
    cr2.location.x = 300
    chaosHead.location.x = 300
    bpy.data.materials["Starssurface.002"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
    bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (1,0,.013702,1)
    bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (0.409468, 0.350815, 0.008739, 1)
    bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0.021858, 0.175326, 1 ,1)
    bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[2].default_value = .005
    bpy.data.node_groups["Geometry Nodes.005"].nodes["Point Distribute.001"].inputs[2].default_value = .005
    bpy.data.node_groups["Geometry Nodes.002"].nodes["Point Distribute.005"].inputs[2].default_value = .001
    bpy.data.materials["Starssurface.005"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
    bpy.data.materials["COINMAINcolor.003"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
    bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (1,0,0,1)
    bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (0.142272,0.978658,0.409468,1)
    bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0, 0, 1, 1)
    bpy.data.materials["Starssurface.005"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[0].color = (1,1,1,1)
    bpy.data.materials["Starssurface.005"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[1].color = (1,0,0,1)
    bpy.data.materials["Starssurface.005"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[2].color = (0,0,0,1)
    bpy.data.materials["LeftEye.010"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1,0.641674,0,1)
    bpy.data.materials["LeftEye.006"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1,0.641674,0,1)
    r1.location.z = 36.1005
    r2.location.z = 36.1005
    r1.scale[0] = 28.017
    r1.scale[1] = 28.017
    r1.scale[2] = 28.017
    r2.scale[0] = 20
    r2.scale[1] = 20
    r2.scale[2] = 20
    bpy.data.materials["BearColor"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["Eyeshadow.001"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["LeftEye.008"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["RightEye"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["LeftEye"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["LeftEye.001"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["Skincolor"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["Skincolor"].blend_method = 'OPAQUE'
    bpy.data.materials["Eyeshadow"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["LeftEye.002"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["Material"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["LeftEye.006"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value =0
    bpy.data.materials["LeftEye.010"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
    bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
    bpy.data.materials["Skincolor"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
    seshydra.location.x = -320
    seshydra.location.y = 0
    schaos.location.x = -200
    schaos.location.y = -100
    t1.location.x = -250
    t1.location.y = 50
    g1a.location.x = -240
    g1b.location.x = -240
    g1c.location.x = -240
    g1a.location.y = 40
    g1b.location.y = 40
    g1c.location.y = 40
    g1a.rotation_euler[0] = 0
    g1a.rotation_euler[1] = 0
    g1a.rotation_euler[2] = 0
    g1b.rotation_euler[0] = 0
    g1b.rotation_euler[1] = 0
    g1b.rotation_euler[2] = 0
    g1c.rotation_euler[0] = 0
    g1c.rotation_euler[1] = 0
    g1c.rotation_euler[2] = 0
    g2a.location.x = -240
    g2b.location.x = -240
    g2c.location.x = -240
    g2a.location.y = 40 - 10
    g2b.location.y = 40 - 10
    g2c.location.y = 40 - 10
    g3a.location.x = -240
    g3b.location.x = -240
    g3c.location.x = -240
    g3a.location.y = 40 - 20
    g3b.location.y = 40 - 20
    g3c.location.y = 40 - 20
    g2a.rotation_euler[0] = 0
    g2a.rotation_euler[1] = 0
    g2a.rotation_euler[2] = 0
    g2b.rotation_euler[0] = 0
    g2b.rotation_euler[1] = 0
    g2b.rotation_euler[2] = 0
    g2c.rotation_euler[0] = 0
    g2c.rotation_euler[1] = 0
    g2c.rotation_euler[2] = 0
    g3a.rotation_euler[0] = 0
    g3a.rotation_euler[1] = 0
    g3a.rotation_euler[2] = 0
    g3b.rotation_euler[0] = 0
    g3b.rotation_euler[1] = 0
    g3b.rotation_euler[2] = 0
    g3c.rotation_euler[0] = 0
    g3c.rotation_euler[1] = 0
    g3c.rotation_euler[2] = 0
    print("Reset Complete!\n")


        #Stores the randomized
    currentbet = betDecider() # Bear Type, only 1
    currentbee = beeDecider() # Bear Effect, only 1
    currentbge = bgeDecider() # Background Effect, only 1
    currentbgo = bgoDecider() # Background Objects


        #Changes the Bear Type
    if(currentbet==1): # Random Bear
        kkeyecolor = hsvrgb(False)
        kkeyeshadow = hsvrgb(True)
        kkskincolor = hsvrgb(True)
        while(abs(kkeyeshadow[0]-kkskincolor[0])<=.02 and abs(kkeyeshadow[1]-kkskincolor[1])<=.02 and abs(kkeyeshadow[2]-kkskincolor[2])<=.02):
            kkeyeshadow = hsvrgb(True)
        kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkskincolor);
        kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(9999,-10000)
        print("Bear Type: Random")
        finaloutput += "BT:Random//"
    elif(currentbet==2): # Bruin Bear
        kkeyecolor = hsvrgb(False)
        kkeyeshadow = hsvrgb(True)
        kkskincolor = (0.254152, 0.084376, 0.009721, 1)
        while(abs(kkeyeshadow[0]-kkskincolor[0])<=.02 and abs(kkeyeshadow[1]-kkskincolor[1])<=.02 and abs(kkeyeshadow[2]-kkskincolor[2])<=.02):
            kkeyeshadow = hsvrgb(True)
        kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkskincolor);
        kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(9999,-10000)
        print("Bear Type: Bruin Bear")
        finaloutput += "BT:Bruin Bear//"
    elif(currentbet==3): # Polar Bear
        kkeyecolor = hsvrgb(False)
        kkeyeshadow = hsvrgb(True)
        kkskincolor = (1,1,1,1)
        while(abs(kkeyeshadow[0]-kkskincolor[0])<=.02 and abs(kkeyeshadow[1]-kkskincolor[1])<=.02 and abs(kkeyeshadow[2]-kkskincolor[2])<=.02):
            kkeyeshadow = hsvrgb(True)
        kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkskincolor);
        kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(9999,-10000)
        print("Bear Type: Polar Bear")
        finaloutput += "BT:Polar Bear//"
    elif(currentbet==4): # Black Bear
        kkeyecolor = hsvrgb(False)
        kkeyeshadow = hsvrgb(True)
        kkskincolor = (0.009721, 0.009134, 0.012286, 1)
        while(abs(kkeyeshadow[0]-kkskincolor[0])<=.02 and abs(kkeyeshadow[1]-kkskincolor[1])<=.02 and abs(kkeyeshadow[2]-kkskincolor[2])<=.02):
            kkeyeshadow = hsvrgb(True)
        kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.009721, 0.009134, 0.012286, 1);
        kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(9999,-10000)
        print("Bear Type: Black Bear")
        finaloutput += "BT:Black Bear//"
    elif(currentbet==5): # Hydra Bear
        kkeyecolor = hsvrgb(False)
        kkeyeshadow = hsvrgb(True)
        kkskincolor = hsvrgb(True)
        while(abs(kkeyeshadow[0]-kkskincolor[0])<=.02 and abs(kkeyeshadow[1]-kkskincolor[1])<=.02 and abs(kkeyeshadow[2]-kkskincolor[2])<=.02):
            kkeyeshadow = hsvrgb(True)
        kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (hsvrgb(True));
        kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        mainBear.location.y = 200
        hydraHead.location.y = 0
        hydraLight.location.y = 0
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(9999,-10000)#1 num 10k is used on publically avaliable version
        print("Bear Type: Hydra Bear")
        finaloutput += "BT:Hydra Bear//"
    elif(currentbet==6): # King Bear
        kkeyecolor = (0.799103,0.708376,0,1)
        kkeyeshadow = (1,1,1,1)
        kBearSkin.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.005602, 0.015207, 1, 1);
        kRightEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kLeftEye.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyecolor);
        kEyeShadowR.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        kEyeShadowL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (kkeyeshadow);
        c1.location.x = 0
        c1.location.y = 0
        c2.location.x = 0
        c2.location.y = 0
        c3.location.x = 0
        c3.location.y = 0
        c4.location.x = 0
        c4.location.y = 0
        bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (0.799103,0.708376,0,1)
        bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (1,1,1,1)
        bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0.005602, 0.015207, 1, 1)
        bpy.data.node_groups["Geometry Nodes.002"].nodes["Point Distribute.005"].inputs[4].default_value = rand(10000,-10000)
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(10000,-10000)
        print("King Bear!!!")
        finaloutput += "BT:King Bear//"
    elif(currentbet==7): # Chaos Bear
        mainBear.location.y = 400
        bearLight.location.y = 400
        bgs.location.y = 400
        bgsl.location.y = 400
        bge.location.y = 500
        bgal.location.y = 600
        bga.location.y = 600
        cr1.location.x = 0
        cr2.location.x = 0
        chaosHead.location.x = 0
        chaosHead.location.y = 0
        bpy.data.node_groups["Geometry Nodes.005"].nodes["Point Distribute.001"].inputs[4].default_value = rand(10000,-10000)
        print("Chaos Bear!!!")
        finaloutput += "BT:Chaos Bear//"
    else:
        print("Overload: Bear Type Index Overload")  
        
        
        #Changes the Bear Effects
    if(currentbee==(-1)): # No Bear Effects
        print("No Bear Effects")
    elif(currentbee==0): # Different Colored Eyes
        coloruno = hsvrgb(False)
        colordos = hsvrgb(False)
        while(abs(coloruno[0]-colordos[0])<.06):
            coloruno = hsvrgb(False)
        if(currentbet==6):
            randnum = rand(1,0)
            while(abs(bpy.data.materials["RightEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value[0]-coloruno[0])<.15):
                coloruno = hsvrgb(False)
            if(randnum==1):
                bpy.data.materials["RightEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = coloruno
            else:
                 bpy.data.materials["LeftEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = coloruno
        elif(currentbet==7):
            randnum = rand(1,0)
            while((coloruno[0]+coloruno[1])>1.3):
                coloruno = hsvrgb(True)
            if(randnum==1):
                bpy.data.materials["LeftEye.010"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = coloruno
            else:
                bpy.data.materials["LeftEye.006"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = coloruno       
        else:
            bpy.data.materials["RightEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = coloruno
            bpy.data.materials["LeftEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = colordos
        print("Different Colored Eyes")
        finaloutput += "BE:Different Colored Eyes//"
    elif(currentbee==1): # Rings
        randnum = rand(2,1)
        if(randnum==2):
            r1.location.x = 0
            r1.location.y = 0
            r2.location.x = 0
            r2.location.y = 0
        else:
            r1.location.x = 0
            r1.location.y = 0
        r1.rotation_euler[0] = math.radians(rand(360,0))
        r1.rotation_euler[1] = math.radians(rand(360,0))
        r1.rotation_euler[2] = math.radians(rand(360,0))
        r2.rotation_euler[0] = math.radians(rand(360,0))
        r2.rotation_euler[1] = math.radians(rand(360,0))
        r2.rotation_euler[2] = math.radians(rand(360,0))
        r1.location.z = 27.5599
        r2.location.z = 27.5599
        if(currentbet!=7):
            r1.scale[0] = 28.017 + 10
            r1.scale[1] = 28.017 + 10
            r1.scale[2] = 28.017 + 10
            r2.scale[0] = 20 + 10
            r2.scale[1] = 20 + 10
            r2.scale[2] = 20 + 10
        if(currentbet==5):
            r1.scale[0] = 28.017 + 30
            r1.scale[1] = 28.017 + 30
            r1.scale[2] = 28.017 + 30
            r2.scale[0] = 20 + 40
            r2.scale[1] = 20 + 40
            r2.scale[2] = 20 + 40
        bpy.data.materials["DiskMat.001"].node_tree.nodes["RGB"].outputs[0].default_value = hsvrgb(True)
        bpy.data.materials["DiskMat.007"].node_tree.nodes["RGB"].outputs[0].default_value = hsvrgb(True)
        print("Rings")
        finaloutput += "BE:Rings//"
    elif(currentbee==2): # Glowing Bear
        bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 9
        bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[0].default_value
        if(currentbet==2):
            bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 34
            print("Glowing Bear")
            finaloutput += "BE:Glowing Bear//"
        elif(currentbet==4):
            bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
        elif(currentbet==7):
            bpy.data.materials["Skincolor"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 24.2
            print("Glowing Bear")
            finaloutput += "BE:Glowing Bear//"
        else:
            print("Glowing Bear")
            finaloutput += "BE:Glowing Bear//"
    elif(currentbee==3): # Panda Coloring
        bpy.data.materials["RightEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[0].default_value
        bpy.data.materials["LeftEye"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = bpy.data.materials["BearColor"].node_tree.nodes["Principled BSDF"].inputs[0].default_value
        bpy.data.materials["LeftEye.006"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1,1,1,1)
        bpy.data.materials["LeftEye.010"].node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1,1,1,1)
        print("Panda Coloring")
        finaloutput += "BE:Panda Coloring//"
    elif(currentbee==4): # Translucent Bear 
        bpy.data.materials["BearColor"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .85
        bpy.data.materials["Eyeshadow.001"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .877
        bpy.data.materials["LeftEye.008"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .877
        bpy.data.materials["RightEye"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .5
        bpy.data.materials["LeftEye"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .5
        bpy.data.materials["Skincolor"].blend_method = 'HASHED'
        bpy.data.materials["LeftEye.001"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0.583
        bpy.data.materials["Skincolor"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0
        bpy.data.materials["Eyeshadow"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0.583
        bpy.data.materials["LeftEye.002"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0.583
        bpy.data.materials["Material"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = 0.417
        bpy.data.materials["LeftEye.006"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .957
        bpy.data.materials["LeftEye.010"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = .957
        print("Translucent Bear")
        finaloutput += "BE:Translucent Bear//"
    elif(currentbee==5): # Solar Eclispse Bear
        negative = False
        ycord = randD(35,-35,3)
        xcord = (math.pow(randD(35,0,4),2))-(math.pow(ycord,2))
        xcord = round(xcord,3)
        if(xcord<0):
            negative = True
        xcord = math.sqrt(abs(xcord))
        if(negative):
            xcord = -xcord
        if(currentbet==5):
            seshydra.location.x = xcord
            seshydra.location.y = ycord
        elif(currentbet==7):
            ycord = randD(15,-15,3)
            xcord = (math.pow(randD(15,0,4),2))-(math.pow(ycord,2))
            xcord = round(xcord,3)
            if(xcord<0):
                negative = True
            xcord = math.sqrt(abs(xcord))
            if(negative):
                xcord = -xcord
            schaos.location.x = xcord
            schaos.location.y = ycord
        else:
            ses.location.x = xcord
            ses.location.y = ycord
        print("Solar Eclispse Bear")
        finaloutput += "BE:Solar Eclispse Bear//"
    else:
        print("Overload: Bear Type Index Overload")  


     #Changes the Background Effects
    if(currentbge==(-1)):
        print("No Background Effects")
    elif(currentbge==0):
        bpy.data.materials["Starssurface.002"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 27.32
        bpy.data.materials["COINMAINcolor.003"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 44.8
        bpy.data.materials["Starssurface.005"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 47.8
        print("Glowing Stars")
        finaloutput += "BGE:Glowing Stars//"
    elif(currentbge==1):
        bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = hsvrgb(True)
        bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = hsvrgb(True)
        bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = hsvrgb(True)
        if(currentbet==7):
            bpy.data.materials["Starssurface.005"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[0].color = hsvrgb(True)
            bpy.data.materials["Starssurface.005"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[1].color = hsvrgb(True)
            bpy.data.materials["Starssurface.005"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[2].color = hsvrgb(True)
        #Change the Color Gradient for King Bears, and if diff gradient then add Eth coins.
        elif(currentbet==6):
            bgs.location.y = 300
            bgsl.location.y = 300
            bpy.data.node_groups["Geometry Nodes.005"].nodes["Point Distribute.001"].inputs[4].default_value = rand(10000,-10000)
        print("Different Stars")
        finaloutput += "BGE:Different Stars//"
    elif(currentbge==2):
        randomnum = randD(.01,.000001,7)
        while(abs(.005-randomnum)<=.002):
            randomnum = randD(.01,.000001,7)
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[2].default_value = randomnum
        bpy.data.node_groups["Geometry Nodes.005"].nodes["Point Distribute.001"].inputs[2].default_value = randomnum
        print("Less/More Stars")
        finaloutput += "BGE:Less/More Stars//"
    elif(currentbge==3):
        bgs.location.x = 300
        bgsl.location.x = 300
        bge.location.x = 300
        bgal.location.x = 300
        bga.location.x = 300
        bgc.location.x = 300
        bgcl.location.x = 300
        bpy.data.node_groups["GeoNodesCone.001"].nodes["Point Distribute.001"].inputs[4].default_value = rand(10000,-10000 )
        if(currentbet==6):
            bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (0.799103,0.708376,0,1)
            bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (1,1,1,1)
            bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0.005602, 0.015207, 1, 1)
        elif(currentbet==7):
            bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (1,0,0,1)
            bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (1,1,1,1)
            bpy.data.materials["Material.017"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0, 0, 0, 1)        
        print("Light Speed Travel")
        finaloutput += "BGE:Light Speed Travel//"
    elif(currentbge==4):
        bgs.location.x = 300
        bgsl.location.x = 300
        bge.location.x = 300
        bga.location.x = 0
        bga.location.y = 0
        bpy.data.node_groups["Geometry Nodes.004"].nodes["Point Distribute.002"].inputs[4].default_value = rand(10000,-10000)
        bpy.data.node_groups["Geometry Nodes.004"].nodes["Point Distribute.001"].inputs[4].default_value = rand(10000,-10000)
        if(currentbet==6):
            bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (0.799103,0.708376,0,1)
            bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (1,1,1,1)
            bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0.005602, 0.015207, 1, 1)
        elif(currentbet==7):
            bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (1,0,0,1)
            bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (1,1,1,1)
            bpy.data.materials["Starssurface.002"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (0, 0, 0, 1)
        print("Meteor Field")
        finaloutput += "BGE:Meteor Field//"
    elif(currentbge==5):
        bpy.data.node_groups["Geometry Nodes.001"].nodes["Point Distribute.001"].inputs[2].default_value = 0
        bpy.data.node_groups["Geometry Nodes.005"].nodes["Point Distribute.001"].inputs[2].default_value = 0
        print("Star-Less Night")
        finaloutput += "BGE:Star-Less Night//"
    else:
        print("Overload: Bear Type Index Overload")


     #Changes the Background Objects
    if(currentbgo==(-1)):
        print("No Bear Objects")
    else:
        for z in range(len(currentbgo)):#Wont display mulobj
            if(currentbgo[z]==0):
                numstars = rand(5,1)
                kknumstar = numstars
                mulscaler = []
                mulcords = []
                mulcolor = []
                mulzrot = []
                for x in range(numstars):
                    tempscale = randD(1.5,1,3)
                    tempinput = cordD(xymidBG,4,tempscale)
                    mulcords.append((tempinput[0],tempinput[1]))
                    mulscaler.append(tempscale)
                    mulcolor.append(hsvrgb(True))
                    mulzrot.append(math.radians(randD(360,0,2)))
                if(numstars>=1):
                    ss1.location.x = mulcords[0][0]
                    ss1.location.y = mulcords[0][1]
                    ss1.scale[0] = mulscaler[0]
                    ss1.scale[1] = mulscaler[0]
                    ss1.scale[2] = mulscaler[0]
                    ss1.rotation_euler[2] =  mulzrot[0]
                    bpy.data.materials["Material.009"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (mulcolor[0])
                if(numstars>=2):
                    ss2.location.x = mulcords[1][0]
                    ss2.location.y = mulcords[1][1]
                    ss2.scale[0] = mulscaler[1]
                    ss2.scale[1] = mulscaler[1]
                    ss2.scale[2] = mulscaler[1]
                    ss2.rotation_euler[2] = mulzrot[1]
                    bpy.data.materials["Material.004"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (mulcolor[1])
                if(numstars>=3):
                    ss3.location.x = mulcords[2][0]
                    ss3.location.y = mulcords[2][1]
                    ss3.scale[0] = mulscaler[2]
                    ss3.scale[1] = mulscaler[2]
                    ss3.scale[2] = mulscaler[2]
                    ss3.rotation_euler[2] = mulzrot[2]
                    bpy.data.materials["Material.006"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (mulcolor[2])
                if(numstars>=4):
                    ss4.location.x = mulcords[3][0]
                    ss4.location.y = mulcords[3][1]
                    ss4.scale[0] = mulscaler[3]
                    ss4.scale[1] = mulscaler[3]
                    ss4.scale[2] = mulscaler[3]
                    ss4.rotation_euler[2] = mulzrot[3]
                    bpy.data.materials["Material.005"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (mulcolor[3])
                if(numstars>=5):
                    ss5.location.x = mulcords[4][0]
                    ss5.location.y = mulcords[4][1]
                    ss5.scale[0] = mulscaler[4]
                    ss5.scale[1] = mulscaler[4]
                    ss5.scale[2] = mulscaler[4]
                    ss5.rotation_euler[2] = mulzrot[4]
                    bpy.data.materials["Material.008"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = (mulcolor[4])
                print("Shooting Stars-----------------------")
                finaloutput += "BGO:Shooting Stars//"
            elif(currentbgo[z]==1):
                numplan = rand(3,1)
                mulscaler = []
                mulcords = []
                mulcolor = []
                mulxrot = []
                mulyrot = []
                mulseed = []
                for x in range(numplan):
                    tempscale = randD(1.9,.6,3)
                    tempinput = cordD(xyBG-5,12,tempscale)
                    mulcords.append((tempinput[0],tempinput[1]))
                    mulscaler.append(tempscale)
                    mulcolor.append(hsvrgb(True))
                    mulxrot.append(math.radians(randD(90,0,2)))
                    mulyrot.append(math.radians(randD(90,0,2)))
                    mulseed.append(math.radians(randD(10000,0,3)))
                if(numplan>=1):
                    p1.location.x = mulcords[0][0]
                    p1.location.y = mulcords[0][1]
                    p1.scale[0] = mulscaler[0]
                    p1.scale[1] = mulscaler[0]
                    p1.scale[2] = mulscaler[0]
                    bpy.data.materials["Material.010"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = mulcolor[0]
                    p1.rotation_euler[0] = mulxrot[0]
                    p1.rotation_euler[1] = mulyrot[0]
                    bpy.data.materials["Material.007"].node_tree.nodes["Noise Texture.001"].inputs[1].default_value = mulseed[0]
                if(numplan>=2):
                    p2.location.x = mulcords[1][0]
                    p2.location.y = mulcords[1][1]
                    p2.scale[0] = mulscaler[1]
                    p2.scale[1] = mulscaler[1]
                    p2.scale[2] = mulscaler[1]
                    bpy.data.materials["Material.011"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = mulcolor[1]
                    p2.rotation_euler[0] = mulxrot[1]
                    p2.rotation_euler[1] = mulyrot[1]
                    bpy.data.materials["Material.011"].node_tree.nodes["Noise Texture"].inputs[1].default_value = mulseed[1]
                if(numplan>=3):
                    p3.location.x = mulcords[2][0]
                    p3.location.y = mulcords[2][1]
                    p3.scale[0] = mulscaler[2]
                    p3.scale[1] = mulscaler[2]
                    p3.scale[2] = mulscaler[2]
                    bpy.data.materials["Material.007"].node_tree.nodes["Principled BSDF"].inputs[0].default_value =  mulcolor[2]
                    p3.rotation_euler[0] = mulxrot[2]
                    p3.rotation_euler[1] = mulyrot[2]
                    bpy.data.materials["Material.010"].node_tree.nodes["Noise Texture.001"].inputs[1].default_value = mulseed[2]
                print("Planets-----------------------")
                finaloutput += "BGO:Planets//"
            elif(currentbgo[z]==2):
                 if(currentbge!=5):
                    tempscale = randD(2.5,1.9,3)
                    tempcord = cordD(xyBG,19,tempscale)
                    cs.location.x = tempcord[0]
                    cs.location.y = tempcord[1]
                    cs.scale[0] = tempscale 
                    cs.scale[1] = tempscale
                    cs.scale[2] = tempscale
                    bpy.data.materials["Starssurface.001"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].color = hsvrgb(True)
                    print("Up-Close Star-----------------------")
                    finaloutput += "BGO:Up-Close Star//"
            elif(currentbgo[z]==3):
                gc.location.x = 0
                gcl.location.x = 0
                gcl1.location.x = -75
                gcl2.location.x = 75
                gc.location.y = 0
                gcl.location.y = 0
                gcl1.location.y = +35
                gcl2.location.y = -35
                bpy.data.materials["CloudyMaterial"].node_tree.nodes["Noise Texture"].inputs[1].default_value = randD(10000,0,4)
                bpy.data.materials["CloudyMaterial"].node_tree.nodes["Principled Volume"].inputs[0].default_value = hsvrgb(True)
                print("Gaseous Clouds-----------------------")
                finaloutput += "BGO:Gaseous Clouds//"
            elif(currentbgo[z]==4):
                numholes = rand(3,1)
                mulscaler = []
                mulcords = []
                mulcolor = []
                mulyrot = []
                mulzrot = []
                for x in range(numholes):
                    tempscaler = randD(2.5,.9,3)
                    tempcolor = hsvrgb(True)
                    mulscaler.append(tempscaler)
                    mulcords.append(cordD(xymidBG,15,tempscaler))
                    mulcolor.append(tempcolor)
                    mulyrot.append(math.radians(randD(360,0,2)))
                    mulzrot.append(math.radians(randD(360,0,2)))
                if(numholes>=1):
                    bpy.data.materials["DiskMat.002"].node_tree.nodes["RGB"].outputs[0].default_value = mulcolor[0]
                    bpy.data.materials["BlackHole_New.002"].node_tree.nodes["Glass BSDF"].inputs[0].default_value = mulcolor[0]
                    b1.location.x = mulcords[0][0]
                    b1.location.y = mulcords[0][1]
                    b1.scale[0] = mulscaler[0]
                    b1.scale[1] = mulscaler[0]
                    b1.scale[2] = mulscaler[0]
                    b1.rotation_euler[1] = mulyrot[0]
                    b1.rotation_euler[2] = mulzrot[0]
                if(numholes>=2):
                    bpy.data.materials["BlackHole_New.003"].node_tree.nodes["Glass BSDF"].inputs[0].default_value = mulcolor[1]
                    bpy.data.materials["DiskMat.003"].node_tree.nodes["RGB"].outputs[0].default_value = mulcolor[1]
                    b2.location.x = mulcords[1][0]
                    b2.location.y = mulcords[1][1]
                    b2.scale[0] = mulscaler[1]
                    b2.scale[1] = mulscaler[1]
                    b2.scale[2] = mulscaler[1]
                    b2.rotation_euler[1] = mulyrot[1]
                    b2.rotation_euler[2] = mulzrot[1]
                if(numholes>=3):
                    bpy.data.materials["BlackHole_New.004"].node_tree.nodes["Glass BSDF"].inputs[0].default_value = mulcolor[2]
                    bpy.data.materials["DiskMat.004"].node_tree.nodes["RGB"].outputs[0].default_value = mulcolor[2]
                    b3.location.x = mulcords[2][0]
                    b3.location.y = mulcords[2][1]
                    b3.scale[0] = mulscaler[2]
                    b3.scale[1] = mulscaler[2]
                    b3.scale[2] = mulscaler[2]
                    b3.rotation_euler[1] = mulyrot[2]
                    b3.rotation_euler[2] = mulzrot[2]
                print("Black Holes-----------------------")
                finaloutput += "BGO:Black Holes//"
            elif(currentbgo[z]==5):
                numray = rand(3,1)
                mulcords = []
                mulcolors = []
                mulxrot = []
                mulyrot = []
                mulzrot = []
                for x in range(numray):
                    tempcolor = (hsvrgb(True),hsvrgb(True))
                    tempcord = (randD(95,-95,3),randD(95,-95,3))
                    mulcords.append(tempcord)
                    mulcolors.append(tempcolor)
                    mulxrot.append(math.radians(randD(90,40,3)))
                    mulyrot.append(math.radians(randD(90,40,3)))
                    mulzrot.append(math.radians(randD(360,0,3)))
                if(numray>=1):
                    g1a.location.x = mulcords[0][0]
                    g1a.location.y = mulcords[0][1]
                    g1a.rotation_euler[0] = mulxrot[0]
                    g1a.rotation_euler[1] = mulyrot[0]
                    g1a.rotation_euler[2] = mulzrot[0]
                    g1b.location.x = mulcords[0][0]
                    g1b.location.y = mulcords[0][1]
                    g1b.rotation_euler[0] = mulxrot[0]
                    g1b.rotation_euler[1] = mulyrot[0]
                    g1b.rotation_euler[2] = mulzrot[0]
                    g1c.location.x = mulcords[0][0]
                    g1c.location.y = mulcords[0][1]
                    g1c.rotation_euler[0] = mulxrot[0]
                    g1c.rotation_euler[1] = mulyrot[0]
                    g1c.rotation_euler[2] = mulzrot[0]
                    bpy.data.materials["Material.015"].node_tree.nodes["Emission"].inputs[0].default_value = mulcolors[0][0]
                    bpy.data.materials["Material.016"].node_tree.nodes["Emission"].inputs[0].default_value = mulcolors[0][1]
                if(numray>=2):
                    g2a.location.x = mulcords[1][0]
                    g2a.location.y = mulcords[1][1]
                    g2a.rotation_euler[0] = mulxrot[1]
                    g2a.rotation_euler[1] = mulyrot[1]
                    g2a.rotation_euler[2] = mulzrot[1]
                    g2b.location.x = mulcords[1][0]
                    g2b.location.y = mulcords[1][1]
                    g2b.rotation_euler[0] = mulxrot[1]
                    g2b.rotation_euler[1] = mulyrot[1]
                    g2b.rotation_euler[2] = mulzrot[1]
                    g2c.location.x = mulcords[1][0]
                    g2c.location.y = mulcords[1][1]
                    g2c.rotation_euler[0] = mulxrot[1]
                    g2c.rotation_euler[1] = mulyrot[1]
                    g2c.rotation_euler[2] = mulzrot[1]
                    bpy.data.materials["Material.037"].node_tree.nodes["Emission"].inputs[0].default_value = mulcolors[1][0]
                    bpy.data.materials["Material.038"].node_tree.nodes["Emission"].inputs[0].default_value = mulcolors[1][1]
                if(numray>=3):
                    g3a.location.x = mulcords[2][0]
                    g3a.location.y = mulcords[2][1]
                    g3a.rotation_euler[0] = mulxrot[2]
                    g3a.rotation_euler[1] = mulyrot[2]
                    g3a.rotation_euler[2] = mulzrot[2]
                    g3b.location.x = mulcords[2][0]
                    g3b.location.y = mulcords[2][1]
                    g3b.rotation_euler[0] = mulxrot[2]
                    g3b.rotation_euler[1] = mulyrot[2]
                    g3b.rotation_euler[2] = mulzrot[2]
                    g3c.location.x = mulcords[2][0]
                    g3c.location.y = mulcords[2][1]
                    g3c.rotation_euler[0] = mulxrot[2]
                    g3c.rotation_euler[1] = mulyrot[2]
                    g3c.rotation_euler[2] = mulzrot[2]
                    bpy.data.materials["Material.041"].node_tree.nodes["Emission"].inputs[0].default_value = mulcolors[2][0]
                    bpy.data.materials["Material.040"].node_tree.nodes["Emission"].inputs[0].default_value = mulcolors[2][1]
                print("Gamma Ray Burst-----------------------")
                finaloutput += "BGO:Gamma Ray Burst//"
            elif(currentbgo[z]==6):
                tempscale = randD(1.5, 1, 3)
                tempx = randD(95,-95,3)
                tempy = randD(95,-95,3)
                sh.location.x = tempx
                sh.location.y = tempy
                sl.location.x = tempx
                sl.location.y = tempy
                sh.rotation_euler[0] = math.radians(randD(35,-35,3))
                sh.rotation_euler[1] = math.radians(randD(35,-35,3))
                sh.rotation_euler[2] = math.radians(randD(360,0,3))
                sh.scale[0] = tempscale
                sh.scale[1] = tempscale
                sh.scale[2] = tempscale
                print("Space Shuttle-----------------------")
                finaloutput += "BGO:Space Shuttle//"
            elif(currentbgo[z]==7):
                tempscaler = randD(1.5,.75,3)
                ufo.location.x = randD(95,-95, 3)
                ufo.location.y = randD(95,-95, 3)
                ufo.rotation_euler[0] = math.radians(randD(60,-60,3))
                ufo.rotation_euler[1] = math.radians(randD(60,-60,3))
                ufo.scale[0] = tempscaler
                ufo.scale[1] = tempscaler
                ufo.scale[2] = tempscaler
                print("UFO-----------------------")
                finaloutput += "BGO:UFO//"
            elif(currentbgo[z]==8):
                temp1 = cordD(xymidBG,25,1)
                er.location.x = temp1[0]
                er.location.y = temp1[1]
                eatm.location.x = temp1[0]
                eatm.location.y = temp1[1]
                erl.location.x = temp1[0]
                erl.location.y = temp1[1]
                angle = randD(360,0,4)
                tempx = (er.location.x) + 25*math.cos(angle)
                tempy = (er.location.y) + 25*math.sin(angle)
                moon.location.x = tempx
                moon.location.y = tempy
                moonl.location.x = tempx
                moonl.location.y = tempy
                print("Earth-----------------------")
                finaloutput += "BGO:Earth//"
            elif(currentbgo[z]==9):
                bpy.data.materials["BlackHole_New.001"].node_tree.nodes["Glass BSDF"].inputs[0].default_value = hsvrgb(True)
                tempscale = randD(1.5,1,3)
                tempcord = cordD(xymidBG,46,tempscale)
                smbh.location.x = tempcord[0]
                smbh.location.y = tempcord[1]
                print("Super Massive Black Hole-----------------------")
                finaloutput += "BGO:Super Massive Black Hole//"
            else:
                print("Overload: Background Object Index Overload")
            #------------------------------------
    print("====================================================")
    print(finaloutput)
    if(kactive):
        D.scenes[0].render.resolution_percentage = 100
        D.scenes[0].render.filepath = addresshighres
        bpy.ops.render.render(write_still=True)

        D.scenes[0].render.resolution_percentage = 35
        D.scenes[0].render.filepath = addresslowres
        bpy.ops.render.render(write_still=True)
                #------------------------------------
    
    #Reset Before Looped
    objxcords = []
    objycords = []
    objsize =  []

#Testing Section
#print(backTypesProbs() + '\n' +  backObjectsProbs() + '\n' + bearEffectsProbs() + '\n' + backEffectsProbs())
'''
print(currentbgo)
print("^^^ Background Objects ^^^")
print(currentbge)
print("^^^ Background Effects ^^^")
print(currentbee)
print("^^^ Bear Effects ^^^")
print(currentbet)
print("^^^ Bear Type ^^^")
print()
print()
'''
