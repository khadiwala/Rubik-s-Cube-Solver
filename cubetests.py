import unittest
from cube import cube

class cubetests(unittest.TestCase):

    def setUp(self):
        self.testcube = cube()

    def test_construction(self):
        """checks that every square on a each face and different for each face"""

        #check that the cube is "solved"
        for face in self.testcube.faces_list:
            for col in range(3):
                for row in range(3):
                    current = face.squares[0][0]
                    self.assertEqual(face.squares[col][row],current)

        #check that all faces are different colors
        facecolors = []
        for face in self.testcube.faces_list:
            for c in facecolors:
                self.assertNotEqual(c,face.squares[0][0])
            facecolors.append(face.squares[0][0])

    def test_get_edge(self):
        e = self.testcube.get_edge('F','L')
        self.assertEquals(e,('R','G'))
        e = self.testcube.get_edge('F','U')
        self.assertEquals(e,('R','W'))
        e = self.testcube.get_edge('U','F')
        self.assertEquals(e,('W','R'))
        e = self.testcube.get_edge('B','L')
        self.assertEquals(e,('O','G'))
        e = self.testcube.get_edge('F','B')#invalid input
        self.assertEquals(e,('0','0'))

    def test_get_corner(self):
        c = self.testcube.get_corner('F','L','U')
        self.assertEquals(c,('R','G','W'))
        c = self.testcube.get_corner('F','R','D')
        self.assertEquals(c,('R','B','Y'))
        c = self.testcube.get_corner('B','R','U')
        self.assertEquals(c,('O','B','W'))
        c = self.testcube.get_corner('B','F','D')#invalid input
        self.assertEquals(c,('0','0','0'))

    def cycle1(self):
        """This 3 cycle taken from http://cubefreak.net/bld/3op_guide.html#CP3"""
        cyclestring = "RB'RF2R'BRF2R2"
        moves = self.testcube.string_to_movelist(cyclestring)
        self.testcube.do_moves(moves)

    def test_rotations(self):
        solved = cube() #solved cube for comparisons

        #each rotation is a different rotation function (F,R,L,etc)
        for rotation in self.testcube.rotations.itervalues():
            rotation()
            self.assertTrue(not self.testcube == solved)
            rotation()
            rotation()
            rotation()
            self.assertTrue(self.testcube == solved)

        #3-cycle: doing this move sequence 3 times brings cube back to solved
        self.cycle1()
        self.assertFalse(self.testcube == solved)
        self.cycle1()
        self.assertFalse(self.testcube == solved)
        self.cycle1()
        self.assertTrue(self.testcube == solved)
        del solved

    def test_do_moves(self):
        manual = cube()  #manual moves for comparison
        self.testcube.do_moves(['F','F','R','L'])
        manual.F()
        manual.F()
        manual.R()
        manual.L()
        self.assertTrue(manual == self.testcube)
        del manual

    def test_stringstomoves(self):
        numcube = cube()    #operations like F2,F3 tested
        ccwcube = cube()    #operations like F'
        correct = cube()    #manual rotation for checks

        #test basic string to list parsing
        teststring = "FRLFUDBF"
        moves = correct.string_to_movelist(teststring)
        for move,char in zip(moves,teststring):
            self.assertTrue(move == char)

        #this tests counter clockwise and triple rotation for all sides
        #(ccw and tripple rotation {ex F3 = F 3 times} are the same)
        for side in correct.sides:
            ccwmoves = ccwcube.string_to_movelist(side+"\'")
            nummoves = numcube.string_to_movelist(side+"3")
            ccwcube.do_moves(nummoves)
            numcube.do_moves(nummoves)
            correct.rotations[side]() #F3 is the same as F'
            correct.rotations[side]()
            correct.rotations[side]()

            #F3 == F F F == F'
            self.assertTrue(correct == numcube)
            self.assertTrue(correct == ccwcube)

            #revert all three back to solved
            correct.rotations[side]()
            ccwcube.rotations[side]()
            numcube.rotations[side]()
            self.assertTrue(correct == self.testcube)
            self.assertTrue(correct == numcube)

        #this tests double rotations (ex. F2 is F 2 times)
        for side in correct.sides:
            moves = numcube.string_to_movelist(side+"2")
            numcube.do_moves(moves)
            correct.rotations[side]()
            correct.rotations[side]()
            self.assertTrue(correct == numcube)

            #revert both back to solved
            correct.rotations[side]()
            correct.rotations[side]()
            numcube.do_moves(moves)
            self.assertTrue(correct == numcube)
        del numcube
        del correct
        del ccwcube

if __name__ == '__main__':
    unittest.main()
