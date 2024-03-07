import cv2
import sys
import imutils
import turtle as t
sys.setrecursionlimit(10000)

def setting():
    global th1, th2, img2
    while True:
        temp = cv2.waitKey()
        if temp == ord("q"):
            th1+=10
        elif temp == ord("w"):
            th1-=10
        elif temp == ord("e"):
            th2+=10
        elif temp == ord("r"):
            th2-=10
        elif temp == ord("m"):
            cv2.destroyAllWindows()
            return
        img2 = cv2.Canny(img,th1,th2)
        cv2.imshow(f'q : +th1 / w : -th1 / e : +th2 / r : -th2 / m : confim',img2)

img = cv2.imread("temp.png")

if img.shape[1] > 900 or img.shape[0] > 900:
    if img.shape[1] > img.shape[0]:
        img = imutils.resize(img, width=900)
    else:
        img = imutils.resize(img, height=900)

th1 = 210
th2 = 710
img2 = cv2.Canny(img,th1,th2)
setting()
height, width = img2.shape
t.setup(width=width, height=height)
t.speed(100)


posx = [1, 1, 0,-1,-1]
posy = [0, 1, 1, 1, 0]

def draw(y,x,prev_dirc):
    for i in range(5):
        final_i = (prev_dirc+i)%5
        next_y = y + posy[final_i]
        next_x = x + posx[final_i]
        if 0<= next_x < width and 0<= next_y < height:
            if img2[next_y][next_x] != 0:
                img2[next_y][next_x] = 0
                if i==0:
                    draw_samedirc(next_y,next_x,final_i)
                    break
                else:
                    t.pendown()
                    t.goto(next_x-(width//2),(height//2)-next_y)
                    draw(next_y,next_x,final_i)
                    break
                
def find_draw(y,x):
    for i in range(5):
        next_y = y + posy[i]
        next_x = x + posx[i]
        if 0<= next_x < width and 0<= next_y < height:
            if img2[next_y][next_x] != 0:
                return True
    return False

def draw_samedirc(y,x,i):
    next_y = y + posy[i]
    next_x = x + posx[i]
    if 0<= next_x < width and 0<= next_y < height and img2[next_y][next_x] != 0:
        img2[next_y][next_x] = 0
        draw_samedirc(next_y,next_x,i)
    else:
        t.goto(x-(width//2),(height//2)-y)
        draw(y,x,-1)

#main
t.penup()
t.goto(-width//2, height//2)
for y in range(height):
    for x in range(width):
        t.penup()
        if img2[y][x] != 0:
            img2[y][x] = 0
            if find_draw(y,x):
                t.goto(x-(width//2),(height//2)-y)
                t.dot(2)
                draw(y,x,-1)
            else:
                continue
input()
