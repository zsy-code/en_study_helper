# -*- encoding: utf-8 -*-
# ---------------------------------------------------
# A tool used to generate ia images from text prompts
# ---------------------------------------------------
# Shiyuan Zhao

import urllib.request
import json
import os
from utils import decode_and_save_base64, timestamp

webui_server_url = 'http://127.0.0.1:7861'

# make some dirs to save generated images/zips
out_dir = 'images_out'
out_dir_t2i = os.path.join(out_dir, 'txt2img')
out_dir_zip = os.path.join(out_dir, 'zip_out')
os.makedirs(out_dir_t2i, exist_ok=True)
os.makedirs(out_dir_zip, exist_ok=True)


def call_api(api_endpoint, **payload):
    """ a general function used to call sd webui api and get response
    """
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'{webui_server_url}/{api_endpoint}',
        headers={'Content-Type': 'application/json'},
        data=data,
    )
    print(f'{webui_server_url}/{api_endpoint}')
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode('utf-8'))


def call_txt2img_api(**payload):
    """ call txt2img api and save generated images
    """
    response = call_api('sdapi/v1/txt2img', **payload)
    result_images_path_list = []
    for index, image in enumerate(response.get('images')):
        save_path = os.path.join(out_dir_t2i, f'txt2img-{timestamp()}-{index}.png')
        decode_and_save_base64(image, save_path)
        result_images_path_list.append(save_path)
    return result_images_path_list


if __name__ == '__main__':
    payload = {
        "prompt": "Photorealistic, forest, young squirrel (a small, curious squirrel), collecting nuts for winter, wondering why some trees provide more nuts than others.",  # extra networks also in prompts
        "negative_prompt": "",
        "seed": -1,
        "steps": 30,
        "width": 768,
        "height": 512,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M",
        "scheduler": "Automatic",
        "n_iter": 2,
        "batch_size": 2,
        "override_settings": {
            'sd_model_checkpoint': "sd_xl_base_1.0",  # this can use to switch sd model
        },
    }
    call_txt2img_api(**payload)