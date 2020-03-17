import tkinter as tk
from tkinter import filedialog
import numpy as np
from interpolation import get_ctrl_pts, write_output
from PIL import Image, ImageTk
from scipy import interpolate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.steps_frame = tk.Frame(self, padx=10, pady=10)
        self.steps_frame.pack(side='top')
        self.steps_sign = tk.Label(self.steps_frame)
        self.steps_sign['text'] = 'Number of Steps for Curve:'
        self.steps_sign.pack(side='left')
        self.steps_var = tk.StringVar()
        self.steps_entry = tk.Entry(self.steps_frame, textvariable=self.steps_var)
        self.steps_entry.pack(side='left')
        self.steps_var.set(50)


        self.interpolate_sign = tk.Label(self)
        self.interpolate_sign['text'] = 'Convert Coordinates to Control Points and Plot'
        self.interpolate_sign.pack(side='top')
        
        self.interpolate_frame = tk.Frame(self, padx=10, pady=10)
        self.interpolate_frame.pack(side='top')
        self.interpolate_file = tk.Label(self.interpolate_frame, relief='sunken', width=75)
        self.interpolate_file['text'] = 'Select Coordinates File'
        self.interpolate_file.pack(side='left')
        self.interpolate_select = tk.Button(self.interpolate_frame, relief='raised', width=20)
        self.interpolate_select['text'] = 'Select File'
        self.interpolate_select['command'] = self.select_coordinate_file
        self.interpolate_select.pack(side='right')

        self.output_frame = tk.Frame(self, padx=10, pady=10)
        self.output_frame.pack(side='top')
        self.output_file = tk.Label(self.output_frame, relief='sunken', width=75)
        self.output_file['text'] = 'Select Output Destination'
        self.output_file.pack(side='left')
        self.output_select = tk.Button(self.output_frame, relief='raised', width=20)
        self.output_select['text'] = 'Select Output Destination'
        self.output_select['command'] = self.select_output
        self.output_select.pack(side='right')

        self.generate_output_button = tk.Button(self, width=75)
        self.generate_output_button['text'] = 'Generate and Plot'
        self.generate_output_button['command'] = self.generate_output
        self.generate_output_button.pack(side='top')

        self.or_label = tk.Label(self, padx=10, pady=10, fg='red')
        self.or_label['text'] = '---- OR ----'
        self.or_label.pack(side='top')

        self.plot_sign = tk.Label(self)
        self.plot_sign['text'] = 'Plot from Output File'
        self.plot_sign.pack(side='top')

        self.plot_frame = tk.Frame(self, padx=10, pady=10)
        self.plot_frame.pack(side='top')
        self.plot_file = tk.Label(self.plot_frame, relief='sunken', width=75)
        self.plot_file['text'] = 'Select Output File'
        self.plot_file.pack(side='left')
        self.plot_select = tk.Button(self.plot_frame, relief='raised', width=20)
        self.plot_select['text'] = 'Select File'
        self.plot_select['command'] = self.select_plot_file
        self.plot_select.pack(side='right')

        self.plot_output_button = tk.Button(self, width=75)
        self.plot_output_button['text'] = 'Plot from Output File'
        self.plot_output_button['command'] = self.plot_output
        self.plot_output_button.pack(side='top')

        self.img = tk.Label(self)
        self.img.pack(side='top')
        self.imageholder = None

    def select_coordinate_file(self):
        selected_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        if selected_file != '':
            self.interpolate_file['text'] = selected_file

    def select_output(self):
        output_file = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        if output_file != '':
            self.output_file['text'] = output_file

    def select_plot_file(self):
        selected_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        if selected_file != '':
            self.plot_file['text'] = selected_file

    def plot_save_bspline(self, ctrl_pt_x, ctrl_pt_y, knots, num_points=50, x=None, y=None, degree=3):
        plt.figure()
        tck=[knots,[ctrl_pt_x,ctrl_pt_y],degree]
        steps=np.linspace(0,1,num_points,endpoint=True)
        out = interpolate.splev(steps,tck) 

        plt.plot(ctrl_pt_x,ctrl_pt_y,'k--',label='Control polygon',marker='o',markerfacecolor='red')
        if x and y:
            plt.scatter(x,y, label='Coordinates',marker='o', color='blue')
        plt.plot(out[0],out[1],'b',linewidth=2.0,label='B-spline curve')
        plt.legend(loc='best')
        plt.title('Cubic B-spline curve')
        plt.savefig('render.png')

    def generate_output(self):
        try:
            steps = int(self.steps_var.get())
            if self.output_file['text'] == 'Select Output Destination' or self.interpolate_file['text'] == 'Select Coordinates File':
                tk.messagebox.showerror('Error', 'Input/Output file not given')
            else:
                ctrl_pt_x, ctrl_pt_y, knots, x, y = get_ctrl_pts(self.interpolate_file['text'])
                write_output(self.output_file['text'], ctrl_pt_x, ctrl_pt_y, knots)
                steps = max((steps, len(ctrl_pt_x*3)))
                self.plot_save_bspline(ctrl_pt_x, ctrl_pt_y, knots, num_points=steps, x=x, y=y)
                load = Image.open("render.png")
                self.imageholder = ImageTk.PhotoImage(load)
                self.img['image'] = self.imageholder
        except:
            tk.messagebox.showerror('Error', 'Invalid Input Given')

    def plot_output(self):
        try:
            steps = int(self.steps_var.get())
            if self.plot_file['text'] == 'Select Output File':
                tk.messagebox.showerror('Error', 'Output file not given')
            else:
                with open(self.plot_file['text'], 'r') as f:
                    degree = int(f.readline())
                    num_ctrl_pt = int(f.readline())
                    knots = [float(x) for x in f.readline().split()]
                    ctrl_pt_x = []
                    ctrl_pt_y = []
                    for i in range(num_ctrl_pt):
                        line = f.readline().split()
                        ctrl_pt_x.append(float(line[0]))
                        ctrl_pt_y.append(float(line[1]))
                steps = max((steps, len(ctrl_pt_x*3)))
                self.plot_save_bspline(ctrl_pt_x, ctrl_pt_y, knots, num_points=steps, degree=degree)
                load = Image.open("render.png")
                self.imageholder = ImageTk.PhotoImage(load)
                self.img['image'] = self.imageholder
        except:
            tk.messagebox.showerror('Error', 'Invalid Input Given')


root = tk.Tk()
root.title('B-Spline Interpolation and Plotting')
# root.geometry('1000x200')
app = Application(master=root)
app.mainloop()