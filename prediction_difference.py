import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
import keyboard


# use case:
# to check difference in prediction between current prediction and previous predictions
def compare_images(image_path1, image_path2, threshold_value=30):
    # Load the two images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # Resize images to be the same size if needed
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions")

    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference
    diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference to get binary image
    _, thresh = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

    # Convert threshold image to color to highlight differences
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # Highlight differences on the original images
    highlighted_image1 = image1.copy()
    highlighted_image2 = image2.copy()

    if np.any(highlighted_image1[thresh != 0]) or np.any(highlighted_image2[thresh != 0]):
        # highlighted_image2[thresh != 0] = [0, 0, 255]
        # Display the images
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
        plt.title('Previous setup: ' + os.path.basename(image_path1))

        plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(2, 2, 2)
        plt.title('Current setup: ' + os.path.basename(image_path2))
        plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.tight_layout()
        plt.show()
        # if keyboard.is_pressed(27):
        #     plt.close()


# previous results: directory against which to perform comparison
# current results: current predictions
previous_results = input("Enter directory against which to perform comparison")
current_results = input("Enter directory of current predictions")

for directory in os.listdir(previous_results):
    prev_dir = os.path.join(previous_results, directory)
    if os.path.isdir(prev_dir):
        for file in os.listdir(prev_dir):
            if not file.split('.')[0].endswith('bottom'):
                image1 = os.path.join(prev_dir, file)
                image2 = os.path.join(current_results, directory, file)
                compare_images(image1, image2)