import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

T=int(input("Enter the Simulation Time in Hours "))
n=int(input("Enter the Number of users "))
tilt=int(input("Enter the tilt angle "))
H_b=50
H_m=1
Tx_p=43
Loss=1
G=14.8
F_MHZ=800
EIRP_bore=Tx_p+G-Loss
d_ortho=15
L=2 #CALLS PER HOUR
D=1/3600 #STEP SIZE
P=L*D #PROBABILITY THAT USER ATTEMPT A CALL
CH={1:15,2:15} #NO OF CHANNELS IN EACH BS
T_set={} #SET UP TIME
c_dict={} #Call duration
d_dict={} #User distribution along the road
HO=-3 #Hand-off value
NH={1:0,2:0} # No of hand-off attempt in BS1 &2 
NSH={1:0,2:0} #No of successful handoff in BS1 &2
NFH={1:0,2:0} #No of faliure handoff in BS1 &2
Nsc={1:0,2:0} #No of successful call in BS1 &2
CDS={1:0,2:0}#call drop due to signal strength on BS1&2                     
Nbc={1:0,2:0} #No of blocked calls
NDC={1:0,2:0} #No of dropped calls 
NCA={1:0,2:0} #No of Call attempts 
CDC={1:0,2:0} #No of Call drop due to capacity
di={}
BS={}
U_con=[]
R_T=-100
SNR=[]
RSL_T=-100
v_dict={}
U_noc=[]
d_list=[]
RSL_1=0
RSL_2=0
TR=[]
Total_T=T*3600
U_list=list(range(1,n+1)) #users initialzation 


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

s1=sha(2,2)#Shadowing for BS1
s2=sha(2,2)#Shadowing for BS2   


def RSL(di_1,BS):
    gamma1=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt((di_1**2)+(d_ortho**2))))
    RSL_1=(EIRP_bore-EIRP(gamma1,tilt))-prop(800,50,np.sqrt((di_1**2)+(d_ortho**2))/1000)+s1[int((di_1-1)/20)]+fad(1,10)
    gamma2=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt(((6000-di_1)**2)+(d_ortho**2))))
    RSL_2=(EIRP_bore-EIRP(gamma2,tilt))-prop(800,50,np.sqrt((6000-di_1)**2+(d_ortho)**2)/1000)+s2[int((6000-di_1-1)/20)]+fad(1,10)
    if BS == 1:
        RSL_S=RSL_1
        RSL_O=RSL_2
    elif BS == 2:
        RSL_O=RSL_1
        RSL_S=RSL_2
    return RSL_S,RSL_O


