# -*- encoding: utf-8 -*-
# ---------------------------------------------------
# A web app demo for word2story
# ---------------------------------------------------
# Shiyuan Zhao

import gradio as gr
import requests
import re, os
from config import sd_payload
from sd_txt2img import call_txt2img_api
from utils import zip_files, timestamp, merge_images

# use a global variable to store the zip file(all generated images)
download_zip = None

def word_to_story(word, grade, interest):
    """ call crewai's agent to generate story
    """
    interest = '[' + '、'.join(interest) + ']'
    data = {'word': word, 'grade': grade, 'interest': interest}
    print('starting process word2story: ', data)
    result = requests.post('http://127.0.0.1:9000/word2story', json=data)
    if 'story' not in result.json():
        return 'ERROR!'
    print('finished process word2story: ', result.json())
    return result.json()['story']


def story_to_shots(story):
    """ call crewai's agent to generate shots
    """
    data = {'story': story}
    print('starting process story2shots: ', data)
    result = requests.post('http://127.0.0.1:9000/story2shots', json=data)
    if 'shots' not in result.json():
        return 'ERROR!'
    print('finished process story2shots: ', result.json())
    return result.json()['shots']


def shots_to_prompts(shots):
    """ call crewai's agent to generate prompts
    """
    data = {'shots': shots}
    print('starting process shots2prompts: ', data)
    result = requests.post('http://127.0.0.1:9000/shots2prompts', json=data)
    if 'prompts' not in result.json():
        return 'ERROR!'
    print('finished process shots2prompts: ', result.json())
    return result.json()['prompts']


def extract_prompts_from_text(text):
    """ extract prompts from AI generated text(used to txt2img)
    """
    if re.search('\n[A-Za-z ]*?(final answer|Final Answer)', text):
        text = text[:re.search('\n[A-Za-z ]*?(final answer|Final Answer)', text)]
    
    prompts_list = re.split('##shot \d##', text)
    prompts_list = [p.strip() for p in prompts_list if p.strip() != '']
    if len(prompts_list) in [4, 5]:
        return prompts_list
    return None

def extract_shots_from_text(text):
    """ extract shots from AI generated text(used to render image)
    """
    if re.search('\n[A-Za-z ]*?(final answer|Final Answer)', text):
        text = text[:re.search('\n[A-Za-z ]*?(final answer|Final Answer)', text)]
    
    if re.search('##[Ss]hot \d##', text):
        text = text[re.search('##[Ss]hot \d##', text).start():]
    shots_list = re.split('##[Ss]hot \d##', text)
    shots_list = [p.strip() for p in shots_list if p.strip() != '']
    if len(shots_list) in [4, 5]:
        return shots_list
    return None


def generate_images(prompt_list, shots_list):
    """ use sdxl to generate images from prompts
    """
    file_path_list = []
    for prompt in prompt_list:
        template_copy = sd_payload.copy()
        template_copy['prompt'] = prompt
        file_list = call_txt2img_api(**template_copy)
        file_path_list.append(file_list)
    if not os.path.exists('images_out/merge_images'):
        os.makedirs('images_out/merge_images')
    merge_file_path = os.path.join('images_out/merge_images', timestamp() + '.png')
    merge_images(file_path_list, merge_file_path, shots_list)
    return merge_file_path, [file for row in file_path_list for file in row]


def prompts_to_image(prompt, shots):
    """ get all iamges from prompts and zip them info a file
    """
    print('starting process prompts2image: ', prompt)
    prompt_list = extract_prompts_from_text(prompt)
    shots_list  = extract_shots_from_text(shots)
    print('spliting process prompt: ', prompt_list)
    assert prompt_list is not None, 'ERROR!'
    image, file_list = generate_images(prompt_list, shots_list)

    global download_zip
    download_zip = os.path.join('images_out', 'zip_out', timestamp() + '.zip')
    file_list.append(image)
    zip_files(file_list, download_zip)
    return image


def extract_english_story_from_text(text):
    """ extract english story from AI generated text
    """
    if re.search('##[Ee]nglish story##', text):
        story = re.split('##[Ee]nglish story##', text)[1].split('##')[0].strip()
        return story
    return text


# build the web app demo
with gr.Blocks() as demo:
    # title
    title_html = "<div style='text-align:center;font-size:20pt;font-weight:bold'>Word2Story Demo</div>"
    gr.Markdown(title_html)
    # description
    gr.Markdown("Start typing words and click the **save** button after each step to execute the next step.")
    
    # input: textbox(a word) radio_btn(grade) check_box(interests)
    # output: textbox(a story)
    with gr.Row():
        with gr.Column():
            input_word = gr.Textbox(label="input a word")
            radio_choices = ["小学", "初中", "高中"]
            radio_grade = gr.Radio(radio_choices, label="Select a grade", value="小学")
            check_choices = ["自然", "科技", "体育", "知识"]
            checkbox_interests = gr.CheckboxGroup(check_choices, label="Select some interests", value=["自然"])

        output_story = gr.Textbox(lines=8, label="output story")
    with gr.Row():
        btn_run_word2story = gr.Button("Run")
        btn_save_word2story = gr.Button("Save")
    
    # input: textbox(a story)
    # output: textbox(shots)
    with gr.Row():
        input_story = gr.Textbox(lines=5, label="input a story")
        output_shots = gr.Textbox(lines=5, label="output shots")
    with gr.Row():
        btn_run_story2shots = gr.Button("Run")
        btn_save_story2shots = gr.Button("Save")

    # intput: textbox(shots)
    # output: textbox(prompts)
    with gr.Row():
        input_shots = gr.Textbox(lines=5, label="input a shots")
        output_prompts = gr.Textbox(lines=5, label="output prompts")
    with gr.Row():
        btn_run_shots2prompts = gr.Button("Run")
        btn_save_shots2prompts = gr.Button("Save")

    # input: textbox(prompts)
    # output: image(generated image)
    with gr.Row():
        input_prompts = gr.Textbox(lines=10, label="input a prompts")
        output_image = gr.Image(label="output image", type='filepath', interactive=False)
    with gr.Row():
        btn_run_prompts2image = gr.Button("Run")
        btn_save_prompts2image = gr.DownloadButton("Save")
    
    # some click function(run & save button)
    btn_run_word2story.click(fn=word_to_story, inputs=[input_word, radio_grade, checkbox_interests], outputs=output_story)
    btn_save_word2story.click(fn=extract_english_story_from_text, inputs=output_story, outputs=input_story)
    btn_run_story2shots.click(fn=story_to_shots, inputs=input_story, outputs=output_shots)
    btn_save_story2shots.click(fn=lambda x: x, inputs=output_shots, outputs=input_shots)
    btn_run_shots2prompts.click(fn=shots_to_prompts, inputs=input_shots, outputs=output_prompts)
    btn_save_shots2prompts.click(fn=lambda x: x, inputs=output_prompts, outputs=input_prompts)
    btn_run_prompts2image.click(fn=prompts_to_image, inputs=[input_prompts, input_shots], outputs=output_image)
    btn_save_prompts2image.click(fn=lambda x: download_zip, inputs=output_image, outputs=btn_save_prompts2image)

# launch the web app demo
demo.launch()