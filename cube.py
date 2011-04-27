from face import face

class cube:

    def __init__(self):
        """create a solved cube object"""

        #INDEX:         0   1   2   3   4   5
        self.sides = ['F','R','B','L','U','D'] #just for convience
        self.colors = ['R','B','O','G','W','Y']
        self.faces_list = []

        #makes a face of each color
        for color in self.colors:
            self.faces_list.append(face(color))

        #Hash table hashes to lists, easy handle
        self.faces = {'F': self.faces_list[0],'R': self.faces_list[1],
                      'B': self.faces_list[2],'L': self.faces_list[3],
                      'U': self.faces_list[4],'D': self.faces_list[5]}

        #this hashes characters to the member functions
        self.rotations ={'F': self.F, 'R': self.R, 'B': self.B,
                         'L': self.L, 'U': self.U, 'D': self.D}

        #this hashes characters to 4-direction tuples NESW
        self.directions = {'F': ('U','R','D','L'), 'R': ('U','B','D','F'),
                           'B': ('U','L','D','R'), 'L': ('U','F','D','B'),
                           'U': ('B','R','F','L'), 'D': ('F','R','B','L')}

    def __eq__(self,other):
        ret = True
        for f1,f2 in zip(self.faces_list,other.faces_list):
            for c1,c2 in zip(f1.squares,f2.squares):
                for p1,p2 in zip(c1,c2):
                    ret = (ret and p1==p2)
        return ret

    def edge_exists(self,f1,f2):
        return f2 in self.directions[f1]

    def get_edge(self,f1,f2):
        if(self.edge_exists(f1,f2)):
            for f1dir,c in enumerate(self.directions[f1]):
                if f2 == c:
                    break
            for f2dir,c in enumerate(self.directions[f2]):
                if f1 == c:
                    break
            return (self.faces[f1].get_edge(f1dir),self.faces[f2].get_edge(f2dir))
        else:
            print "cube edge getting error"
            return ('0','0')

    def corner_exists(self,f1,f2,f3):
        return (f2 in self.directions[f1]) and (f3 in self.directions[f1])

    def get_corner_index(self,f1,f2,f3):
        """return 0,1,2,3 indicating the direction
        relative to f1 of the corner f1,f2,f3
        0 - NW; 1 - NE; 2 - SW; 3 - SE
        """
        if(self.corner_exists(f1,f2,f3)):
            for direction,nbr in enumerate(self.directions[f1]):
                if f2 == nbr:
                    f2p = direction
                elif f3 == nbr:
                    f3p = direction
            if (f2p == 0 or f3p == 0):
                if f2p == 3 or f3p == 3:
                    return 0    #NW
                elif f2p == 1 or f3p ==1:
                    return 1    #NE
            elif f2p == 2 or f3p == 2:
                if f2p == 3 or f3p ==3:
                    return 2    #SW
                elif f2p == 1 or f3p == 1:
                    return 3    #SE
        print "corner index error"
        return -1


    def get_corner(self,f1,f2,f3):
        """Return the tuple for corner f1,f2,f3"""
        p1 = self.get_corner_index(f1,f2,f3)
        p2 = self.get_corner_index(f2,f1,f3)
        p3 = self.get_corner_index(f3,f1,f2)
        return (self.faces[f1].get_corner(p1),
                self.faces[f2].get_corner(p2),
                self.faces[f3].get_corner(p3))

    def print_cube(self):
        """print a 2d cube"""
        for face in self.faces_list:
            face.print_face()
            print ""
        print ""

    def print_cube_string(self):
        """get cube string"""
        s = "\n"
        for face in self.faces_list:
            s += face.print_face_string()
            s += '\n'
        return s

    def do_moves(self,movelist):
        """Perform all the moves in a list"""
        for move in movelist:
            self.rotations[move]()

    def string_to_movelist(self,moves):
        """Convert a string into a list of moves

        Implements support counter clockwise moves (denoted with ')
        as well as repeated moves (Ex F3 preforms F 3 times)

        """
        moves = moves.upper()
        movelist = []

        for i,char in enumerate(moves):
            if char == "\'":
                c = moves[i-1]
                #doing a move 3 times is the same as doing the oppisite
                movelist.append(c)
                movelist.append(c)
            elif char=='2' or char=='3': #only 2 and 3 make sense here
                c = moves[i-1]
                for i in range(int(char)-1):
                    movelist.append(c)
            elif char in self.sides:
                movelist.append(char)
            else:
                print "Invalid rotation in input string"
        return movelist

    def do_string(self,s):
        self.do_moves(self.string_to_movelist(s))

    def F(self):
        """rotate the front face of the cube (red)"""
        self.faces['F'].rotate(1)
        uppercolors = self.faces['U'].get_row(2)
        downcolors = self.faces['D'].get_row(0)
        rightcolors = self.faces['R'].get_col(0)
        leftcolors = self.faces['L'].get_col(2)
        leftcolors.reverse()
        rightcolors.reverse()

        self.faces['R'].shift_col(0,uppercolors)
        self.faces['D'].shift_row(0,rightcolors)
        self.faces['U'].shift_row(2,leftcolors)
        self.faces['L'].shift_col(2,downcolors)

    def R(self):
        """rotate the right face of the cube"""
        self.faces['R'].rotate(1)
        frontcolors = self.faces['F'].get_col(2)
        downcolors = self.faces['D'].get_col(2)
        uppercolors = self.faces['U'].get_col(2)
        backcolors = self.faces['B'].get_col(0)
        uppercolors.reverse()
        backcolors.reverse()

        self.faces['F'].shift_col(2,downcolors)
        self.faces['U'].shift_col(2,frontcolors)
        self.faces['D'].shift_col(2,backcolors)
        self.faces['B'].shift_col(0,uppercolors)

    def B(self):
        """rotate the back face of the cube"""
        self.faces['B'].rotate(1)
        rightcolors = self.faces['R'].get_col(2)
        leftcolors = self.faces['L'].get_col(0)
        uppercolors = self.faces['U'].get_row(0)
        downcolors = self.faces['D'].get_row(2)
        uppercolors.reverse()
        downcolors.reverse()

        self.faces['U'].shift_row(0,rightcolors)
        self.faces['D'].shift_row(2,leftcolors)
        self.faces['R'].shift_col(2,downcolors)
        self.faces['L'].shift_col(0,uppercolors)

    def L(self):
        """rotate the left face of the cube"""
        self.faces['L'].rotate(1)
        frontcolors = self.faces['F'].get_col(0)
        uppercolors = self.faces['U'].get_col(0)
        backcolors = self.faces['B'].get_col(2)
        downcolors = self.faces['D'].get_col(0)
        backcolors.reverse()
        downcolors.reverse()

        self.faces['F'].shift_col(0,uppercolors)
        self.faces['U'].shift_col(0,backcolors)
        self.faces['D'].shift_col(0,frontcolors)
        self.faces['B'].shift_col(2,downcolors)

    def U(self):
        """rotate the up face of the cube"""
        self.faces['U'].rotate(1)
        frontcolors = self.faces['F'].get_row(0)
        rightcolors = self.faces['R'].get_row(0)
        backcolors = self.faces['B'].get_row(0)
        leftcolors = self.faces['L'].get_row(0)

        self.faces['F'].shift_row(0,rightcolors)
        self.faces['R'].shift_row(0,backcolors)
        self.faces['B'].shift_row(0,leftcolors)
        self.faces['L'].shift_row(0,frontcolors)

    def D(self):
        """rotate the down (bottom) face of the cube"""
        self.faces['D'].rotate(1)
        frontcolors = self.faces['F'].get_row(2)
        rightcolors = self.faces['R'].get_row(2)
        backcolors = self.faces['B'].get_row(2)
        leftcolors = self.faces['L'].get_row(2)

        self.faces['F'].shift_row(2,leftcolors)
        self.faces['R'].shift_row(2,frontcolors)
        self.faces['B'].shift_row(2,rightcolors)
        self.faces['L'].shift_row(2,backcolors)

if __name__ == '__main__':
    mycube = cube()
    #mycube.faces[0].squares[1][0] = 'Z'
    #mycube.faces[0].squares[2][1] = 'X'
    #mycube.faces[0].squares[0][2] = 'V'
    #mycube.R()
    mycube.do_moves(['R','R','F','R','F','F','R','L','B','U','B','U','R','F','L','D','L','D','D','B','U','F','R','D','L'])
    #mycube.print_cube()
    for f in mycube.faces_list:
        im = f.face_to_image()
        im.save("facepics/"+f.center+".BMP")
