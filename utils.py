import matplotlib.pyplot as plt
import cv2

# Utilidades para mostrar imágenes
plt.rcParams['figure.figsize'] = [10, 5]
def show(img, title=""):
    if len(img.shape) == 2:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()