for count in range(Total_T):#Start the simulation with step size= 1sec
    for j in U_con: # Monitoring Other users
        C_T = c_dict[j]+T_set[j] # Time elapsed=call duration + call setup
        d_T=d_dict[j]+(di[j]*(v_dict[j]*(count-T_set[j])))
        if count>=C_T or (d_T<0 or d_T>6000):# Checking if user successfully end the call.
            Nsc[BS[j]]= Nsc[BS[j]]+1
            CH[BS[j]]=CH[BS[j]]+1
            U_noc.append(j)
            di.pop(j,None)
            c_dict.pop(j,None)
            v_dict.pop(j,None)
            d_dict.pop(j,None)
            BS.pop(j,None)
        else:
            if BS[j]==1:
                RSL_1, RSL_2 = RSL(d_T,BS[j])
                SNR=((RSL_1-RSL_2),d_T,BS[j]) #save SNR in a list
                TR.append(SNR)
                if  RSL_1<RSL_T:
                    CDS[1]=CDS[1]+1
                    CH[1]=CH[1]+1
                    U_noc.append(j)
                    di.pop(j,None)
                    c_dict.pop(j,None)
                    v_dict.pop(j,None)
                    d_dict.pop(j,None)
                    BS.pop(j,None)
                    
                else:
                    if RSL_2 > RSL_1+HO:
                        NH[1]=NH[1]+1 #increase handoff Attempt value in BS 1/2
                        if CH[2]>0 :
                            NSH[1]=NSH[1]+1 # increase handoff Attempt value in BS 1
                            BS[j]=2
                            CH[1]=CH[1]+1
                            CH[2]=CH[2]-1
                        else:
                            NFH[1]=NFH[1]+1
                            
            else:
                 RSL_2, RSL_1= RSL(d_T,BS[j])
                 SNR=((RSL_2-RSL_1),d_T,BS[j]) #save SNR in a list
                 TR.append(SNR)
                 if  RSL_2<RSL_T:
                     CDS[BS[j]]=CDS[BS[j]]+1
                     CH[BS[j]]=CH[BS[j]]+1
                     U_noc.append(j)
                     di.pop(j,None)
                     c_dict.pop(j,None)
                     v_dict.pop(j,None)
                     d_dict.pop(j,None)
                     BS.pop(j,None)
                 else:
                     if RSL_1 > RSL_2+HO:# create debug file
                         NH[2]=NH[2]+1 #increase handoff Attempt value in BS 1/2
                         if CH[1]>0:
                             NSH[2]=NSH[2]+1 # increase handoff Attempt value in BS 2
                             BS[j]=1
                             CH[2]=CH[2]+1
                             CH[1]=CH[1]-1
                         else:
                             NFH[2]=NFH[2]+1
                             

    U_temp  = []
    for i in U_list:
        if np.random.uniform(0, 1) > P:
            continue
        else:
            d_dict[i]=np.random.uniform(0,6000) #determine user location along the road
            if d_dict[i]>3000:
                di[i]=-1
            else:
                di[i]=1    
            gamma1=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt((d_dict[i]**2)+(d_ortho**2))))
            RSL_1=(EIRP_bore-EIRP(gamma1,tilt))-prop(800,50,np.sqrt((d_dict[i]**2)+(d_ortho**2))/1000)+s1[int((d_dict[i]-1)/20)]+fad(1,10)
            gamma2=np.rad2deg(np.arctan((H_b-H_m)/np.sqrt(((6000-d_dict[i])**2)+(d_ortho**2))))
            RSL_2=(EIRP_bore-EIRP(gamma2,tilt))-prop(800,50,np.sqrt((6000-d_dict[i])**2+(d_ortho)**2)/1000)+s2[int((6000-d_dict[i]-1)/20)]+fad(1,10)
            if RSL_1 >RSL_2: # Comparing RSL values
                if RSL_1>R_T: # Comparing with threshold
                    NCA[1]=NCA[1]+1 #No of call attempts
                    if CH[1]>0 :
                        T_set[i]=count
                        c_dict[i]=np.random.exponential(180) #call duration
                        v_dict[i]=np.random.normal(12,3) #determine user speed
                        U_temp.append(i) #appending active users
                        CH[1]=CH[1]-1
                        BS[i]= 1
                        #TR[i]=[c_dict[i],BS[i],di[i],v_dict[i]]
                    else:
                        Nbc[1]=Nbc[1]+1 #Blocked call due to BS-1
                        if RSL_2>R_T:
                            if CH[2]>0:
                                T_set[i]=count
                                c_dict[i]=np.random.exponential(180)
                                v_dict[i]=np.random.normal(12,3)
                                BS[i]= 2 #"BS-2"
                                U_temp.append(i) #appending active users
                                CH[2]=CH[2]-1
                            else:
                                CDC[1]= CDC[1]+1 #call drop due to capacity
                        
                                
                else:
                    CDS[1]=CDS[1]+1 #call drop due to signal strength 
                
            else:
                if RSL_2>R_T:
                    NCA[2]=NCA[2]+1 #Call Attempt value is increased 
                    if CH[2]>0:
                        T_set[i]=count
                        c_dict[i]=np.random.exponential(180)
                        v_dict[i]=np.random.normal(12,3)
                        BS[i]=2 #"BS-2"
                        U_temp.append(i) #appending active users
                        CH[2]=CH[2]-1

                    else:
                        Nbc[2]= Nbc[2]+1 #Blocked call due to BS-2
                        if RSL_1>R_T:
                            if CH[1]>0:
                                T_set[i]=count
                                c_dict[i]=np.random.exponential(180)
                                v_dict[i]=np.random.normal(12,3)
                                BS[i]=1 #"BS-1"
                                U_temp.append(i) #appending active users
                                CH[1]=CH[1]-1
                            else:
                                CDC[2]= CDC[2]+1 #call drop due to capacity
                                                    
                else:
                   CDS[2]=CDS[2]+1 #call drop due to signal strength 
    
    #UPDATING LISTS FOR EVERY COUNTER TO TRACK USERS WHO ARE CONNECTED AND DISCONNECTED 
    U_con=list(set(U_con)-set(U_noc))
    U_list=list(set(U_list)-set(U_temp)) + U_noc
    U_con=U_con + U_temp
    U_noc=[]
    
    for j in range(1,T+1,1): #CODE TO SIMULATE RESULTS FOR EVERY 1 HOUR OF TOTAL SIMULATION TIME
        if count==(j*3600)-1:
            print("\n")
            table = [['No of channels currently in use', 15-CH[1], 15-CH[2]], ['No of call attempts', NCA[1], NCA[2]], ["No of successful calls",Nsc[1], Nsc[2]],["No of successful handoffs",NSH[1],NSH[2]],["No of handoff faliures ", NFH[1],NFH[2]],["No of call drop due to signal strength",CDS[1],CDS[2]],["No of call drop due to capacity",CDC[1],CDC[2]],["No of blocked calls due to capacity", Nbc[1],Nbc[2]]]
            df = pd.DataFrame(table, columns = ["STATISTICS FOR {} HOUR OF SIMULATION TIME IS".format(j), 'BS-1', 'BS-2'],)
            print(df)
       
