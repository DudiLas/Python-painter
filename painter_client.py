import pygame
import socket
import select
import random
#------constants------
WINDOW_WIDTH = 1080
WINDOW_HEIGTH = 720
#colors
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,51)
PINK = (255,51,153)
BLUE = (51,51,255)
PURPLE = (153,0,153)
ORANGE = (255,128,0)
BROWN = (153,76,0)
GREEN = (0,255,0)
LIGHT_BLUE = (102,255,255)
GRAY = (128,128,128)
DARK_GREEN = (51,102,0)

WORDS = ["dog", "cat", "apple", "horse", "food", "egg", "piano", "role", "hang", "meat", "cheat", "act", "trouble", "camp", "tire", "curtain"]
LEFT = 1
SCROLL = 2
RIGHT = 2

RAD = 3

COLOR_WIDTH = 50
COLOR_HEIGTH = 50

colors_list = [(RED,(200,620)),(YELLOW,(250,620)),(PINK,(300,620)),(BLUE,(350,620)),(PURPLE,(400,620)),(ORANGE,(450,620)) ,\
    (BLACK, (200, 670)), (BROWN,(250,670)), (GREEN,(300,670)), (LIGHT_BLUE,(350,670)) ,(GRAY,(400,670)) ,(DARK_GREEN,(450,670))]
MAX_lENGTH = 1024



lft = "" # leftover from the last send



def reset_screen(color):
    screen.fill(color)
    pygame.display.flip()

def dislpay_color_board(colors_list):
    for color in colors_list:
        display_color(color)

def display_color(color):
    pygame.draw.rect(screen, color[0], (color[1][0],color[1][1], COLOR_WIDTH, COLOR_HEIGTH))

def find_color(pos, colors_list):
    x = pos[0]
    y = pos[1]
    for color in colors_list:
        if x>= color[1][0] and x <= color[1][0]+49 and y>= color[1][1] and y <= color[1][1]+49:
            return color[0]
    return 0

def display_board(word):
    global won
    reset_edge()
    pygame.draw.rect(screen, BLACK, (197, 0, 3, 720))
    pygame.draw.rect(screen, BLACK, (200, 617, 680, 3))
    pygame.draw.rect(screen, BLACK, (200, 97, 680, 3))
    pygame.draw.rect(screen, BLACK, (880, 0, 3, 720))
    dislpay_color_board(colors_list)
    img = pygame.image.load("D:/untitled/garbage.png")
    screen.blit(img,(500,620))


    print(word)
    print_guessed()
    print_job()

    if won == 1:
        print_text("won", (960, 160), 60)


    print_word(len(word), word)




    pygame.display.flip()

def reset_edge():
    pygame.draw.rect(screen, WHITE, (0, 0, 1080, 100))
    pygame.draw.rect(screen, WHITE, (0, 620, 1080, 100))
    pygame.draw.rect(screen, WHITE, (0, 0, 200, 720))
    pygame.draw.rect(screen, WHITE, (880, 0, 200, 720))


def check_for_erase(pos,word):
    if pos[0] > 499 and pos[0] < 600 and pos[1] >619 and pos[1] < 720:
        reset_screen(WHITE)
        display_board(word)
        return 1
    return 0

def print_by_data(data,word):
    global lft,round

    temp = data[-1]
    data = data[:-1]
    data[0] = lft + data[0]
    lft = temp

    for cir in data:

        if cir == "res":
            reset_screen(WHITE)
            display_board(word)
        elif cir == "move":

            round = 0
        else:
            cir = cir.split("*")
            pygame.draw.circle(screen, (int(cir[0]), int(cir[1]), int(cir[2])), (int(cir[3]), int(cir[4])), int(cir[5]))
            pygame.display.flip()


# letters is a list of known letters of the word
def print_word(length, letters):
    heigth = 60
    len_of_let = 40
    space = 10
    start_pos = 540 - length*25
    for i in range(0,length):
        if letters[i] == "":
            pygame.draw.rect(screen, BLACK, (start_pos + i*len_of_let + i*space, heigth, len_of_let, 3))
        else:
            print_text(letters[i],(start_pos + i*len_of_let + i*space+20, heigth), 60)

def print_text(txt,pos,size):
    font = pygame.font.Font('D:/untitled/lala.ttf', size)

    text = font.render(txt, True, BLACK, WHITE)

    textRect = text.get_rect()

    textRect.center = pos

    screen.blit(text, textRect)
