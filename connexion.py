# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 18:22:37 2022

@author: SIDIBE ISSIAKA
"""
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.messagebox import *
import sqlite3 as q3
from tkinter import*


###################################################################################




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
        
        if result == mdp: 
            #si le mot de passe entré correspond au mot de passe enregistré dans la base de donnée
            #Ouverture de la fenetre de simulation
            simulation = tk.Tk()
            simulation.geometry('650x550')
            simulation.title("Interface de simulation")
            simulation.config(bg="#E2F0D9")
            simulation.resizable(width="false", height="false")

            #fin
            simulation.mainloop()
        else:
            showerror('error', "le mot de passe est incorrect !!!")
        connection.close()


#############################################################



###############################################################

def valider_inscription():
    mdp = entry_pwd.get()
    mdp2 = entry_pwd2.get()
    nom = entry_pseudo.get()
    if (entry_pseudo.get() == "") and (mdp =="") and (mdp2=="") :
        showerror('error', "tous les champs doivent etre completé !!!")
    #if mdp =="":
    #    showerror('error', "tous les champs doivent etre completé !!!")
    #if mdp2=="":
        #showerror('error', "tous les champs doivent etre completé !!!")
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
