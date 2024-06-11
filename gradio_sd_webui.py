# -*- encoding: utf-8 -*-
# ---------------------------------------------------
# A web app demo for hb sd text2image demo
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

def words_to_story(words, grade, interest, word_count):
    """ call crewai's agent to generate story
    """
    words = re.split(';|；', words)
    interest = '[' + '、'.join(interest) + ']'
    data = {'words': str(words), 'grade': grade, 'interest': interest, 'word_count': word_count}
    print('starting process word2story: ', data)
    result = requests.post('http://127.0.0.1:9000/words2story', json=data)
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
        return story, story
    return text, text


def story_to_blank_questions(words, story, difficulty):
    """ call crewai's agent to generate blank questions based on word list and story
    """
    words = re.split(';|；', words)
    data = {'words': str(words), 'story': story, 'difficulty': difficulty}
    print('starting process story2bq: ', data)
    result = requests.post('http://127.0.0.1:9000/story2blank_questions', json=data)
    if 'questions' not in result.json():
        return 'ERROR!'
    print('finished process story2bq: ', result.json())
    questions = result.json()['questions']
    return_text = ''
    for i, item in enumerate(questions):
        return_text += f'{i+1}.{item["question"]}\n答案: {item["answer"]}\n解析:{item["explanation"]}\n'
    return return_text


def story_to_reading_questions(story, qtypes):
    """ call crewai's agent to generate reading questions based on story and question types
    """
    qtypes = re.split(';|；', qtypes)
    data = {'article': story, 'qtype_list': str(qtypes)}
    print('starting process story2rq: ', data)
    result = requests.post('http://127.0.0.1:9000/story2read_questions', json=data)
    if 'questions' not in result.json():
        return 'ERROR!'
    print('finished process story2bq: ', result.json())
    questions = result.json()['questions']
    return_text = ''
    for i, item in enumerate(questions):
        question_text = item["question"]
        choices_text = "\n".join(item["choices"])
        answer_text = item["answer"]
        explanation_text = item["explanation"]
        return_text += f'{i+1}.{question_text}\n{choices_text}\n答案: {answer_text}\n解析:{explanation_text}\n'
    return return_text
    

def story_to_all_questions(words, story, difficulty, qtypes):
    """ generate all questions based on words, story and question types
    """
    bq = story_to_blank_questions(words, story, difficulty)
    rq = story_to_reading_questions(story, qtypes)
    return bq, rq


def words_to_sentences(words, grade, interests):
    """ call crewai's agent to generate sentences based on word list and grade and interests
    """
    words = re.split(';|；', words)
    result_dict = {}
    for word in words:
        data = {'word': word, 'grade': grade, 'interest': str(interests)}
        print('starting process word2sentence: ', data)
        result = requests.post('http://127.0.0.1:9000/word2sentence', json=data)
        if 'sentences' not in result.json():
            return 'ERROR!'
        print('finished process word2sentence: ', result.json())
        sentences = result.json()['sentences']
        result_dict[word] = sentences
        
    print(result_dict)
    return_text = ''
    for word in words:
        return_text += f'**{word}**:\n'
        for i, sentence in enumerate(result_dict[word]):
            return_text += f'{i+1}. {sentence["sentence"]}\n释义: {sentence["translation"]}\n'
    return return_text


def generate_base_content(words, grade, interest, word_count):
    """ call crewai's agent to generate base content
    """
    story = words_to_story(words, grade, interest, word_count)
    sentences = words_to_sentences(words, grade, interest)
    return story, sentences


# build the web app demo
with gr.Blocks() as demo:
    # title
    title_html = "<div style='text-align:center;font-size:20pt;font-weight:bold'>Stable Diffusion Text2Image Demo</div>"
    gr.Markdown(title_html)
    # # description
    # gr.Markdown("Start typing words and click the **save** button after each step to execute the next step.")
    
    # input: textbox(a word) radio_btn(grade) check_box(interests)
    # output: textbox(a story)
    with gr.Row():
        input_prompt = gr.Textbox(lines=5, label="input prompt")
        input_negative_prompt = gr.Textbox(lines=5, label="input negative prompt")
        # with gr.Column():
        #     btn_run_base_content = gr.Button("Generate")

    with gr.Row():
        with gr.Column():
            input_width = gr.Slider(minimum=128, maximum=2048, step=1, value="768", label="图像宽度", interactive=True)
            input_height = gr.Slider(minimum=128, maximum=2048, step=1, value="512", label="图像高度", interactive=True)

        with gr.Column():
            input_iter = gr.Slider(minimum=1, maximum=20, step=1, value="2", label="总批次数", interactive=True)
            input_batch = gr.Slider(minimum=1, maximum=20, step=1, value="2", label="单批数量", interactive=True)


    with gr.Row():
        # 定义模板数据
        templates = {
            "Template 1": "path/to/example1.jpg",
            "Template 2": "path/to/example2.jpg",
            "Template 3": "path/to/example3.jpg"
        }

# launch the web app demo
demo.launch()