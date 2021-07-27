import os
import random
import re
from PIL import Image

def split_data():
    '''Function to split data for image segmentation'''

    # chnaging pwd to data folder
    %cd /content/drive/MyDrive/Dataset/aug_data

    DATA_PATH = '/content/drive/MyDrive/Dataset/aug_data/'
    IMAGE_PATH = os.path.join(DATA_PATH, 'images')
    MASK_PATH = os.path.join(DATA_PATH, 'masks')

    # Create folders to hold images and masks
    folders = ['train_images', 'train_masks', 'val_images', 'val_masks', 'test_images', 'test_masks']

    for folder in folders:
        os.makedirs(DATA_PATH + folder)
    
    # Get all images and masks, sort them, shuffle them to generate data sets.
    all_images = sorted(os.listdir(IMAGE_PATH))
    all_masks = sorted(os.listdir(MASK_PATH))

    random.seed(230)
    random.shuffle(all_images)

    # Generate train, val, and test sets for images
    train_split = int(0.7*len(all_images))
    val_split = int(0.9 * len(all_images))

    train_images = all_images[:train_split]
    val_images = all_images[train_split:val_split]
    test_images = all_images[val_split:]

    # Generate corresponding mask lists for masks
    train_masks = [f for f in all_masks if os.path.splitext(f)[0] in [os.path.splitext(x)[0]
                                                                      for x in train_images]]
    val_masks = [f for f in all_masks if os.path.splitext(f)[0] in [os.path.splitext(x)[0]
                                                                    for x in val_images]]
    test_masks = [f for f in all_masks if os.path.splitext(f)[0] in [os.path.splitext(x)[0]
                                                                     for x in test_images]]

    #Add train, val, test images and masks to relevant folders
    def add_images(dir_name, image):
        img = Image.open(os.path.join(IMAGE_PATH, image))
        img.save(DATA_PATH+'/{}'.format(dir_name)+'/'+image)
    
    def add_masks(dir_name, image):
        img = Image.open(os.path.join(MASK_PATH, image))
        img.save(DATA_PATH+'/{}'.format(dir_name)+'/'+image)

    
    image_folders = [(train_images, 'train_images'), (val_images, 'val_images'), 
                    (test_images, 'test_images')]

    mask_folders = [(train_masks, 'train_masks'), (val_masks, 'val_masks'), 
                    (test_masks, 'test_masks')]

    # Add frames
    for folder in image_folders:
        array = folder[0]
        name = [folder[1]] * len(array)

        list(map(add_images, name, array))
            
    # Add masks
    for folder in mask_folders:
        array = folder[0]
        name = [folder[1]] * len(array)
        
        list(map(add_masks, name, array))

    print("Data Split Done...")

    for folder in folders:
        print(folder, ':', len(os.listdir(os.path.join(DATA_PATH, folder))))