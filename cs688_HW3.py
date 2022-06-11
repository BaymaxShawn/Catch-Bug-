#CS688_HW3
#Shawn_Hu

import numpy as np
import cv2 as cv
import os

#loading the pictures
path = r"/Users/huchangguo/Desktop/picture"
ori_pic = cv.imread(os.path.join(path, 'Catch the bug3.png'))
ori_bug = cv.imread(os.path.join(path, 'Bug Final.png'))


#resize the picture to fasten the algorithm 把图片原始大小改成更小，处理起来速度更快，缺点是精度越差
percentage = 6
dmpic = (int(ori_pic.shape[1] * percentage / 100), int(ori_pic.shape[0] * percentage / 100))
img = cv.resize(ori_pic, dmpic, interpolation = cv.INTER_AREA)
dmbug = (int(ori_bug.shape[1] * percentage / 100), int(ori_bug.shape[0] * percentage / 100))
bug = cv.resize(ori_bug, dmbug, interpolation = cv.INTER_AREA)

#convert the bug to time series with HOG algorithm 降为一维的时间序列，查看variable explorer，bug那有三个数，是三围矩阵。长宽rgb。
h_bug = bug.flatten()
#smooth the bug time series with moving average 平滑处理，计算moving average
window = 8
m_bug = []
for i in range(len(h_bug)-window+1):
    m_bug.append(sum(h_bug[i:i+window])/window)
m_bug = np.array(m_bug)

#make the slice from the original image 做切片，
temsiz = 500000000
#设一个很大的数，保证一定能在这张图片上找到bug
for y in range(img.shape[0]-bug.shape[0]):
    for x in range(img.shape[1]-bug.shape[1]):
        slice = img[y:y+bug.shape[0],x:x+bug.shape[1]]
#slice=是在从压缩过的图片里，裁处一个切片，切片大小是bug压缩后的大小，然后做相似度的对比，从而找出bug
        t_slice = slice.flatten()
        m_slice = []
        for i in range(len(t_slice)-window+1):
            m_slice.append(sum(t_slice[i:i+window])/window)
        m_slice = np.array(m_slice)
        #compute the Euclidean distance 点和点之间的距离，距离越小，相似度越像
        distance = np.sqrt(np.sum(np.square(m_slice-m_bug)))
        if distance < temsiz:
            temsiz = distance
            coordinate = (x,y)
#get the coordinate in the original size image 还原原来的比例
new_x = coordinate[0]*100/percentage
new_y = coordinate[1]*100/percentage
#然后打印出来
print("The coordinate of the bug is (",new_x,new_y,")")

#highlight the bug in the origin image region 在原始图片里话了一个红色长方体，找出那个bug
cv.rectangle(ori_pic, (int(new_x),int(new_y)), (int(new_x)+ori_bug.shape[1],int(new_y)+ori_bug.shape[0]), (0,255,0), 4)
cv.imwrite(os.path.join(path, 'Catch the bug3.png'), ori_pic)
    



