from commun import morpho,strel
import numpy as np
import cv2

image=cv2.imread("images/adresse1.png")

vert=image[:,:,0]

im_seuil=morpho.myseuil(vert,120)
cv2.imshow("adresse 1",im_seuil)
cv2.waitKey(0)


cv2.imshow("adresse 1",im_seuil)




def connexes(im_seuil):
    vide=np.zeros(im_seuil.shape,im_seuil.dtype)
    ligne,colone = np.nonzero(im_seuil)
    nb_morceau=0
    g8= strel.build("carre",3)
    for pixel in zip(ligne,colone):
        if(im_seuil[pixel]>0):
            vide[pixel]=255
            une_compo= morpho.myreconinf(vide,g8,im_seuil )
            vide[pixel]=0
            im_seuil=im_seuil- une_compo
            nb_morceau = nb_morceau+1
            #cv2.imshow("recons",im_seuil)
            # cv2.waitKey(0)
    return (nb_morceau)

nb=connexes(im_seuil)
t=0
while (nb>3):
    t=t+5
    el=strel.build("ligne",t,0)
    im2=morpho.fermeture(im_seuil,el)
    nb=connexes(im2)

print(t)

el=strel.build("ligne",20,0)
im3=morpho.fermeture(im_seuil,el)
cv2.imshow("recons",im3)
cv2.waitKey(0)

print(connexes(im3))
def connexes2(im_seuil,im3):
    vide=np.zeros(im_seuil.shape,im_seuil.dtype)
    im = np.zeros(im_seuil.shape, im_seuil.dtype)
    ligne,colone = np.nonzero(im_seuil)
    nb_morceau=0
    g8= strel.build("carre",3)
    for pixel in zip(ligne,colone):
        if(im_seuil[pixel]>0):
            vide[pixel]=255
            une_compo= morpho.myreconinf(vide,g8,im3 )
            vide[pixel]=0
            im =np.minimum(une_compo,im_seuil)
            nb_morceau = nb_morceau+1
            cv2.imshow("im",im)
            cv2.waitKey(0)
            im_seuil=im_seuil-im
    return (nb_morceau)
connexes2(im_seuil,im3)