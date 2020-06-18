import math
from decimal import *
import re
import numpy as np
 
 
def recoloring(h, s, v):
    h_i = math.floor((h/60) % 6)
    v_min = ((100-s)*v)/100
    a = (v - v_min) * ((h % 60)/60)
    v_inc = v_min + a
    v_dec = v-a
    r, g, b = 0, 0, 0
    if h_i == 0:
        r, g, b = v, v_inc, v_min
    elif h_i == 1:
        r, g, b = v_dec, v, v_min
    elif h_i == 2:
        r, g, b = v_min, v, v_inc
    elif h_i == 3:
        r, g, b = v_min, v_dec, v
    elif h_i == 4:
        r, g, b = v_inc, v_min, v
    elif h_i == 5:
        r, g, b = v, v_min, v_dec
    return r*Decimal('2.55'), g*Decimal('2.55'), b*Decimal('2.55')
def distance(rgb, rgb1):
    r,g,b=rgb
    r1,g1,b1=rgb1
    return ((r-r1)**2+(g-g1)**2+(b-b1)**2).sqrt()
lines = eval(input())
b = b''
for i in range(0,len(lines)-1):
    b+=lines[i:i+1]
    if (lines[i-3:i] == b'255' or lines[i-3:i] == "255") and (lines[i:i+1] == b'\n' or lines[i:i+1] == "\n"):
        break
d = lines[i+1:]
b = b.decode()
b = re.sub(' +', ' ', b).strip().rstrip().splitlines()
while ' ' in b:
    b.remove(' ')
temp = []
for i in range(0, len(b)-1):
    if b[i].count("#") == 0:
        t = b[i].split()
        if len(t) == 0:
            continue
        for j in range(len(t)):
            if t[j].isdigit():
                temp.append(int(t[j])) 
arr = []
for i in range(0,len(d),3):
    arr.append([d[i], d[i+1], d[i+2]])
maxval = b[-1]
width, height = temp
arr_new = np.reshape(arr,(height,width,3)).tolist()
arr1=[]
arr_comments = []
for i in range(len(b)):    
    if b[i].find('#') != -1:
        if b[i].find('!') != -1 and (b[i][1]=='!' or b[i][2] == '!'):
            arr_comments.append(b[i].replace('#', '').replace('!', '').split())
            arr1.append(int(b[i].replace('#', '').replace('!', '').split()[0]))
            f=max(arr1)+1
arr1=[[]]*f
for i in range(len(arr_comments)):
    r=int(arr_comments[i][0])
    arr_comments[i][0] = int(arr_comments[i][0])
    arr_comments[i][1] = Decimal(arr_comments[i][1][:len(arr_comments[i][1])-1])
    if "%" in arr_comments[i][2]:
        arr_comments[i][2] = Decimal(arr_comments[i][2][:len(arr_comments[i][2])-1])
    else:
        arr_comments[i][2] = Decimal(arr_comments[i][2])*100
    if "%" in arr_comments[i][3]:
        arr_comments[i][3] = Decimal(arr_comments[i][3][:len(arr_comments[i][3])-1])
    else:
        arr_comments[i][3] = Decimal(arr_comments[i][3])*100
    arr_comments[i][1], arr_comments[i][2], arr_comments[i][3] = recoloring(arr_comments[i][1], arr_comments[i][2], arr_comments[i][3])
    arr1[r]=[arr_comments[i][1],arr_comments[i][2],arr_comments[i][3]]
arr_comments=[[]]*(len(arr1))
arr2=[]
for i in range(1,len(arr1)):
    arr_comments[i]=[arr1[i][0], arr1[i][1], arr1[i][2]]
for i in range(len(arr_new)):
    for g in range(len(arr_new[i])):
        arr2=[]
        for f1 in range(1,len(arr1)):
            arr2.append(distance(arr_new[i][g],arr1[f1]))
        a=arr2.index(min(arr2))+1
        arr_new[i][g]=arr_comments[a]
arr_new = np.array(arr_new).ravel().tolist()
arr_new = [int(x.quantize(Decimal("1"))) for x in arr_new]
print(b'P6 '+str(width).encode()+b' '+str(height).encode()+b' '+str(maxval).encode()+b'\n'+bytes(arr_new))
