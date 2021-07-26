import cv2
import numpy as np
from numpy.core.fromnumeric import shape
from Database import Database
from PySide6.QtWidgets import QWidget


class Filter(QWidget):
    def __init__(self, frame):
        super(Filter, self).__init__()
        self.frame = frame

    def blur(self):
        blured_frame = cv2.blur(self.frame, (30, 30))
        return blured_frame

    def moreLigth(self):
        kernel1 = np.array([[0, 0, 0],
                            [0, 4, 0],
                            [0, 0, 0]])
        identity = cv2.filter2D(src=self.frame, ddepth=-1, kernel=kernel1)
        return identity

    def sketch(self):
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray_frame_inv = 255 - gray_frame
        gray_frame_inv = cv2.GaussianBlur(gray_frame_inv, (21, 21), 0)
        output = cv2.divide(gray_frame, 255-gray_frame_inv, scale=256.0)
        return output

    def flip(self):
        return cv2.flip(self.frame, 0)

    def blackAndWithe(self):
        photo_hsv = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(photo_hsv)
        s = np.zeros((s.shape[0], s.shape[1]), dtype=np.uint8)
        photo = cv2.merge((h, s, v))
        photo = cv2.cvtColor(photo, cv2.COLOR_HSV2RGB)
        return photo

    def noRed(self):
        r, g, b = cv2.split(self.frame)
        r = np.zeros((r.shape[0], r.shape[1]), dtype=np.uint8)
        photo = cv2.merge((r, g, b))
        return photo

    def noBlue(self):
        r, g, b = cv2.split(self.frame)
        b = np.zeros((b.shape[0], b.shape[1]), dtype=np.uint8)
        photo = cv2.merge((r, g, b))
        return photo

    def noGreen(self):
        r, g, b = cv2.split(self.frame)
        g = np.zeros((g.shape[0], g.shape[1]), dtype=np.uint8)
        photo = cv2.merge((r, g, b))
        return photo

    def inverte(self):
        photo = (255 - self.frame)
        return photo

    def threeColor(self):
        photo = self.frame
        r = photo.copy()
        r[:, :, 0] = 0
        r[:, :, 1] = 0
        photo[:,:photo.shape[1] // 3] = r[:,:photo.shape[1] // 3]

        g = photo.copy()
        g[:, :, 0] = 0
        g[:, :, 2] = 0
        photo[:,photo.shape[1] // 3:int(photo.shape[1] / 1.5)] = g[:, photo.shape[1] // 3:int(photo.shape[1] / 1.5)]

        b = photo.copy()
        b[:, :, 1] = 0
        b[:, :, 2] = 0
        photo[:,int(photo.shape[1] / 1.5):] = b[:,int(photo.shape[1] / 1.5):]

        return photo