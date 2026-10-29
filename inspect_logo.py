from PIL import Image

img = Image.open('assets/logo_pget.png')
print("Format:", img.format)
print("Size:", img.size)
print("Mode:", img.mode)

