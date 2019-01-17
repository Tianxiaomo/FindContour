#!/usr/bin/env python
# encoding: utf-8
'''
@author: tianxiaomo
@license: (C) Apache.
@contact: huguanghao520@gmail.com
@software: 
@file: getContour_myself.py
@time: 2019/1/15 16:30
@desc:
'''
import numpy as np
import matplotlib.pyplot as plot
import cv2
import os
import time


def findContour(img):
    dirt = [[-1, 0],
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1]]

    temp = np.zeros([img.shape[0]+2,img.shape[1]+2])
    temp[1:-1,1:-1] = temp[1:-1,1:-1]+img

    # d = 4*img - temp[2:,1:-1]-temp[:-2,1:-1]-temp[1:-1,2:]-temp[1:-1,:-2]
    # u = img - temp[:-2,1:-1]
    # r = img - temp[1:-1,2:]
    # l = img - temp[1:-1,:-2]
    #
    # z = r+l+d+u

    z = 4*img - temp[2:,1:-1]-temp[:-2,1:-1]-temp[1:-1,2:]-temp[1:-1,:-2]
    z = np.clip(z,0,1)

    contour = []

    flag = False

    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            if z[i,j]:
                l = []
                l.append([i,j])
                z[i,j] = 0
                d = 0
                while True:
                    for k in range(8):
                        k_d = (d+k)% 8
                        x,y = dirt[k_d]
                        if z[i+y,j+x]:
                            l.append([i+y,j+x])
                            z[i+y,j+x] = 0
                            d = (k_d + 4)%8
                            i,j = i+y,j+x
                            break
                        if k == 7:
                            flag = True
                    if flag:
                        l = np.asarray(l)
                        contour.append([l[:,0],l[:,1]])
                        flag = False
                        break
    return contour


def Fit_Line(points):
    sum_x = 0
    sum_y = 0
    sig_xx = 0
    sig_xy = 0

    for y,x in zip(points[0],points[1]):
        sum_x += x
        sum_y += y
        sig_xx += x*x
        sig_xy += y*y

    n = len(points)
    x_bar = sum_x / n
    y_bar = sum_y / n
    nxy_bar = n * x_bar * y_bar
    nxx_bar = n * x_bar * x_bar
    k = (sig_xy - nxy_bar) / (sig_xx - nxx_bar)  # 斜率
    b = y_bar - k * x_bar
    return k, b

def PCA_Line(data):
    temp = []
    temp.append(data[1])
    temp.append(data[0])
    data = np.asarray(temp).T
    N = data.shape[0]
    dataHomo = data.copy()
    dataHomo = dataHomo.astype(np.float)
    dataHomo[:, 0] -= np.sum(data[:,0]) / N
    dataHomo[:, 1] -= np.sum(data[:,1]) / N
    # data matrix
    dataMatrix = np.dot(dataHomo.transpose(), dataHomo)
    u, s, vh = np.linalg.svd(dataMatrix, full_matrices=True)
    n = u[:, -1]
    k2 = -n[0] / n[1]
    b2 = np.sum(data[:, 1]) / N - k2 * np.sum(data[:, 0]) / N

    return k2,b2

def rotateBox(points,k):
    if k != 0:
        e = np.arctan(abs(k))
        s = np.sin(e)
        c = np.cos(e)
        if k > 0:
            t = np.asarray([[c,s],[-s,c]])
            t_n = np.asarray([[c,-s],[s,c]])
        else:
            t = np.asarray([[c,-s],[s,c]])
            t_n = np.asarray([[c, s], [-s, c]])

        r = np.dot(t,np.asarray([points[1],points[0]]))
        x_max = r[0].max()
        x_min = r[0].min()
        y_max = r[1].max()
        y_min = r[1].min()
        box = np.asarray([[x_min,y_max],
                          [x_min,y_min],
                          [x_max,y_min],
                          [x_max,y_max]])
        box = box.T

        box = np.dot(t_n,box)
    else:
        r = np.asarray([points[1],points[0]])
        x_max = points[1].max()
        x_min = points[1].min()
        y_max = points[0].max()
        y_min = points[0].min()
        box = np.asarray([[x_min, y_max],
                          [x_min, y_min],
                          [x_max, y_min],
                          [x_max, y_max]])
        box = box.T
    return r,box

if __name__ == '__main__':
    img = np.load('temp.npy')
    img = np.where(img > 1, 1, 0)

    n = 8

    new = time.time()
    contour = findContour(img)
    # print(len(contour))
    # print(time.time()-new)
    img = np.zeros([104, 160])
    for n in range(len(contour)):
        if contour[n][0].shape[0] < 10:
            continue
        img[contour[n][0],contour[n][1]] = 1
        # plot.imshow(img)
        k2, b2 = PCA_Line(contour[n])
        # plot.axis("equal")
        if abs(k2) < 0.1:
            k2 = 0
        points,box = rotateBox(contour[n],k2)
        # points = points.astype(np.int)
        # plot.scatter(box[0, :], box[1, :],s=5)

        # box_x = list(box[0])
        # box_x.append(box_x[0])
        # box_y = list(box[1])
        # box_y.append(box_y[0])
        # plot.plot(box_x,box_y,color='r')
    print(time.time() - new)
    # plot.show()


