import cv2
import numpy as np



# Fonction permettant de realiser l'erosion d'une image par un element structurant
def erosion(image, element_structurant):
    return cv2.erode(image, element_structurant)


# Fonction permettant de realiser la dilatation d'une image par un element structurant
def dilatation(image, element_structurant):
    return cv2.dilate(image, element_structurant)


# Fonction permettant de realiser l'ouverture d'une image par un element structurant
def ouverture(image, element_structurant):
    return dilatation(erosion(image,element_structurant),element_structurant)


# Fonction permettant de realiser la fermeture d'une image par un element structurant
def fermeture(image, element_structurant):
    return erosion(dilatation(image,element_structurant),element_structurant)

# Fonction permettant de calculer le gradient morphologique d'une image (par rapport a un element structurant)
def gradient(image, element_structurant):
   return dilatation(image,element_structurant)- erosion(image,element_structurant)







def myreconinf(mask,el,im):
    back= mask
    dil =myconddilat(mask,el,im)
    while not np.array_equal(back,dil):
        back =dil
        dil =myconddilat(dil,el,im)
    return back


def myconddilat(mask,el,im):
    return np.minimum(dilatation(mask,el),im)













# Fonction permettant de realiser la reconstructions inferieure d'un marqueur dans une image, a l'aide d'un element structurant
def reconstruction_inferieure(image, marqueur, element_structurant):
    backup = marqueur
    #On fait une dilatation conditionnelle du marqueur dans l'image
    dil=np.minimum(dilatation(marqueur, element_structurant), image)
    #A completer
    #dil = ???
    #Tant que la dilatation conditionnelle n'a pas converge
    while( not np.array_equal(backup, dil)):
        backup = dil
        #On refait une dilatation conditionnelle de dil dans image
        dil = np.minimum(dilatation(marqueur, element_structurant), image)
    return dil




# Fonction permettant de realiser l'ouverture par reconstruction d'une image
def ouverture_reconstruction(image, element_ouverture, element_reconstruction):
    return reconstruction_inferieure(ouverture(image,element_ouverture),element_reconstruction,image)



    #A completer
    #return ???



#Fonction permettant de realiser le h-maxima d'une image
#Prend en parametre l'image, le niveau h, et l'element structurant a utiliser pour la reconstruction
def myseuil(im,s):
    res= np.zeros(im.shape,im.dtype)
    res [im>s]=255
    return res

def myseuil_interactif(im):
    global myseuil

    def myseuil_interactif_callback(val):
        global seuil
        seuil=val
        cv2.imshow('Seuil Interactif',myseuil(im,seuil))

    cv2.namedWindow('Seuil Interactif')
    cv2.createTrackbar('Seuil','Seuil Interactif',100,256,myseuil_interactif_callback)
    myseuil_interactif_callback(100)

    cv2.waitKey(0)
    cv2.destroyWindow('Seuil Interactif')
    return seuil