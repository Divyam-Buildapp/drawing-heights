import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image, ImageFilter
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import whiten
from matplotlib import image as mpimg
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import extcolors
import pandas as pd
from colormap import rgb2hex

def connected_component_label(input_image_path, fig_size=(5,5)):

    dir_path = "static/images/"
    image_name = "image_segment.png"
    # Getting the input image
    input_name = input_image_path
    output_width = 900                   #set the output size
    img = Image.open(input_name)
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((output_width,hsize), Image.ANTIALIAS)

    #save
    # resize_name = 'resize_' + input_name  #the resized image name
    # img.save(resize_name)                 #output location can be specified before resize_name

    # read
    # plt.figure(figsize=(9, 9))
    # img_url = resize_name
    # img = plt.imread(img_url)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()

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
    plt.tight_layout()

    img = mpimg.imread(input_image_path)
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
    x_posi, y_posi, y_posi2 = -20, -120, -120
    for c, p in zip(list_color, list_precent):
        if list_color.index(c) < 9:
            y_posi += 120
            rect = patches.Rectangle((x_posi+100, y_posi), 360, 100, facecolor = c)
            ax2.add_patch(rect)
            ax2.text(x = x_posi+500, y = y_posi+80, s = str(list_color.index(c) + 1) + ': ' + c + ', ' + str(round(p*100/sum(list_precent),2)) +'%', fontdict={'fontsize': 160})
        elif list_color.index(c) >= 9 and list_color.index(c) <= 17:
            y_posi2 += 120
            rect = patches.Rectangle((x_posi + 1200, y_posi2), 360, 100, facecolor = c)
            ax2.add_artist(rect)
            ax2.text(x = x_posi+1600, y = y_posi2+80, s = str(list_color.index(c) + 1) + ': ' + c + ', ' + str(round(p*100/sum(list_precent),2)) +'%', fontdict={'fontsize': 160})

    ax2.axis('off')
    fig.set_facecolor('white')
    plt.imshow(bg)   
    plt.tight_layout()  
    plt.savefig(dir_path + image_name)  
    # exact_color('sample8_1.jpg', 900, 20, 2.5)
    return image_name






