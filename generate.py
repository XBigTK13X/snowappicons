import os
from typing import Tuple
from PIL import Image

def resize_keep_aspect(img, target_size):
    orig_w, orig_h = img.size
    target_w, target_h = target_size

    if target_w is None and target_h is None:
        return img  # no resize

    if target_w is None:
        # scale width from target height
        scale = target_h / orig_h
        target_w = int(orig_w * scale)
    elif target_h is None:
        # scale height from target width
        scale = target_w / orig_w
        target_h = int(orig_h * scale)

    return img.resize((target_w, target_h), Image.LANCZOS)


def create_composite(
    background_size:Tuple[int,int],
    background_color:Tuple[int,int,int],
    image_a_path:str,
    image_b_path:str,
    image_c_path:str,
    size_a:Tuple[int,int],
    size_b:Tuple[int,int],
    size_c:Tuple[int,int],
    pos_a:Tuple[int,int],
    pos_b:Tuple[int,int],
    pos_c:Tuple[int,int],
    output_path:str
):
    background = Image.new("RGB", background_size, background_color)

    img_a = Image.open(image_a_path).convert("RGBA")
    img_b = Image.open(image_b_path).convert("RGBA")
    if not 'appicon' in output_path:
        img_c = Image.open(image_c_path).convert("RGBA")

    img_a = resize_keep_aspect(img_a, size_a)
    img_b = resize_keep_aspect(img_b, size_b)
    if not 'appicon' in output_path:
        img_c = resize_keep_aspect(img_c, size_c)

    background.paste(img_a, pos_a, img_a)
    background.paste(img_b, pos_b, img_b)
    if not 'appicon' in output_path:
        background.paste(img_c, pos_c, img_c)

    background.save(output_path, "PNG")

character_image = './v2/character/snowflake.png'

text_images = []
for root,dirs,files in os.walk('./v2/text'):
    for ff in files:
        file_path = os.path.join(root,ff)
        text_images.append(file_path)

inputs = [
    ['snowstream',(219, 158, 44)],
    ['snowgroove',(172,3,244)],
    ['snowpage',(105, 127, 255)],
    ['snowtome',(255, 255, 255)],
    ['snowjam',(255, 255, 255)],
    ['snowcloud',(255, 255, 255)],
    ['snowblue',(255, 255, 255)]
]

exports = [
    {
        'name': 'appicon',
        'width': 1000,
        'height': 1000,
        'pos_a': (.20,.20),
        'pos_b': (.40,.40),
        'pos_c': (.25,.45),
        'scale': 1
    },
    {
        'name': 'splash',
        'width': 1000,
        'height': 1000,
        'pos_a': (.15,.25),
        'pos_b': (.5,.25),
        'pos_c': (.2,.55),
        'scale': 1
    },
    {
        'name': 'tvbanner',
        'width': 1200,
        'height': 600,
        'pos_a': (.33,.15),
        'pos_b': (.5,.15),
        'pos_c': (.15,.25),
        'scale': .5
    },
]

export_count = 1
export_total = len(exports) * len(inputs)
for export in exports:
    width = export['width']
    height = export['height']
    scale = export['scale']
    print(f"\nExporting {export['name']}")
    for input in inputs:        
        export_dir = os.path.join('./generated',input[0])
        os.makedirs(export_dir,exist_ok=True)
        export_path = os.path.join(export_dir,f"{export['name']}.png")
        print(f"\t({export_count}/{export_total}) {export_path}")
        export_count += 1
        create_composite(
            background_size=(width, height),
            background_color=input[1],

            image_a_path='./v2/character/snowflake.png',
            size_a=(int(width*scale*.33), None),
            pos_a=(int(width*export['pos_a'][0]), int(height*export['pos_a'][1])),

            image_b_path=f"./v2/accent/{input[0]}.png",
            size_b=(int(width*scale*.33), None),
            pos_b=(int(width*export['pos_b'][0]), int(height*export['pos_b'][1])),

            image_c_path=f"./v2/text/{input[0]}.png",
            size_c=(int(width*.65), None),
            pos_c=(int(width*export['pos_c'][0]), int(height*export['pos_c'][1])),

            output_path=export_path
        )
