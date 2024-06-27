from scipy.spatial.distance import euclidean
import pandas as pd
from matplotlib.colors import hsv_to_rgb
import cv2
from skimage.io import imread, imshow
from skimage.color import rgb2hsv
from skimage import data
import os
import matplotlib.pyplot as plt
import argparse
import numpy as np 
from math import sqrt
import time
from PIL import Image, ImageFilter
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import whiten
from matplotlib import image as mpimg
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import extcolors
from colormap import rgb2hex
import colorsys

def area_ratio(color_no, image_path):

    dir_path = "static/images/"
    image_name = "final_segment.png"
    # Getting the input image
    input_name = image_path
    output_width = 900                   #set the output size
    img = Image.open(input_name)
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((output_width,hsize), Image.ANTIALIAS)

    colors_x = extcolors.extract_from_path(input_name, tolerance = 12, limit = 63)
    colors_x

    def color_to_df(input):
        colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
        
        #convert RGB to HEX code
        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                              int(i.split(", ")[1]),
                              int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
        df_r = [int(i.split(", ")[0].replace("(","")) for i in df_rgb]
        df_g = [int(i.split(", ")[1]) for i in df_rgb]
        df_b = [int(i.split(", ")[2].replace(")","")) for i in df_rgb]
        
        df = pd.DataFrame(zip(df_color_up, df_percent, df_rgb), columns = ['c_code','occurence','rgb values'])
        list_color = list(df['c_code'])
        list_precent = [int(i) for i in list(df['occurence'])]
        df_percent_value = [round(p*100/sum(list_precent),4) for p in list(list_precent)]

        df = pd.DataFrame(zip(df_color_up, df_percent, df_rgb, df_r, df_g, df_b, df_percent_value), columns = ['c_code','occurence','rgb_values', "r value", "g value", "b value", "percent area"])
        return df

    # print(colors_x[0][0])
    df_color = color_to_df(colors_x)
    # print(df_color)

    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [str(list_color.index(c) + 1) + ': ' + str(round(p*100/sum(list_precent),2)) +'%' for c, p in zip(list_color, list_precent)]
    fig, ax = plt.subplots(figsize=(90,90),dpi=10)
    wedges, text = ax.pie(list_precent,
                          labels= text_c,
                          labeldistance= 1.05,
                          colors = list_color,
                          textprops={'fontsize': 100, 'color':'black'}
                        )
    plt.setp(wedges, width=0.3)

    #create space in the center
    plt.setp(wedges, width=0.36)

    ax.set_aspect("equal")
    fig.set_facecolor('white')
    # plt.show()

    #create background color
    fig, ax = plt.subplots(figsize=(192,108),dpi=10)
    fig.set_facecolor('white')
    plt.savefig('bg.png')
    plt.close(fig)

    #create color palette
    bg = plt.imread('bg.png')
    fig = plt.figure(figsize=(90, 90), dpi = 10)
    ax = fig.add_subplot(1,1,1)

    x_posi, y_posi, y_posi2 = 120, 25, 25
    for c, p in zip(list_color, list_precent):
        if  list_color.index(c) < 9:
            y_posi += 100
            rect = patches.Rectangle((x_posi, y_posi), 290, 80, facecolor = c)
            ax.add_patch(rect)
            ax.text(x = x_posi+360, y = y_posi+55,  s = str(list_color.index(c) + 1) + ': ' + c + ', ' + str(round(p*100/sum(list_precent),2)) +'%', fontdict={'fontsize': 100})
        elif list_color.index(c) >= 9 and list_color.index(c) <= 17:
            y_posi2 += 100
            rect = patches.Rectangle((x_posi + 900, y_posi2), 290, 80, facecolor = c)
            ax.add_artist(rect)
            ax.text(x = x_posi+1260, y = y_posi2+55,  s = str(list_color.index(c) + 1) + ': ' + c + ', ' + str(round(p*100/sum(list_precent),2)) +'%', fontdict={'fontsize': 100})
            
    ax.axis('on')
    # plt.imshow(bg)
    # plt.tight_layout()

    img = mpimg.imread(image_path)
    bg = plt.imread('bg.png')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(100,180), dpi = 10)

    #donut plot
    wedges, text = ax1.pie(list_precent,
                          labels= text_c,
                          labeldistance= 1.05,
                          colors = list_color,
                          textprops={'fontsize': 110, 'color':'black'})
    plt.setp(wedges, width=0.3)

    #add image in the center of donut plot
    imagebox = OffsetImage(img, zoom=2)
    ab = AnnotationBbox(imagebox, (0, 0))
    ax1.add_artist(ab)

    #color palette
    x_posi, y_posi, y_posi2 = -40, -120, -120
    for c, p in zip(list_color, list_precent):
        if list_color.index(c) < 9:
            y_posi += 120
            rect = patches.Rectangle((x_posi, y_posi), 360, 100, facecolor = c)
            ax2.add_patch(rect)
            ax2.text(x = x_posi+400, y = y_posi+80, s = str(list_color.index(c) + 1) + ': ' + c + ', ' + str(round(p*100/sum(list_precent),2)) +'%', fontdict={'fontsize': 160})
        elif list_color.index(c) >= 9 and list_color.index(c) <= 17:
            y_posi2 += 120
            rect = patches.Rectangle((x_posi + 1200, y_posi2), 360, 100, facecolor = c)
            ax2.add_artist(rect)
            ax2.text(x = x_posi+1600, y = y_posi2+80, s = str(list_color.index(c) + 1) + ': ' + c + ', ' + str(round(p*100/sum(list_precent),2)) +'%', fontdict={'fontsize': 160})

    ax2.axis('off')
    fig.set_facecolor('white')
    # plt.imshow(bg)   
    # plt.tight_layout()  


    # input value of color from the user
    # print(df_color)
    # print(np.array(df_color.iloc[color_no - 1]["rgb_values"]))
    a_ratio = df_color.iloc[color_no - 1]["percent area"]
    r = df_color.iloc[color_no - 1]["r value"]
    g = df_color.iloc[color_no - 1]["g value"]
    b = df_color.iloc[color_no - 1]["b value"]
    # print(r,g,b)
    # (r,g,b) = np.array(list(df_color.iloc[color_no - 1]["rgb_values"]))  # (0, 255, 179)
    r = r/255
    g = g/255
    b = b/255

    # print(r,g,b)

    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    # print('HSV : ', h, s, v)

    img = mpimg.imread(image_path)
    img_hsv = rgb2hsv(img)
    fig, ax = plt.subplots(1, 3, figsize=(20, 5))
    ax[0].imshow(img_hsv[:,:,0], cmap='binary')
    ax[0].set_title('Hue')
    ax[1].imshow(img_hsv[:,:,1], cmap='binary')
    ax[1].set_title('Saturation')
    ax[2].imshow(img_hsv[:,:,2], cmap='binary')
    ax[2].set_title('Value')

    fig, ax = plt.subplots(3, 1, figsize=(40, 12))
    ax[0].imshow(img_hsv[:,:,0],cmap='hsv')
    ax[0].set_title('hue')
    ax[1].imshow(img_hsv[:,:,1],cmap='hsv')
    ax[1].set_title('transparency')
    ax[2].imshow(img_hsv[:,:,2],cmap='hsv')
    ax[2].set_title('value')

    # ratio = [1, 0.53, 2, 0.76, 0.5, 2.125, 0.56,
    #         1.28, 1.09, 1.02]

    # cbar = fig.colorbar(imshow(img_hsv[:,:,0],cmap='hsv'))
    cbar = fig.colorbar(ax[2].imshow(img_hsv[:,:,0],cmap='hsv'), orientation="horizontal")
    cbar.set_ticks([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1])
    cbar.set_ticklabels(["0.05", "0.10", "0.15", "0.20", "0.25", "0.30", "0.35", "0.40", "0.45", "0.50", "0.55", "0.60", "0.65", "0.70", "0.75", "0.80", "0.85", "0.90", "0.95", "1"])

    # plt.colorbar(orientation="horizontal").ax.set_xticklabels(ratio, rotation=45)

    fig.tight_layout()
    # plt.show()


    #refer to hue channel (in the colorbar)
    lower_mask = img_hsv[:,:,0] > h - 0.02
    #refer to hue channel (in the colorbar)
    upper_mask = img_hsv[:,:,0] < h + 0.02
    #refer to transparency channel (in the colorbar)
    saturation_mask = img_hsv[:,:,1] > 0.3
    
    mask = upper_mask*lower_mask*saturation_mask
    red = img[:,:,0]*mask
    green = img[:,:,1]*mask
    blue = img[:,:,2]*mask
    img_masked = np.dstack((red,green,blue))
    # imshow(img_masked)
    # cv2.imwrite("sample11_2.jpg", img_masked)
    return a_ratio

# print(area_ratio(1, "static/images/1image_visualize.png"))