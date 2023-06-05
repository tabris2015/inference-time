from PIL import Image

sizes = {
    "128x128": (128, 128),
    "300x300": (300, 300),
    "400x400": (400, 400),
    "470x470": (470, 470),
    "650x650": (650, 650),
    "680x680": (680, 680),
    "820x820": (820, 820),
    "960x960": (960, 960),
    "992x992": (992, 992),
    "1200x1200": (1200, 1200),
    "1500x1500": (1500, 1500),
}


for image_name, (width, height) in sizes.items():
    img = Image.new(mode="RGB", size=(width, height), color=(100, 100, 100))
    img.save(f"img/{image_name}.png")

