import os
import operator
import os.path
import time

CRED = "\033[91m"
CEND = "\033[0m"
highscore = "highscore.txt"

player = True
p1_char = "\033[32m" + "X" + "\033[0m"
p2_char = "\033[34m" + "O" + "\033[0m"
playername1 = ""
playername2 = ""
round = 0
vertical = []
Vertic = False
diagonal = []
Diag = False
d_checkrow = 0
d_checkval = 0

os.system("clear")


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

def Choose_Zone(p, char):
    zone = input("\n" + get_Name(p) +  " [" + char + "]: ")
    if len(zone) < 2:
        Print_Board()
        print(CRED, "\nWrong input! (e.g. a1)", CEND)
        return Choose_Zone(p, char)
    zoneid = get_RowColumn(zone)
    #
    if int(zoneid[0]) == 0:
        Print_Board()
        print(CRED, "\nA sor indexe nem lehet 0!", CEND)
        return Choose_Zone(p, char)
    #
    if int(zoneid[0]) > size:
        Print_Board()
        print(CRED, "\nYour row is out of range!", CEND)
        return Choose_Zone(p, char)
    #
    max = 65 + (size - 1)
    if ord(zoneid[1]) > max:
        Print_Board()
        print(CRED, "\nYour column is out of range!", CEND)
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

def Char_Highlight(row, start, mylist, p):
    if mylist == board:
        for i in range(get_Max(size)):
            board[row][start] = get_Char(p, True)
            board[row][start] = CRED + board[row][start] + CEND
            start += 1
        Print_Board()
    elif mylist == vertical:
        for i in range(get_Max(size)):
            board[row][start] = get_Char(p, True)
            board[row][start] = CRED + board[row][start] + CEND
            row += 1
        Print_Board()
    elif mylist == diagonal:
        start2 = -1
        row2 = -1
        #
        if size >= 8:
            if IsUnderAxis(row, False) == False:
                start2 = row + start
                row2 = start
                #
                start = start2
                row = row2
            elif IsUnderAxis(row, False) == True:
                start2 = start
                row2 = ((row + 1) + start) - (get_Max(size) - 1) - (size - 8)
                #
                row = row2
        else:
            if IsUnderAxis(row, True) == False:
                start2 = row + start
                row2 = start
                #
                start = start2
                row = row2
            elif IsUnderAxis(row, True) == True:
                start2 = start
                row2 = ((row + 1) + start) - (get_Max(size) - 1) - (size - 3) + 1
                #
                row = row2
        for i in range(get_Max(size)):
            board[row][start] = get_Char(p, True)
            board[row][start] = CRED + board[row][start] + CEND
            row += 1
            start += 1
        Print_Board()

def IsUnderAxis(row, check): # False = 8+
    num = 0
    if check == False:
        num = 4 # Nagy pályán 4 a különbség
    else:
        num = 2 # Kis pályán 2
    #
    if row >= (size - num):
        return True
    else:
        return False

def Horizontal_Check(p, char, mylist, rev=False):
    start = 0 # Sor index
    found = False # Eggyezés
    count = 0 # Találat
    num = -1 # Soron belüli érték index
    s_hl = -1 # Start_Highlight index
    #
    for i,val in enumerate(mylist):
        if i == start:
            for n in range(len(val)):
                num += 1
                if val[n] == char:
                    found = True
                    count += 1
                    if s_hl == -1:
                        s_hl = n
                else:
                    found = False
                    count = 0
                    s_hl = -1
                ##################
                if found == True and count == get_Max(size):
                    if mylist == board:
                        Char_Highlight(i, s_hl, mylist, p)
                    elif mylist == vertical:
                        Char_Highlight(s_hl, i, mylist, p)
                    elif mylist == diagonal:
                        if rev == True:
                            Reverse_()
                            Char_Highlight(i, s_hl, mylist, p)
                            Reverse_()
                            Print_Board()
                        else:
                            Char_Highlight(i, s_hl, mylist, p)
                    Win(p)
                    return AskIfBackToMenu()
                if num == size - 1: # Végig ért a soron!
                    start += 1
                    found = False
                    count = 0
                    num = -1


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
            d_checkrow = p - (size - 1)
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
    Horizontal_Check(p, char, diagonal, True)

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
        Print_Board()
        print(CRED, "You can't place that here!", CEND)
        return Choose_Zone(GetID(char), char)

def GetID(char):
    if char == "X":
        return 1
    if char == "O":
        return 2

# Indexeli az oszlopokat. Pl.: A = 0
def IndexColumn(c):
    return ord(c) - 64

def get_Name(p):
    if p == 1:
        return playername1
    elif p == 2:
        return playername2

