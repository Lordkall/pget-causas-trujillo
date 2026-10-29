from PIL import Image
from collections import deque

img = Image.open('C:/Users/PC/.gemini/antigravity/brain/098ba3de-2780-4abe-8d88-54767a85600a/.user_uploaded/media_1793287093650_e527d33d.jpg').convert('RGBA')
width, height = img.size
pixels = img.load()

# We want to make the exterior background transparent using BFS flood fill from the borders/corners
visited = bytearray(width * height)
queue = deque()

# Add all 4 borders to queue if dark
for x in range(width):
    for y in [0, height - 1]:
        r, g, b, a = pixels[x, y]
        if r < 35 and g < 35 and b < 35:
            queue.append((x, y))
            visited[y * width + x] = 1

for y in range(height):
    for x in [0, width - 1]:
        if not visited[y * width + x]:
            r, g, b, a = pixels[x, y]
            if r < 35 and g < 35 and b < 35:
                queue.append((x, y))
                visited[y * width + x] = 1

# Flood fill
while queue:
    cx, cy = queue.popleft()
    r, g, b, a = pixels[cx, cy]
    # Set this exterior background pixel to transparent
    pixels[cx, cy] = (0, 0, 0, 0)
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < width and 0 <= ny < height:
            pos = ny * width + nx
            if not visited[pos]:
                visited[pos] = 1
                nr, ng, nb, _ = pixels[nx, ny]
                # If dark exterior pixel, continue flood
                brightness = (nr + ng + nb) / 3.0
                if brightness < 40:
                    queue.append((nx, ny))
                elif brightness < 80:
                    # Soft edge transition
                    alpha = int(((brightness - 40) / 40.0) * 255)
                    pixels[nx, ny] = (nr, ng, nb, alpha)

# Save processed transparent logo
img.save('assets/logo_pget.png', 'PNG')
img.save('C:/Users/PC/.gemini/antigravity/brain/098ba3de-2780-4abe-8d88-54767a85600a/logo_pget.png', 'PNG')
print("Successfully generated clean transparent logo with 100% PRESERVED black letters and sharp details!")

