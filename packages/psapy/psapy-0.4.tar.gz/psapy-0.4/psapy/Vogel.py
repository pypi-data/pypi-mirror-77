# coding=utf-8
from __future__ import division 
import math
import psapy.FluidProps as FluidProps
import matplotlib.pyplot as plt
  
def Darcy_IPR(k,h,visc, re,rw, s, P, OilFVF, nPoints):
    """Function to calculate IPR using Darcy's Equation.  It returns a list with a pair of Pressure and rates"""
    PwfList=[]
    QList=[]
    QList.append(0)
    PwfList.append(P)

    mStep=P/nPoints
    i=1

    while (i<=nPoints):
        
        Pwf=PwfList[i-1]-mStep
        Q= (k*h/visc)*(P-Pwf)/(141.2*OilFVF*visc*(math.log(re/rw)-0.75+s))
        
        QList.append(Q)
        PwfList.append(Pwf)

        i=i+1

    DarcyList=[QList,PwfList]

    return DarcyList

def VogelIPR(P, Pb, Pwf, Qo, nPoints):
    """Function to calculate IPR using Vogel's Equation.  It returns a list with a pair of Pressure and rates"""
    
    PwfList=[]
    QList=[]
    QList.append(0)
    PwfList.append(P)
    VogelList=[]
    mStep=P/nPoints
    i=1

    if Pwf>=Pb:
        J=Qo/(P-Pwf)
       
    else:
        J=Qo/((P-Pb)+((Pb/1.8)*(1-0.2*(Pwf/Pb)-0.8*(Pwf/Pb)**2)))

    while (i<=nPoints):
                     
        Pwfs=PwfList[i-1]-mStep
        
        if Pwfs>=Pb:
           
            Q=J*(P-Pwfs)
        else:
            
            Qb=J*(P-Pb)
            Q=Qb+(J*Pb/1.8)*(1-0.2*(Pwfs/Pb)-0.8*(Pwfs/Pb)**2)
       

        QList.append(Q)
        PwfList.append(Pwfs)

        i=i+1

    VogelList=[QList,PwfList]

    return VogelList

def Vogel_DarcyIPR(P, k,h,visc, re,rw, s, OilFVF,Temp, Pb, nPoints):
    """Function to calculate IPR using Vogel's Equation.  It returns a list with a pair of Pressure and rates"""
    
    PwfList=[]
    QList=[]
    QList.append(0)
    PwfList.append(P)
    VogelList=[]
    mStep=P/nPoints
    i=1

    
    J= (k*h/visc)/(141.2*OilFVF*visc*(math.log(re/rw)-0.75+s))
              

    while (i<=nPoints):
                     
        Pwfs=PwfList[i-1]-mStep

        
        if Pwfs>=Pb:
            Q=J*(P-Pwfs)
      
        else:
            
            Qb=J*(P-Pb)
            Q=Qb+(J*Pb/1.8)*(1-0.2*(Pwfs/Pb)-0.8*(Pwfs/Pb)**2)
       

        QList.append(Q)
        PwfList.append(Pwfs)

        i=i+1

    VogelList=[QList,PwfList]
    return VogelList

