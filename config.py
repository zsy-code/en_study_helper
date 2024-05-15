# -*- encoding: utf-8 -*-
# ------------------------------------------------------
# A sdxl payload config
# ------------------------------------------------------
# Shiyuan Zhao

sd_payload = {
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