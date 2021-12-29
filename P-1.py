import matplotlib.pyplot as plt
import numpy as np


H_b=50
H_m=1
Tx_p=43
Loss=1
G=14.8
F_MHZ=800
EIRP_bore=Tx_p+G-Loss
d_ortho=15
alpha=[0,2,5,10]
i=0 #Index for shadowing array
c={0:'b',2:'r',5:'g',10:'c'} #Dictionary for Color in graph

#Accessing data from Vertical_pattern text file
newDict = {}
with open('vertical_pattern.txt', 'r') as f:
    for line in f:
        splitLine = line.split()
        newDict[float(splitLine[0])] = float(splitLine[1])
        

def prop(F_MHZ,H_b,di):
    Ok_hata=(26.16*np.log10(F_MHZ))-(13.82*np.log10(H_b))+(44.9-(6.55*np.log10(H_b)))*np.log10(di)+69.55+(1.56*np.log10(F_MHZ)-0.8)-(1.1*np.log10(F_MHZ)-0.7)*H_m
    return Ok_hata
def sha(mu,sigma):
    s= np.random.normal(mu,sigma,300)
    return s
def fad(sigma,n):
    f=np.random.rayleigh(sigma,n)
    f_db=10*(np.log10(f*f))
    f_db.sort()
    return f_db[1]

def EIRP(gamma,alpha):
    x=gamma-alpha
    if x<0:
        x=360+x
        x1=float(int(x))
        x2=float(int(x)+1)
        if x2==360:
            y1=(newDict[x1])
            y2=(newDict[0])
        else:
            y1=(newDict[x1])
            y2=(newDict[x2])
            
    else:
        x1=float(int(x))
        x2=float(int(x)+1)
        if x2==360:
            y1=(newDict[x1])
            y2=(newDict[0])
        else:
            y1=(newDict[x1])
            y2=(newDict[x2])
    y=(x-x1)*y2+(x2-x)*y1
    return y
#EIPR at Boresight-PL for base station 1
plt.figure(0)
di_1=np.linspace(0,6000,6001)
y1=EIRP_bore-prop(800,50,np.sqrt((di_1**2)+(d_ortho**2))/1000)
plt.plot(di_1,y1,label="1.EIRP_Bore-PL")

#EIPR in the direction of the mobile -PL for different alpha values of base station 1
for tilt in alpha:
    y2=[]
    for di_1 in range(0,6001,1):
        gamma=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt((di_1**2)+(d_ortho**2))))
        y2.append((EIRP_bore-EIRP(gamma,tilt))-prop(800,50,np.sqrt((di_1**2)+(d_ortho**2))/1000))
    plt.plot(range(0,6001,1),y2,c[tilt],label="{}.EIRP-PL at alpha={}".format((alpha.index(tilt)+1+1),tilt))
plt.xlabel('Distance')  
plt.ylabel('RSL(DBm)')
plt.title('RSL with out fading and shadowing for 1st Basestation')
plt.legend(loc= 'upper right')

#EIPR at Boresight-PL for base station 2
plt.figure(1)
di_2=np.linspace(6000,-1,6001)
y3=EIRP_bore-prop(800,50,np.sqrt((di_2**2)+(d_ortho**2))/1000)
plt.plot(range(0,6001,1),y3,label="1.EIRP_Bore-PL")

#EIPR in the direction of the mobile -PL for different alpha values of base station 2
for tilt in alpha:
    y4=[]
    for di_2 in range(6000,-1,-1):
        gamma=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt((di_2**2)+(d_ortho**2))))
        y4.append((EIRP_bore-EIRP(gamma,tilt))-prop(800,50,np.sqrt((di_2**2)+(d_ortho**2))/1000))
    plt.plot(range(0,6001,1),y4,c[tilt],label="{}.EIRP-PL at alpha={}".format((alpha.index(tilt)+1+1),tilt))
plt.xlabel('Distance')  
plt.ylabel('RSL(DBm)')
plt.title('RSL with out fading and shadowing for 2nd Basestation')
plt.legend(loc= 'upper right')

#EIPR in the direction of the mobile -PL for alpha=2 degrees of base station 1 and 2            
plt.figure(2)             
y5=[]
y6=[]
y7=[]
y8=[]
for  di in range(0,6001,1):
    tilt=2
    gamma1=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt((di**2)+(d_ortho**2))))
    gamma2=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt(((6000-di)**2)+(d_ortho**2))))
    y5.append((EIRP_bore-EIRP(gamma1,tilt))-prop(800,50,np.sqrt((di**2)+(d_ortho**2))/1000))
    y6.append((EIRP_bore-EIRP(gamma2,tilt))-prop(800,50,np.sqrt(((6000-di)**2)+(d_ortho**2))/1000))


#RSL including shadowing and fading for alpha=2 degrees of base station 1 and 2  
s1=sha(2,2)#Shadowing for BS1
s2=sha(2,2)#Shadowing for BS2
for  i in y5:
    j=int(y5.index(i)/20)
    if j == 300:
        j = 299
    y7.append(i+s1[j]+fad(1,10))
for  i in y6:
    j=int(y6.index(i)/20)
    if j == 300:
        j = 299
    y8.append(i+s2[j]+fad(1,10))
    
plt.plot(range(0,6001,1),y7,'r',label="EIRP_moblie-PL for 1nd base station")
plt.plot(range(0,6001,1),y8,'b',label="EIRP_moblie-PL for 2st base station")
plt.plot(range(0,6001,1),y5,'y',label="RSL for 1st base station")
plt.plot(range(0,6001,1),y6,'g',label="RSL for 2nd base station")

plt.xlabel('Distance')  
plt.ylabel('RSL(DBm)')
plt.title('RSL with fading and shadowing for 1st & 2nd Basestation')
plt.legend(loc= 'upper right')
plt.show()

        

        
    
