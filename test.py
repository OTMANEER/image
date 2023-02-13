import numpy

from commun import morpho, strel
import numpy as np
import cv2


def nombre_composantes_8_connexes(image):
    nbMorceaux = 0
    gamma8 = strel.build("carre", 1)
    imMarqueur = np.zeros(image.shape, image.dtype)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i, j] == 255):
                imMarqueur[i, j] = 255
                imReConfInf = morpho.myreconinf(imMarqueur, gamma8, image)
                nbMorceaux += 1
                image = image - imReConfInf
                imMarqueur[i, j] = 0

    return nbMorceaux


def nombre_composantes_8_connexes_v2(imSeuil, imFermeture):
    nbMorceaux = 0
    gamma8 = strel.build("carre", 3)
    imMarqueur = np.zeros(imSeuil.shape, imSeuil.dtype)
    for i in range(imSeuil.shape[0]):
        for j in range(imSeuil.shape[1]):
            if (imFermeture[i, j] == 255):
                imMarqueur[i, j] = 255
                imReConfInf = morpho.myreconinf(imMarqueur, gamma8, imFermeture)
                res = np.minimum(imSeuil, imReConfInf)
                nbMorceaux += 1
                filename = "images/Ligne" + str(nbMorceaux) +".png"
                cv2.imwrite(filename, res)
                imFermeture = imFermeture - imReConfInf
                imMarqueur[i, j] = 0
    return nbMorceaux


# Exo2 Question1
im = cv2.imread("images/adresse1.png")
im = im[:, :, 0]
imOpen = morpho.ouverture(im, strel.build('carre', 10))
imTopHat = im - imOpen
# Exo2 Question2
imSeuil = morpho.myseuil(imTopHat, 35)
# Exo2 Question3
print("Nombre morceaux : " + str(nombre_composantes_8_connexes(imSeuil)))


# cv2.imshow('Fermeture', imFermeture)
# cv2.waitKey(0)

#Exo2 Question4
#La transformation qui permet de supprimer les canyons d’une image est la fermeture
t = 0
nbMorceaux = nombre_composantes_8_connexes(imSeuil)
while nbMorceaux > 3:
    t += 5
    el = strel.build("ligne", t, 0)
    imFermeture = morpho.fermeture(imSeuil, el)
    nbMorceaux = nombre_composantes_8_connexes(imFermeture)
print("t : "+str(t))
print(imFermeture[imSeuil==255])
# Exo2 Question5
el = strel.build("ligne", 15, 0)
imFermeture = morpho.fermeture(imSeuil, el)
nombre_composantes_8_connexes_v2(imSeuil, imFermeture)