def get_Char(p, direct=False):
    if direct == False:
        if p == 1:
            return p1_char
        elif p == 2:
            return p2_char
    else:
        if p == 1:
            return "X"
        elif p == 2:
            return "O"

def Win(p):
    print("\n" + get_Name(p) +  " [" + get_Char(p) + "] Wins!")
    if os.path.exists("highscore.txt") == True:
        f = open(highscore, "a+")
        f.write(get_Name(p) + "\n")
        f.close
    else:
        f = open(highscore, "w")
        f.write(get_Name(p))
        f.close

def Start_Check():
    global size
    while True:
        try:
            size = int(input("Mekkora legyen a pálya? "))
        except ValueError:
            os.system("clear")
            print(CRED, "Csak számot adhatsz meg!", CEND)
        else:
            break
    if size > 26 or size < 3:
        os.system("clear")
        print(CRED, "Ekkora pályát nem definiálhatsz!\n", CEND)
        return Start_Check()

def Play_game():
    global size
    global tie_count
    global dlist_num
    global board

    size = 0
    Start_Check()
    board = CreateBoard(size)
    tie_count = size**2
    dlist_num = (size + size) -1

    while True:
        if player == True:
            Print_Board()
            Choose_Zone(1, get_Char(1))
        else:
            Print_Board()
            Choose_Zone(2, get_Char(2))

def Playername1(): # jatekos1neve bekeres
    global playername1
    print("Enter your name!")
    playername1 = str(input("Player 1: "))
    if len(playername1) < 3:
        os.system("clear")
        print(CRED, "Your name has to contain at least 3 characters!\n", CEND)
        return Playername1()
    os.system("clear")

def Playername2(): # jatekos2neve bekeres
    global playername2
    print("Enter your name!")
    playername2 = str(input("Player 2: "))
    if playername1 == playername2:
        os.system("clear")
        print(CRED, "Choose another name!\n", CEND)
        return Playername2()
    if len(playername2) < 3:
        os.system("clear")
        print(CRED, "Your name has to contain at least 3 characters!\n", CEND)
        return Playername2()
    os.system("clear")

def PrintMenu(): #menu nyomtatasa
    print("\n1. Play game")
    print("2. Highscore")
    print("3. Exit\n")

def Call_Highscore(): # a highscore meghivasa
    while True:
        if os.path.exists("highscore.txt") == False:
            print(CRED, "There is no one on the highscore list yet!\n", CEND)
            AskIfBackToMenu()
        else:
            tempscores = []
            tempscoresdict = {}
            with open(highscore) as f:
                content = f.read().splitlines()

            for i in content:
                if tempscores.count(i) == 0:
                    tempscores.append(i)
                    tempscores.append(content.count(i))
                    tempscoresdict.update({str(i) : int(content.count(i))})
            count = 0
            for key, value in sorted(tempscoresdict.items(), key=lambda kv: kv[1], reverse=True):
                count += 1
                print(str(count) + ". " "%s: %s" % (key, value))
            AskIfBackToMenu()

def AskIfBackToMenu(): #vissza a menube kerdes
    while True:
        backtomenu = str(input("Back to menu? y/n\n"))
        backtomenu = backtomenu.lower()
        if backtomenu == "y":
            os.system("clear")
            Call_Menu()
        elif backtomenu == "n":
            os.system("clear")
            print("Come back anytime!")
            exit()
        else:
            os.system("clear")
            print(CRED, "Wrong input!\n", CEND)
            return AskIfBackToMenu()

def Call_Menu(): # menu meghivasa - jatek indulasa
    while True:
        os.system("clear")
        print("Choose one! (1,2,3)\n")
        PrintMenu()
        menuinput = input()
        if menuinput == "1":
            os.system("clear")
            Playername1()
            Playername2()
            Play_game()
            break
        elif menuinput == "2":
            os.system("clear")
            Call_Highscore()
            break
        elif menuinput == "3":
            os.system("clear")
            print("Come again!\n")
            exit()
        else:
            return Call_Menu()

def StartupGraphics():
    col = 31
    os.system("clear")
    for i in range(6):
        print(f'\033[{col}m 888   d8b        888                   888                    \n888   Y8P        888                   888                    \n888              888                   888                    \n888888888 .d8888b888888 8888b.  .d8888b888888 .d88b.  .d88b.  \n888   888d88P"   888       "88bd88P"   888   d88""88bd8P  Y8b \n888   888888     888   .d888888888     888   888  88888888888 \nY88b. 888Y88b.   Y88b. 888  888Y88b.   Y88b. Y88..88PY8b.     \n "Y888888 "Y8888P "Y888"Y888888 "Y8888P "Y888 "Y88P"  "Y8888  \n', CEND)
        col += 1
        time.sleep(0.35)
        os.system("clear")

StartupGraphics()
Call_Menu()
