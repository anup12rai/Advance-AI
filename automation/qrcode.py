import qrcode

youtube_url = "https://mime.io/"

img = qrcode.make(youtube_url)
img.save("christmas.png")

print("QR Code generated successfully!")
