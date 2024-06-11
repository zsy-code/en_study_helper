# -*- encoding: utf-8 -*-
# ------------------------------------------------------
# A sdxl payload config
# ------------------------------------------------------
# Shiyuan Zhao
import os
# os.environ["OPENAI_API_KEY"] = "NA"

BASE_INTFERANCE_MODEL = "vllm"

def config_openai_model(type):
    if type == "vllm":
        os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
        os.environ["OPENAI_API_KEY"] = "token-abc123"
        os.environ["OPENAI_MODEL_NAME"] = "shenzhi-wang/Llama3-8B-Chinese-Chat"
    else:
        os.environ["OPENAI_API_BASE"]="http://localhost:1234/v1"
        os.environ["OPENAI_API_KEY"]="lm-studio"

config_openai_model(BASE_INTFERANCE_MODEL)

sd_payload = {
	"alwayson_scripts": {
		"ADetailer": {
			"args": [False, {
				"ad_cfg_scale": 7,
				"ad_confidence": 0.3,
				"ad_controlnet_guidance_end": 1,
				"ad_controlnet_guidance_start": 0,
				"ad_controlnet_model": "None",
				"ad_controlnet_module": "inpaint_global_harmonious",
				"ad_controlnet_weight": 1,
				"ad_denoising_strength": 0.4,
				"ad_dilate_erode": 4,
				"ad_inpaint_height": 512,
				"ad_inpaint_only_masked": True,
				"ad_inpaint_only_masked_padding": 32,
				"ad_inpaint_width": 512,
				"ad_mask_blur": 4,
				"ad_mask_max_ratio": 1,
				"ad_mask_merge_invert": "None",
				"ad_mask_min_ratio": 0,
				"ad_model": "mediapipe_face_full",
				"ad_negative_prompt": "",
				"ad_noise_multiplier": 1,
				"ad_prompt": "",
				"ad_restore_face": False,
				"ad_steps": 28,
				"ad_use_cfg_scale": False,
				"ad_use_inpaint_width_height": False,
				"ad_use_noise_multiplier": False,
				"ad_use_steps": False,
				"ad_x_offset": 0,
				"ad_y_offset": 0,
				"is_api": []
			}, {
				"ad_cfg_scale": 7,
				"ad_confidence": 0.3,
				"ad_controlnet_guidance_end": 1,
				"ad_controlnet_guidance_start": 0,
				"ad_controlnet_model": "None",
				"ad_controlnet_module": "inpaint_global_harmonious",
				"ad_controlnet_weight": 1,
				"ad_denoising_strength": 0.4,
				"ad_dilate_erode": 4,
				"ad_inpaint_height": 512,
				"ad_inpaint_only_masked": True,
				"ad_inpaint_only_masked_padding": 32,
				"ad_inpaint_width": 512,
				"ad_mask_blur": 4,
				"ad_mask_max_ratio": 1,
				"ad_mask_merge_invert": "None",
				"ad_mask_min_ratio": 0,
				"ad_model": "None",
				"ad_negative_prompt": "",
				"ad_noise_multiplier": 1,
				"ad_prompt": "",
				"ad_restore_face": False,
				"ad_steps": 28,
				"ad_use_cfg_scale": False,
				"ad_use_inpaint_width_height": False,
				"ad_use_noise_multiplier": False,
				"ad_use_steps": False,
				"ad_x_offset": 0,
				"ad_y_offset": 0,
				"is_api": []
			}]
		},
		"API payload": {
			"args": []
		},
		"Additional networks for generating": {
			"args": [True, False, "LoRA", "sdxl_lora_80scartoon(a4e287eb6883)", 1, 1, "LoRA", "None", 1, 1, "LoRA", "None", 1, 1, "LoRA", "None", 1, 1, "LoRA", "None", 1, 1, None, "Refresh models"]
		},
		"Anthony's QR Toolkit": {
			"args": []
		},
		"Aspect Ratio Helper": {
			"args": []
		},
		"Comments": {
			"args": []
		},
		"ControlNet": {
			"args": [{
				"batch_images": "",
				"control_mode": "Balanced",
				"enabled": False,
				"guidance_end": 1,
				"guidance_start": 0,
				"image": None,
				"input_mode": "simple",
				"is_ui": True,
				"loopback": False,
				"low_vram": False,
				"model": "None",
				"module": "none",
				"output_dir": "",
				"pixel_perfect": False,
				"processor_res": -1,
				"resize_mode": "Crop and Resize",
				"threshold_a": -1,
				"threshold_b": -1,
				"weight": 1
			}, {
				"batch_images": "",
				"control_mode": "Balanced",
				"enabled": False,
				"guidance_end": 1,
				"guidance_start": 0,
				"image": None,
				"input_mode": "simple",
				"is_ui": True,
				"loopback": False,
				"low_vram": False,
				"model": "None",
				"module": "none",
				"output_dir": "",
				"pixel_perfect": False,
				"processor_res": -1,
				"resize_mode": "Crop and Resize",
				"threshold_a": -1,
				"threshold_b": -1,
				"weight": 1
			}, {
				"batch_images": "",
				"control_mode": "Balanced",
				"enabled": False,
				"guidance_end": 1,
				"guidance_start": 0,
				"image": None,
				"input_mode": "simple",
				"is_ui": True,
				"loopback": False,
				"low_vram": False,
				"model": "None",
				"module": "none",
				"output_dir": "",
				"pixel_perfect": False,
				"processor_res": -1,
				"resize_mode": "Crop and Resize",
				"threshold_a": -1,
				"threshold_b": -1,
				"weight": 1
			}]
		},
		"Cutoff": {
			"args": [False, "", 0.5, True, False, "", "Lerp", False]
		},
		"Extra options": {
			"args": []
		},
		"Face Editor EX": {
			"args": [False, 1.6, 0.97, 0.4, 0, 20, 0, 12, "", True, False, False, False, 512, False, True, ["Face"], False, "{\n    \"face_detector\": \"RetinaFace\",\n    \"rules\": {\n        \"then\": {\n            \"face_processor\": \"img2img\",\n            \"mask_generator\": {\n                \"name\": \"BiSeNet\",\n                \"params\": {\n                    \"fallback_ratio\": 0.1\n                }\n            }\n        }\n    }\n}", "None", 40]
		},
		"Hypertile": {
			"args": []
		},
		"LLuL": {
			"args": [False, 1, 0.15, False, "OUT", ["OUT"], 5, 0, "Bilinear", False, "Bilinear", False, "Lerp", "", "", False, False, None, True]
		},
		"OpenPose Editor": {
			"args": []
		},
		"Refiner": {
			"args": [False, "", 0.8]
		},
		"Sampler": {
			"args": [20, "DPM++ 2M", "Automatic"]
		},
		"Seed": {
			"args": [-1, False, -1, 0, 0, 0]
		},
		"Simple wildcards": {
			"args": []
		}
	},
	"batch_size": 2,
	"cfg_scale": 7,
	"comments": {},
	"denoising_strength": 0.7,
	"disable_extra_networks": False,
	"do_not_save_grid": False,
	"do_not_save_samples": False,
	"enable_hr": False,
	"height": 512,
	"hr_negative_prompt": "",
	"hr_prompt": "",
	"hr_resize_x": 0,
	"hr_resize_y": 0,
	"hr_scale": 2,
	"hr_second_pass_steps": 0,
	"hr_upscaler": "Latent",
	"n_iter": 2,
	"negative_prompt": "ugly, deformed, noisy, blurry, low contrast, ",
	"override_settings": {},
	"override_settings_restore_afterwards": True,
	"prompt": "Sony A7,soft lighting. A squirrel standing on the side of the road with a sign that says \"Nuts wanted\" soft watercolor.,",
	"restore_faces": False,
	"s_churn": 0.0,
	"s_min_uncond": 0.0,
	"s_noise": 1.0,
	"s_tmax": None,
	"s_tmin": 0.0,
	"sampler_name": "DPM++ 2M",
	"scheduler": "Automatic",
	"script_args": [],
	"script_name": None,
	"seed": -1,
	"seed_enable_extras": True,
	"seed_resize_from_h": -1,
	"seed_resize_from_w": -1,
	"steps": 20,
	"styles": [],
	"subseed": -1,
	"subseed_strength": 0,
	"tiling": False,
	"width": 768,
    "override_settings": {
        'sd_model_checkpoint': "sd_xl_base_1.0",  # this can use to switch sd model
    },
}