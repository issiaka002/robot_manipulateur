# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 18:22:37 2022

@author: SIDIBE ISSIAKA
"""

import Verification as v
import numpy as np

import math
from tkinter import*
import tkinter
import matplotlib
from tkinter.messagebox import *
import time as t
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from random import choice


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#¬from distutils import command
#from turtle import color, right
#from typing import Collection
matplotlib.use("TkAgg")


def round_rectangle(x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)


global L0, L1, L2, theta1, theta2, XB, YB, SO1, CO1, nombre_de_pas, nombre_maxi_pas, X_Pi, Y_Pi,canvas,largeur,hauteur,pointA,absA,ordA,XA0,YA0
X_Pi = []
Y_Pi = []
XA0=0
YA0=0
nombre_de_pas=0



# Fonction MGD
def fonction_MGD():
    
    """DEFINITION DES VALEUR INITIAL"""
    XB,YB = v.lienSaisir(abcisse_de_B), v.lienSaisir(ordonnee_de_B)
    theta1, theta2 = math.radians(v.AngleSaisir(angle_1_field)), math.radians(v.AngleSaisir(angle_2_field))
    L0, L1, L2 = v.lienSaisir(link_zero_field), v.lienSaisir(link_one_field), v.lienSaisir(link_two_field)
    nombre_de_pas = int(v.valeurSaisir(pas_field))
    time=v.valeurSaisir(duration_field)
    
    """DEFINITION DES MATRICES DE PASSAGE"""
    T01 = np.array([[np.cos(theta1),-np.sin(theta1),0,L0],
                    [np.sin(theta1),np.cos(theta1),0,0],
                    [0,0,1,0],
                    [0,0,0,1]])
    T12 = np.array([[np.cos(theta2),-np.sin(theta2),0,L1],
                    [np.sin(theta2),np.cos(theta2),0,0],
                    [0,0,1,0],
                    [0,0,0,1]])
    T02 = T01.dot(T12)
    print(T01)
    print(T12)
    print(T02)
    A2=np.array([[L2],[0],[0],[1]]) 
    A21=np.array([[L1],[0],[0],[1]]) 
    A10=np.array([[L0],[0],[0],[1]]) 
    A0 = T02.dot(A2)
    #Position de A2 dans le R0
    A20 = T01.dot(A21)
    print(A20)
    #Angle de rotation de 0A2
    rotAngle = math.degrees(math.atan2(T02[[1],[0]], T02[[0],[0]]))
    
    #LES MATRICES DE PASSAGE INVERSE
    Mat1T0 = np.array([[math.cos(theta1),math.sin(theta1),0,-L0*math.cos(theta1)],[-math.sin(theta1),math.cos(theta1),0,L0*math.sin(theta1)],[0,0,1,0],[0,0,0,1]])
    T21 = np.array([[math.cos(theta2),math.sin(theta2),0,-L0*math.cos(theta2)],[-math.sin(theta2),math.cos(theta2),0,L1*math.sin(theta2)],[0,0,1,0],[0,0,0,1]])
    return [ L0, A20, A0, L1, L2,nombre_de_pas,YB,XB,time]


def inverse(x,y):
     
    # Cette fonction implémente le modèle géométrique inverse

    L0 = v.lienSaisir(link_zero_field)
    L1 = v.lienSaisir(link_one_field)
    L2 = v.lienSaisir(link_two_field)
    B1 = -2*y*L1
    B2 = 2*L1*(L0-x)
    B3 = L2**2-y**2-(L0-x)**2-L1**2
    teta_1, teta_2, SO1, CO1 = 0, 0, 0, 0
    epsi = 1
    if B3==0 :
        teta_1 = math.degrees(math.atan2(-B2,B1))
    else:
        if ((B1**2+B2**2-B3**2)>=0) :
            SO1 = (B3*B1+epsi*B2*math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
            CO1 = (B3*B2-epsi*B1*math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
            teta_1 = math.degrees(math.atan2(SO1,CO1))
        
    Yn1,Yn2 = L2*SO1, L2*CO1
    if L2!=0 :
        teta_2 = math.degrees(math.atan2(Yn1/L2,Yn2/L2))
    print(teta_1)
    print(teta_2)
    return [teta_1,teta_2]


def dessiner():
    plot.cla()
    result = fonction_MGD()
    L0, A20, A0, YB, XB = result[0], result[1], result[2], result[4], result[5]
    
    #nombre_maxi_pas = result[0]
    plot.set_xlabel('ABSCISSE')
    plot.set_ylabel('ORDONNEE')
    plot.yaxis.set_ticks_position('right')
    plot.set_xticks(range(18))
    plot.set_yticks(range(18))
    plot.set_xlim((15,0))
    plot.set_ylim((0, 15))
    plot.grid(True)
    
    #le sol
    plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=15)
    #base du robot 
    plot.plot([0.5,0.7],[0.0,0.0],"k-",lw=55, c="red")
    
    #lien L0
    plot.plot([0.5,0.5],[0.0,L0],"b-",lw=10, c='red')
    #lien L1
    plot.plot([0.5,A20[1]],[L0,A20[0]],"b-",lw=10, c='red')
    #lien L2
    plot.plot([A20[1],A0[1]],[A20[0],A0[0]],"b-",lw=10, c='red')
    
    #Articulations entre les differents liens
    plot.scatter([0.5], [L0], s =600, color= 'orange')
    plot.scatter([A20[1]], [A20[0]], s =600, color = 'orange')
    
    #la pince (point A)
    plot.scatter([A0[1]], [A0[0]], s =600, color = 'blue', marker="$\cap$")
    #point B
    plot.scatter([YB], [XB], s =800, color = 'red')

    graphe.draw()



def simuler():
    etat_simuler=True
    global X_Pi, Y_Pi
    X_Pi = []
    Y_Pi = []
    result = fonction_MGD()
    nombre_de_pas = result[5]
    L0 = result[0]
    L1 = result[3]
    L2 = result[4]
    YB = result[6]
    A0 = result[2]
    XB = result[7]
    A20 = result[1]
    time=result[8]
    vitesse = float(time/nombre_de_pas)
    for i in range(1,nombre_de_pas+1):

        """On efface le graphe dessiné dans le cavas"""
        plot.cla()
        
        """On redessine le nouveau le meme graphe"""
        plot.set_xlabel('Axe Y0')
        plot.set_ylabel('Axe X0')
        plot.yaxis.set_ticks_position('right')
        plot.set_xticks(range(18))
        plot.set_yticks(range(18))
        plot.set_xlim((15,0))
        plot.set_ylim((0,15))
        plot.grid(True)
        
        """On détermine les coordonnées du point Pk"""
        #Distance dans la direction X
        disXPas = (XB-A0[0])/nombre_de_pas
        if disXPas<0:
            disXPas = np.abs(disXPas)

        #Distance dans la direction Y
        disYPas = (YB-A0[1])/nombre_de_pas
        if disYPas<0:
            disYPas = np.abs(disYPas)
        
        # Coordonnées du point Pk
        if XB>=A0[0] :
            Xi = A0[0]+i*disXPas
        else:
            Xi = A0[0]-i*disXPas

        if YB>A0[1]:
            Yi = A0[1]+i*disYPas
        else:
            Yi = A0[1]-i*disYPas

        # Détermination des variables articulaires théta 1 et théta 2
        theta=inverse(Xi,Yi)
        
        # Coordonnées du point A2
        XA2i =L1*math.cos(math.radians(theta[0]))+L0
        YA2i =L1*math.sin(math.radians(theta[0]))
        
        #Trajectoire
        XA0 = result[2][0]
        XB = result[7]
        YA0 = result[2][1]
        YB = result[6]
        a = (YA0-YB)/(XA0-XB)
        b = YB-a*XB
        x=range(-100,101)
        
        #une droite
        y = a*x + b
        
        #coordonnees des Pi
        X_Pi.append(Xi)
        Y_Pi.append(Yi)
        
        #Les points de deplacement
        for e in range(0,len(X_Pi)):
            plot.scatter([Y_Pi[e]], [X_Pi[e]], color = 'blue', s=30)


        #Point Pi
        plot.scatter([Yi], [Xi], color = 'blue', s=800, marker="$\cap$")
        #Point A0
        plot.scatter([0.5], [L0], s =600, color = 'orange')
        #Point A2
        plot.scatter([YA2i], [XA2i], s =600, color = 'orange')
        
        #tracer L0
        plot.plot([0.5,0.5],[0.0,L0],"b-",lw=11, c="red")
        #tracer L1
        plot.plot([0.5,YA2i],[L0,XA2i],"b-",lw=11, c="red")
        #tracer L2
        plot.plot([YA2i,Yi],[XA2i,Xi],"b-",lw=11, c="red")
        
        
        #Le point de depart (A)
        plot.scatter([A0[1]], [A0[0]], s =300, color = 'blue')
        
        """
        if i!=0:
            #Le point A
            plot.scatter([A0[1]], [A0[0]], s =400, color = 'black')
        else:
            #Le point A
            plot.scatter([A0[1]], [A0[0]], s =600, color = '#FF0000')
         """
         
        if i==nombre_de_pas:
            #Lorsqu'on atteint le point d'arrivé (B)
            plot.scatter([YB], [XB], s =1000, color = 'red')
        else:
            #Le point B
            plot.scatter([YB], [XB], s =190, color = 'blue')
        
       
        #base du robot 
        plot.plot([0.5,0.7],[0.0,0.0],"k-",lw=55, c='red')
        #Le sol
        plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=15)
        
        graphe.draw()
        #Le Bip
        t.sleep(vitesse)
        simulation.update()
    
    frame4=Frame(simulation,bg="#FFFFFF",bd=1,relief=SUNKEN)
    information=Label(frame4,text="Informations de débogage",font=("courrier",10),bg="#808080")
    information.pack(fill=X,ipadx=120)
    largeur=500
    hauteur=225
    canvas=Canvas(frame4,width=largeur,height=hauteur)
    vbar=Scrollbar(frame4,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
        
    canvas.create_text(largeur/2,20,text='Coordonnées du point A')
    canvas.create_text(largeur/2,40,text='('+str(XA0)+','+str(YA0)+')')
    canvas.create_text(largeur/2,60,text='Coordonnées des points Pk')
    for i in range(1,nbrePas+1):
        canvas.create_text(largeur/2,60+20*i,text='('+str(X_Pi[i-1])+','+str(Y_Pi[i-1])+')')
        
    canvas.pack()

    frame4.grid(row=1,column=1,sticky=W,padx=0,pady=0)
    """
    frame_infos=Frame(simulation,bg="#FFFFFF",bd=2,relief=SUNKEN)
    information=Label(frame_infos,text="Infore",font=("courrier",12))
    information.pack(fill=X,ipadx=120)
    largeur=120
    hauteur=70
    canvas=Canvas(frame_infos,width=largeur,height=hauteur, bg="blue")
    vbar=Scrollbar(frame_infos,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
  
    canvas.create_text(50,10,text='Coordonnées du point A', font=('TkMenuFont',15, 'italic'), fill='blue')
    canvas.create_text(largeur/2,40,text='('+str(XA0)+','+str(YA0)+')')
    canvas.create_text(largeur/2,60,text='Coordonnées des points Pk')
    for i in range(1,nombre_de_pas+1):
        canvas.create_text(100,100,text='('+str(X_Pi[i-1])+','+str(Y_Pi[i-1])+')', anchor='nw', font='TkMenuFont', fill='red')
        
    canvas.pack()

    frame_infos.grid(row=1,column=1,sticky=W,padx=0,pady=0)
    """

def demo():
    tableau_valeur =[9,6,6,53,50,1,4,40,3]
    L0, L1, L2 = tableau_valeur[0], tableau_valeur[1], tableau_valeur[2]
    theta1, theta2 =tableau_valeur[3], tableau_valeur[4]
    XB, YB = tableau_valeur[5], tableau_valeur[6]
    
    nombre_de_pas, time = tableau_valeur[7], tableau_valeur[8]
    link_zero_field.delete(0,END)
    link_zero_field.insert(0,L0)
    link_one_field.delete(0,END)
    link_one_field.insert(0,L1)
    link_two_field.delete(0,END)
    link_two_field.insert(0,L2)
    angle_1_field.delete(0,END)
    angle_1_field.insert(0,theta1)
    angle_2_field.delete(0,END)
    angle_2_field.insert(0,theta2)
    abcisse_de_B.delete(0,END)
    abcisse_de_B.insert(0,XB)
    ordonnee_de_B.delete(0,END)
    ordonnee_de_B.insert(0,YB)
    pas_field.delete(0,END)
    pas_field.insert(0,nombre_de_pas)
    duration_field.delete(0,END)
    duration_field.insert(0,time)
    
    dessiner()
    t.sleep(2)
    simuler()

def nouveau():
    link_zero_field.delete(0,END)
    link_one_field.delete(0,END)
    link_two_field.delete(0,END)
    angle_1_field.delete(0,END)
    angle_2_field.delete(0,END)
    abcisse_de_B.delete(0,END)
    ordonnee_de_B.delete(0,END)
    pas_field.delete(0,END)
    duration_field.delete(0,END)
    plot.cla()
    plot.set_xlabel('Axe Y0')
    plot.set_ylabel('Axe X0')
    plot.yaxis.set_ticks_position('right')
    plot.set_xticks(range(18))
    plot.set_yticks(range(18))
    plot.set_xlim((15,0))
    plot.set_ylim((0,15))
    plot.grid(True)
    graphe.draw() 
    frame_infos=Frame(simulation,bg="#FFFFFF",bd=1,relief=SUNKEN)
    information=Label(frame_infos,text="Informations de débogage",font=("courrier",10),bg="#808080")
    information.pack(fill=X,ipadx=120)

    canvas=Canvas(frame_infos,width=500,height=255)
    vbar=Scrollbar(frame_infos,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
    rounded_rect(canvas, 20, 20, 60, 40, 10)
    canvas.pack()
    frame_infos.grid(row=1,column=1,sticky=W,padx=0,pady=0)


def quitter():
    if askyesno('Quitter','Voulez-vous vraiment quitter cette page?'):
        #showwarning('Quitter','Merci à vous')
        simulation.destroy()



"""CREATION DE LA FENETRE DE SIMULATION"""
simulation = tkinter.Tk()
simulation.geometry("1100x700")
simulation.title("Interface de simulation")
simulation.configure(background="#E2F0D9")
simulation.resizable(width=False, height=False)

label_titre =tkinter.Label(simulation, text="ROBOT MANIPULATEUR 2D",justify="center", font="AgencyFB 22 bold underline",background="#E2F0D9", foreground="black")
label_titre.pack(pady=10)

frame_parametre=tkinter.Frame(simulation, width=167, height=600,background="#E2F0D9", border=4, relief="groove")
frame_parametre.place(x=50, y=50)

frame_cote = tkinter.Button(simulation, width=2, height=305, relief="groove", bd=0, bg='blue').place(x=0,y=0)

frame_dessin=tkinter.Frame(simulation, background="white", border=4, relief="groove")
frame_dessin.place(x=226, y=50)

frame_bouton=tkinter.Frame(simulation, width=160, height=460,background="#E2F0D9", border=4, relief="groove")
frame_bouton.place(x=890,y=50)

frame_infos=tkinter.Frame(simulation, width=660, height=130,background="white", border=4, relief="groove")
frame_infos.place(x=222, y=518)

frame_auteur=tkinter.Frame(simulation, width=160, height=190,background="white", border=4, relief="groove")
frame_auteur.place(x=890, y=450)

label_parametres =tkinter.Label(frame_parametre,text="LES PARAMETRES",anchor= 'w',font="AgencyFB 12 bold underline",bg="#E2F0D9",fg="black")
label_parametres.place(x=0,y=0, width=175)

label_liens =tkinter.Label(frame_parametre,text="Variables géométriques",anchor= 'w',font="AgencyFB 8 bold",bg="grey",fg="black")
label_liens.place(x=0,y=30, width=160)

label_lien0 =tkinter.Label(frame_parametre,text="Longueur du lien L0",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_lien0.place(x=0,y=60, width=120)

link_zero_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
link_zero_field.place(x=120, y=60)

label_lien1 =tkinter.Label(frame_parametre,text="Longueur du lien L1",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_lien1.place(x=0,y=90, width=120)

link_one_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
link_one_field.place(x=120, y=90)

label_lien2 =tkinter.Label(frame_parametre,text="Longueur du lien L2",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_lien2.place(x=0,y=120, width=120)

link_two_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
link_two_field.place(x=120, y=120)

label_angles =tkinter.Label(frame_parametre,text="Variables articulaires",anchor= 'w',font="AgencyFB 8 bold",bg="grey",fg="black")
label_angles.place(x=0,y=150, width=160)

label_angle1 =tkinter.Label(frame_parametre,text="Mesure de l'angle θ1",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_angle1.place(x=0,y=180, width=120)

angle_1_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
angle_1_field.place(x=120, y=180)

label_angle2 =tkinter.Label(frame_parametre,text="Mesure de l'angle θ2",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_angle2.place(x=0,y=210, width=120)

angle_2_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
angle_2_field.place(x=120, y=210)

label_pointB =tkinter.Label(frame_parametre,text="Point B à atteindre",anchor= 'w',font="AgencyFB 8 bold",bg="grey",fg="black")
label_pointB.place(x=0,y=240, width=160)

label_abscisseB =tkinter.Label(frame_parametre,text="Ordonnée du point B",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_abscisseB.place(x=0,y=270, width=120)

abcisse_de_B = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
abcisse_de_B.place(x=120, y=270)



label_ordonneeB =tkinter.Label(frame_parametre,text="Abscisse du point B",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_ordonneeB.place(x=0,y=300, width=120)

ordonnee_de_B = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
ordonnee_de_B.place(x=120, y=300)

label_autres =tkinter.Label(frame_parametre,text="Paramètres du mouvement",anchor= 'w',font="AgencyFB 8 bold",bg="grey",fg="black")
label_autres.place(x=0,y=330, width=160)

label_NbPas =tkinter.Label(frame_parametre,text="Nombre de pas ",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_NbPas.place(x=0,y=360, width=120)

pas_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
pas_field.place(x=120, y=360)

label_duree =tkinter.Label(frame_parametre,text="Durée du trajet A-B ",anchor= 'w',font="AgencyFB 8 bold",bg="#E2F0D9",fg="black")
label_duree.place(x=0,y=390, width=120)

duration_field = tkinter.Entry(frame_parametre,bd=1, width=6,font="AgencyFB 8 bold",bg="white", selectbackground="blue",fg="black",justify="left")
duration_field.place(x=120, y=390)

# Interface graphique informations de debogage
label_infos =tkinter.Label(frame_infos,text="Informations de débogage",justify="left",font="AgencyFB 8 bold",bg="grey",fg="black")
label_infos.place(x=0,y=0, width=630)
scroll=tkinter.Scrollbar(frame_infos, orient= "vertical")
scroll.place(x=635, y=3,height=120)


# Interface graphique des boutons
label_bouton =tkinter.Label(frame_bouton,text="Boutons du simulateur",justify="left",font="AgencyFB 8 bold",bg="grey",fg="black")
label_bouton.place(x=0,y=0, width=155)

bouton_demo=tkinter.Button(frame_bouton,text="Demo",font="AgencyFB 10 bold",justify="center",bg="orange",fg="white",width=10,height=1,bd=5,command=demo)
bouton_demo.place(x=30, y=80)

bouton_dessiner=tkinter.Button(frame_bouton,text="Dessiner",font="AgencyFB 10 bold",justify="center",bg="#70AD47",fg="white",width=10,height=1,bd=5,command=dessiner)
bouton_dessiner.place(x=30, y=125)

bouton_simuler=tkinter.Button(frame_bouton,text="Simuler",font="AgencyFB 10 bold",justify="center",bg="#70AD47",fg="white",width=10,height=1,bd=5,command=simuler)
bouton_simuler.place(x=30, y=170)

bouton_nouveau=tkinter.Button(frame_bouton,text="Nouveau",font="AgencyFB 10 bold",justify="center",bg="grey",fg="white",width=10,height=1,bd=5,command=nouveau)
bouton_nouveau.place(x=30, y=215)

bouton_quitter=tkinter.Button(frame_bouton,text="Quitter",font="AgencyFB 10 bold",justify="center",bg="red",fg="white",width=10,height=1,bd=5,command=quitter)
bouton_quitter.place(x=30, y=260)

label_auteur =tkinter.Label(frame_auteur,text="Auteur du simulateur",justify="left",font="AgencyFB 8 bold",bg="grey",fg="black")
label_auteur.place(x=0,y=0, width=155)

"""Contruction d'un canvas"""

canvas =Canvas(frame_dessin,width=500,height=500, bg="blue")
canvas.grid(row=0,column=1)
schema = Figure(figsize=(18.5, 13), dpi=35)
plot = schema.add_subplot(1, 1, 1)
plot.set_xlabel('ABSCISSE')
plot.set_ylabel('ORDONNEE')
plot.yaxis.set_ticks_position('right')
plot.set_xticks(range(22))
plot.set_yticks(range(22))
plot.set_xlim((20,0))
plot.set_ylim((0, 20))
plot.grid(True)

"""
# Partie Auteur du simulateur
frame5=Frame(simulation,bg="#98FB98",bd=1,relief=SUNKEN)
simulateur=tkinter.Label(frame5,text="Auteur du simulateur",font=("courrier",10),bg="#808080")
simulateur.pack(fill=X)

largeur=250
hauteur=225
logo=ImageTk.PhotoImage(Image.open('yaya.jpg'))
canvas=Canvas(frame5,width=largeur,height=hauteur)
canvas.create_image(largeur/2,hauteur/2,image=logo)
canvas.pack()

#frame5.grid(row=1,column=2,sticky=E)

frame.pack(expand=YES)
"""
graphe = FigureCanvasTkAgg(schema, canvas)
graphe.draw()
graphe.get_tk_widget().pack()


def enter(event):
    tof = ['ferrari1.jpg', 'ferrari2.jpg', 'ferrari3.jpg', 'ferrari4.jpeg', 'ferrari5.jpg','ferrari6.jpg']
    load = Image.open(f"{choice(tof)}")
    photo = ImageTk.PhotoImage(load)
    label_image.config(image=photo)
    label_image.image=photo

def out(event):
    tof = ['ferrari1.jpg', 'ferrari2.jpg', 'ferrari3.jpg', 'ferrari4.jpeg', 'ferrari5.jpg','ferrari6.jpg']
    load = Image.open(f"{choice(tof)}")
    photo = ImageTk.PhotoImage(load)
    label_image.config(image=photo)
    label_image.image=photo

load = Image.open("ferrari1.jpg")
#load.show()
photo = ImageTk.PhotoImage(load)
label_image=tkinter.Label(frame_parametre, image=photo)
label_image.place(x=0,y=430)
#label_image.bind("<Enter>", enter)
#label_image.bind("<Leave>", out)
simulation.mainloop()


