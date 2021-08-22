from rubik_solver import utils
import re

class CUBE:
    def __init__(self):
        self.set_cube()
    
    def set_cube(self):
        self.cube = { 
                    'U':['y','y','y','y','y','y','y','y','y'],
                    "L":['b','b','b','b','b','b','b','b','b'], 
                    "F":["r","r","r","r","r","r","r","r","r"], 
                    "R":["g","g","g","g","g","g","g","g","g"], 
                    "B":["o","o","o","o","o","o","o","o","o"], 
                    "D":["w","w","w","w","w","w","w","w","w"]
                    }

    def rotate_side(self, side):
        self.return_cube[side][0] = self.cube[side][6]
        self.return_cube[side][1] = self.cube[side][3]
        self.return_cube[side][2] = self.cube[side][0]
        self.return_cube[side][3] = self.cube[side][7]
        self.return_cube[side][4] = self.cube[side][4]
        self.return_cube[side][5] = self.cube[side][1]
        self.return_cube[side][6] = self.cube[side][8]
        self.return_cube[side][7] = self.cube[side][5]
        self.return_cube[side][8] = self.cube[side][2] 

    def rotate(self, side):
        self.return_cube = {}
        self.return_cube = {"U":self.cube['U'][:],"B":self.cube['B'][:],"F":self.cube['F'][:],"D":self.cube['D'][:],"L":self.cube['L'][:],"R":self.cube['R'][:]}
        if side == "U":
            self.rotate_side("U")

            self.return_cube["F"][0] = self.cube["R"][0]
            self.return_cube["F"][1] = self.cube["R"][1]
            self.return_cube["F"][2] = self.cube["R"][2]
            self.return_cube["L"][0] = self.cube["F"][0]
            self.return_cube["L"][1] = self.cube["F"][1]
            self.return_cube["L"][2] = self.cube["F"][2]
            self.return_cube["B"][0] = self.cube["L"][0]
            self.return_cube["B"][1] = self.cube["L"][1]
            self.return_cube["B"][2] = self.cube["L"][2]
            self.return_cube["R"][0] = self.cube["B"][0]
            self.return_cube["R"][1] = self.cube["B"][1]
            self.return_cube["R"][2] = self.cube["B"][2]

        elif side == "L":
            self.rotate_side("L")

            self.return_cube['U'][0] = self.cube['B'][8]
            self.return_cube['U'][3] = self.cube['B'][5]
            self.return_cube['U'][6] = self.cube['B'][2]
            self.return_cube['F'][0] = self.cube['U'][0]
            self.return_cube['F'][3] = self.cube['U'][3]
            self.return_cube['F'][6] = self.cube['U'][6]
            self.return_cube['D'][0] = self.cube['F'][0]
            self.return_cube['D'][3] = self.cube['F'][3]
            self.return_cube['D'][6] = self.cube['F'][6]
            self.return_cube['B'][2] = self.cube['D'][6]
            self.return_cube['B'][5] = self.cube['D'][3]
            self.return_cube['B'][8] = self.cube['D'][0]

        elif side == "F": 
            self.rotate_side("F")
            self.return_cube['U'][6] = self.cube['L'][8]
            self.return_cube['U'][7] = self.cube['L'][5]
            self.return_cube['U'][8] = self.cube['L'][2]
            self.return_cube['L'][2] = self.cube['D'][0]
            self.return_cube['L'][5] = self.cube['D'][1]
            self.return_cube['L'][8] = self.cube['D'][2]
            self.return_cube['R'][0] = self.cube['U'][6]
            self.return_cube['R'][3] = self.cube['U'][7]
            self.return_cube['R'][6] = self.cube['U'][8]
            self.return_cube['D'][0] = self.cube['R'][6]
            self.return_cube['D'][1] = self.cube['R'][3]
            self.return_cube['D'][2] = self.cube['R'][0]

        elif side == "R":
            self.rotate_side("R")

            self.return_cube['U'][2] = self.cube['F'][2]
            self.return_cube['U'][5] = self.cube['F'][5]
            self.return_cube['U'][8] = self.cube['F'][8]
            self.return_cube['F'][2] = self.cube['D'][2]
            self.return_cube['F'][5] = self.cube['D'][5]
            self.return_cube['F'][8] = self.cube['D'][8]
            self.return_cube['B'][0] = self.cube['U'][8]
            self.return_cube['B'][3] = self.cube['U'][5]
            self.return_cube['B'][6] = self.cube['U'][2]
            self.return_cube['D'][2] = self.cube['B'][6]
            self.return_cube['D'][5] = self.cube['B'][3]
            self.return_cube['D'][8] = self.cube['B'][0]

        elif side == "B":
            self.rotate_side("B")
            self.return_cube['U'][0] = self.cube['R'][2]
            self.return_cube['U'][1] = self.cube['R'][5]
            self.return_cube['U'][2] = self.cube['R'][8]
            self.return_cube['R'][2] = self.cube['D'][8]
            self.return_cube['R'][5] = self.cube['D'][7]
            self.return_cube['R'][8] = self.cube['D'][6]
            self.return_cube['L'][0] = self.cube['U'][2]
            self.return_cube['L'][3] = self.cube['U'][1]
            self.return_cube['L'][6] = self.cube['U'][0]
            self.return_cube['D'][6] = self.cube['L'][0]
            self.return_cube['D'][7] = self.cube['L'][3]
            self.return_cube['D'][8] = self.cube['L'][6]

        elif side == "D":
            self.rotate_side("D")
            self.return_cube['F'][6] = self.cube['L'][6]
            self.return_cube['F'][7] = self.cube['L'][7]
            self.return_cube['F'][8] = self.cube['L'][8]
            self.return_cube['R'][6] = self.cube['F'][6]
            self.return_cube['R'][7] = self.cube['F'][7]
            self.return_cube['R'][8] = self.cube['F'][8]
            self.return_cube['L'][6] = self.cube['B'][6]
            self.return_cube['L'][7] = self.cube['B'][7]
            self.return_cube['L'][8] = self.cube['B'][8]
            self.return_cube['B'][6] = self.cube['R'][6]
            self.return_cube['B'][7] = self.cube['R'][7]
            self.return_cube['B'][8] = self.cube['R'][8]

        self.cube = self.return_cube
   
    def get_solution(self):
        result = list(map(str, utils.solve("".join(self.cube["U"] + self.cube["L"]  + self.cube["F"]+ self.cube["R"]+ self.cube["B"]+ self.cube["D"]), "Kociemba")))
        ACROSS_BLOCK = {"R" : "L", "L":"R", "U":"D", "D":"U", "F":"B","B":"F" }
        short_v = []
        append = True
        for index, rotation in enumerate(result[:len(result) - 1]):
            if append:
                if  "".join(re.findall("[A-Z]", rotation)) == ACROSS_BLOCK[ "".join(re.findall("[A-Z]",result[index+1]))]:
                    short_v.append([rotation,result[index+1]])
                    append = False
                else:
                    short_v.append(rotation)
            else:
                append = True
        short_v.append(result[-1])
        return short_v
