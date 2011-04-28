import copy
from PIL import Image
class face:

    def __init__(self,color):
        self.squares = []
        self.center = color #fixed point
        for i in range(3):
            self.squares.append([color]*3)
        self.colors = {'R' : (255,0,0),'B' : (0,0,255),
                       'O' : (255,165,0),'G' : (0,255,0),
                       'W' : (255,255,255),'Y' : (255,255,0)}
    def __eq__(self,other):
        ret = True
        for c1,c2 in zip(self.squares,other.squares):
            for p1,p2 in zip(c1,c2):
                ret = ret and (p1 == p2)
        return ret

    def print_face(self):
        for i in range(len(self.squares)):
            for column in self.squares:
                print column[i] + " ",
            print ""

    def print_face_string(self):
        s = ""
        for i in range(len(self.squares)):
            s += "  "
            for column in self.squares:
                s += column[i]
                s += " "
            s += "\n"
        return s

    def shift_face(self,colors):
        """input a face as list of 3 columns"""
        self.squares = colors

    def shift_col(self,col,colors):
        """replace the column col with list colors"""
        self.squares[col] = colors

    def shift_row(self,row,colors):
        """replace the row row with list colors"""
        for i in range(3):
            self.squares[i][row] = colors[i]

    def rotate(self,rotations):
        """rotate rotations * 90 degrees"""
        for i in range(rotations):
            self._rotate90()

    def get_row(self,row):
        return [col[row] for col in self.squares]

    def get_col(self,col):
        return self.squares[col]

    def get_edge(self,direction):
        """
        return the edge corresponding to direction
        0 - north
        1 - east
        2 - south
        3 - west
        """
        if direction == 0:
            return self.squares[1][0]
        elif direction == 1:
            return self.squares[2][1]
        elif direction == 2:
            return self.squares[1][2]
        elif direction == 3:
            return self.squares[0][1]
        else:
            print "Edge finding error"
            return '0'

    def get_corner(self,corner_index):
        """
        return the corner corresponding to the index
        0 - NorthWest
        1 - NorthEast
        2 - SouthWest
        3 - SouthEast
        """
        index_to_coords = {0 : (0,0), 1 : (2,0),
                           2 : (0,2), 3 : (2,2)}
        if corner_index in range(4):
            p = index_to_coords[corner_index]
            return self.squares[p[0]][p[1]]
        else:
            print "Corner finding error"
            return '0'

    def face_to_image(self,distort='no'):
        """returns a BMP based on this face"""
        sticker_dim = 30
        face_dim = 90
        black = (0,0,0)
        pix_lis = []
        ret = Image.new("RGB",(face_dim,face_dim))

        for x in range(face_dim):
            for y in range(face_dim):
                #in between stickers black, else a color
                if x % sticker_dim <= 1 or y % sticker_dim <= 1:
                    pix_lis.append(black)
                else:
                    pix_lis.append(self.colors[self.squares[y/sticker_dim][x/sticker_dim]])
        ret.putdata(pix_lis)
        if distort == 'no':
            return ret
        elif distort == 'right':
            return ret.transform(ret.size,Image.PERSPECTIVE,(1,0,0,0,1,0,-.004,0))
        elif distort == 'top':
            ret = ret.rotate(180)
            return (ret.transform(ret.size,Image.PERSPECTIVE,(1,0,0,0,1,0,0,-.004))).rotate(180)
        elif distort == 'bottom':
            return (ret.transform(ret.size,Image.PERSPECTIVE,(1,0,0,0,1,0,0,-.004))).transpose(Image.FLIP_LEFT_RIGHT)
        else:
            return None


    #clockwise
    def _rotate90(self):
        """rotate 90 degrees"""
        temp = copy.deepcopy(self.squares)
        self.squares[0][0] = temp[0][2]
        self.squares[0][1] = temp[1][2]
        self.squares[0][2] = temp[2][2]
        self.squares[1][0] = temp[0][1]
        self.squares[1][1] = temp[1][1]
        self.squares[1][2] = temp[2][1]
        self.squares[2][0] = temp[0][0]
        self.squares[2][1] = temp[1][0]
        self.squares[2][2] = temp[2][0]

if __name__ == '__main__':
    f = face('W')
    im = f.face_to_image()
    im.save("w.BMP")