def generate_word():
    index = random.randint(0, len(WORDS) - 1)
    word = WORDS[index]
    return list(word)

def print_guessed():
    global guess_word
    inp_x = 900
    inp_y = 640

    for ch in guess_word:
        print_text(ch,(inp_x,inp_y),30)
        inp_x += 27

def print_job():
    global is_turn
    if is_turn ==1 :
        print_text("draw", (960, 60), 60)
    else:
        print_text("guess", (960, 60), 60)




#init screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGTH)
screen =  pygame.display.set_mode(size)

client_socket = socket.socket()
client_socket.connect(("127.0.0.1", 8820))
cl_num = int(client_socket.recv(MAX_lENGTH).decode().split("*")[1])


pygame.display.set_caption('Show Text')



reset_screen(WHITE)

if cl_num == 0:
# check if stop accpeting clients and start the game
    input("write anything if you want to start")
    client_socket.send("start".encode())
else:
    client_socket.recv(1024).decode()



temp = 0
col = BLACK# defult color
fin = False
pressed = 0
state =  0
button = 0
pos = (0,0)
res = 0
len_word =0
guess_word = ""
won = 0
win_word = ""
round = 1
data = []
is_turn = 0
#main loop
while not fin:
    reset_screen(WHITE)
    lft = ""
    round = 1
    won = 0
    print("before")
    if len(data) > 0 and "turn" in data[-1]:
        dat = data[-1]

    else:
        dat =  client_socket.recv(MAX_lENGTH).decode()
    print("after")

    turn = int(dat.split("*")[1])
    dat = dat.split("*")
    word = []
    if turn == cl_num:
        is_turn = 1
        word = generate_word()
        client_socket.send(("word*"+ "".join(word)).encode())
    else:
        is_turn = 0
        if len(dat) > 3 and dat[2] == "word":
            win_word = dat[3]
        else:
            win_word = client_socket.recv(MAX_lENGTH).decode().split("*")[1]

        print(dat)
        print(win_word)
        for i in range(len(win_word)):
            word.append("")
    print("after2")
    display_board(word)
    while round == 1:
        if fin == True:
            break
        events = pygame.event.get()
        rlist, wlist, elist = select.select([client_socket], [client_socket], [])
        for event in events:
            rlist, wlist, elist = select.select([client_socket], [client_socket], [])
            #quiting the game by pressing the x button
            if event.type == pygame.QUIT:
                fin = True
                continue
            if turn == cl_num:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = True
                    button = event.button
                    pos = pygame.mouse.get_pos()
                    temp = find_color(pos, colors_list)
                    if temp != 0:
                        col = temp
                    res = check_for_erase(pos,word)

                if event.type == pygame.MOUSEBUTTONUP:
                    state = False


                pos = pygame.mouse.get_pos()
                if state and button == LEFT and pos[0]> 199 and pos[0] <880 and pos[1] >=100 and pos[1]<620:
                    #sends the data by the format:col0*col1*col2*x*y*radius
                    client_socket.send((str(col[0]) + "*" + str(col[1]) + "*" +str(col[2]) +  "*" + str(pos[0]) + "*" + str(pos[1]) + "*" + str(RAD) + "/").encode())

                    pygame.draw.circle(screen,col, pos, RAD)
                    pygame.display.flip()
                if res == 1:
                    client_socket.send(("res/").encode())
                    res = 0
            else:
                if event.type == pygame.KEYDOWN and won == 0:

                    if(event.key == 8):
                        #delete letter
                        if(len(guess_word) != 0):
                            guess_word = guess_word[:-1]

                    elif(event.key == 13):

                        if(guess_word == win_word):
                            won = 1
                            word = list(win_word)


                            client_socket.send(("won*" + str(cl_num)).encode())

                        guess_word = ""


                    elif len(guess_word)< 7:
                        guess_word += (chr(event.key))
                    display_board(word)
                    pygame.display.flip()

        if client_socket in rlist:

            data = client_socket.recv(MAX_lENGTH).decode()
            if data == "exit":
                fin = True
                continue
            elif(data != ""):

                data = data.split("/")
                print_by_data(data, word)


client_socket.send("exit".encode())
client_socket.close()








pygame.quit()