from PIL import Image, ImageSequence
import matplotlib.pyplot as plt

image_old = 'animation_5_480.gif' #choose animation
im = Image.open(image_old)

i = 0
width = 640
height = 480
j = 4 # height/frames , j = 4 --> sensor slow do

image = Image.new(mode='RGB', size=(width, height))


# ims = []
# for frame in ImageSequence.Iterator(im):
#     ims.append(im.crop((0, i*j, 640, i*j+j)))
#     image.paste(ims[i], (0, i*j)) 
#     #save("gif-webp-"+str(i)+".webp",format = "WebP", lossless = True)
#     i += 1 # how many frames (if i=2 --> j/2) 
#     #image.show()

# image.show()


ims = []
frames = []

for i, frame in enumerate(ImageSequence.Iterator(im)):  #saving frames and rows (1st row from 1st frame,2nd row from 2nd frame etc.)
    ims.append(im.crop((0, i*j, 640, i*j+j)))
    frames.append(frame.crop((0, 0, 640, 480)))
    if i == height//j:  #if we want to slow down sensor
        break



for k, item in enumerate(frames):
    for n in range(k):
        item.paste(ims[n], (0, n*j)) #pasting each row to frame

    
    
frames[0].save('rolling_shutter_5_480_4.gif', #creating gif from new frames
               save_all=True, append_images=frames[1:], optimize=False, duration=40, loop=0)
