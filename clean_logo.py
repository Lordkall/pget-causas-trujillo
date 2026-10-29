from PIL import Image
import numpy as np

img = Image.open('assets/logo_pget.png').convert('RGBA')
arr = np.array(img)

# Corner is black (0,0,0). Let's see: anything near black (< 20 in all RGB channels) from the outside can be made transparent!
# Let's do a flood fill from corners or threshold distance from center
width, height = img.size
center_x, center_y = width / 2, height / 2
max_radius = width / 2

# Inspect edge pixels
print("Top-left corner:", arr[0, 0])
print("Center:", arr[512, 512])

# Let's create an alpha mask where pixels that are black (< 25 in R, G, B) become transparent
r = arr[:, :, 0]
g = arr[:, :, 1]
b = arr[:, :, 2]
brightness = (r.astype(int) + g.astype(int) + b.astype(int)) / 3

# If brightness is low (< 30), make alpha 0; smooth ramp between 30 and 70
alpha = np.clip((brightness - 25) / 45.0 * 255, 0, 255).astype(np.uint8)

# Also ensure outside circular radius is transparent
y, x = np.ogrid[:height, :width]
dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
circle_mask = dist_from_center <= (max_radius - 5)

arr[:, :, 3] = np.minimum(alpha, np.where(circle_mask, 255, 0).astype(np.uint8))

clean_png = Image.fromarray(arr, 'RGBA')
clean_png.save('assets/logo_pget_clean.png', 'PNG')
clean_png.save('C:/Users/PC/.gemini/antigravity/brain/098ba3de-2780-4abe-8d88-54767a85600a/logo_pget_clean.png', 'PNG')
print("Successfully generated assets/logo_pget_clean.png with transparent background!")

