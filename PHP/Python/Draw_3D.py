#coding:utf-8
import numpy as np
import sys, json

def sin(l1,l2):
        return np.sqrt(1-(np.dot(l1,l2)/np.sqrt(np.dot(l1,l1)*np.dot(l2,l2)))**2)

def cos(l1,l2):
        return np.dot(l1,l2)/np.sqrt(np.dot(l1,l1)*np.dot(l2,l2))

def area(a,b,c):
        return abs(0.5*np.sqrt((a-b)[0]**2+(a-b)[1]**2+(a-b)[2]**2)*np.sqrt((a-c)[0]**2+(a-c)[1]**2+(a-c)[2]**2)*sin(a-b,a-c))

def capacity(dot,a,b,c,s):
        return (1.0/3)*np.abs(np.dot(dot,s.n)+s.d)*area(a,b,c)

class face:
 	def __init__(self,qx,qj):
 		self.Qx = qx
 		self.Qj = qj
 		self.n = np.array([-np.cos(qx*np.pi/180)*np.sin(qj*np.pi/180),np.sin(qx*np.pi/180)*np.sin(qj*np.pi/180),np.cos(qj*np.pi/180)],dtype=float)
 		self.d = 0.0

class line:
        def __init__(self,face1,face2):
                self.l = np.cross(face1.n,face2.n)/sin(face1.n,face2.n)

def Hoek(jl1qx,jl1qj,jl2qx,jl2qj,pdmqx,pdmqj,pmqx,pmqj,llfqx,llfqj,hight,length):
        #points
        jl1 = face(jl1qx,jl1qj)
        jl2 = face(jl2qx,jl2qj)
        pdm = face(pdmqx,pdmqj)
        pm = face(pmqx,pmqj)
        llf = face(llfqx,llfqj)
        Hight = hight
        Length = length
        lAB = line(jl1,pm)
        lBE = line(jl1,pdm)
        lAC = line(jl2,pm)
        lBC = line(pm,pdm)
        lAD = line(jl1,jl2)
        lDE = line(jl1,llf)
        lCF = line(jl2,pdm)
        lEF = line(pdm,llf)
        A = np.array([0,0,0],dtype = float)
        B = A + (Hight/lAB.l[2])*lAB.l
        C = A + (sin(lAB.l,lBC.l)/sin(lAC.l,lBC.l))*np.sqrt(B[0]**2+B[1]**2+B[2]**2)*lAC.l
        G = B - (sin(lBC.l,lCF.l)/sin(lBE.l,lCF.l))*np.sqrt((B-C)[0]**2+(B-C)[1]**2+(B-C)[2]**2)*lBE.l
        E = B - Length*(B-G)/np.sqrt((B-G)[0]**2+(B-G)[1]**2+(B-G)[2]**2)
        D = A + (sin(E,lDE.l)/sin(lAD.l,lDE.l))*np.sqrt(E[0]**2+E[1]**2+E[2]**2)*G/np.sqrt(G[0]**2+G[1]**2+G[2]**2)
        F = C - (sin(C-E,lEF.l)/sin(lEF.l,lCF.l))*np.sqrt((C-E)[0]**2+(C-E)[1]**2+(C-E)[2]**2)*(C-G)/np.sqrt((C-G)[0]**2+(C-G)[1]**2+(C-G)[2]**2)
        
        #slope
        K = 2*B-C
        M = 2*C-B
        bottom1 = np.array([np.sin(pm.Qx*np.pi/180),np.cos(pm.Qx*np.pi/180),0],dtype = float)
        bottom2 = np.array([-np.cos(pm.Qx*np.pi/180),np.sin(pm.Qx*np.pi/180),0],dtype = float)
        H = cos(K,bottom1)*np.sqrt(K[0]**2+K[1]**2+K[2]**2)*bottom1
        L = cos(M,bottom1)*np.sqrt(M[0]**2+M[1]**2+M[2]**2)*bottom1
        I = H + np.dot(G,bottom2)*bottom2
        O = L + np.dot(G,bottom2)*bottom2
        pdm.d = -np.dot(B,pdm.n)
        J = np.array([I[0],I[1],(pdm.d+pdm.n[0]*I[0]+pdm.n[1]*I[1])/(-pdm.n[2])],dtype = float)
        N = np.array([O[0],O[1],(pdm.d+pdm.n[0]*O[0]+pdm.n[1]*O[1])/(-pdm.n[2])],dtype = float)
        H = H + bottom1
        L = L - bottom1
        I = I + bottom1 - bottom2
        O = O - bottom1 - bottom2

        # Convert into an list
        Point = [A.tolist(), B.tolist(), C.tolist(), D.tolist(), E.tolist(), F.tolist(), G.tolist(), H.tolist(), I.tolist(), J.tolist(), K.tolist(), L.tolist(), M.tolist(), N.tolist(), O.tolist()]
        return Point

# Load the data that PHP sent us
try:
    data = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

# data = "115.0,45.0,235.0,45.0,195.0,12.0,185.0,65.0,165.0,70.0,30.48,12.19"
#Get the list of the data
data_str = data.split(",")
data_li = [float(x) for x in data_str]

result = Hoek(data_li[0], data_li[1], data_li[2], data_li[3], data_li[4], data_li[5], data_li[6], data_li[7], data_li[8], data_li[9], data_li[10], data_li[11])
print result