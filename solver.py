from cube import cube

class solver(cube):

    def __init__(self):
        cube.__init__(self)
        self.solmoves = []

    def solve(self):
        self.solmoves = []
        self.solve_upper()
        self.solve_middle()
        self.solve_down()

############################ SOLVING UPPER ROW ##################################
    def solve_upper(self):
        self._upper_edges_FRBL()
        self._upper_edges_D()
        self._upper_corners()

    def _upper_edges_FRBL(self):
        """Moves upper edges that are lined up to top, moves rest to down face"""

        #this for loop takes care of edges that are 'ready' to be shifted
        for i in range(4):      #the four not top/bottom faces
            for d in range(4):  #each edge (NESW)
                c = self.faces_list[i].get_edge(d)
                if c == self.faces['U'].center:  #has a upper edge piece
                    homeface = self.sides[i]
                    nbrface = self.directions[homeface][d]
                    e = self.get_edge(homeface,nbrface)
                    if e[1] == self.faces[nbrface].center:  #found an edge that belongs in U
                        if d == 1:      #east - need to rotate nbr cw
                            self.solmoves.append(nbrface)
                            self.do_moves([nbrface])
                            self._upper_edges_FRBL()
                            return
                        elif d == 3:    #west - need to rotate nbr ccw
                            self.solmoves.extend(self.string_to_movelist(nbrface + '\''))
                            self.do_moves(self.string_to_movelist(nbrface + '\''))
                            self._upper_edges_FRBL()
                            return
                        else:           #north or south - not possible
                            print "This is not a valid cube"
                            return

        #this moves any other edges to the down face
        for i in range(4):      #the four not top/bottom faces
            for d in range(4):  #each edge (NESW)
                c = self.faces_list[i].get_edge(d)
                if c == self.faces['U'].center:  #has a upper edge piece
                    homeface = self.sides[i]
                    nbrface = self.directions[homeface][d]
                    if e[1] != self.faces[nbrface].center:
                        if d == 0:        #north - homeface, right', down, right moves it
                            right = self.directions[homeface][1]
                            ms = self.string_to_movelist(homeface+right+'\''+'D'+right)
                            self.solmoves.extend(ms)
                            self.do_moves(ms)
                            self._upper_edges_D()
                            self._upper_edges_FRBL()
                            return
                        elif d == 1:      #east - need rotate nbr ccw
                            ms = self.string_to_movelist(nbrface + '\'')
                            self.solmoves.extend(ms)
                            self.do_moves(ms)
                            self._upper_edges_D()
                            self._upper_edges_FRBL()
                            return
                        elif d == 2:    #south - bottom edge, homeface,left,down,left' moves it
                            left = self.directions[homeface][3] #get west (left) face
                            ms = self.string_to_movelist(homeface+left+'D'+left+'\'')
                            self.solmoves.extend(ms)
                            self.do_moves(ms)
                            self._upper_edges_D()
                            self._upper_edges_FRBL()
                            return
                        elif d == 3:    #west - need to rotate nbr cw
                            self.solmoves.append(nbrface)
                            self.do_moves([nbrface])
                            self._upper_edges_D()
                            self._upper_edges_FRBL()
                            return
                        else:
                            print "This is not a valid cube"
                            return

    def _upper_edges_D(self):
        """Set edges under their 'home' and rotate them up"""
        for i in range(4):
            c = self.faces['D'].get_edge(i)
            if c == self.faces['U'].center:
                homeface = 'D'
                nbrface = self.directions[homeface][i]
                e = self.get_edge(homeface,nbrface)
                if(e[1] == self.faces[nbrface].center):
                    self.solmoves.extend([nbrface,nbrface])
                    self.do_moves([nbrface,nbrface])
                    self._upper_edges_D()

        upedge_present = False
        for i in range(4):
            c = self.faces['D'].get_edge(i)
            if c == self.faces['U'].center: #any remaining edge is not set
                homeface = 'D'
                nbrface = self.directions[homeface][i]
                upedge_present = True
                k = i
                while(e[1] != self.faces[nbrface].center):
                    k = (k + 1) % 4
                    self.solmoves.append('D')
                    self.D()
                    nbrface = self.directions[homeface][k]
                    e = self.get_edge(homeface,nbrface)
        if(upedge_present):
            self._upper_edges_D()
        return

    def _upper_corners(self):
        self._upper_corners_inplace()
        self._upper_corners_uslice()
        self._upper_corners_dface()

    def _upper_corners_inplace(self):
        """move in place corners on the FRLB U slice up to top"""
        while self._upper_corners_adjust():
            for i in range(4): #all non down non upper faces
                for ci in [2,3]: #southern corners
                    corncolor = self.faces_list[i].get_corner(ci)
                    if corncolor == self.faces['U'].center:
                        homeface = self.sides[i]
                        eorw = 3 if ci == 2 else 1
                        ewnbr = self.directions[homeface][eorw]
                        corn = self.get_corner(homeface,'D',ewnbr)
                        if (set([corn[1],corn[2]]) ==  #move this corner into place with DLD'L'
                           set([self.faces[homeface].center,self.faces[ewnbr].center])):
                            if eorw == 3: #west
                                movelist = self.string_to_movelist("D"+ewnbr+"D'"+ewnbr+"'")
                            else:         #east
                                movelist = self.string_to_movelist("D'"+ewnbr+"'"+"D"+ewnbr)
                            self.solmoves.extend(movelist)
                            self.do_moves(movelist)

    def _upper_corners_adjust(self):
        """rotate the d slice until a corner is in place, false if all gone"""
        corner_inplace = False
        rot = 0
        while rot < 4 and not corner_inplace:
            for i in range(4):
                for ci in [2,3]:
                    corncolor = self.faces_list[i].get_corner(ci)
                    if corncolor == self.faces['U'].center:
                        homeface = self.sides[i]
                        eorw = 3 if ci == 2 else 1
                        ewnbr = self.directions[homeface][eorw]
                        corn = self.get_corner(homeface,'D',ewnbr)
                        if (set([corn[1],corn[2]]) ==
                           set([self.faces[homeface].center,self.faces[ewnbr].center])):
                            corner_inplace = True
            if not corner_inplace:
                self.solmoves.append('D')
                self.D()
                rot += 1
        return corner_inplace

    def _upper_corners_uslice(self):
        """moves any upper corners in the U slice of the lateral faces to d slice"""
        c_in_uslice = False
        for i in range(4): #all non down non upper faces
            for ci in [0,1]: #northern corners
                corncolor = self.faces_list[i].get_corner(ci)
                if corncolor == self.faces['U'].center:
                    c_in_uslice = True
                    homeface = self.sides[i]
                    eorw = 3 if ci == 0 else 1
                    ewnbr = self.directions[homeface][eorw]
                    if ci == 0:
                        movelist = self.string_to_movelist(ewnbr+"D'"+ewnbr+"'")
                    else:
                        movelist = self.string_to_movelist(ewnbr+"'"+"D"+ewnbr)
                    self.solmoves.extend(movelist)
                    self.do_moves(movelist)
                    break
            if c_in_uslice:
                break

        if c_in_uslice:
            self._upper_corners_inplace()
            self._upper_corners_uslice()

    def _upper_corners_dface(self):
        """moves corners from D onto a lateral face"""
        #ex. corner 0 on D is below corner 3 on U
        dc_to_uc = {0 : 2, 1 : 3, 2 : 0, 3 : 1}

        down = self.faces['D']
        up = self.faces['U']
        c_in_dface = False
        c_adjusted = False
        for ci in range(4):
            corncolor = down.get_corner(ci)
            if corncolor == up.center:
                if up.get_corner(dc_to_uc[ci]) != up.center:
                    c_adjusted = True
                    w = self.directions['D'][3]
                    e = self.directions['D'][1]
                    if ci == 0: #nw
                        movelist = self.string_to_movelist(w+"D'"+w+"'")
                    elif ci == 1: #ne
                        movelist = self.string_to_movelist(e+"'"+"D"+e)
                    elif ci == 2: #sw
                        movelist = self.string_to_movelist(w+"'"+"D"+w)
                    else:       #se
                        movelist = self.string_to_movelist(e+"D'"+e+"'")
                    self.solmoves.extend(movelist)
                    self.do_moves(movelist)
                    break
                else:
                    c_in_dface = True
        if c_adjusted:
            self._upper_corners_inplace()
            self._upper_corners_dface
        elif c_in_dface:
            self.solmoves.append("D")
            self.D()
            self._upper_corners_dface()

