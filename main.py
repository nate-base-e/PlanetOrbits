import math
from math import sin
from math import cos
from math import pi
from math import radians
import datetime


def dcos(val):
    return cos(radians(val))


def dsin(val):
    return sin(radians(val))


def Ecalc(Mvald, evalr):
    Mvalr = Mvald * pi / 180

    En = Mvalr - evalr * sin(Mvalr)
    dM = Mvalr - (En - evalr * sin(En))
    dE = dM / (1 - evalr * cos(En))

    while math.fabs(dE) > 10 ** (-6):
        dM = Mvalr - (En - evalr * sin(En))
        dE = dM / (1 - evalr * cos(En))
        En = En + dE

    return (En * 180 / pi)


j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0)
today = datetime.datetime.today()
delta = today - j2000
Tval = (delta.days) / 36525

# a, e, I, L, long. peri., long. node
planetDictionary = {'mercury': [[0.38709843, 0.20563661, 7.00559432, 252.25166724, 77.45771895, 48.33961819],
                                [0.00000000, 0.00002123, -0.00590158, 149472.67486623, 0.15940013, -0.12214182]],
                    'venus': [[0.72332102, 0.00676399, 3.39777545, 181.97970850, 131.76755713, 76.67261496],
                              [-0.00000026, -0.00005107, 0.00043494, 58517.81560260, 0.05679648, -0.27274174]],
                    'earthb': [[1.00000018, 0.01673163, -0.00054346, 100.46691572, 102.93005885, -5.11260389],
                               [-0.00000003, -0.00003661, -0.01337178, 35999.37306329, 0.31795260, -0.24123856]],
                    'mars': [[1.52371243, 0.09336511, 1.85181869, -4.56813164, -23.91744784, 49.71320984],
                             [0.00000097, 0.00009149, -0.00724757, 19140.29934243, 0.45223625, -0.26852431]],
                    'jupiter': [[5.20248019, 0.04853590, 1.29861416, 34.33479152, 14.27495244, 100.29282654],
                                [-0.00002864, 0.00018026, -0.00322699, 3034.90371757, 0.18199196, 0.13024619]],
                    'saturn': [[9.54149883, 0.05550825, 2.49424102, 50.07571329, 92.86136063, 113.63998702],
                               [-0.00003065, -0.00032044, 0.00451969, 1222.11494724, 0.54179478, -0.25015002]],
                    'uranus': [[19.18797948, 0.04685740, 0.77298127, 314.20276625, 172.43404441, 73.96250215],
                               [-0.00020455, -0.00001550, -0.00180155, 428.49512595, 0.09266985, 0.05739699]],
                    'neptune': [[30.06952752, 0.00895439, 1.77005520, 304.22289287, 46.68158724, 131.78635853],
                                [0.00006447, 0.00000818, 0.00022400, 218.46515314, 0.01009938, -0.00606302]]}

# b, c, s, f
addVals = {'jupiter': [-0.00012452, 0.06064060, -0.35635438, 38.35125000],
           'saturn': [0.00025899, -0.13434469, 0.87320147, 38.35125000],
           'uranus': [0.00058331, -0.97731848, 0.17689245, 7.67025000],
           'neptune': [-0.00041348, 0.68346318, -0.10162547, 7.67025000]}

planetVal = "mercury"

orbitVals = planetDictionary[planetVal]
finalOrbitVals = []
for i in range(6):
    finalOrbitVals.append(orbitVals[0][i] + Tval * orbitVals[1][i])

bval = 0
cval = 0
sval = 0
fval = 0
addValPlanets = ['jupiter', 'saturn', 'uranus', 'neptune']
if planetVal in addValPlanets:
    addList = addVals[planetVal]
    bval = addList[0]
    cval = addList[1]
    sval = addList[2]
    fval = addList[3]

aval = finalOrbitVals[0]
eval = finalOrbitVals[1]
Ival = finalOrbitVals[2]
Lval = finalOrbitVals[3]
wbval = finalOrbitVals[4]
oval = finalOrbitVals[5]

# Got rid of e* because it was not working for the Newton solver

wval = wbval - oval

Mval = (Lval - wbval + bval * Tval ** 2 + cval * dcos(fval * Tval) + sval * dsin(
    fval * Tval)) % 360
print(Mval)

# Converts the Mval into radians in the function and returns Eval in degrees
Eval = Ecalc(Mval, eval)

xp = aval * (dcos(Eval) - eval)

yp = aval * math.sqrt(1 - eval ** 2) * dsin(Eval)

zp = 0

xecl = xp * (dcos(wval) * dcos(oval) - dsin(wval) * dsin(oval) * dcos(Ival)) + yp * (
        -dsin(wval) * dcos(oval) - dcos(wval) * dsin(oval) * dcos(Ival))
yecl = xp * (dcos(wval) * dsin(oval) + dsin(wval) * dcos(oval) * dcos(Ival)) + yp * (
        -dsin(wval) * dsin(oval) + dcos(wval) * dcos(oval) * dcos(Ival))
zecl = xp * (dsin(wval) * dsin(Ival)) + yp * (dcos(wval) * dsin(Ival))
se = 23.43928
xeq = xecl
yeq = dcos(se) * yecl - dsin(se) * zecl

rotAngle = (math.atan(yecl / xecl)) * 180 / pi
if xecl < 0:
    rotAngle += 180
elif yecl < 0:
    rotAngle += 360
radius = math.sqrt(xecl ** 2 + yecl ** 2)

print("xecl(au): ", xecl, "  yecl(au): ", yecl)
print("xp: ", xp, "   yp:", yp)
print("xeq: ", xeq, "yeq: ", yeq)
print("radius(au): ", radius, "  Angle(deg):", rotAngle)
