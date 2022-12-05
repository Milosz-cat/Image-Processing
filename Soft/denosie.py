import numpy as np
import cv2


def splot(img):
    
    #kernel =  np.ones((5,5),np.float32)/25 #0.04 5x5
    
    # kernel = np.array([[1, 4,  6 , 4,  1],
    #                    [4, 16, 24, 16, 4],
    #                    [6, 24, 36, 24, 6], #36
    #                    [4, 16, 24, 16, 4],
    #                    [1, 4,  6,  4,  1]])/256
    
    kernel = np.array([[1, 4,  6,    4,  1],
                       [4, 16, 24,   16, 4],
                       [6, 24, -476, 24, 6], 
                       [4, 16, 24,   16, 4],
                       [1, 4,  6,    4,  1],])*(-1/256)
    

    no_noise = cv2.filter2D(original, -1, kernel)
    cv2.imwrite('Leo_splot_filter.jpg', no_noise)
    
    return no_noise
    

def median(img):

    def Sort(sub_li):
        l = len(sub_li)
        for i in range(l):
            for j in range(l-i-1):
                if (sub_li[j][1] > sub_li[j + 1][1]):
                    tempo = sub_li[j]
                    sub_li[j]= sub_li[j + 1]
                    sub_li[j + 1]= tempo
        return sub_li
    
    img_new = np.zeros(img.shape)
 
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            temp = [[img[i-1, j-1], np.sum(img[i-1, j-1])],
                    [img[i-1, j], np.sum(img[i-1, j])],
                    [img[i-1, j + 1], np.sum(img[i-1, j + 1])],
                    [img[i, j-1], np.sum(img[i, j-1])],
                    [img[i, j], np.sum(img[i, j])],
                    [img[i, j + 1], np.sum(img[i, j + 1])], 
                    [img[i + 1, j-1], np.sum(img[i + 1, j-1])],
                    [img[i + 1, j], np.sum(img[i + 1, j])],
                    [img[i + 1, j + 1], np.sum(img[i + 1, j + 1])]]
                
            Sort(temp)
            img_new[i, j, 0] = temp[4][0][0]
            img_new[i, j, 1] = temp[4][0][1]
            img_new[i, j, 2] = temp[4][0][2]
    
    cv2.imwrite('Leo_median_filter.jpg', img_new)
    
    return img_new


img_noise = cv2.imread("./Leopard-with-noise.jpg")  
original = cv2.imread("./Leopard-original.jpg")  

splot_img = splot(img_noise)
median_img = median(img_noise) # takes a lot of time
bilateral_img = cv2.bilateralFilter(img_noise, 25, 100, 100)

cv2.imwrite('Leo_bilateral_filter.jpg', bilateral_img)

mse_splot = np.square(np.subtract(original, splot_img)).mean() #23.734772046407063
mse_median = np.square(np.subtract(original, median_img)).mean() #242.3105821609497
mse_bilateral = np.square(np.subtract(original, bilateral_img)).mean() #75.21398798624675

print(mse_splot, mse_median, mse_bilateral)
