import matplotlib.pyplot as plt
import json
import math
import easygui
import numpy as np
import os

path = easygui.fileopenbox()

jet_current = []
thrust = []
efficiency = []


def load_log():
    global jet_current
    global thrust
    global efficiency

    with open(path, "r") as log_file:
         for line in log_file.readlines():
            obj = json.loads(line)
            jet_current.append(obj["current"])
            thrust.append(obj["thrust"])
            efficiency.append(obj["thrust"]/obj["current"])
def plot():
    fig, ax1 = plt.subplots()

    ax1.plot(jet_current, label="Jet Current", color = 'g')
    

    ax2 = ax1.twinx() #second y axis
    ax2.plot(thrust, label="Thrust", color="r")
    ax2.legend(loc = 'upper right')
        
    plt.title("Jet Current Draw and Boat Speed vs. Time")
    ax1.set_xlabel("Time (deciseconds)")
    ax1.set_ylabel("Jet Current Draw (Amps)")
    ax1.legend(loc = 'lower right')
    ax2.set_ylabel("Thrust (grams-force)")
    ax1.grid()
    #plt.figure()
    fig, ax3 = plt.subplots()
    ax3.plot(efficiency, label="Jet Efficiency", color = 'b')
    plt.title("Efficiency (grams-force/Amp)")
    ax3.set_xlabel("Time (deciseconds)")
    ax3.set_ylabel("Efficiency (grams-force/Amp)")
    ax3.legend(loc = 'lower right')
    ax3.grid()

    plt.show()

load_log()
plot()