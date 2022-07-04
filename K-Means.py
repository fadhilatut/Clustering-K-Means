from tkinter import*
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import mode
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, ttk
from pandastable import Table
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import os

root = Tk()
root.geometry("400x550")
root.resizable(1,1)
f1 = LabelFrame(root)
f1.pack()
f1.place(height=400, width=320, x = 38, y = 93)

class GUI:
    df=pd.DataFrame({})
   
    def __init__(self,master):
        self.master = master
        master.title("K-Means Clustering")
       
        #Data Path
        self.pathLabel = Label(master, text="Data Path:")
        vcmd = master.register(self.validate)
        self.pathEntry = Entry(master, validate  ="key")
        self.browse_button = Button(master, text = "Browse", command = lambda:self.browse())

        #Number of cluster k
        self.numkLabel = Label(master,text="Num of cluster k:")
        vcmd = master.register(self.validate)
        self.numkEntry = Entry(master,validate="key")

        #graph
        self.sse_btn = Button(master, text = "Graph", command = lambda:self.graph())

        #cluster
        self.cluster_button = Button(master,text="Cluster", command = lambda:self.kMeans())

        #Layout

        self.pathLabel.pack()
        self.pathLabel.place(x = 38 ,y = 10)

        self.pathEntry.pack()
        self.pathEntry.place(x = 155 , y = 10 )

        self.browse_button.pack()
        self.browse_button.place(x=293, y = 10)

        self.numkLabel.pack()
        self.numkLabel.place(x =38, y = 32)
        
        self.numkEntry.pack()
        self.numkEntry.place(x =155 , y = 32)

        self.sse_btn.pack()
        self.sse_btn.place(x = 100, y = 60)

        self.cluster_button.pack()
        self.cluster_button.place(x=168, y =60)
        

    def validate(self, new_text):
        '''if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False'''

    def browse(self):
        #get data
        self.datapath = filedialog.askopenfilename()
        self.pathEntry.insert(0, self.datapath)
        #valid check
        if(not self.datapath):
            messagebox.showinfo("K Means Clustering", "Please Choose data file")
            return
        self.df = pd.read_csv(self.datapath, sep=";")
        new = tk.Toplevel(root)
        new.geometry("400x550")
        new.title = ('Dataset')
        f2 = LabelFrame(new)
        f2.pack()
        f2.place(height=300 ,width=250)
        self.table = self.pt = Table(f2, dataframe=self.df, showtoolbar=False, showstatusbar=False)
        self.pt.show()
      
       
    def graph(self):
        cost = []
        for i in range(1,11):
            self.KM = KMeans(n_clusters = i, max_iter = 500)
            self.KM.fit(self.df)
            cost.append(self.KM.inertia_)
        
        plt.grid()
        plt.plot(range(1,11), cost, color ='g', linewidth ='3')
        plt.xlabel("Value of K")
        plt.ylabel("Squarred Error (Cost)")
        plt.show()
        
        return
        

                   
    def kMeans(self):
        try:
            clusNum=int(self.numkEntry.get())
            if(clusNum<=0):
                messagebox.showerror("K Means Clustering", "Number of clusters must be positive")
                return
        except Exception:
            messagebox.showerror("K Means Clustering", "invalid numbers")
            return
        cluster = KMeans (n_clusters = clusNum,random_state=0, max_iter = 500).fit(self.df)
        centroids = cluster.clutkster_centers_
        print(centroids)
        cluster.labels_
        self.df["cluster"] = cluster.labels_
        datakp=self.df
        datakp.sort_values(by=['cluster'], inplace=True)
    
       #table
        self.table = self.pt = Table(f1, dataframe=datakp, showtoolbar=False, showstatusbar=False)
        self.pt.autoResizeColumns()
        self.pt.show()
    
     
        messagebox.showinfo("K Means Clustering", "Clustering completed successfully!")
        return

    
my_gui = GUI(root)
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure?"):
        root.destroy()
        os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

