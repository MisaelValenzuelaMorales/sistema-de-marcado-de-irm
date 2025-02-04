import matplotlib.pyplot as plt
from skimage import io, color
from skimage.metrics import structural_similarity as ssim

# Cargar las imágenes
imagen1 = io.imread('RMI3_o.jpeg')
imagen2 = io.imread('RMI_marcada_1.png')

# Convertir las imágenes a escala de grises si son de color
if imagen1.ndim == 3:
    imagen1 = color.rgb2gray(imagen1)

if imagen2.ndim == 3:
    imagen2 = color.rgb2gray(imagen2)

# Asegurarse de que las imágenes tengan el mismo tamaño
if imagen1.shape != imagen2.shape:
    raise ValueError('Las imágenes deben tener el mismo tamaño.')

# Determinar el rango de datos
data_range = imagen1.max() - imagen1.min()

# Calcular el índice de similitud estructural (SSIM)
ssimval, ssimmap = ssim(imagen1, imagen2, data_range=data_range, full=True)

# Mostrar el valor de SSIM
print(f'El valor de SSIM es: {ssimval:.4f}')

# Mostrar las imágenes y el mapa de similitud
fig, axes = plt.subplots(1, 3, figsize=(10, 4))
ax = axes.ravel()

ax[0].imshow(imagen1, cmap='gray')
ax[0].set_title('Imagen original')

ax[1].imshow(imagen2, cmap='gray')
ax[1].set_title('Imagen marcada')

ax[2].imshow(ssimmap, cmap='jet')
ax[2].set_title(f'Mapa SSIM\n SSIM = {ssimval:.4f}')
plt.colorbar(ax[2].imshow(ssimmap, cmap='jet'), ax=ax[2])

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()

