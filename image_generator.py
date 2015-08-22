import numpy as np
import cv2

class ImageGenerator(object):
    def __init__(self):
        self.image_width = 512
        self.image_height = 512

        # text params
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.char_size = 4
        self.text_color = (255, 255, 255)
        self.line_width = 4

    def frame(self, text):
        # estimate the text bounding box
        ((text_width, text_height), _) = cv2.getTextSize(text, self.font, \
                self.char_size, self.line_width)

        # calc. text origin (aligned to center)
        xy = (self.image_width/2 - text_width/2, \
                self.image_height/2 + text_height/2)

        # clear the image
        image = np.zeros((self.image_width, self.image_height, 3), np.uint8)

        # draw text
        cv2.putText(image, text, xy, self.font, self.char_size, \
                self.text_color, self.line_width)

        return image
