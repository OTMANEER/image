import numpy
import cv2
import strel

def my_first_erode(im):
    imsortie = numpy.copy(im)
    ligne = im.shape[0]
    colonne = im.shape[1]
    for i in range(1, ligne-1):
        for j in range(1, colonne-1):
            imsortie[i, j] = numpy.amin(im[i-1:i+2, j-1:j+2])
    return imsortie

def my_first_dilate(im):
    imsortie = numpy.copy(im)
    ligne = im.shape[0]
    colonne = im.shape[1]
    for i in range(1, ligne-1):
        for j in range(1, colonne-1):
            imsortie[i, j] = numpy.amax(im[i-1:i+2, j-1:j+2])
    return imsortie

def myerode(img, el):
    return cv2.erode(img, el)

def mydilate(img, el):
    return cv2.dilate(img, el)

def mygrad(img, st):
    return mydilate(img, st) - myerode(img, st)

def myopen(img, el):
    return mydilate(myerode(img,el),el)

def myclose(img, el):
    return myerode(mydilate(img,el),el)

def myconddilat(I, M, E):
    return numpy.minimum(I, mydilate(M, E))

def myconderode(I, M, E):
    return numpy.maximum(I, myerode(M, E))

def myreconinf(I, M, E):
    tmp = M
    rec = myconddilat(I, M, E)
    while not numpy.array_equal(tmp, rec):
        tmp = rec
        rec = myconddilat(I, rec, E)
    return rec

def myreconsup(I, M, E):
    tmp = M
    rec = myconderode(I, M, E)
    while not numpy.array_equal(tmp, rec):
        tmp = rec
        rec = myconderode(I, rec, E)
    return rec

def myopenrecon(I, E1, E2):
    return myreconinf(I, myopen(I, E1), E2)
def mycloserecon(I, E1, E2):
    return myreconsup(I, myclose(I, E1), E2)

def myopen_interactif(im, type):
    global rayon

    def myopen_interactif_callback(val):
        global rayon
        rayon=val
        cv2.imshow('ouverture Interactif', myopen(im, strel.build(type, rayon)))

    cv2.namedWindow('ouverture Interactif')
    cv2.createTrackbar('Rayon', 'ouverture Interactif', 10, 100, myopen_interactif_callback)
    myopen_interactif_callback(10)

    cv2.waitKey(0)
    cv2.destroyWindow('ouverture Interactif')
    return open

