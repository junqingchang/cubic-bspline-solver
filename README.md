# Cubic B-Spline Solver

## Running the program
The program has 2 variations, the Command Line Interface (CLI) version, as well as a GUI version. 

For the CLI version, to run it: 
```
python interpolation.py <input-file> <output-file> (−−plot) (−−steps n) 
```

The program takes in 2 required variables, input ﬁle and output ﬁle, which stands for the input ﬁle provided to the program and the output ﬁle path to save the output. 

The 2 optional parameters are -–plot and -–steps. -–plot enables the plotting function and will display the curve using matplotlib, -–steps allows users to state how many steps to insert in the graph (more steps equals smoother graph) 

For the GUI version, it has an additional feature compared to the CLI version which allows users to plot a curve from the output ﬁle directly. The GUI is split into 2 parts, the top which allows user to select the input ﬁle and the directory to save the output, and the bottom which allows user to select an output ﬁle. Both parts share the same parameter at the top of the GUI (Number of Steps for Curve) which allows users to set how many steps to plot with. Upon hitting either of the button with the proper ﬁles, a plot will be generated below.

For the GUI version, to run it:
```
python main,py
```
