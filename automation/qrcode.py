import qrcode

# Create simple QR code
img = qrcode.make("Hello World")

# Save image
img.save("hello_world.png")

print("QR code created: hello_world.png")
