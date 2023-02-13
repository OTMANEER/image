import cv2
import numpy

def myerode(i, es):
    return cv2.erode(i, es)

def mydilate(i,es):
    return cv2.dilate(i,es)

def mygrad(i,es):
    return (mydilate(i,es) - myerode(i,es))

def myopen(i,es):
    return mydilate(myerode(i, es), es)

def myclose(i,es):
    return myerode(mydilate(i, es), es)

def seuil(image,s):
    res = numpy.zeros(image.shape, image.dtype)
    res[image > s] = 255  # pour chaque pixel > s on le met à 255
    return res

def myconddilat(im,M,el):
    return numpy.minimum(im,mydilate(M,el))

def myconderod(im,M,el):
    return numpy.maximum(im,myerode(M,el))

def myreconinf(im,M,el):
    r_copy = M
    r = myconddilat(im,M,el) # faire dilation jusqu'à stabilité
    while not numpy.array_equal(r_copy,r):
        r_copy = r
        r = myconddilat(im,r,el)
    return r


def myreconsup(im,M,el):
    r_copy = M
    r = myconddilat(im,M,el) # faire dilation jusqu'à stabilité
    while not numpy.array_equal(r_copy,r):
        r_copy = r
        r = myconderod(im,r,el)
    return r

def myopenrecon(im,el_o,el_r):
    M = myopen(im,el_o)
    return myreconinf(im,M,el_r)

def mycloserecon(im,el_c,el_r):
    M = myclose(im,el_c)
    return myreconsup(im,M,el_r)

def myhmaxima(image,h,el):
    im_h = numpy.maximum(image,h)-h
    return myreconinf(image,im_h,el)