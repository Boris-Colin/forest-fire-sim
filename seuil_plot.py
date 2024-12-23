from matplotlib.pyplot import figure
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from test_percolation_seuil import P as X, Q as Y

print("Data generated!")


def sigmoid(x, a, b, c, d):
    return a/(b+np.exp(-c*x))+d


x = np.array(X)
y = np.array(Y)
popt, _ = curve_fit(sigmoid, x, y, maxfev=5000)

# Ordonnées de la courbe fittée
yy = sigmoid(x, *popt)

# Dessin
figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
plt.plot(x, yy, color="blue", linewidth=3)
plt.plot(x, y, 'o', markersize=4, color='red')
plt.xlabel('Densité')
plt.ylabel('Taux forêt brûlée')
plt.show()
