import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

path = '/home/gea/Desktop/notebooks/Notebooks/Year_2/Lab_2/easy_fit/data_hist.txt'
y = np.loadtxt(path)
# _, y = np.loadtxt("dati.txt")


# metodo 1 - quanti bin voglio, auomaticamente rimuove outliers  
vm=int(np.average(y))
bons=10
plt.figure(figsize=(8,5))
counts, bins, _ = plt.hist(y,bins=bons,range=(vm-bons/2,vm+bons/2))
xxx=np.linspace(vm-bons/2+.5,vm+bons/2-.5,bons)

# ora x e y sono xxx e counts

# metodo 2 - da dove a dove, rimuovi outliers a mano
'''
# rimuovi outliers  
mean = np.mean(y)
std = np.std(y)
mask = np.abs(y - mean) < 3 * std
Vdig_clean = y[mask]

bin_min = int(np.min(Vdig_clean))
bin_max = int(np.max(Vdig_clean)) + 1
bins = np.arange(bin_min, bin_max + 1, 1)
plt.figure(figsize=(8,5))
plt.hist(Vdig, bins=bins)
'''

# Gaussiana
def ff(x, mean, sigma, A):
    return A * np.exp(-(x-mean)**2/(2*sigma**2))
init = (np.mean(y), np.std(y), max(counts))
pars,covm=curve_fit(ff,xxx,counts,init,absolute_sigma=False)
print(pars)
print(covm)
xx=np.linspace(min(xxx),max(xxx),500)
plt.plot(xx,ff(xx,*pars), color='red')

plt.show()