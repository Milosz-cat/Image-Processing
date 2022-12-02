import cv2
import numpy as np
import time
import math
from PIL import Image  

def rotation(angle):
    
    def shear(angle,x,y):
        '''
        |1  -tan(𝜃/2) |  |1        0|  |1  -tan(𝜃/2) | 
        |0      1     |  |sin(𝜃)   1|  |0      1     |
        '''
        # shear 1
        tangent=math.tan(angle/2)
        new_x=round(x-y*tangent)
        new_y=y
        
        #shear 2
        new_y=round(new_x*math.sin(angle)+new_y)      #since there is no change in new_x according to the shear matrix

        #shear 3
        new_x=round(new_x-new_y*tangent)              #since there is no change in new_y according to the shear matrix
        
        return new_y,new_x
    
    image = np.array(Image.open("barbara.bmp"))
    text = angle
    
    # Define the most occuring variables
    angle=math.radians(angle)                               #converting degrees to radians
    cosine=math.cos(angle)
    sine=math.sin(angle)
    height=image.shape[0]                                   #define the height of the image
    width=image.shape[1]                                    #define the width of the image

    # Define the height and width of the new image that is to be formed
    new_height = round(abs(image.shape[0]*cosine)+abs(image.shape[1]*sine))+1
    new_width = round(abs(image.shape[1]*cosine)+abs(image.shape[0]*sine))+1

    # define another image variable of dimensions of new_height and new _column filled with zeros
    output = np.zeros((new_height,new_width))

    # Find the centre of the image about which we have to rotate the image
    original_centre_height = round(((image.shape[0]+1)/2)-1)    #with respect to the original image
    original_centre_width  = round(((image.shape[1]+1)/2)-1)    #with respect to the original image

    # Find the centre of the new image that will be obtained
    new_centre_height = round(((new_height+1)/2)-1)        #with respect to the new image
    new_centre_width = round(((new_width+1)/2)-1)          #with respect to the new image

    for i in range(height):
        for j in range(width):
            #co-ordinates of pixel with respect to the centre of original image
            y=image.shape[0]-1-i-original_centre_height                   
            x=image.shape[1]-1-j-original_centre_width                      
            new_y,new_x=shear(angle,x,y)

            # new_y=round(-x*sine+y*cosine)
            # new_x=round(x*cosine+y*sine)
            '''since image will be rotated the centre will change too, 
            so to adust to that we will need to change new_x and new_y with respect to the new centre'''
            new_y=new_centre_height-new_y
            new_x=new_centre_width-new_x

            output[new_y,new_x]=image[i,j]

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

rotation(45)

mse_splot_nn = np.square(np.subtract(big_nn, original)).mean()
mse_splot_bl = np.square(np.subtract(big_bl, original)).mean()

print(mse_splot_nn, mse_splot_bl)

cv2.waitKey(0)
cv2.destroyAllWindows()