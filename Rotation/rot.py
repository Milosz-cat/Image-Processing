import cv2
import numpy as np
import time
import math
from PIL import Image  

def rotation(angle):
     
    image = np.array(Image.open("barbara.bmp"))
    text = angle
    
    angle=math.radians(angle)                               #converting degrees to radians
    cosine=math.cos(angle)
    sine=math.sin(angle)
    height=image.shape[0]                                 
    width=image.shape[1]                                   

    new_height = round(abs(image.shape[0]*cosine)+abs(image.shape[1]*sine))+1
    new_width = round(abs(image.shape[1]*cosine)+abs(image.shape[0]*sine))+1

    output = np.zeros((new_height,new_width))

    original_centre_height = round(((image.shape[0]+1)/2)-1)    
    original_centre_width  = round(((image.shape[1]+1)/2)-1)    

    new_centre_height = round(((new_height+1)/2)-1)        
    new_centre_width = round(((new_width+1)/2)-1)         \

    for i in range(height - 1):
        for j in range(width - 1):
            y=image.shape[0]-1-i-original_centre_height                   
            x=image.shape[1]-1-j-original_centre_width                      


            new_y=round(-x*sine+y*cosine)
            new_x=round(x*cosine+y*sine)
            
            #since image will be rotated the centre will change too, 
            #so to adust to that we will need to change new_x and new_y with respect to the new centre'
            
            new_y=new_centre_height-new_y
            new_x=new_centre_width-new_x

            output[new_y,new_x]=image[i,j]

    
    h, w = output.shape
    for i in range(h - 1):
        for j in range(w - 1):
            if output[i][j] == 0:
                #output[i][j] = (output[i][j-1] + output[i][j+1])//2
                output[i][j] = (output[i][j-1] + output[i][j+1] + output[i+1][j] + output[i-1][j])//4


                

    pil_img=Image.fromarray((output).astype(np.uint8))                       # converting array to image
    pil_img.save(f"Rotated{text}.bmp")                 
    

def reduction_2(img):
    
    if img.shape[0] != img.shape[1] and img.shape[0]%2 != 0 and img.shape[1]%2 != 0:
        print('Bad image resolutin!')
    
    new = np.zeros((img.shape[0]//2, img.shape[1]//2, 3), dtype=int)
    for i in range(0, img.shape[0]//2):
        for j in range(0, img.shape[1]//2):
            new[i, j] = np.add(np.add(np.divide(img[2*i, 2*j], 4), np.divide(img[2*i+1, 2*j], 4)), np.add(np.divide(img[2*i+1, 2*j+1], 4), np.divide(img[2*i, 2*j+1], 4)))
    
    cv2.imwrite("Small_nn.bmp", new)
    return new

def increase_2_nn(img):
    new = np.zeros((img.shape[0]*2, img.shape[1]*2, 3), dtype=int)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            new[2*i+1, 2*j+1]  = img[i, j]
            new[2*i+1, 2*j]  = img[i, j]
            new[2*i, 2*j+1]  = img[i, j]
            new[2*i, 2*j] = img[i, j]
    
    cv2.imwrite("Big_nn.bmp", new)
    return new

def increase_2_bl(img):
    new_1 = np.zeros((img.shape[0]*2, img.shape[1]*2, 3), dtype=int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_1[i, 2*j] = img[i, j]   
        for j in range(img.shape[1]-1):
            new_1[i, 2*j+1] = (img[i, j] + img[i, j+1])/2
    new_2 = np.zeros((img.shape[0]*2, img.shape[1]*2, 3), dtype=int)
    for i in range(img.shape[0]):
        for j in range(new_1.shape[1]-1):
            new_2[2*i, j] = new_1[i, j]   
        for j in range(new_1.shape[1]):
            new_2[2*i +1, j] = (new_1[i, j] + new_1[i+1, j])/2
          
    
    cv2.imwrite("Big_bl.bmp", new_2)
    return new_2


original  = np.array(cv2.imread("./barbara.bmp"))

start = time.time()
small = reduction_2(original)
end = time.time()
print(end - start)

start = time.time()
big_nn = increase_2_nn(small)
end = time.time()
print(end - start)

start = time.time()
big_bl = increase_2_bl(small)
end = time.time()
print(end - start)

rotation(123) # choose any angle to rotate

mse_splot_nn = np.square(np.subtract(big_nn, original)).mean()
mse_splot_bl = np.square(np.subtract(big_bl, original)).mean()

print(mse_splot_nn, mse_splot_bl)

cv2.waitKey(0)
cv2.destroyAllWindows()