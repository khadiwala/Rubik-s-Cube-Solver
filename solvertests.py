import unittest
from solver import solver
from cube import cube

class solvertests(unittest.TestCase):

    def setUp(self):
        self.testcube = solver()
        self.solved = cube()
        self.strings = ["FRLUULRFFBLF","FBFRRBLF","UULLFBLUURRDDBDRDLLFBBB",
                        "DBLURFBLURUDDDBFRLLRUFFB","BRBULFFUDDUBRBURLDUBLDRU",
                        "BFRDUFRLURFBDURBFLRUULRDBFLRUFBRLDUFRDDRFBLDUFBDRLUBF",
                        "UBRDULRUDRURBFURDBFRDLUBFRLUDBFRDUBFRLUDBFRURDFBURLBF"]

    def test_solving_steps(self):
       cubes = []
       for s in self.strings:
            c = solver()
            c.do_string(s)
            cubes.append(c)
       for c in cubes:
            c.solmoves = []
            c._upper_edges_FRBL()
            c._upper_edges_D()
            self.check_top_edges(c)

            c._upper_corners()
            self.check_top_corners(c)

            c.solve_middle()
            self.check_middle(c)

            c.solve_down()
            temp = solver()
            self.assertTrue(c == temp)

    def check_top_edges(self,c):
        u = c.faces['U']
        for i in range(4):
            self.assertTrue(u.get_edge(i) == u.center)

    def check_top_corners(self,c):
        u = c.faces['U']
        for i in range(4):
            self.assertTrue(u.get_corner(i) == u.center)

    def check_middle(self,c):
        for i in range(4):
            f = c.faces[c.sides[i]]
            for j in range(3):
                self.assertTrue(f.squares[j][1] == f.center)

if __name__ == '__main__':
    unittest.main()
