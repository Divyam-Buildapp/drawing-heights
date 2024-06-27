import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image, ImageFilter
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import whiten
from matplotlib import image as mpimg
import pandas as pd

def visualization(image_file_path, fig_size=(5,5)):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=fig_size)
    img = cv2.imread(image_file_path)
    dir_path = "static/images/"
    image_name = "image_visualize.png"
    # print("Image Shape: {}".format(img.shape))
    # print("Height: {} pixels".format(img.shape[0]))
    # print("width: {} pixels".format(img.shape[1]))
    # print("size: ", img.size)
    # print("Type: ", type(img))
    # fig = plt.figure(figsize=(10,8))
    
    ax1.imshow(img, cmap = "gray")
    ax1.set_title("Original Image")
    ax1.grid()
    ax1.axis()
    ax1.legend
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    img = cv2.imread(image_file_path, 0)
    # Converting those pixels with values 1-127 to 0 and others to 1
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    # Applying cv2.connectedComponents() 
    num_labels, labels = cv2.connectedComponents(img)
    
    # Map component labels to hue val, 0-179 is the hue range in OpenCV
    label_hue = np.uint8(180*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # Converting cvt to BGR
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 0
    
    
    # Showing Original Image
    # fig = plt.figure(figsize=(10,8))
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.axis("on")
    # plt.title("Orginal Image")
    # plt.show()
    
    #Showing Image after Component Labeling
    # fig = plt.figure(figsize=(10,8))
    segment_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2RGB)
    ax2.imshow(segment_img)
    # cv2_imshow(segment_img)
    label_image_name = "1"+image_name
    cv2.imwrite(dir_path + label_image_name, segment_img)
    ax2.axis('on')
    ax2.set_title("Image after Component Labeling")
    plt.legend
    plt.savefig(dir_path + image_name)
    # plt.show()
    # print("\n", num_labels, labels)
    # connected_component_label("sample9.jpg")


    # image = mpimg.imread(image_file_path)

    # #construct to a dataframe for future data process

    # df = pd.DataFrame()
    # df['r']=pd.Series(image[:,:,0].flatten())
    # df['g']=pd.Series(image[:,:,1].flatten())
    # df['b']=pd.Series(image[:,:,2].flatten())

    # df['r_whiten'] = whiten(df['r'])
    # df['g_whiten'] = whiten(df['g'])
    # df['b_whiten'] = whiten(df['b'])

    # cluster_centers, distortion = kmeans(df[['r_whiten', 'g_whiten', 'b_whiten']], 33)
    # r_std, g_std, b_std = df[['r', 'g', 'b']].std()
    # colors=[]

    # for color in cluster_centers:
    #     sr, sg, sb = color
    #     colors.append((int(sr*r_std), int(sg*g_std), int(sb*b_std)))

    # print("\n", "No. of segmented colors:", len(colors), "\n", colors) 
    # # fig = plt.figure(figsize=(10,8))
    # ax2.imshow(image)
    # ax2.set_title("Image after Component Labeling")
    # plt.legend(["Image after Component Labeling"])
    # plt.show()

    return image_name, label_image_name

# visualization("sample9.jpg")