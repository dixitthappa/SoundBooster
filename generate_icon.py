from PIL import Image, ImageDraw

img = Image.new('RGB', (64, 64), color=(30, 30, 30))
draw = ImageDraw.Draw(img)
draw.polygon([(10,20),(10,44),(28,44),(28,20)], fill=(255,255,255))
draw.polygon([(32,12),(32,52),(52,44),(52,20)], fill=(255,255,255))
img.save('assets/icon.png')
img.save('assets/icon.ico', sizes=[(64, 64), (32, 32), (16, 16)])
print("Icons created.")
