from tkinter import *

img_num = 10
root = Tk()
imgs = [PhotoImage(file = ".\pic\0"+str(i)+".gif") for i in range(img_num)]

width,height = 10,10
playground = [[" " for y in range(height)] for x in range(width)]
img_map = [[" " for y in range(height)] for x in range(width)]
cv = Canvas(root, bg='g',width = 610, height = 610)#can change

def create_map(pg,w,h):
    tmp_map = []
    m = (w*h)//img_num
    print(m)
    for x in range(m):
        for i in range(img_num):
            tmp_map.append(x)
    random.shuffle(tmp_map)
    for x in range(w):
        for y in range(h):
            pg[x][y] = tmp_map[x*h + y]
