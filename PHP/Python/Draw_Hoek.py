import math, sys, json


class vector3:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __add__(self,other):
        return vector3(self.x+other.x,self.y+other.y,self.z+other.z)
    def __sub__(self, other):
        return vector3(self.x-other.x,self.y-other.y,self.z-other.z)
    def __mul__(self, other):
        return float(self.x*other.x + self.y*other.y + self.z*other.z)
    def __pow__(self, other):
        return vector3(self.y*other.z-other.y*self.z, self.z*other.x-self.x*other.z, self.x*other.y-other.x*self.y)
    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+','+str(self.z)+')'

# Load the data that PHP sent us
try:
    data = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

# data = "115.0,45.0,235.0,45.0,195.0,12.0,185.0,65.0,165.0,70.0,30.48,2560.0,1000.0,23.9,20.0,47.8,30.0,12.19,-1,1"
#Get the list of the data
data_str = data.split(",")
data_li = [float(x) for x in data_str]

a1 = data_li[0] /180*math.pi
b1 = data_li[1] /180*math.pi
a2 = data_li[2] /180*math.pi
b2 = data_li[3] /180*math.pi
a5 = data_li[8] /180*math.pi
b5 = data_li[9] /180*math.pi
a4 = data_li[6] /180*math.pi
b4 = data_li[7] /180*math.pi
a3 = data_li[4] /180*math.pi
b3 = data_li[5] /180*math.pi
H1 = data_li[10] /0.3048
gamma = data_li[11] * 0.062422
gamma_water = data_li[12] * 0.062422
C1 = data_li[13] *20.8854
c1 = data_li[14] /180*math.pi
C2 = data_li[15] *20.8854
c2 = data_li[16] /180*math.pi
L = data_li[17] /0.3048
eta = data_li[18] # For -1, overhanged; for 1, not overhanged

a = vector3(math.sin(b1)*math.sin(a1),math.sin(b1)*math.cos(a1),math.cos(b1))
b = vector3(math.sin(b2)*math.sin(a2),math.sin(b2)*math.cos(a2),math.cos(b2))
d = vector3(math.sin(b3)*math.sin(a3),math.sin(b3)*math.cos(a3),math.cos(b3))
f = vector3(math.sin(b4)*math.sin(a4),math.sin(b4)*math.cos(a4),math.cos(b4))
f5 = vector3(math.sin(b5)*math.sin(a5),math.sin(b5)*math.cos(a5),math.cos(b5))
#a.The normal vertor of those surfaces

g = f**a
g5 = f5**a
i = b**a
j = f**d
j5 = f5**d
k = i**b
l = a**i
#b.The direction vectors of the interpolation lines of surfaces

m = g*d
m5 = g5*d
n = b*j
n5 = b*j5
P = i*d
q = b*g
q5 = b*g5
r = a*b
S5 = a*f5
V5 = b*f5
W5 = i*f5
lamda = i*g
lamda5 = i*g5
epsilon = f*f5
#c.Those parameters corelated with those cosine


R = math.sqrt(1-r*r)
rho = (n*q)/abs(n*q)/(R*R)
miu = (m*q)/abs(m*q)/(R*R)
niu = P/abs(P)/R
G = (g.x)**2 + (g.y)**2 + (g.z)**2
G5 = (g5.x)**2 + (g5.y)**2 + (g5.z)**2
M = math.sqrt((G*P**2 - 2*m*P*lamda + m**2*R**2))
M5 = math.sqrt((G5*P**2 - 2*m5*P*lamda5 + m5**2*R**2))
h = H1/abs(g.z)
h5 = (M*h - abs(P)*L)/M5
B = ((math.tan(c1))**2 + (math.tan(c2))**2 - 2*miu*r/rho*math.tan(c1)*math.tan(c2))/R**2
#Miscellaneous parameters

bi = math.asin(niu*i.z)
ai = math.atan((-niu*i.x)/(-niu*i.y))
#The dip of the interpolation line of surface 1 and surface 2

if (P*i.z < 0 or eta*q*i.z<0):
    print 'No wedge!'
    exit()
