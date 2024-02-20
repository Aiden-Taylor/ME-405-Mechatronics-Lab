"""!
@file step_GUI.py

Send a PWM signal to the micro controller to control the speed of the motor and measure the response.
Plot the output in a GUI with multiple trials overlayed on the same graph.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Julia Fay & Jack Foxcroft & Aiden Taylor
@date   2024-2-19 Original program, based on example from above listed source
and provided to us from the lab instructor. 
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import math
import time
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class Step_GUI():

    def __init__(self,in_serial_port):
    
        #initialize the time and voltage arrays 
        self.time = []
        self.voltage = []
        self.serial_port = in_serial_port 

    def read_input(self):
        """!
            The read_input function first runs the main.py file on the mcu that triggers the step response
            and stores the data. Then it reads the step response data from the serial port and stores the
            csv data in the time and voltage arrays. 
            
            """

        # Define the serial port and baud rate
        #serial_port = 'COM5'  #change to match the port of the computer this is being run on
        baud_rate = 115200  # Set the baud rate to match your MCU's configuration
            
        with Serial(self.serial_port, baud_rate, timeout=1) as ser:
            ser.write(b"\x03") #sends a ctrl+c
            ser.write(b"\x04") #sends a ctrl+d
            
            # Read data from the serial port
            for line in ser: 
                            # Read data from the serial port
                    try:
                        line = line.decode('utf-8').strip()
                        x = line.split('#')
                        x = x[0].split(',')
                        
                        if line == 'end':
                            pass
                        
                        elif (x[0] != "\n") & (x[0] != ''):
                            #print(x)
                            try:
                                self.time.append(float(x[0]))
                            except Exception as e:
                                print(e)
                            try:
                                self.voltage.append(float(x[1].replace('\n', '')))
                            except Exception as e:
                                print(e)
                                
                    except ValueError:
                        print('Error reading data')
                    

    def plot_step(self,plot_axes, plot_canvas, xlabel, ylabel):
        """!
        The plot_step function makes a plot embeded into a GUI showing both the
        measured step response data and the accompanying theoretical curve.
        @param plot_axes The plot axes supplied by Matplotlib
        @param plot_canvas The plot canvas, also supplied by Matplotlib
        @param xlabel The label for the plot's horizontal axis
        @param ylabel The label for the plot's vertical axis
        """
        #read the data from the serial port 

        self.read_input()

        # Draw the plot. Of course, the axes must be labeled. A grid is optional
        plot_axes.plot(self.time, self.voltage)
        plot_axes.set_xlabel(xlabel)
        plot_axes.set_ylabel(ylabel)
        plot_axes.grid(True)
        plot_canvas.draw()


    def tk_matplot(self,xlabel, ylabel, title):
        """!
        Create a TK window with one embedded Matplotlib plot.
        This function makes the window, displays it, and runs the user interface
        until the user closes the window. The plot function, which must have been
        supplied by the user, should draw the plot on the supplied plot axes and
        call the draw() function belonging to the plot canvas to show the plot. 
        @param plot_function The function which, when run, creates a plot
        @param xlabel The label for the plot's horizontal axis
        @param ylabel The label for the plot's vertical axis
        @param title A title for the plot; it shows up in window title bar
        """
        # Create the main program window and give it a title
        tk_root = tkinter.Tk()
        tk_root.wm_title(title)

        # Create a Matplotlib 
        fig = Figure()
        axes = fig.add_subplot()

        # Create the drawing canvas and a handy plot navigation toolbar
        canvas = FigureCanvasTkAgg(fig, master=tk_root)
        toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
        toolbar.update()

        # Create the buttons that run tests, clear the screen, and exit the program
        button_quit = tkinter.Button(master=tk_root,
                                    text="Quit",
                                    command=tk_root.destroy)
        button_clear = tkinter.Button(master=tk_root,
                                    text="Clear",
                                    command=lambda: axes.clear() or canvas.draw())
        button_run = tkinter.Button(master=tk_root,
                                    text="Run Test", 
                                    command=lambda: self.plot_step(axes, canvas, xlabel, ylabel))

        # Arrange things in a grid because "pack" is weird
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
        toolbar.grid(row=1, column=0, columnspan=3)
        button_run.grid(row=2, column=0)
        button_clear.grid(row=2, column=1)
        button_quit.grid(row=2, column=2)

        # This function runs the program until the user decides to quit
        tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
# if __name__ == "__main__":


var = Step_GUI('COM3')
var.tk_matplot(
            xlabel="Time (ms)",
            ylabel="Position",
            title="DC Motor Control")


