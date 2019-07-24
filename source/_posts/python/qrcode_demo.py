import qrcode

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=1
)
qr.add_data("https://1005281342.github.io")
qr.make(fit=True)
img = qr.make_image()
img.save("crazyofme_qrcode.png")
