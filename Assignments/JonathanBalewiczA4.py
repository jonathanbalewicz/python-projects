"""@with nobody
JonathanBalewiczA4Q1
COMP 1012  SECTION A01
INSTRUCTOR Bristow
ASSIGNMENT: A4 Question 1
AUTHOR    Jonathan Balewicz
VERSION   2018-04-05
PURPOSE: Simulate Diffusion
"""
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
##### CHANGE THIS TO YOUR STUDENT NUMBER
SEED = 7836603
########################################

np.random.seed(SEED)
def highlight_dense_region(atoms, width):
    xmin_range=int(atoms[:,0].min()*10) # coords are in every 10 units
    xmax_range=int(atoms[:,0].max()*10)+1
    rows=(abs(int(atoms[:,0].min()*10))+abs(int(atoms[:,0].max()*10)+2))# number of rows in the array of squares
    cols=abs(int(atoms[:,1].min()*10))+abs(int(atoms[:,1].max()*10)+2)
    row_min=int(abs(atoms[:,0].min()*10))# abs of the lowest coord of the atoms
    col_min=int(abs(atoms[:,1].min()*10))
    count=np.zeros((rows, cols))
    for x1 in range(xmin_range,xmax_range):
        x1=x1/10
        for y1 in range(int(atoms[:,1].min()*10), int(atoms[:,1].max()*10)+1):
            y1=y1/10
            xmin=x1<atoms[:,0]
            xmax=x1+width>atoms[:,0]
            ymin=y1<atoms[:,1]
            ymax=y1+width>atoms[:,1]
            cond_x=xmin&xmax
            cond_y=ymin&ymax
            cond_both=cond_x&cond_y
            count[int(x1*10+row_min),int(y1*10+col_min)]=cond_both.sum()# count is an array of the atoms in each square
    most_num=np.argmax(count)# number of the square with the most atoms
    row=(most_num//cols)+xmin_range# convert to count array coords
    col=(most_num % cols)+int(atoms[:,1].min()*10)
    return (row/10,col/10)# convert back to full units and return
    
    
"""This function will find the width x width square with the
highest number of atoms. It will highlight the region on
a matplotlib plot.
width: the width of one side of the square."""
    
def plot_atoms(atoms, container_radius, filename):
    fig, ax =plt.subplots()
    circle=patches.Circle((0,0),radius=container_radius, fc="r")
    ax.add_patch(circle)
    for atom in atoms:
        plt.scatter(atom[0], atom[1], c="g", zorder=2)
    Rectangle_width=10
    ax.add_patch(patches.Rectangle(highlight_dense_region(atoms, Rectangle_width),Rectangle_width,Rectangle_width,zorder=3,fill=False))#highlight dense region
    plt.savefig(filename)
    plt.show()
    

    """
    This function will plot atoms on a matplotlib plot and writes
    the file
    atoms: a 2d numpy array with x,y coordinates of atoms.
    filename: the name of the file to write out.
    """
    

def get_positive_number(prompt):
    value=input(prompt)
    while not value.isnumeric() or int(value) <= 0:
        value=input(prompt)
    return int(value)
    """
          This function repeatedly asks the user for input until they
          enter a positive integer.
        
          prompt: the string to be displayed (what the user should enter)
          returns a positive number (an int)
    """


def make_atoms(num_atoms, x, y):
    atoms=np.full((int(num_atoms),2),[float(x),float(y)])
    return atoms
    """
      This function generates an array (size=num_atoms)
      of x,y coordinates (representing atom locations). All atoms are
      at initial_x,initial_y by default.
    
      num_atoms: the number of atoms to create
      x: the x coordinate where all atoms should be
      y: the y coordinate where all atoms should be
      returns a 2d numpy array of x,y coordinates
    """
def walk(atoms, radius, move, range):
    rand_array=np.random.uniform(min(range), max(range)-1, (len(atoms), 2))
    atoms+=rand_array
    
    bumped=np.sum(np.sqrt(atoms[:,0]**2 + atoms[:,1]**2)>radius)
    
    atoms[np.sqrt((atoms[:,0])**2 + (atoms[:,1])**2)>radius,0]=atoms[np.sqrt((atoms[:,0])**2 + (atoms[:,1])**2)>radius,0]*move
    atoms[np.sqrt((atoms[:,0])**2 + (atoms[:,1])**2)>radius,1]=atoms[np.sqrt((atoms[:,0])**2 + (atoms[:,1])**2)>radius,1]*move
    return (atoms, bumped)
    """
  This function moves all of the atoms a random amount on their x
  coordinate and their y coordinate. If any atoms move outside the
  container on their random walk, this function will move them back
  inside by moving them back toward the origin.

  atoms: a 2d array of x,y coordinates of atoms
  radius: the radius of the container
  move: the percentage (between 0 and 1) to move the point back toward the origin
  range: a tuple of the range of random numbers [a,b)
  returns a modified array and the number of atoms that were moved
    """


def print_atoms(atoms, radius):
    """
      Print out the atoms onto our screen.
    
      atoms: a 2d array of x,y coordinates of atoms
      radius: the radius of the container
    """
    
    shift = radius * 2
    # some geometry, all atoms are around the origin and our
    # array coordinates are only in the top-right quadrant
    # so we need to translate them into that quadrant
    moved = atoms + make_atoms(len(atoms), radius, radius)
    
    # now we're going to create an array to "draw" on
    canvas = np.zeros((shift, shift))
    
    for atom in moved:
        # "draw" on the canvas (non-zero places in our)
        # grid have atoms
        canvas[int(atom[0])-1,int(atom[1]-1)] = 1
      
      # now draw the canvas to the screen
    for x in range(shift):
        for y in range(shift):
            if canvas[x,y]:
                print(canvas[x,y], end="")
            else:
                # we also want to draw the bounds of our container
                # so check to see if the x,y coordinate we're
                # currently looking at is within the radius of the
                # beaker.
                distance = ((x - radius) ** 2 + (y - radius) ** 2) ** 0.5
                # print out a ` to indicate we're "outside" and a space
                # to indicate we're "inside"
                if distance > radius:
                  print("`", end="")
                else:
                  print(" ", end="")
            print()

print("COMP 1012 Diffusion simulation (seed={})".format(SEED))

simulations = get_positive_number("How many units of time? ")
atom_count = get_positive_number("How many atoms? ")
beaker_size = get_positive_number("What is the radius of the beaker? ")

atoms = make_atoms(atom_count, 0, 0)
bumps = 0
move = 0.9
random_range = (-1, 2)

plot_atoms(atoms,beaker_size,"JonathanBalewiczA4Q2-atoms-initial.png")

for t in range(simulations):
    (_, bumped) = walk(atoms, beaker_size, move, random_range)
    if t%100==0 and t!=0:
        plot_atoms(atoms,beaker_size,"JonathanBalewiczA4Q2-atoms-{}.png".format(t))
    bumps += bumped
    

print_atoms(atoms, beaker_size)


print("Atoms bumped against the edge of the beaker {} times.".format(bumps))
plot_atoms(atoms,beaker_size,"FirstnameLastnameA4Q2-atoms-final.png")

print ("\nProgrammed by the Jonathan Balewicz")
print ("Date: " + time.ctime())
print ("End of processing")