if (epsilon*eta*q5*i.z<0 or h5<0 or int(abs(m5*h5/(m*h)))>1 or int(abs(n*q5*m5*h5/(n5*q*m*h)))>1):
    print 'No crack!'
    exit()
#The shape of the wedge

A1 = (abs(m*q)*h**2 - abs(m5*q5)*h5**2)/(2*abs(P))
A2 = (abs(q*m**2*h**2/n) - abs(q5*m5**2*h5**2/n5))/(2*abs(P))
A5 = abs(m5*q5*h5**2/(2*n5))
W = (gamma*(q**2*m**2*h**3/abs(n) - q5**2*m5**2*h5**3/abs(n5)))/(6*abs(P))
#The area and the weight of the block

#---------------------------------------------------------Condition without water---------------------------------------------------------------

N11 = rho*W*k.z
N21 = miu*W*l.z
#The normal force of the surfaces

if (N11<0 and N21<0):         #Lose touch with both surface
    F1 = 0
if (N11>0 and N21<0):         #Only in touch with surface 1
    Na = W*a.z
    Sx = -Na*a.x
    Sy = -Na*a.y
    Sz = -Na*a.z + W
    Sa = math.sqrt(Sx**2 + Sy**2 + Sz**2)
    Qa = Na*math.tan(b1) + C1*A1
    F1 = Qa/Sa
if (N11<0 and N21>0):         #Only in touch with surface 2
    Nb = W*b.z
    Sx = -Nb*b.x
    Sy = -Nb*b.y
    Sz = -Nb*b.z + W
    Sb = math.sqrt(Sx**2 + Sy**2 + Sz**2)
    Qb = Nb*math.tan(b2) + C2*A2
    F1 = Qb/Sb
if (N11>0 and N21>0):         #Keep in touch with both
    S = niu*W*i.z
    Q = N11*math.tan(c1) + N21*math.tan(c2) + C1*A1 + C2*A2
    F1 = Q/S


#----------------------------------------------------------Condition with water----------------------------------------------------------------
u1 = gamma_water*h5*abs(m5)/(3*d.z)
u2 = gamma_water*h5*abs(m5)/(3*d.z)
u5 = gamma_water*h5*abs(m5)/(3*d.z)
V = u5*A5*eta*(epsilon/abs(epsilon))
#Water pressure

N12 = rho*(W*k.z + V*(r*V5-S5)) - u1*A1
N22 = miu*(W*l.z + V*(r*S5-V5)) - u2*A2
#The normal force of the surfaces

if (N12<0 and N22<0):         #Lose touch with both surface
    F2 = 0
if (N12>0 and N22<0):         #Only in touch with surface 1
    Na = W*a.z - V*S5 - u2*A2*r
    Sx = -(Na*a.x + V*f5.x + u2*A2*b.x)
    Sy = -(Na*a.y + V*f5.y + u2*A2*b.y)
    Sz = -(Na*a.z + V*f5.z + u2*A2*b.z) + W
    Sa = math.sqrt(Sx**2 + Sy**2 + Sz**2)
    Qa = (Na - u1*A1)*math.tan(b1) + C1*A1
    F2 = Qa/Sa
if (N12<0 and N22>0):         #Only in touch with surface 2
    Nb = W*b.z - V*V5 - u1*A1*r
    Sx = -(Nb*b.x + V*f5.x + u1*A1*a.x)
    Sy = -(Nb*b.y + V*f5.y + u1*A1*a.y)
    Sz = -(Nb*b.z + V*f5.z + u1*A1*a.z) + W
    Sb = math.sqrt(Sx**2 + Sy**2 + Sz**2)
    Qb = (Nb - u2*A2)*math.tan(b2) + C2*A2
    F2 = Qb/Sb
if (N12>0 and N22>0):         #Keep in touch with both
    S = niu*(W*i.z - V*W5)
    Q = N12*math.tan(c1) + N22*math.tan(c2) + C1*A1 + C2*A2
    F2 = Q/S

#Return the result back to php
if(data_li[19] == 0):
    print F1
else:
    print F2