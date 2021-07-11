import os

os.system("clear")
win = False
player = True
p1_char = "X"
p2_char = "O"
playername1 = ""
playername2 = ""
round = 0
vertical = []
Vertic = False
diagonal = []
Diag = False
d_checkrow = 0
d_checkval = 0

#CALLBACKS#########################################################################################################################

# Input alapján vissza adja szétválasztva a sort és az oszlopot
def get_RowColumn(input):
    row = ""
    column = ""
    for i,j in enumerate(input):
        if i == 0:
            column = j
        else:
            row += str(j)
    return row, column.upper()

# Létrehozza az n*n-es listát
def CreateBoard(s):
    global board
    board = []    
    for i in range(s):
        board.append([])
        for n in range(s):
            board[i].append("N")
    return board

# Oszlop indexelés
def Abc(s):
    a_list = "  "
    i = 0
    num = 65 # 65 = A
    while i != s:
        a_list += chr(num) + " "
        num += 1
        i += 1
    return a_list

# Tábla frissítés
def Print_Board():
    os.system("clear")
    count = 0
    line = 2
    game = ""
    global board
    for i in range(len(board)):
        row = board[i]
        if i == 0:
            game += "\n " + Abc(size) + "\n" + str(line-1) + " "
        for j in range(len(row)):
            num = board[i][j]
            if count == size: #Max line
                count = 0
                if line <= 9:
                    game += "\n" + str(line) + " "
                else:
                    game += "\n" + str(line)
                line += 1
            count += 1
            if num == "N":
                game += "|_"
            else:
                game += "|" + num
            if j == size-1:
                game += "|"
    print(game)
    print(diagonal)
    #print(board)

def Choose_Zone(p, char):
    Print_Board()
    zone = input("\n" + get_Name(p) +  " [" + char + "]: ")
    zoneid = get_RowColumn(zone)
    #
    if int(zoneid[0]) == 0:
        print("A sor indexe nem lehet 0!")
        return Choose_Zone(p, char)
    #
    if int(zoneid[0]) > size:
        print("Your row is out of range!")
        return Choose_Zone(p, char)
    #
    max = 65 + (size - 1)
    if ord(zoneid[1]) > max:
        print("Your column is out of range!")
        return Choose_Zone(p, char)
    #
    Choose(int(zoneid[0]), IndexColumn(zoneid[1]), char)
    Print_Board()
    global round
    round += 1
    global player
    player = not player
    global tie_count
    tie_count -= 1
    if tie_count == 0:
        print("TIE!")
        exit()
    if round >= 5:
        Check_Winner(p, char)

def get_Max(size):
    if size <=7:
        return 3
    else:
        return 5
    
def Horizontal_Check(p, char, mylist):
    start = 0 # Sor index
    found = False # Eggyezés
    count = 0 # Találat
    num = -1 # Soron belüli érték index
    #
    for i,val in enumerate(mylist):
        if i == start:
            for n in range(len(val)):
                num += 1
                if val[n] == char:
                    found = True
                    count += 1
                    print(count)
                else:
                    found = False
                    count = 0
                ##################
                if found == True and count == get_Max(size):
                    if mylist == board:
                        print(i,".sor. Győzelem!")
                    elif mylist == vertical:
                        print(i,".oszlop. Győzelem!")
                    elif mylist == diagonal:
                        print("Átló Győzelem!")
                    exit()
                if num == size - 1: # Végig ért a soron!
                    start += 1
                    found = False
                    count = 0
                    num = -1
    #print(diagonal)

def Add_Vertical(row, val):
    global Vertic, vertical
    if Vertic == False: # Nincs létrehozva a lista
        for i in range(size):
            vertical.append([])
        Vertic = True
        Add_Vertical(row, val)
    else: 
        for i in range(len(vertical)):
            if i == row:
                vertical[i].append(val)
            
def Vertical_Read(row):
    for i in range(len(board)):
        val = board[i]
        for j, letter in enumerate(val):
            if j == row:
                Add_Vertical(row, letter)

