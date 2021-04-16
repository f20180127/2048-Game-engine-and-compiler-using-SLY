#2048 game engine

import random

#Matrix class has been defined to add the basic fundamental funtionalities of the 2048 game.
class Matrix:
    
    #Defining the game matrix
    def __init__(self):
        self.n=4
        self.cell_value=[[0]*4 for i in range(4)]
        self.cell_name=[[[]]*4 for i in range(4)]
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0
    
    #Generating a random cell at empty position
    def generate_random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.cell_value[i][j] == 0:
                    cells.append((i, j))
        curr=random.choice(cells)
        i=curr[0]
        j=curr[1]
        self.cell_value[i][j]=2

    #Transpose of the game matrix
    def transpose_matrix(self):
        self.cell_value=[list(t)for t in zip(*self.cell_value)]
        self.cell_name=[list(t)for t in zip(*self.cell_name)]
    
    #Reversing the game matrix
    def reverse_matrix(self):               
        for index in range(4):
            i=0
            j=3
            while(i<j):
                self.cell_value[index][i],self.cell_value[index][j] = self.cell_value[index][j],self.cell_value[index][i]
                self.cell_name[index][i],self.cell_name[index][j] = self.cell_name[index][j],self.cell_name[index][i]
                i+=1
                j-=1

    #Compressing the game matrix to a side
    def compress_matrix(self):
        self.compress=False
        temp=[[0] *4 for i in range(4)]
        tempVar=[[[]]*4 for i in range(4)]
        for i in range(4):
            cnt=0
            for j in range(4):
                if self.cell_value[i][j]!=0:
                    temp[i][cnt]=self.cell_value[i][j]
                    if cnt!=j:
                        self.compress=True
                    cnt+=1
        self.cell_value=temp
        for i in range(4):
            cnt=0
            for j in range(4):
                if len(self.cell_name[i][j])!=0: 
                    tempVar[i][cnt]=self.cell_name[i][j]
                    cnt+=1
        self.cell_name=tempVar
    
        
    #Checking if 2 tiles can be merged
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.cell_value[i][j] == self.cell_value[i][j+1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.cell_value[i+1][j] == self.cell_value[i][j]:
                    return True
        return False

    #Merging the cells according to the operation given by user.
    def merge_matrix(self,option):
        self.merge=False
        for i in range(4):
            for j in range(4 - 1):
                if self.cell_value[i][j] == self.cell_value[i][j + 1] and self.cell_value[i][j] != 0:
                    if option=="ADD":
                        self.cell_value[i][j]=self.cell_value[i][j]+self.cell_value[i][j]
                        self.cell_name[i][j]=self.cell_name[i][j]+self.cell_name[i][j+1]
                    elif option=="MULTIPLY":
                        self.cell_value[i][j]=self.cell_value[i][j]*self.cell_value[i][j]
                        self.cell_name[i][j]=self.cell_name[i][j]+self.cell_name[i][j+1]
                    elif option=="DIVIDE":
                        self.cell_value[i][j]=int(self.cell_value[i][j]/self.cell_value[i][j])
                        self.cell_name[i][j]=self.cell_name[i][j]+self.cell_name[i][j+1]
                    elif option=="SUBTRACT":
                        self.cell_value[i][j]=self.cell_value[i][j]-self.cell_value[i][j]
                        self.cell_name[i][j]=[]
        
                    self.cell_name[i][j+1]=[]
                    self.cell_value[i][j + 1] = 0
                    self.score += self.cell_value[i][j]
                    self.merge = True
    
    #Assigning name to a tile
    def assign_name(self,name,x,y):
        for i in range(4):
            for j in range(4):
                for a in self.cell_name[i][j]:
                    if a==name:
                        return -1

        if self.cell_value[x][y]!=0:
            self.cell_name[x][y]=self.cell_name[x][y]+[name] 
            return 1;
        elif self.cell_value[x][y]==0:
            return 0;
    
    #Assigning value to a tile
    def assign_value(self,val,x,y):
        self.cell_value[x][y]=val 

        #Dropping the name of varianle if its tile value is made 0
        if val==0:
            self.cell_name[x][y]=[] 
        print("2048> The current state is:")
        self.display()
    
    #Display particular cell of 2048 matrix
    def peep(self,x,y):
        print(self.cell_value[x][y])

    #Display the 2048 matrix
    def display(self):
        print("-----------------")
        for i in range(4):
            for j in range(4): 
                if(j==0):
                    print('| ',end = '')
                print(self.cell_value[i][j],end=' | ')
            print()
            print("-----------------")
        print()

#Game class has been defined to perform game operations.
class Game:
    def __init__(self,gamepanel):
        self.gamepanel=gamepanel
        self.end=False
        self.won=False
        
    #Display the 2048 matrix
    def display(self):
        print("-----------------")
        for i in range(4):
            for j in range(4): 
                if(j==0):
                    print('| ',end = '')
                print(self.gamepanel.cell_value[i][j],end=' | ')
            print()
            print("-----------------")
        print()
    
    #Start the 2048 game
    def start(self):
        self.gamepanel.generate_random_cell()
        self.gamepanel.generate_random_cell()
        print("2048> The start state is:")
        self.display()
    
    #Perform a 2048 move
    def perform_move(self,option,x):
        if self.end or self.won:
            return

        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False
        presed_key=x
        if presed_key=='UP':
            self.gamepanel.transpose_matrix()
            self.gamepanel.compress_matrix()
            self.gamepanel.merge_matrix(option)
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_matrix()
            self.gamepanel.transpose_matrix()
        elif presed_key=='DOWN':
            self.gamepanel.transpose_matrix()
            self.gamepanel.reverse_matrix()
            self.gamepanel.compress_matrix()
            self.gamepanel.merge_matrix(option)
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_matrix()
            self.gamepanel.reverse_matrix()
            self.gamepanel.transpose_matrix()
        elif presed_key=='LEFT':
            self.gamepanel.compress_matrix()
            self.gamepanel.merge_matrix(option)
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_matrix()
        elif presed_key=='RIGHT':
            self.gamepanel.reverse_matrix()
            self.gamepanel.compress_matrix()
            self.gamepanel.merge_matrix(option)
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_matrix()
            self.gamepanel.reverse_matrix()
        else:
            pass
        
        #flag for checking if a value 2048 exists in a cell
        flag=0
        for i in range(4):
            for j in range(4):
                if(self.gamepanel.cell_value[i][j]==2048):
                    flag=1
                    break
        #2048 found -> finish the game.
        if(flag==1): 
            self.won=True
            print("Congrats. Game Won.")
            return
        for i in range(4):
            for j in range(4):
                if self.gamepanel.cell_value[i][j]==0:
                    flag=1
                    break
        #Game Lost
        if not (flag or self.gamepanel.can_merge()):
            self.end=True
            print("Game Over. You Lost.")
        if self.gamepanel.moved:
            self.gamepanel.generate_random_cell()
        print("2048> The current state is:")
        self.display()


#Lexer for 2048 game
from sly import Lexer
class BasicLexer(Lexer):
    tokens = {VAR,NUMBER,OPERATION,DIRECTION,ASSIGN,TO,IS,VALUE,IN,OPERATION_ERROR,DIRECTION_ERROR,ASSIGN_ERROR,IN_ERROR,VALUE_ERROR,IS_ERROR,TO_ERROR}
    ignore = '\t '
    literals = {'.',','}
    
    #Regular expression rules for tokens
    OPERATION = r'ADD|SUBTRACT|MULTIPLY|DIVIDE'
    OPERATION_ERROR=r'[aA][dD][dD]|[sS][uU][bB][tT][rR][aA][cC][tT]|[mM][uU][lL][tT][iI][pP][lL][yY]|[dD][iI][vV][iI][dD][eE]'
    DIRECTION = r'LEFT|RIGHT|UP|DOWN'
    DIRECTION_ERROR=r'[lL][eE][fF][tT]|[rR][iI][gG][hH][tT]|[uU][pP]|[dD][oO][wW][nN]'
    ASSIGN = r'ASSIGN'
    ASSIGN_ERROR=r'[aA][sS][sS][iI][gG][nN]'
    TO = r'TO'
    TO_ERROR=r'[tT][oO]'
    IS = r'IS'
    IS_ERROR=r'[iI][sS]'
    VALUE = r'VALUE'
    VALUE_ERROR=r'[vV][aA][lL][uU][eE]'
    IN = r'IN'
    IN_ERROR=r'[iI][nN]'
    VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'


#Parser for 2048 game
from sly import Parser

class BasicParser(Parser):
    tokens = BasicLexer.tokens
    
    #Overriding of error function in sly for arbitrary inputs.
    def error(self, token):
        raise Exception
        
    def __init__(self):
        self.env = { }
    
    @_('')
    def statement(self, p):
        pass

    #Full Stop Error
    @_('OPERATION DIRECTION')
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1
    
    @_('ASSIGN NUMBER TO NUMBER "," NUMBER')
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1
    
    @_('NUMBER "," NUMBER IS VAR')
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1
    
    @_('VALUE IN NUMBER "," NUMBER')
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1
    
    #Move Done
    @_('OPERATION DIRECTION "."')
    def statement(self, p):
        print("Thanks, move done, random tile added.")
        game2048.perform_move(p[0], p[1])
        return 0
    
    #Syntax Error
    @_('OPERATION_ERROR DIRECTION_ERROR "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('OPERATION_ERROR DIRECTION "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('OPERATION DIRECTION_ERROR "."')
    def statement(self, p):
        print("Syntax Error")
        return -1   
    
    #Assign Number to position
    @_('ASSIGN NUMBER TO NUMBER "," NUMBER "."')
    def statement(self, p):
        if(int(p[3])>=1 and int(p[3])<=4 and int(p[5])>=1 and int(p[5])<=4):
            print("Thanks, assignment done.")
            gamepanel.assign_value(int(p[1]), int(p[3])-1, int(p[5])-1)
            if(int(p[1])==2048):
                return 1;
            return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return 0
    
    #Syntax Error in Assign Number
    @_('ASSIGN_ERROR NUMBER TO_ERROR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('ASSIGN NUMBER TO_ERROR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('ASSIGN_ERROR NUMBER TO NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    #Name assign
    @_('NUMBER "," NUMBER IS VAR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            if p[4]=="VAR":
                print("NO, a keyword cannot be a variable name")
                return -1   
            else:
                flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("The tile mentioned is empty and cannot be named.")
                    return -1
                elif flag==-1:
                    print("The name mentioned already exists.")
                    return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
    
    @_('NUMBER "," NUMBER IS OPERATION_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
    
    @_('NUMBER "," NUMBER IS DIRECTION_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
        
    @_('NUMBER "," NUMBER IS ASSIGN_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
        
    @_('NUMBER "," NUMBER IS TO_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
        
    @_('NUMBER "," NUMBER IS IS_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
        
    @_('NUMBER "," NUMBER IS VALUE_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
        
    @_('NUMBER "," NUMBER IS IN_ERROR "."')
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            flag=gamepanel.assign_name(p[4],int(p[0])-1,int(p[2])-1)
            if flag==1:
                print("Thanks, naming done.")
                return 0
            elif flag==0:
                print("The tile mentioned is empty and cannot be named.")
                return -1
            elif flag==-1:
                print("The name mentioned already exists.")
                return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
        
    #Var is a Keyword error
    @_('NUMBER "," NUMBER IS OPERATION "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    @_('NUMBER "," NUMBER IS DIRECTION "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    @_('NUMBER "," NUMBER IS ASSIGN "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    @_('NUMBER "," NUMBER IS TO "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    @_('NUMBER "," NUMBER IS VALUE "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    @_('NUMBER "," NUMBER IS IN "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    @_('NUMBER "," NUMBER IS IS "."')
    def statement(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        return -1
    
    #Name assign Syntax Error
    @_('NUMBER "," NUMBER IS_ERROR VAR "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    #Value in index
    @_('VALUE IN NUMBER "," NUMBER "."')
    def statement(self, p):
        if(int(p[2])>=1 and int(p[2])<=4 and int(p[4])>=1 and int(p[4])<=4):
            print("Value is:", end=' ')
            gamepanel.peep(int(p[2])-1,int(p[4])-1)
            return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1
    
    #Syntax Error in Value IN
    @_('VALUE_ERROR IN_ERROR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('VALUE_ERROR IN NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('VALUE IN_ERROR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1


#stderr handling.
import sys 

def print_to_stderr(*a):
    print(*a, file = sys.stderr)
    return

#concat the cell values and cell names
def find(x,y):
    s = ""
    for i in range(4):
        for j in range(4):
            s+=str(x[i][j])
            s+=" "
    for i in range(4):
        for j in range(4):
            if len(y[i][j]) != 0:
                s+=str(i+1)
                s+=","
                s+=str(j+1)
                k=0
                for ele in y[i][j]: 
                    if(k==0):
                        s+=ele 
                    else:
                        s+=','
                        s+=ele
                    k=k+1
                s+=" "
    return s

#Starting the game by creating instance for lexer and parser and calling them for input tokens.
if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    print("2048> Hi, I am the 2048-game Engine.")
    gamepanel = Matrix()
    game2048 = Game(gamepanel)
    game2048.start()
    print_to_stderr(find(gamepanel.cell_value, gamepanel.cell_name))
    won = 0
    #Run the game until 2048 occurs
    while (won!=1):
        #User Input
        print('2048> Please type a command.')
        print('----> ', end='')
        text = input()
        
        try:
            won = parser.parse(lexer.tokenize(text))
        except:
            print("Sorry I don't understand that.")
            print_to_stderr("-1")
            continue
            
        if(won==1):
            print_to_stderr(find(gamepanel.cell_value, gamepanel.cell_name))
            print("Congrats. Game Won.")
        if(won==-1):
            print_to_stderr("-1")
        if(won==0):
            print_to_stderr(find(gamepanel.cell_value, gamepanel.cell_name))