########################END SOLVING UPPER/ BEGIN MIDDLE ##########################

    def solve_middle(self):
        """solve the middle layer"""
        #self.print_cube()
        adjusted = False
        rot = 0
        while not adjusted and rot < 4:
            for i in range(4): #for lateral faces
                homeside = self.sides[i]
                homeface = self.faces[homeside]
                west = self.directions[homeside][3]
                east = self.directions[homeside][1]
                if homeface.get_edge(2) == homeface.center:#south edge
                    e = self.get_edge(homeside,"D")
                    if e[1] == self.faces[west].center:
                        self._middle_edge_swap(3,homeside)
                        adjusted = True
                        break
                    elif e[1] == self.faces[east].center:
                        self._middle_edge_swap(1,homeside)
                        adjusted = True
                        break
            if not adjusted:
                rot += 1
                self.solmoves.append("D")
                self.D()
        if adjusted:
            self.solve_middle()
        else:   #we are either done or there is an edge that needs to move
            for i in range(4):
                homeside = self.sides[i]
                east = self.sides[(i+1) % 4]
                e = self.get_edge(homeside,east)
                if (e[0] != self.faces[homeside].center or
                   e[1] != self.faces[east].center):
                    self._middle_edge_swap(1,homeside)
                    self.solve_middle()
                    break

    def _middle_edge_swap(self,eorw,rel):
        """Do eorw edge swap relative to rel, eorw=1 east, eorw=3 west"""
        ewnbr = self.directions[rel][eorw]
        if eorw == 1:
            #D'R'DRDFD'F' relative to F
            movelist = self.string_to_movelist("D'"+ewnbr+"'"+"D"+ewnbr+"D"+rel+"D'"+rel+"'")
        elif eorw == 3:
            #DLD'L'D'F'DF relative to F
            movelist = self.string_to_movelist("D"+ewnbr+"D'"+ewnbr+"'"+"D'"+rel+"'"+"D"+rel)
        self.solmoves.extend(movelist)
        self.do_moves(movelist)

