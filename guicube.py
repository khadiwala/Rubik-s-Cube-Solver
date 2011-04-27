
from PIL import ImageTk, Image
from Tkinter import *

from solver import solver
from random import choice
from time import sleep
import tkMessageBox

class CubeSolver:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.rcube = solver()
        self.scramble_moves = []

        bframe = Frame(frame) #frame for cube manipulation

        #rotation buttons
        self.r = Button(bframe, text="Right", command=lambda: self.do_rotation('R'))
        self.r.grid(row=1)
        self.l = Button(bframe, text="Left", command=lambda: self.do_rotation('L'))
        self.l.grid(row=1,column=1)
        self.f = Button(bframe, text="Front", command=lambda: self.do_rotation('F'))
        self.f.grid(row=2)
        self.b = Button(bframe, text="Back", command=lambda: self.do_rotation('B'))
        self.b.grid(row=2,column=1)
        self.u = Button(bframe, text="Upper", command=lambda: self.do_rotation('U'))
        self.u.grid(row=3)
        self.d = Button(bframe, text="Down", command=lambda: self.do_rotation('D'))
        self.d.grid(row=3,column=1)

        self.newcube = Button(bframe, text="Create New Cube", command=self.create_cube)
        self.newcube.grid(row=0,column=0)

        self.scramble = Button(bframe, text="Scramble Cube",command=self.scramble_cube)
        self.scramble.grid(row=0,column=1)

        bframe.pack(side=RIGHT)

        downframe = Frame(frame)

        self.quit = Button(downframe, text="QUIT", fg="red", command=frame.quit)
        self.quit.pack(side=RIGHT)

        solveframe = Frame(downframe)

        self.solve = Button(solveframe, text="Solve Cube",command=self.solve_cube)
        self.solve.pack(side=LEFT)

        self.solinfo = Button(solveframe, text="Solution Info",command=self.sol_info)
        self.solinfo.pack(side=RIGHT)

        solveframe.pack(side=LEFT)
        downframe.pack(side=BOTTOM,pady=15,padx=15)

        self.cube_disp(frame)
        #self.output_cube()

    def create_cube(self):
        del self.rcube
        self.rcube = solver()
        self.output_cube()
        self.scramble_moves = []

    def do_rotation(self,rot):
        self.rcube.do_string(rot)
        self.scramble_moves.append(rot)
        self.output_cube()

    def scramble_cube(self):
        """does a 200 random moves"""
        for i in range(200):
            self.cubedis.update_idletasks()
            self.random_move()

    def random_move(self):
        c = choice(self.rcube.sides)
        self.do_rotation(c)

    #def solve_cube(self):
    #    self.rcube.solve()
    #    self.output_cube()

    def solve_cube(self):
        self.rcube.solve()
        self.rcube.do_moves(self.scramble_moves)
        for move in self.rcube.solmoves:
            sleep(.05)
            self.rcube.do_string(move)
            self.output_cube()
            self.cubedis.update_idletasks()
        print "solution: ",
        print self.rcube.solmoves
        print "Solution took " + str(len(self.rcube.solmoves)) + " steps"
        self.scramble_moves = []

    def sol_info(self):
        self.rcube.prune_solution_string()
        tkMessageBox.showinfo("Solution Info", "The solution took "+
        str(self.rcube.ignore_c_length('x')) +" moves\n"+"Moves: "+str(self.rcube.solmoves))
        #Message(self.cubedis,text=)).pack(side=BOTTOM)

    def cube_disp(self,frame):
        #txtfrm = Frame(frame)
        #self.cubedis = Text(txtfrm,height=25,width=10,background='white')
        #self.cubedis.pack(side=LEFT)
        #txtfrm.pack(side=TOP)
        self.cubedis = Canvas(frame,width=240,height=420)
        self.cubedis.pack(side=RIGHT)
        self.output_cube_help()
    def output_cube(self):
        #s = self.rcube.print_cube_string()
        #self.cubedis.delete(1.0, END)
        #self.cubedis.insert(END,s)
        self.cubedis.delete(ALL)
        self.output_cube_help()

    def output_cube_help(self):
        self.f = ImageTk.PhotoImage(self.rcube.faces['F'].face_to_image())
        self.r = ImageTk.PhotoImage(self.rcube.faces['R'].face_to_image(distort='right'))
        self.u = ImageTk.PhotoImage(self.rcube.faces['U'].face_to_image(distort='top'))
        self.b = ImageTk.PhotoImage(self.rcube.faces['B'].face_to_image())
        self.l = ImageTk.PhotoImage(self.rcube.faces['L'].face_to_image(distort='right'))
        self.d = ImageTk.PhotoImage(self.rcube.faces['D'].face_to_image(distort='bottom'))
        self.cubedis.create_image(0,90,anchor=NW,image=self.f)
        self.cubedis.create_image(90,90,anchor=NW,image=self.r)
        self.cubedis.create_image(0,0,anchor=NW,image=self.u)
        self.cubedis.create_image(0,200,anchor=NW,image=self.b)
        self.cubedis.create_image(90,200,anchor=NW,image=self.l)
        self.cubedis.create_image(0,290,anchor=NW,image=self.d)




root = Tk()
app = CubeSolver(root)
root.mainloop()
