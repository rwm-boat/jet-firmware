import matplotlib.pyplot as plt
import json
import math
import easygui
import numpy as np
import os

path_1 = easygui.fileopenbox()
path_2 = easygui.fileopenbox()
path_3 = easygui.fileopenbox()
path_4 = easygui.fileopenbox()

jet_current_1 = []
jet_current_2 = []
jet_current_3 = []
jet_current_4 = []

thrust_1 = []
thrust_2 = []
thrust_3 = []
thrust_4 = []


efficiency_1 = []
efficiency_2 = []
efficiency_3 = []
efficiency_4 = []

def load_log():
    global jet_current_1
    global thrust_1
    global jet_current_2
    global thrust_2
    global jet_current_3
    global thrust_3
    global jet_current_4
    global thrust_4
    global efficiency_1
    global efficiency_2
    global efficiency_3
    global efficiency_4

    with open(path_1, "r") as log_file:
         for line in log_file.readlines():
            obj = json.loads(line)
            jet_current_1.append(obj["current"])
            thrust_1.append(obj["thrust"])
            efficiency_1.append(obj["thrust"]/obj["current"])
    with open(path_2, "r") as log_file:
         for line in log_file.readlines():
            obj = json.loads(line)
            jet_current_2.append(obj["current"])
            thrust_2.append(obj["thrust"])
            efficiency_2.append(obj["thrust"]/obj["current"])
    with open(path_3, "r") as log_file:
         for line in log_file.readlines():
            obj = json.loads(line)
            jet_current_3.append(obj["current"])
            thrust_3.append(obj["thrust"])
            efficiency_3.append(obj["thrust"]/obj["current"])
    with open(path_4, "r") as log_file:
         for line in log_file.readlines():
            obj = json.loads(line)
            jet_current_4.append(obj["current"])
            thrust_4.append(obj["thrust"])
            efficiency_4.append(obj["thrust"]/obj["current"])
def plot():
    fig, ax1 = plt.subplots()

    ax1.plot(jet_current_1, label="Jet Current 22mm (amps)", color = 'g', linestyle = "dotted")
    ax1.plot(jet_current_2, label="Jet Current 24mm (amps)", color = 'k', linestyle = "dotted")
    ax1.plot(jet_current_3, label="Jet Current 16mm (amps)", color = 'r', linestyle = "dotted")
    ax1.plot(jet_current_4, label="Jet Current 18mm (amps)", color = 'b', linestyle = "dotted")
    ax1.legend(loc = 'lower right')
    

    ax2 = ax1.twinx() #second y axis
    ax2.plot(thrust_1, label="Thrust 22mm (grams)", color="g")
    ax2.plot(thrust_2, label="Thrust 24mm (grams)", color="k")
    ax2.plot(thrust_3, label="Thrust 16mm (grams)", color="r")
    ax2.plot(thrust_4, label="Thrust 18mm (grams)", color="b")
    ax2.legend(loc = 'upper left')

    plt.minorticks_on()
            
    plt.title("Jet Current Draw and Thrust vs. Throttle Request")
    ax1.set_xlabel("Throttle Request")
    ax1.set_ylabel("Jet Current Draw (Amps)")

    ax2.set_ylabel("Thrust (grams-force)")
    ax1.grid()
    ax2.grid()
    #plt.figure()
    fig, ax3 = plt.subplots()
    ax3.plot(efficiency_1, label="Jet Efficiency 12mm", color = 'g')
    ax3.plot(efficiency_2, label="Jet Efficiency 14mm", color = 'k')
    ax3.plot(efficiency_3, label="Jet Efficiency 16mm", color = 'r')
    ax3.plot(efficiency_4, label="Jet Efficiency 18mm", color = 'b')
    plt.title("Efficiency (grams-force/Amp)")
    ax3.set_xlabel("Throttle Request")
    ax3.set_ylabel("Efficiency (grams-force/Amp)")
    ax3.legend(loc = 'lower right')
    ax3.grid()

    plt.show()

load_log()
plot()