import os
from typing import Tuple
from PIL import Image

character_image = './v2/character/snowflake.png'

text_images = []
for root,dirs,files in os.walk('./v2/text'):
    for ff in files:
        file_path = os.path.join(root,ff)
        text_images.append(file_path)

inputs = [
    {
        'name':'snowstream',
        'background': (253, 111, 1),
        'accent': {
            'position': (0,.1)
        },
        'splash': {
            'text':{
                'position': (-0.025,0)
            }
        }
    },
    {
        'name':'snowgroove',
        'background': (172,3,244)
    },
    {
        'name':'snowpage',
        'background': (105, 127, 255),
        'accent': {
            'position': (0,.05)
        }
    },
    {
        'name':'snowtome',
        'background': (255, 255, 255)
    },
    {
        'name':'snowjam',
        'background': (255, 255, 255)
    },
    {
        'name':'snowcloud',
        'background': (255, 255, 255)
    },
    {
        'name':'snowblue',
        'background': (255, 255, 255)
    }
]

exports = [
    {
        'name': 'appicon',
        'width': 1000,
        'height': 1000,
        'character': {
            'position': (.25,.25)
        },
        'accent': {
            'position': (.45,.45)
        },
        'text': {
            'position': (.25,.45)
        },
        'scale': 1
    },
    {
        'name': 'splash',
        'width': 1000,
        'height': 1000,
        'character': {
            'position': (.15,.25)
        },
        'accent': {
            'position': (.5,.25)
        },
        'text': {
            'position': (.2,.55)
        },
        'scale': 1
    },
    {
        'name': 'tvbanner',
        'width': 1200,
        'height': 600,
                'character': {
            'position': (.275,.15)
        },
        'accent': {
            'position': (.525,.15)
        },
        'text': {
            'position': (.175,.25)
        },
        'scale': .5
    },
]

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
    character:dict,
    accent:dict,
    text:dict,
    output_path:str
):
    background = Image.new("RGB", background_size, background_color)

    character_image = Image.open(character['image_path']).convert("RGBA")
    account_image = Image.open(accent['image_path']).convert("RGBA")
    text_image = None
    if not 'appicon' in output_path:
        text_image = Image.open(text['image_path']).convert("RGBA")

    character_image = resize_keep_aspect(character_image, character['size'])
    account_image = resize_keep_aspect(account_image, accent['size'])
    if not 'appicon' in output_path:
        text_image = resize_keep_aspect(text_image, text['size'])

    background.paste(character_image, character['position'], character_image)
    background.paste(account_image, accent['position'], account_image)
    if not 'appicon' in output_path:
        background.paste(text_image, text['position'], text_image)

    background.save(output_path, "PNG")

export_count = 1
export_total = len(exports) * len(inputs)
for export in exports:
    width = export['width']
    height = export['height']
    scale = export['scale']
    print(f"\nExporting {export['name']}")
    for input in inputs:
        export_dir = os.path.join('./generated',input['name'])
        os.makedirs(export_dir,exist_ok=True)
        export_path = os.path.join(export_dir,f"{export['name']}.png")
        print(f"\t({export_count}/{export_total}) {export_path}")
        export_count += 1

        character_position = export['character']['position']
        if 'character' in input and 'position' in input['character']:
            character_position = (character_position[0]+input['character']['position'][0],character_position[1]+input['character']['position'][1])
        character = {
            'image_path': './v2/character/snowflake.png',
            'size': (int(width*scale*.33), None),
            'position': (int(width*character_position[0]), int(height*character_position[1])),
        }

        accent_position = export['accent']['position']
        if 'accent' in input and 'position' in input['accent']:
            accent_position = (accent_position[0]+input['accent']['position'][0],accent_position[1]+input['accent']['position'][1])
        accent = {
            'image_path':f"./v2/accent/{input['name']}.png",
            'size':(int(width*scale*.33), None),
            'position': (int(width*accent_position[0]), int(height*accent_position[1])),
        }

        text_position = export['text']['position']
        if 'text' in input and 'position' in input['text']:
            text_position = (text_position[0]+input['text']['position'][0],text_position[1]+input['text']['position'][1])
        if export['name'] in input and 'text' in input[export['name']] and 'position' in input[export['name']]['text']:
            text_position = (text_position[0]+input[export['name']]['text']['position'][0],text_position[1]+input[export['name']]['text']['position'][1])
        text = {
            'image_path':f"./v2/text/{input['name']}.png",
            'size':(int(width*.65), None),
            'position': (int(width*text_position[0]), int(height*text_position[1])),
        }

        create_composite(
            background_size=(width, height),
            background_color=input['background'],
            character=character,
            accent=accent,
            text=text,
            output_path=export_path
        )

