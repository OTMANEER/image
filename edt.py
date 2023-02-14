import cv2
import numpy as np
import morpho, strel, myutil

def filtrer_taille(im, el, n):
    hauteur, largeur = im.shape
    M=np.zeros(im.shape, im.dtype)
    im2 = np.copy(im)
    r=np.zeros(im.shape, im.dtype)
    for i in range(0, hauteur):
        for j in range(0, largeur):
            if (im2[i, j] > 0):
                M[i, j] = 255
                recon_M = morpho.myreconinf(im2, M, el)
                M[i, j] = 0
                im2 = im2-recon_M
                if np.sum(recon_M)/255>n:
                    r=r+recon_M
    return r


im = cv2.imread('feuille1.png', cv2.IMREAD_GRAYSCALE)
#cv2.imshow('edt', im)

d = strel.build('disque', 4)
fe = morpho.myclose(im, d)
#cv2.imshow('edt ferm', fe)

im2 = fe - im

image_traitee = np.copy(im2)

#cv2.imshow('edt ferm res', im2)
s = myutil.myseuil(im2, 25)
#cv2.imshow('Binaire', s)

smax = 0
amax = 0
for angle in range(0,180):
    l=strel.build('ligne', 40, angle)
    op = morpho.myopen(s, l)
    #print(angle)
    somme = np.sum(op)
    if(somme > smax):
        smax = somme
        amax = angle
print(amax)

angle1 = amax
angle2=(angle1+90)%180

l1 = strel.build('ligne', 10, angle1)
l2 = strel.build('ligne', 10, angle2)

#resumtat no satisfaisant
'''
op1 = morpho.myopen(s, l1)
op2 = morpho.myopen(s, l2)
#gamma4:  strel.build('diamant', 1)
res = s-np.maximum(op1, op2)
resop = morpho.myopenrecon(res, strel.build('diamant', 1),  strel.build('diamant', 1))
cv2.imshow('Result', resop)
cv2.waitKey(0)
'''

op1 = morpho.myopen(image_traitee, l1)
op2 = morpho.myopen(image_traitee, l2)
res = np.maximum(op1 , op2)
#s2 = myutil.myseuil_interactif(res)
s2 = myutil.myseuil(res, 25)

g4 = strel.build('diamant', 1)
lignes = filtrer_taille(s2, g4, 100)

texte = s - lignes
texte2 = filtrer_taille(texte, g4, 10)
texte3 = morpho.myclose(texte2, l1)

#colorer les contours du texte

imc = cv2.imread('feuille1.png')
g=morpho.mygrad(texte3, g4)

rouge = imc[:,:,2]
bleuvert = imc[:,:,0]

rouge[g>0] =255
bleuvert[g>0] = 0
imc[:,:,2]=rouge
imc[:,:,0]=bleuvert
imc[:,:,1]=bleuvert

#redressage de l'image
#import myimage

#imc = myimage.rotation(imc, 180-angle1)

#cv2.imshow('image', imc)
cv2.waitKey(0)