#PLOTTING GRAPGS OF SNR COUNT ALONG THE ROAD   
S=[]
N_1=[0]*60
N_2=[0]*60
N_3=[0]*60
N_4=[0]*60
N_5=[0]*60
N_6=[0]*60
for k in range(len(TR)):
    i=int(TR[k][1]/100)
    if TR[k][2]==1:
        if TR[k][0]<5:
            N_1[i]=N_1[i]+1
        elif TR[k][0]>=5 and TR[k][0]<10:
            N_2[i]=N_2[i]+1
        else:
            N_3[i]=N_3[i]+1
    else:
        if TR[k][0]<5:
            N_4[i]=N_4[i]+1
        elif TR[k][0]>=5 and TR[k][0]<10:
            N_5[i]=N_5[i]+1
        else:
            N_6[i]=N_6[i]+1

X = np.arange(100,6001,100)
fig = plt.figure()
fig1 = plt.figure()
ax = fig.add_axes([0,0,1,1])
ay = fig1.add_axes([0,0,1,1])
ax.bar(X + 0, N_1, color = 'r', label='SNR<5dB',width = 25)
ax.bar(X + 25, N_2, color = 'm',label='5dB<SNR<10dB', width = 25)
ax.bar(X + 50, N_3, color = 'g', label='SNR>10dB',width = 25)
ax.set_xlabel('Distance')
ax.set_ylabel('Count')
ax.set_title('SNR Count along the road')
ay.bar(X + 0, N_4, color = 'r',label='SNR<5dB', width = 25)
ay.bar(X + 25, N_5, color = 'm',label='5dB<SNR<10dB',width = 25)
ay.bar(X + 50, N_6, color = 'g',  label='SNR>10dB',width = 25)
ay.set_xlabel('Distance')
ay.set_ylabel('Count')
ay.set_title('SNR Count along the road')
ax.legend()
ay.legend()
plt.show()



       
   
   