######################### END MIDDLE / BEGIN BOTTOM ###########################

    def solve_down(self):
        self._down_solve_cross()
        self._down_swap_corners()
        self._down_rotate_corners()
        self._down_swap_edges()

    def _down_solve_cross(self):
        pattern = self._down_pattern_type()
        if pattern == "cross":
            return
        relf = self.directions['D'][0] #north
        relr = self.directions['D'][3] #west
        if pattern == "Lpattern":
            movelist = self.string_to_movelist(relf+'D'+relr+"D'"+relr+"'"+relf+"'")
            self.solmoves.extend(movelist)
            self.do_moves(movelist)
            self._down_solve_cross()
            return
        if pattern == "vertical":
            self.solmoves.append("D")
            self.D() #now horizontal
        movelist = self.string_to_movelist(relf+relr+'D'+relr+"'"+"D'"+relf+"'")
        self.solmoves.extend(movelist)
        self.do_moves(movelist)
        return

    def _down_pattern_type(self):
        down = self.faces['D']
        count = 0
        for i in range(4):
            if down.get_edge(i) == down.center:
                count += 1
        if count < 2:
            return "Lpattern"
        if count == 4:
            return "cross"
        isVert = down.get_edge(0) == down.get_edge(2) #does north == south
        isHorz = down.get_edge(1) == down.get_edge(3) #east == west
        if isVert:
            return "vertical"
        if isHorz:
            return "horizontal"
        while(down.get_edge(2) != down.center):
            self.solmoves.append("D")
            self.D()
        if down.get_edge(1) == down.center:
            return "Lpattern"
        else:
            movelist = self.string_to_movelist("D'")
            self.solmoves.extend(movelist)
            self.do_moves(movelist)
            return "Lpattern"


    def _down_align_corners(self):
        nw = self.get_corner('F','L','D')
        ne = self.get_corner('F','R','D')
        sw = self.get_corner('B','L','D')
        se = self.get_corner('B','R','D')
        nwinplace = (set([nw[0],nw[1],nw[2]]) ==
                     set([self.faces['F'].center,self.faces['L'].center,self.faces['D'].center]))
        neinplace = (set([ne[0],ne[1],ne[2]]) ==
                     set([self.faces['F'].center,self.faces['R'].center,self.faces['D'].center]))
        swinplace = (set([sw[0],sw[1],sw[2]]) ==
                     set([self.faces['B'].center,self.faces['L'].center,self.faces['D'].center]))
        seinplace = (set([se[0],se[1],se[2]]) ==
                     set([self.faces['B'].center,self.faces['R'].center,self.faces['D'].center]))
        bools = [nwinplace,neinplace,swinplace,seinplace]
        count = 0
        for cond in bools:
            if cond:
                count += 1
        if count == 4:
            return "done"
        elif count < 2:
            self.solmoves.append('D')
            self.D()
            return self._down_align_corners()
        else:
            if nwinplace and neinplace:
                return "north"
            elif neinplace and seinplace:
                return "east"
            elif seinplace and swinplace:
                return "south"
            elif nwinplace and swinplace:
                return "west"
            else:
                return "diagonal"

    def _down_swap_corners(self):
        #import pdb; pdb.set_trace()
        cornerstate = self._down_align_corners()
        if cornerstate == "done":
            return
        if cornerstate == "north":
            rell = self.directions['D'][0] #south
            relr = self.directions['D'][2] #north
        elif cornerstate == "south":
            rell = self.directions['D'][2] #north
            relr = self.directions['D'][0] #south
        elif cornerstate == "east":
            rell = self.directions['D'][1] #west
            relr = self.directions['D'][3] #east
        elif cornerstate == "west":
            rell = self.directions['D'][3] #east
            relr = self.directions['D'][1] #west
        else: #diagonal
            rell = self.directions['D'][3] #west
            relr = self.directions['D'][1] #east
            movelist = self.string_to_movelist(rell+"D'"+relr+"'"+"D"+rell+"'"+"D'"+relr+"DD")
            self.solmoves.extend(movelist)
            self.do_moves(movelist)
            self._down_swap_corners()
            return

        movelist = self.string_to_movelist(rell+"D'"+relr+"'"+"D"+rell+"'"+"D'"+relr+"DD")
        self.solmoves.extend(movelist)
        self.do_moves(movelist)

    def _down_rotate_corners(self):
        down = self.faces['D']
        count = 0
        while(count < 4):
            while(down.get_corner(3) != down.center):
                self._down_swap_cycle()
            if(down.get_corner(3) == down.center):
                count += 1
                self.solmoves.append("D")
                self.D()

    def _down_swap_cycle(self):
        east = self.directions['D'][1]
        movelist = self.string_to_movelist(east+"'"+"U"+east+"U'")
        self.solmoves.extend(movelist)
        self.do_moves(movelist)

    def _down_swap_edges(self):
        count = 0
        correctdir = -1
        for i in range(4): #lateral faces
            if self.faces[self.sides[i]].get_edge(2) == self.faces[self.sides[i]].center:
                count += 1
                correctdir = i
        if count == 4:
            return
        if correctdir != -1:
            north = self.directions['D'][(correctdir + 1) % 4]
            east = self.directions['D'][(correctdir+2) % 4]
            south = self.directions['D'][(correctdir+3) % 4]
            if self.faces[north].get_edge(2) == self.faces[east].center:
                movelist = self.string_to_movelist(east+"2"+"D"+south+north+"'"+east+"2"+south+"'"+north+"D"+east+"2")
                self.solmoves.extend(movelist)
                self.do_moves(movelist)
            elif self.faces[north].get_edge(2) == self.faces[south].center:
                movelist = self.string_to_movelist(east+"2"+"D'"+south+north+"'"+east+"2"+south+"'"+north+"D'"+east+"2")
                self.solmoves.extend(movelist)
                self.do_moves(movelist)
            else:
                print "probably an invalid cube"
        else:
            correctdir = 0
            north = self.directions['D'][(correctdir + 1) % 4]
            east = self.directions['D'][(correctdir+2) % 4]
            south = self.directions['D'][(correctdir+3) % 4]
            movelist = self.string_to_movelist(east+"2"+"D'"+south+north+"'"+east+"2"+south+"'"+north+"D'"+east+"2")
            self.solmoves.extend(movelist)
            self.do_moves(movelist)
            self._down_swap_edges()

    def prune_solution_string(self):
        prev = ''
        prevprev=''
        prunedmoves = []
        for c in self.solmoves:
            if c != prev:
                prunedmoves.append(c)
            if c==prev and c==prevprev:
                prunedmoves.append("x")
            prevprev = prev
            prev = c
        self.solmoves = prunedmoves

    def ignore_c_length(self,c):
        ignore_c_string = [d for d in self.solmoves if d!=c]
        return len(ignore_c_string)



#
#corners_to_directions = {0 : (0,3), 1 : (0,1)
#                         2 : (2,3), 3 : (2,1)}
if __name__ == '__main__':
    c = solver()
    c.do_string("FBURBULLLBRUDUDBRLUDFFUD")
    c.solve()
