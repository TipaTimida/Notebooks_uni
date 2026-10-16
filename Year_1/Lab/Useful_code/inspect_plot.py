import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import os

# Visualizzazione dell’immagine in matplotlib
# Va da sé: dovete sostituire il percorso al file contenente l’immagine con quello appropriato per voi.
# Una volta aperta l’immagine in matplotlib potete andare sopra con il mouse e
# vedrete la posizione (in pixel) visualizzata sulla barra inferiore della finestra.
# Questo vi permette di misurare manualmente la posizione di un numero arbitrario
# di punti nell’immagine stessa.


# School/Lab/First_semester_home/catenaria.jpg


# -------------------------- INPUT

file_path = '/home/gea/Desktop/notebooks/output.png'
# to get file path, right click on file i want and click on copy path  
 
# ------------------------------



plt.figure('Immagine originale')
img = matplotlib.image.imread(file_path)

# plt.gca().invert_yaxis()
# if want the y axis to have the 0 at bottom, not at top


plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.imshow(img)
plt.show()