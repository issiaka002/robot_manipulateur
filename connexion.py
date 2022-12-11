# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 18:22:37 2022

@author: SIDIBE ISSIAKA
"""



# -*- coding: utf-8 -*-
import tkinter as tk
import numpy as np
from tkinter.messagebox import *
import matplotlib.pyplot as plt
import math
import sqlite3 as q3



from distutils import command
from tkinter import*
from turtle import color, right
from typing import Collection
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

###################################################################################


global L0, L1, L2, O1, O2, XB, YB, SO1, CO1, nbrePas, nbreMaxPas, X_Pi, Y_Pi,canvas,largeur,hauteur,pointA,absA,ordA,XA0,YA0
X_Pi = []
Y_Pi = []
XA0=0
YA0=0
nbrePas=0



def verifSaisieInt(valeur):
    try:
        f =int(valeur)
        return True
    except:
        return False

def verifSaisieFloat(valeur):
    try:
        f =float(valeur)
        return True
    except:
        return False

def recupValeurLien(case):
    if (verifSaisieFloat(case.get())==True):
        return float(case.get())
    else:
        case.delete(0,END)
        case.insert(0,"3")
        return 3

def recupValeurAngle(angle):
    if (verifSaisieFloat(angle.get())==True):
        return float(angle.get())
    else:
        angle.delete(0,END)
        angle.insert(0,"30")
        return 30

def recupValeur(txt):
    if (verifSaisieInt(txt.get())==True):
        return int(txt.get())
    else:
        txt.delete(0,END)
        txt.insert(0,"2")
        return 2

# Fonction MGD
def calcul():
    
    L0 = recupValeurLien(link_zero_field)
    L1 = recupValeurLien(link_one_field)
    L2 = recupValeurLien(link_two_field)
    O1 = math.radians(recupValeurAngle(angle_1_field))
    O2 = math.radians(recupValeurAngle(angle_2_field))
    nbrePas = int(recupValeur(pas_field))
    YB = recupValeurLien(ordonnee_de_B)
    XB = recupValeurLien(abcisse_de_B)
    temps=recupValeur(duration_field)
    #LES MATRICES DE PASSAGE DIRECTE
    Mat0T1 = np.array([[math.cos(O1),-math.sin(O1),0,L0],[math.sin(O1),math.cos(O1),0,0],[0,0,1,0],[0,0,0,1]])
    Mat1T2 = np.array([[math.cos(O2),-math.sin(O2),0,L1],[math.sin(O2),math.cos(O2),0,0],[0,0,1,0],[0,0,0,1]])
    Mat0T2 = Mat0T1.dot(Mat1T2)
    print(Mat0T1)
    A2=np.array([[L2],[0],[0],[1]]) 
    A21=np.array([[L1],[0],[0],[1]]) 
    A10=np.array([[L0],[0],[0],[1]]) 
    A0 = Mat0T2.dot(A2)
    #Position de A2 dans le R0
    A20 = Mat0T1.dot(A21)
    print(A20)
    #Angle de rotation de 0A2
    rotAngle = math.degrees(math.atan2(Mat0T2[[1],[0]], Mat0T2[[0],[0]]))
    #LES MATRICES DE PASSAGE INVERSE
    Mat1T0 = np.array([[math.cos(O1),math.sin(O1),0,-L0*math.cos(O1)],[-math.sin(O1),math.cos(O1),0,L0*math.sin(O1)],[0,0,1,0],[0,0,0,1]])
    Mat2T1 = np.array([[math.cos(O2),math.sin(O2),0,-L0*math.cos(O2)],[-math.sin(O2),math.cos(O2),0,L1*math.sin(O2)],[0,0,1,0],[0,0,0,1]])
    #txtXA.insert(0,float(A0[1]))
    #txtYA.insert(0,float(A0[0]))
    return [ L0, A20, A0, L1, L2,nbrePas,YB,XB,temps]


def inverse(x,y):
     
    # Cette fonction implémente le modèle géométrique inverse

    L0 = recupValeurLien(link_zero_field)
    L1 = recupValeurLien(link_one_field)
    L2 = recupValeurLien(link_two_field)
    B1 = -2*y*L1
    B2 = 2*L1*(L0-x)
    B3 = L2**2-y**2-(L0-x)**2-L1**2
    teta_1=0
    teta_2=0
    SO1 = 0
    CO1 = 0
    epsi = 1
    if B3==0 :
        teta_1 = math.degrees(math.atan2(-B2,B1))
    else:
        if ((B1**2+B2**2-B3**2)>=0) :
            SO1 = (B3*B1+epsi*B2*math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
            CO1 = (B3*B2-epsi*B1*math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
            teta_1 = math.degrees(math.atan2(SO1,CO1))
        
    Yn1 = L2*SO1
    Yn2 = L2*CO1
    if L2!=0 :
        teta_2 = math.degrees(math.atan2(Yn1/L2,Yn2/L2))
    print(teta_1)
    print(teta_2)

    return [teta_1,teta_2]

def dessiner():
    plot.cla()

    result = calcul()
    L0 = result[0]
    A20 = result[1]
    A0 = result[2]
    #YB = result[4]
    #XB = result[5]
    #nbreMaxPas = result[0]
    plot.set_xlabel('Axe Y0')
    plot.set_ylabel('Axe X0')
    plot.yaxis.set_ticks_position('right')
    plot.set_xticks(range(10))
    plot.set_yticks(range(10))
    plot.set_xlim((9,0))
    plot.set_ylim((0, 9))
    plot.grid(True)

    #tracer L0
    plot.plot([0.5,0.5],[0.0,L0],"b-",lw=7)
    #tracer L1
    plot.plot([0.5,A20[1]],[L0,A20[0]],"b-",lw=7)
    #tracer L2
    plot.plot([A20[1],A0[1]],[A20[0],A0[0]],"b-",lw=7)
    #Le point A
    plot.scatter([A0[1]], [A0[0]], s =500, color = 'red')
    #Le point B
    #plot.scatter([YB], [XB], s =500, color = 'red')
    #Les Articulations
    plot.scatter([0.5], [L0], s =500, color = 'orange')
    plot.scatter([A20[1]], [A20[0]], s =500, color = 'orange')
    #La base et le sol
    plot.plot([0.5,0.7],[0.0,0.0],"k-",lw=10)
    plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=3)
    graphique.draw()

def simuler():
    etat_simuler=True
    global X_Pi, Y_Pi
    X_Pi = []
    Y_Pi = []
    result = calcul()
    nbrePas = result[5]
    L0 = result[0]
    L1 = result[3]
    L2 = result[4]
    YB = result[6]
    A0 = result[2]
    XB = result[7]
    A20 = result[1]
    temps=result[8]
    vitesse = float(temps/nbrePas)
    for i in range(1,nbrePas+1):

        # On efface le graphe dessiné dans le cavas puis 
        # on redessine le nouveau graphe avec les mêmes 
        # caracteristiques.

        plot.cla()
        
        plot.set_xlabel('Axe Y0')
        plot.set_ylabel('Axe X0')
        plot.yaxis.set_ticks_position('right')
        plot.set_xticks(range(10))
        plot.set_yticks(range(10))
        plot.set_xlim((9,0))
        plot.set_ylim((0,9))
        plot.grid(True)
        
        # On détermine les coordonnées du point Pk

        #Distance dans la direction X
        disXPas = (XB-A0[0])/nbrePas
        if disXPas<0:
            disXPas = -disXPas

        #Distance dans la direction Y
        disYPas = (YB-A0[1])/nbrePas
        if disYPas<0:
            disYPas = -disYPas
        
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
        y = a*x + b
         #Trace la droite
        plot.plot([YB,YA0],[XB,XA0],lw=5)
        
        #Droite entre A et Pi
        plot.plot([A0[1],Yi],[A0[0],Xi],"y-",lw=5)
        #sauvegarde les coordonnees des Pi
        X_Pi.append(Xi)
        Y_Pi.append(Yi)
        
        #Les Pas
        
        for j in range(0,len(X_Pi)) :
            plot.scatter([Y_Pi[j]], [X_Pi[j]], color = '#FF00CC')

        #tracer L0
        plot.plot([0.5,0.5],[0.0,L0],"b-",lw=7)
        #tracer L1
        plot.plot([0.5,YA2i],[L0,XA2i],"b-",lw=7)
        #tracer L2
        plot.plot([YA2i,Yi],[XA2i,Xi],"b-",lw=7)
        #Point Pi
        plot.scatter([Yi], [Xi], color = '#FF0000')
        #Point A0
        plot.scatter([0.5], [L0], s =500, color = 'black')
        #Point A2
        plot.scatter([YA2i], [XA2i], s =500, color = 'black')
        if i!=0:
            #Le point A
            plot.scatter([A0[1]], [A0[0]], s =100, color = '#006633')
        else:
            #Le point A
            plot.scatter([A0[1]], [A0[0]], s =500, color = '#FF0000')
            
        if i==nbrePas:
            #Le point B
            plot.scatter([YB], [XB], s =300, color = '#FF0000')
        else:
            #Le point B
            plot.scatter([YB], [XB], s =300, color = '#00FF33')
        
        #Le sol
        plot.plot([0.5,0.7],[0.0,0.0],"k-",lw=10)
        plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=3)
        
        graphique.draw()

        #Le Bip
        winsound.Beep(200, 250)
        time.sleep(vitesse)
        fen_simulation.update()
    
    frame_infos=Frame(fen_simulation,bg="#FFFFFF",bd=1,relief=SUNKEN)
    information=Label(frame_infos,text="Informations de débogage",font=("courrier",10),bg="#808080")
    information.pack(fill=X,ipadx=120)
    largeur=500
    hauteur=225
    canvas=Canvas(frame_infos,width=largeur,height=hauteur)
    vbar=Scrollbar(frame_infos,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
        
    canvas.create_text(largeur/2,20,text='Coordonnées du point A')
    canvas.create_text(largeur/2,40,text='('+str(XA0)+','+str(YA0)+')')
    canvas.create_text(largeur/2,60,text='Coordonnées des points Pk')
    for i in range(1,nbrePas+1):
        canvas.create_text(largeur/2,60+20*i,text='('+str(X_Pi[i-1])+','+str(Y_Pi[i-1])+')')
        
    canvas.pack()

    frame_infos.grid(row=1,column=1,sticky=W,padx=0,pady=0)


def demo():

    result =[3.5,3,3,55,75,0,1,10,5]
    nbrePas = result[7]
    L0 = result[0]
    L1 = result[1]
    L2 = result[2]
    YB = result[6]
    XB = result[5]
    O1=result[3]
    O2=result[4]
    temps=result[8]
    link_zero_field.delete(0,END)
    link_zero_field.insert(0,L0)
    link_one_field.delete(0,END)
    link_one_field.insert(0,L1)
    link_two_field.delete(0,END)
    link_two_field.insert(0,L2)
    angle_1_field.delete(0,END)
    angle_1_field.insert(0,O1)
    angle_2_field.delete(0,END)
    angle_2_field.insert(0,O2)
    abcisse_de_B.delete(0,END)
    abcisse_de_B.insert(0,XB)
    ordonnee_de_B.delete(0,END)
    ordonnee_de_B.insert(0,YB)
    pas_field.delete(0,END)
    pas_field.insert(0,nbrePas)
    duration_field.delete(0,END)
    duration_field.insert(0,temps)

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
    plot.set_xticks(range(10))
    plot.set_yticks(range(10))
    plot.set_xlim((9,0))
    plot.set_ylim((0,9))
    plot.grid(True)
    graphique.draw()
    
    frame_infos=Frame(fen_simulation,bg="#FFFFFF",bd=1,relief=SUNKEN)
    information=Label(frame_infos,text="Informations de débogage",font=("courrier",10),bg="#808080")
    information.pack(fill=X,ipadx=120)

    largeur=500
    hauteur=225
    canvas=Canvas(frame_infos,width=largeur,height=hauteur)
    vbar=Scrollbar(frame_infos,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)

    canvas.pack()


    frame_infos.grid(row=1,column=1,sticky=W,padx=0,pady=0)




###################################################################################
#LES FONCTIONS
def test():
    mdp=entry_pwd.get()
    nom=entry_pseudo.get()
    pseudo=(f'{nom}',)
    if (entry_pseudo.get() == "" or mdp ==""):
        showerror('error', "les champs doivent etre completé !!!")
    else:
        connection = q3.connect("essai_baseDD.db")
        curseur = connection.cursor()
        curseur.execute('SELECT * FROM si_users WHERE nom= ?',pseudo)
        result = curseur.fetchone()[2]
        
        if result == mdp: #si le mot de passe entré correspond au mot de passe enregistré dans la base de donnée
            #Ouverture de la fenetre de simulation
            simulation = tk.Tk()
            simulation.geometry('650x550')
            simulation.title("Interface de simulation")
            simulation.config(bg="#E2F0D9")
            simulation.resizable(width="false", height="false")

            #Etap 2: organisation et placement des widgets
            label_titre = tk.Label(simulation, text="ROBOT MANIPULATION 2D", justify="center", font="AgencyFB 16 bold", bg="#E2F0D9", fg="black")
            label_titre.pack(pady=10)

            frame_parametre= tk.Frame(simulation,bg="#E2F0D9",width=165, height=425, bd=2, relief="groove" )
            frame_parametre.place(x=0, y=50)

            frame_dessin = tk.Frame(simulation, width=265, height=255, bg="white", bd=2, relief="groove")
            frame_dessin.place(x=170,y=50)

            frame_bouton = tk.Frame(simulation, width=160, height=255, bg="#E2F0D9", bd=2, relief="groove")
            frame_bouton.place(x=440,y=50)

            frame_infos = tk.Frame(simulation, width=265, height=165, bg="white", bd=2, relief="groove")
            frame_infos.place(x=170, y=310)

            frame_auteur = tk.Frame(simulation, width=160, height=165, bg="white", border=2, relief="groove")
            frame_auteur.place(x=440, y=310)

            #Etape3: elaboration et placement des widgets
            label_parametre = tk.Label(frame_parametre, text="LES PARAMETRES", anchor='w', font="AgencyFB 12 bold", bg="#E2F0D9", fg="black")
            label_parametre.place(x=0, y=0,width=160)

            label_liens = tk.Label(frame_parametre, text="Variable géometriques", anchor='w', font="AgencyFB 8 bold", bg="grey", fg="black")
            label_liens.place(x=0, y=30, width=160)

            label_lien0 = tk.Label(frame_parametre, text="Longueur du lien L0", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_lien0.place(x=0, y=60, width=120)
            saisie_lien0 = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg ="#E2F0D9", fg="black", justify="left")
            saisie_lien0.place(x=120, y=60)

            label_lien1 = tk.Label(frame_parametre, text="Longueur du lien L1", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_lien1.place(x=0, y=90, width=120)
            saisie_lien1 = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg ="#E2F0D9", fg="black", justify="left")
            saisie_lien1.place(x=120, y=90)

            label_lien2 = tk.Label(frame_parametre, text="Longueur du lien L2", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_lien2.place(x=0, y=120, width=120)
            saisie_lien2 = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg ="#E2F0D9", fg="black", justify="left")
            saisie_lien2.place(x=120, y=120)


            label_angles = tk.Label(frame_parametre, text="Variable articulaires", anchor='w', font="AgencyFB 8 bold", bg="grey", fg="black")
            label_angles.place(x=0, y=150, width=160)

            label_angle1 = tk.Label(frame_parametre, text="Mesure de l'angle O1", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_angle1.place(x=0, y=180, width=120)
            saisie_angle1 = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg="white", selectbackground="blue", fg="black", justify="left")
            saisie_angle1.place(x=120, y=180)

            label_angle2 = tk.Label(frame_parametre, text="Mesure de l'angle O2", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_angle2.place(x=0, y=210, width=120)
            saisie_angle2 = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg="white", selectbackground="blue", fg="black", justify="left")
            saisie_angle2.place(x=120, y=210)

            label_pointB = tk.Label(frame_parametre, text="Point B à atteindre", anchor='w', font="AgencyFB 8 bold", bg="grey", fg="black")
            label_pointB.place(x=0, y=240, width=160)

            label_abscisseB = tk.Label(frame_parametre, text="Abscisse du point B ", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_abscisseB.place(x=0, y=270, width=120)
            saisie_abscisseB = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg="white", selectbackground="blue", fg="black", justify="left")
            saisie_abscisseB.place(x=120, y=270)

            label_ordonneeB = tk.Label(frame_parametre, text="Ordonnee du point B ", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_ordonneeB.place(x=0, y=300, width=120)
            saisie_ordonneeB = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg="white", selectbackground="blue", fg="black", justify="left")
            saisie_ordonneeB.place(x=120, y=300)

            label_autres = tk.Label(frame_parametre, text="Parametre du mouvement", anchor='w', font="AgencyFB 8 bold", bg="grey", fg="black")
            label_autres.place(x=0, y=330, width=160)

            label_NbPas = tk.Label(frame_parametre, text="Nombre de pas ", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_NbPas.place(x=0, y=360, width=120)
            saisie_NbPas = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg="white", selectbackground="blue", fg="black", justify="left")
            saisie_NbPas.place(x=120, y=360)

            label_duree = tk.Label(frame_parametre, text="Durée su trajet A-B ", anchor='w', font="AgencyFB 8 bold", bg="#E2F0D9", fg="black")
            label_duree.place(x=0, y=390, width=120)
            saisie_duree = tk.Entry(frame_parametre, bd=1, width=6, font="AgencyFB 8 bold", bg="white", selectbackground="blue", fg="black", justify="left")
            saisie_duree.place(x=120, y=390)

            #interface graphique informations debogage
            label_infos = tk.Label(frame_infos, text="Informations de débogage ", anchor='w', font="AgencyFB 8 bold", bg="grey", fg="black")
            label_infos.place(x=0, y=0, width=260)

            scroll = tk.Scrollbar(frame_infos, orient="vertical")
            scroll.place(x=243, y=20, height=140)

            #inetrface graphique des boutons
            label_bouton = tk.Label(frame_bouton, text="Boutons de simulateur", justify="left", font="AgencyFB 8 bold ", bg="grey", fg="black")
            label_bouton.place(x=0, y=0, width=155)

            bouton_demo= tk.Button(frame_bouton, text="Demo", font="AgencyFB 10 bold", justify="center", bg="orange", fg="white", width=8, height=1, bd=5 )
            bouton_demo.place(x=30,y=30)

            bouton_dessiner= tk.Button(frame_bouton, text="Dessiner", font="AgencyFB 10 bold", justify="center", bg="#70AD47", fg="white", width=8, height=1, bd=5, command=dessiner )
            bouton_dessiner.place(x=30,y=75)

            bouton_simuler= tk.Button(frame_bouton, text="Simuler", font="AgencyFB 10 bold", justify="center", bg="#70AD47", fg="white", width=8, height=1, bd=5 )
            bouton_simuler.place(x=30,y=120)

            bouton_nouveau= tk.Button(frame_bouton, text="Nouveau", font="AgencyFB 10 bold", justify="center", bg="grey", fg="white", width=8, height=1, bd=5 )
            bouton_nouveau.place(x=30,y=165)

            bouton_quitter= tk.Button(frame_bouton, text="Quitter", font="AgencyFB 10 bold", justify="center", bg="red", fg="white", width=8, height=1, bd=5 )
            bouton_quitter.place(x=30,y=210)


            #interface graphique auteur
            label_auteur = tk.Label(frame_auteur, text="Auteur de simulation", justify="left", font="AgencyFB 8 bold", bg='grey', fg="black")
            label_auteur.place(x=0, y=0, width=155)

            #fin
            simulation.mainloop()
        else:
            showerror('error', "le mot de passe est incorrect !!!")
        connection.close()


#############################################################



#Permet de dissiner avec plt
"""def dissiner():
    global Nbpas, L0, L1, L2, Teta1, Teta2, XB, YB, fig, tab_z, tab_t, a, b, teta1rad, teta2rad, O3, O2, z, angle
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    
   Recupération des differentes valeurs des longueurs des liens, angles et point
    L0 = float(saisie_lien0.get())
    L1 = float(saisie_lien1.get())
    L2 = float(saisie_lien2.get())
    
    Th1 = float(saisie_angle1.get())
    Th2 = float(saisie_angle2.get())
    # conversion des angles en radian
    th1 = math.radians(h1)
    th2 = math.radians(h2)
    
    XB = float(saisie_abscisseB.get())
    YB = float(saisie_ardonneeB.get())
    Nbpas = int(saisie_NbPas.get())

        #Générer des images post scripts (cas des figures)
        #matplotlib.use('TkAgg')

        #Matrice T10 & T21
    T01 = np.array([[np.cos(th1), -np.sin(th1), 0, l0],
                    [np.sin(th1), np.cos(th1), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    T12 = np.array([[np.cos(th2), -np.sin(th2), 0, l1],
                    [np.sin(th2), np.cos(th2), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

        #Coordonnées de A dans le répère R2
    O3 = np.matrix([[L2], [0], [0], [1]])
        #Coordonnées de A2 dans le répère R2
    O2 = np.matrix([[0], [0], [0], [1]])
        #Matrice globale T20
    T20 = np.dot(T10, T21)
        #
    O20 = np.dot(T20, O2)
        #Coordonnées de A dans le répère R0
    O30 = np.dot(T20, O3)
        #Angle d'orientation
    angle = math.degrees(math.atan2(T20[[1], [0]], T20[[0], [0]]))
        #Effaçage de la figure actuel
    plt.clf()
        #Coefficient a de la droite ax+b
    a = (O30[1]-YB)/(O30[0]-XB)
        #Coefficient b
    b = YB-(a*XB)
    tab_t = np.linspace(0, 5, 100)
    tab_z = equation(tab_t, float(a), float(b))

        #Inverser le répère
    plt.gca().invert_xaxis()

        #Tracez de la droite d'équation ax+b
        #plt.plot(tab_z, tab_t, '-.', lw=0.2, c='black')

    xa = round(float(O30[0]), 2)
    ya = round(float(O30[1]), 2)
    xa_ini = xa
    ya_ini = ya

    Dx = np.array([XB, xa_ini])
    Dy = np.array([YB, ya_ini])
    plt.plot(Dy, Dx, '-', color='black')

    plt.scatter(YB, XB, s=150, color='green', label='A SA PORTEE')

    plt.legend()

        #Tracez des liens et articulations du robot
    plt.bar(0, 0.3, lw=150, c='black')
    plt.plot([0, 0], [0, L0], lw=8, c='b')

    plt.scatter([0, O20[1]], [L0, O20[0]], lw=10, c='black')
    plt.plot([0, O20[1]], [L0, O20[0]], lw=8, c='b')

    plt.scatter([float(O30[1]), float(O30[1])], [float(O30[0]), float(
            O30[0])], lw=4, c='black', marker="$\cap$", s=450)
    plt.plot([float(O20[1]), float(O30[1])], [
                 float(O20[0]), float(O30[0])], lw=8, c='b')

    plt.gca().yaxis.set_ticks_position("right")
    plt.ylabel("L'axe ordonnée")
    plt.grid()
        
        #Ouverture de la première figure
    fig = plt.figure(1)
        #Création d'un canvas pour l'affichage de la première figure
    canvas = FigureCanvasTkAgg(fig, master=mymaster)
    plot_widget = canvas.get_tk_widget()
    plot_widget.place(width=560, height=530, x=290, y=70)


"""

###############################################################

def valider_inscription():
    mdp = entry_pwd.get()
    mdp2 = entry_pwd2.get()
    nom = entry_pseudo.get()
    if (entry_pseudo.get() == ""):
        showerror('error', "tous les champs doivent etre completé !!!")
    if mdp =="":
        showerror('error', "tous les champs doivent etre completé !!!")
    if mdp2=="":
        showerror('error', "tous les champs doivent etre completé !!!")
    else:
        conn = q3.connect("essai_baseDD.db")
        curseur = conn.cursor()
        #tab = (f'{mdp}',f'{nom}')
        curseur.execute(f"INSERT INTO si_users(nom,password) VALUES('{nom}','{mdp}')")
        conn.commit()
        showinfo('Validation', "Enregistrement effectué avec succès")
        conn.close()
        inscription.destroy()
        connexion.destroy()
        
############################################################




#Etap 1:fenetre d'inscription            
def creer_compte():
    
    global inscription
    inscription = tk.Tk()
    inscription.geometry('600x310')
    inscription.title("Inscription")
    inscription.config(bg="#E2F0D9")
    inscription.resizable(width="false", height="false")

    frame_form = tk.Frame(inscription, width=470, height=250, bg="#E2F0D9", bd=3, relief="groove")
    frame_form.place(x=70,y=30)
    frame_cote = tk.Button(inscription, width=2, height=305, bd=0, bg='blue').place(x=0,y=0)
    label_pseudo = tk.Label(frame_form, text="Pseudo: ", font=('arial', 16, 'bold'), bg="#E2F0D9", fg="black", anchor='w')
    label_pseudo.place(x=10, y=30)
    label_pseudo.focus_set()
    global entry_pseudo
    entry_pseudo = tk.Entry(frame_form, width=30,font=('arial', 12), bd=0)
    entry_pseudo.place(x=166, y=35)

    label_pwd = tk.Label(frame_form, text="Mot de passe:", font=('arial', 16, 'bold'), bg="#E2F0D9", fg="black", anchor='w')
    label_pwd.place(x=10, y=60)
    global entry_pwd
    entry_pwd = tk.Entry(frame_form, width=30,font=('arial', 12), bd=0, show="*")
    entry_pwd.place(x=166, y=65)
    
    label_pwd2 = tk.Label(frame_form, text="Confirmation:", font=('arial', 16, 'bold'), bg="#E2F0D9", fg="black", anchor='w')
    label_pwd2.place(x=10, y=96)
    global entry_pwd2
    entry_pwd2 = tk.Entry(frame_form, width=30,font=('arial', 12), bd=0, show="*")
    entry_pwd2.place(x=166, y=100)
    btn_oublie = tk.Button(frame_form, text="J'ai déja un compte", bg='#E2F0D9', font=('arial', 12), fg='blue', bd=0, command=interface_connexion)
    btn_oublie.place(x=167, y=176)
    btn_connect = tk.Button(frame_form, text="Incription", bg='black', font=('arial', 13, 'bold'), fg='white', width=30)
    btn_connect.place(x=90, y=140)
    btn_connect.config(command=valider_inscription)
    inscription.mainloop()
    connexion.destroy()


#Etap 1:fenetre de "connexion"
def interface_connexion():
    global connexion
    connexion = tk.Tk()
    connexion.geometry('600x310')
    connexion.title("Connexion")
    connexion.config(bg="#E2F0D9")
    connexion.resizable(width="false", height="false")

    frame_cote = tk.Button(connexion, width=2, height=305, bd=0, bg='blue').place(x=0,y=0)

    frame_form = tk.Frame(connexion, width=470, height=250, bg="#E2F0D9", bd=3, relief="groove")
    frame_form.place(x=70,y=30)

    #global message
    #message = tk.Entry(frame_form, width=51, font=('arial',12), fg="green", bg='#E2F0D9')
    #message.place(x=0,y=0)

    label_pseudo = tk.Label(frame_form, text="Pseudo: ", font=('arial', 16, 'bold'), bg="#E2F0D9", fg="black", anchor='w')
    label_pseudo.place(x=10, y=30)
    label_pseudo.focus_set()

    global entry_pseudo
    entry_pseudo = tk.Entry(frame_form, width=30,font=('arial', 14), bd=0)
    entry_pseudo.place(x=166, y=35)

    label_pwd = tk.Label(frame_form, text="Mot de passe:", font=('arial', 16, 'bold'), bg="#E2F0D9", fg="black", anchor='w')
    label_pwd.place(x=10, y=60)
    global entry_pwd
    entry_pwd = tk.Entry(frame_form, width=30,font=('arial', 14), bd=0, show="*")
    entry_pwd.place(x=166, y=65)

    btn_connect = tk.Button(frame_form, text="Connection", bg='black', font=('arial', 13, 'bold'), fg='white', width=30)
    btn_connect.place(x=90, y=130)
    btn_connect.config(command=test)

    btn_oublie = tk.Button(frame_form, text="mot de passe oublié", bg='#E2F0D9', font=('arial', 12), fg='blue', bd=0)
    btn_oublie.place(x=252, y=176)

    btn_oublie = tk.Button(frame_form, text="Je n'ai pas de compte", bg='#E2F0D9', font=('arial', 12), fg='blue', bd=0, command=creer_compte)
    btn_oublie.place(x=85, y=176)
    connexion.mainloop()
    inscription.destroy()
    
interface_connexion()
