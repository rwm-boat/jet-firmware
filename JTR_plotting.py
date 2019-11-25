import matplotlib.pyplot as plt
import json
import math
import easygui
import numpy as np
import os

path = easygui.fileopenbox()

jet_current = []
thrust = []

def load_log():
    global jet_current
    global thrust

    with open(path, "r") as log_file:
         for line in log_file.readlines():
            obj = json.loads(line)
            jet_current.append(obj["current"])
            thrust.append(obj["thrust"]*9.8)
def plot():
    fig, ax1 = plt.subplots()

    ax1.plot(jet_current, label="Jet Current (Amps)", color = 'g')

    ax2 = ax1.twinx() #second y axis
    ax2.plot(thrust, label="Thrust", color="r")
    ax2.legend(loc = 'upper right')
        
    plt.title("Jet Current Draw and Boat Speed vs. Time")
    ax1.set_xlabel("Time (deciseconds)")
    ax1.set_ylabel("Jet Current Draw (Amps)")
    ax1.legend(loc = 'lower right')
    ax2.set_ylabel("Thrust Newtons")
    ax1.grid()
    plt.show()

load_log()
plot()