from PIL import Image, ImageDraw
import math

img = Image.open('assets/logo_pget.png').convert('RGBA')
width, height = img.size
pixels = img.load()

# Center and radius
cx, cy = width / 2.0, height / 2.0
max_r = min(cx, cy)

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # Distance from center
        d = math.sqrt((x - cx)**2 + (y - cy)**2)
        
        # Outer black area
        brightness = (r + g + b) / 3.0
        
        if d > max_r - 2:
            pixels[x, y] = (r, g, b, 0)
        elif brightness < 30:
            # Pure black background outside the logo
            # Check if it's outside the main shield
            if d > max_r * 0.4:
                pixels[x, y] = (r, g, b, 0)
            else:
                pass
        elif brightness < 60 and d > max_r * 0.7:
            # Gradual alpha for the outer glow
            alpha = int(((brightness - 30) / 30.0) * 255)
            pixels[x, y] = (r, g, b, max(0, min(255, alpha)))

img.save('assets/logo_pget.png', 'PNG')
img.save('C:/Users/PC/.gemini/antigravity/brain/098ba3de-2780-4abe-8d88-54767a85600a/logo_pget.png', 'PNG')
print("Successfully replaced assets/logo_pget.png with transparent clean PNG!")