def Vertical_Check(p, char):
    global Vertic, vertical
    Vertic = False
    vertical = []
    for i in range(size):
        Vertical_Read(i) 
    Horizontal_Check(p, char, vertical)

def get_Phase(p, view=False): # False = Balról jobbra!
    global d_checkrow, d_checkval
    if view == False: 
        d_checkval = p
        if p <= (size - 1):
            d_checkrow = 0
    #-Tábla tengely-----------------------------
        elif p <= (dlist_num - 1):
            d_checkrow = p - 4
            d_checkval = 0

def Correct_Diagonal(mylist):
    count = 0
    for i, row in enumerate(mylist):
        if len(row) < get_Max(size):
            mylist[i].clear()
            count += 1
        elif len(row) >= get_Max(size) or len(row) < size:
            for n in range(size - len(row)):
                mylist[i].append("")
    i = 0
    while i != count:
        for n in mylist:
            if n == []:
                mylist.remove(n)
        i += 1

def Add_Diagonal(row, val):
    global Diag, diagonal
    if Diag == False: # Nincs létrehozva a lista
        for i in range(dlist_num):
            diagonal.append([])
        Diag = True
        Add_Diagonal(row, val)
    else: 
        for i in range(len(diagonal)):
            if i == row:
                diagonal[i].append(val)
    print(diagonal, "\n")

def Diag_Left_Read(p, view=False):
    global d_checkrow, d_checkval
    count = 0
    get_Phase(p)
    for i in range(len(board)):
        if view == True:
            board[i].reverse()
        val = board[i]
        for j, letter in enumerate(val):
            if i == d_checkrow and j == d_checkval:
                d_checkval += 1
                d_checkrow += 1
                Add_Diagonal(p, letter)
    if view == True:
        Reverse_()

def Reverse_():
    for i in range(len(board)):
        board[i].reverse()

def Diagonal_Check(p, char):
    global Diag, diagonal
    Diag = False
    diagonal = []
    #Bal------------------------------------
    for i in range(dlist_num): # Ez a Phase!
        Diag_Left_Read(i)
    Correct_Diagonal(diagonal)
    Horizontal_Check(p, char, diagonal)
    #Jobb------------------------------------
    diagonal = []
    Diag = False
    for i in range(dlist_num): # Ez a Phase!
        Diag_Left_Read(i, True)
    Correct_Diagonal(diagonal)
    print(diagonal)
    Horizontal_Check(p, char, diagonal)

def Check_Winner(p, char):
    Horizontal_Check(p, char, board)
    Vertical_Check(p, char)
    Diagonal_Check(p, char)

# Elhelyezi a karaktert a táblán
def Choose(sor, oszlop, char):
    sor -= 1
    oszlop -= 1
    global board
    if board[sor][oszlop] == "N":
        board[sor][oszlop] = char
    else:
        print("Wrong input!")
        return Choose_Zone()

# Indexeli az oszlopokat. Pl.: A = 0
def IndexColumn(c):
    return ord(c) - 64

def GetID(char):
    if char == "X":
        return 1
    elif char == "O":
        return 2

def get_Name(p):
    if p == 1:
        return playername1
    elif p == 2:
        return playername2

def get_Char(p):
    if p == 1:
        return p1_char
    elif p == 2:
        return p2_char

def Win(p):
    print("\n" + get_Name(p) +  " [" + get_Char(p) + "] Wins!")
    global win
    win = True

##################################################################################################################################
def Start_Check():
    global size
    while True:
        try:
            size = int(input("Mekkora legyen a pálya? "))
        except ValueError:
            print("Csak számot adhatsz meg!")
        else:
            break
    if size > 26 or size < 3:
        print("Ekkora pályát nem definiálhatsz!")
        return Start_Check()

size = 0
Start_Check()
board = CreateBoard(size)
tie_count = size**2
dlist_num = (size + size) -1

while True:
    if player == True:
        Choose_Zone(1, get_Char(1))
    else:
        Choose_Zone(2, get_Char(2))