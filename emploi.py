import cv2
import numpy as np
from commun import morpho,myutil,strel


#compter les composantes connexes
def filtrer_taille(im,el,n):
    hauteur,largeur = im.shape
    M = np.zeros(im.shape,im.dtype)
    im2  = np.copy(im)
    r = np.zeros(im.shape,im.dtype) # le resultat

    for i in range (0,hauteur):
        for j in range(0,largeur):
            if(im2[i,j]>0):
                M[i,j] = 255
                recon_M = morpho.myreconinf(M,el,im2)
                M[i,j] =  0
                im2 = im2-recon_M
                if np.sum(recon_M)/255 > n:
                    r = r+recon_M
    return r

image = cv2.imread('feuille1.png',cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',image)

d = strel.build('disque',4)
fe = morpho.myclose(image,d)

im2 = fe - image
image_traitee  = np.copy(im2)

s= myutil.myseuil(im2,1)
cv2.imshow('fermeture',s)

#pour savoir l'orientationd de l'image on peut faire un elem ligne

smax = 0
amax = 0

for angle in range (0,180):
    ligne = strel.build('ligne', 40, angle)
    op = morpho.myopen(s,ligne)
    somme = np.sum(op)
    if(somme > smax):
        smax = somme
        amax = angle

print(amax)

#Effacer toutes les lignes d'une image et garder que le texte
angle1 =amax
angle2 = (angle1+90)%180
l1 = strel.build('ligne',10,angle1)
l2 = strel.build('ligne',10,angle2)

op1 = morpho.myopen(image_traitee,l1)
op2 = morpho.myopen(image_traitee,l2)

r = np.maximum(op1,op2) # les lignes de l'images

cv2.imshow('r',r)
s2 = myutil.myseuil(r,36)

cv2.imshow('ss',s2)

g4 = strel.build('diamant',1)
lignes = filtrer_taille(s2,g4,200)

cv2.imshow('ligne',s2 - lignes)


texte = s2 - lignes

texte2 = filtrer_taille(texte,g4,10)

texte3 = morpho.myclose(texte2,l1)

#
#
#
# imagec = cv2.imread('feuille1.png')
#
# g = morpho.mygrad(texte3,g4)
#
# imagec[g > 0] = [255,0,0]
#
#
# cv2.imshow('texte',imagec)
#

cv2.waitKey(0)