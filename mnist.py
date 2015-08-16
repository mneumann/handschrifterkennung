"""
Utilities for reading
the MNIST database of handwritten digits:
http://yann.lecun.com/exdb/mnist/
"""

import os, struct
from array import array

class DigitImage(object):
    def __init__(self, width, height, data, label):
        self.width = width
        self.height = height
        self.data = data
        if len(self.data) <> width*height:
            raise ValueError("Invalid size")
        if not (label >= 0 and label <= 9):
            raise ValueError("Invalid label")
        self.label = label

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getLabel(self):
        return self.label

    def pixelAt(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self.data[x + y*self.width]
        else:
            raise ValueError("Invalid coordinates")

    def display(self, threshold=200):
        s = ''
        for i in xrange(len(self.data)):
            if self.data[i] > threshold:
                s += '@'
            else:
                s += '.'
            if i > 0 and i % self.width == 0:
                s += '\n'
        s += '\n'
        return s

    def __str__(self):
        return "label: " + str(self.label) + '\n' + self.display()

    def __repr__(self):
        return self.__str__()


def read_labels(filename):
    with open(filename, 'rb') as f:
        magic_nr, size = struct.unpack(">II", f.read(8))
        if magic_nr <> 0x0801:
            raise ValueError, "invalid labels file: magic mismatch"
        labels = array("b", f.read())
        if len(labels) <> size:
            raise ValueError, "invalid labels file: invalid size"
        if all(digit >= 0 and digit <= 9 for digit in labels):
            return labels
        else:
            raise ValueError, "invalid labels file: invalid digit label"

def read_images(filename, labels):
    with open(filename, 'rb') as f:
        magic_nr, size, rows, cols = struct.unpack(">IIII", f.read(16))
        if magic_nr <> 0x0803:
            raise ValueError, "invalid images file: magic mismatch"
        if len(labels) <> size:
            raise ValueError, "mismatching len of labels and images"

        data = array("B", f.read())
        images = []

        for i in xrange(size):
            images.append(DigitImage(cols, rows, data[rows*cols*i : rows*cols*(i+1)], labels[i]))

        if len(images) <> size:
            raise ValueError, "invalid images file: size mismatch"

        return images


def read_digit_images(dataset = "training", path = "datasets"):
    if dataset is "training":
        fname_img = os.path.join(path, 'train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    else:
        raise ValueError, "dataset must be 'testing' or 'training'"

    labels = read_labels(fname_lbl)
    images = read_images(fname_img, labels)

    return images

x = read_digit_images(dataset = 'training', path = 'datasets')
print x
