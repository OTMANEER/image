
import cv2
import numpy
from commun import morpho,strel,myutil



im = cv2.imread('./exo2/adresse1.png')
im = im[:, :, 0]
d = strel.build('carre',10)

im_open = morpho.myopen(im,d)

im_base_open = im - im_open

im_seuil = myutil.myseuil(im_base_open, 34)

def connexe(im_seuil):
    mar = numpy.zeros(im_seuil.shape, im_seuil.dtype)
    nb = 0
    for i in range(im_seuil.shape[0]):
        for j in range(im_seuil.shape[1]):
            if (im_seuil[i,j] == 255) :
                mar[i,j] = 255
                obj = morpho.myreconinf(im_seuil,mar, strel.build('carre',1))
                nb += 1
                im_seuil = im_seuil - obj
                mar[i,j] = 0
    return nb

nb = connexe(im_seuil)
t=0
while(nb>3):
    t=t+5
    el = strel.build('ligne', t, 0)
    nv_img = morpho.myclose(im_seuil, el)
    nb = connexe(nv_img)
    print("nb : " + str(nb))
cv2.imshow('img sep', nv_img)

print("t : " + str(t))

el = strel.build('ligne', 15, 0)



#Dans ce cas on a l'image resultat donc on peut faire le travail suivant avec plein de


el = strel.build('ligne', 15, 1)

cv2.imshow('image fermeture',nv_img)

image_vide = numpy.zeros(nv_img.shape,nv_img.dtype)


cv2.waitKey(0)


mar = numpy.zeros(nv_img.shape, nv_img.dtype)
nb = 0
for i in range(nv_img.shape[0]):
    for j in range(nv_img.shape[1]):
        if (nv_img[i, j] == 255):
            # cv2.imshow('img sep', im_seuil)
            # cv2.waitKey(0)
            mar[i, j] = 255
            obj = morpho.myreconinf(nv_img, mar, strel.build('carre', 1))
            min = numpy.minimum(im_seuil, obj)
            cv2.imwrite('ligne' + str(nb) + '.png', min)
            nb += 1
            nv_img = nv_img - obj
            mar[i, j] = 0





def connexe2(im_seuil):
    el = strel.build('ligne', 15, 1)
    nv_img = morpho.myclose(im_seuil, el)
    mar = numpy.zeros(nv_img.shape, nv_img.dtype)
    nb = 0
    for i in range(nv_img.shape[0]) :
        for j in range(nv_img.shape[1]):
            if (nv_img[i,j] == 255) :
                #cv2.imshow('img sep', im_seuil)
                #cv2.waitKey(0)
                mar[i,j] = 255
                obj = morpho.myreconinf(nv_img,mar, strel.build('carre',1))
                min = numpy.minimum(im_seuil, obj)
                cv2.imwrite('ligne' + str(nb) + '.png', min)
                nb += 1
                nv_img = nv_img - obj
                mar[i,j] = 0
    return nb

connexe2(im_seuil)
