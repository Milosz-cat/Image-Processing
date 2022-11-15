import cv2
import numpy as np
from PIL import Image

def reduction_2(img):
    if img.shape[0] != img.shape[1] and img.shape[0]%2 != 0 and img.shape[1]%2 != 0:
        print('Bad image resolutin!')
    
    new = np.zeros((img.shape[0]//2, img.shape[1]//2, 3), dtype=int)
    for i in range(0, img.shape[0]//2):
        for j in range(0, img.shape[1]//2):
            new[i, j] = np.add(np.add(np.divide(img[2*i, 2*j], 4), np.divide(img[2*i+1, 2*j], 4)), np.add(np.divide(img[2*i+1, 2*j+1], 4), np.divide(img[2*i, 2*j+1], 4)))
    
    cv2.imwrite("Small.bmp", new)
    return new

def increase_2(img):
    new = np.zeros((img.shape[0]*2, img.shape[1]*2, 3), dtype=int)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            new[2*i+1, 2*j+1]  = img[i, j]
            new[2*i+1, 2*j]  = img[i, j]
            new[2*i, 2*j+1]  = img[i, j]
            new[2*i, 2*j] = img[i, j]
    
    cv2.imwrite("Big.bmp", new)
    


original = cv2.cvtColor(cv2.imread("./barbara.bmp"), cv2.COLOR_BGR2RGB)
orginal = np.array(original)

small = reduction_2(original)
increase_2(small)


cv2.waitKey(0)
cv2.destroyAllWindows()