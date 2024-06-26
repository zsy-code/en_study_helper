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
gl_file_list = []

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
    if re.search('##[Rr]ole', text):
        text = text[:re.search('##[Rr]ole', text).start()]
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
    global download_zip
    global gl_file_list
    image, gl_file_list = generate_images(prompt_list, shots_list)
    download_zip = os.path.join('images_out', 'zip_out', timestamp() + '.zip')
    gl_file_list.append(image)
    zip_files(gl_file_list, download_zip)
    gl_file_list.insert(0, download_zip)
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
        print(result)
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


def show_all_files(input_prompts):
    global gl_file_list
    return [gr.update(lines=21, max_lines=21), gr.File(value=gl_file_list, visible=True, height=120, interactive=False)]


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
            input_word = gr.Textbox(lines=1.6, label="input some words(separated by ';')")
            radio_grade_choices = ["小学", "初中", "高中"]
            radio_grade = gr.Radio(radio_grade_choices, label="Select a grade", value="小学")
            check_choices = ["自然", "科技", "体育", "生活", "教育", "社会"]
            checkbox_interests = gr.CheckboxGroup(check_choices, label="Select some interests", value=["自然"])
            input_word_count = gr.Number(label="input word count", value=300)
            btn_run_base_content = gr.Button("Run")

        with gr.Column():
            output_story = gr.Textbox(lines=17, label="output story", max_lines=16)
            with gr.Row():
                btn_regenerate_story = gr.Button("Regenerate Story")
                btn_save_word2story = gr.Button("Save")

        with gr.Column():
            output_sentences = gr.Textbox(lines=17, label="output sentences", max_lines=16)
            btn_regenerate_sentences = gr.Button("Regenerate Sentences")
    # with gr.Row():
    #     btn_run_word2story = gr.Button("Run")
    #     btn_save_word2story = gr.Button("Save")
    
    gr.Markdown("---")
    gr.Markdown("## Auto Question Area")
    with gr.Row():
        with gr.Column():
            input_story_quest = gr.Textbox(lines=10, label="input a story", max_lines=10)
            radio_difficulty_choices = ['junior', 'senior']
            radio_difficulty = gr.Radio(radio_difficulty_choices, label="Select a difficulty for blank quesitons", value='junior')
            input_qtype = gr.Textbox(label="input question types(separated by ';')")

        output_blank_questions = gr.Textbox(lines=18, label="output blank questions", max_lines=18)
        output_reading_questions = gr.Textbox(lines=18, label="output reading questions", max_lines=18)
    
    with gr.Row():
        btn_run_all_question = gr.Button("Run")
        btn_regenerate_blank_question = gr.Button("Regenerate BQ")
        btn_regenerate_reading_question = gr.Button("Regenerate RQ")

    gr.Markdown("---")
    gr.Markdown("## Auto Image Area")
    # input: textbox(a story)
    # output: textbox(shots)
    with gr.Row():
        input_story_shots = gr.Textbox(lines=12, label="input a story", max_lines=12)
        output_shots = gr.Textbox(lines=12, label="output shots", max_lines=12)
    with gr.Row():
        btn_run_story2shots = gr.Button("Run")
        btn_save_story2shots = gr.Button("Save")

    # intput: textbox(shots)
    # output: textbox(prompts)
    with gr.Row():
        input_shots = gr.Textbox(lines=12, label="input shots", max_lines=12)
        output_prompts = gr.Textbox(lines=12, label="output prompts", max_lines=12)
    with gr.Row():
        btn_run_shots2prompts = gr.Button("Run")
        btn_save_shots2prompts = gr.Button("Save")

    # input: textbox(prompts)
    # output: image(generated image)
    with gr.Row():
        input_prompts = gr.Textbox(lines=12, label="input prompts", max_lines=12)
        with gr.Column():
            output_image = gr.Image(label="output image", type='filepath', interactive=False, height=324)
            output_files = gr.File(label="output files", interactive=False, visible=False, height=120)
    with gr.Row():
        btn_run_prompts2image = gr.Button("Run")
        btn_save_prompts2image = gr.DownloadButton("Save")
    
    # some click function(run & save button)
    # base generate area
    btn_run_base_content.click(fn=generate_base_content, inputs=[input_word, radio_grade, checkbox_interests, input_word_count], outputs=[output_story, output_sentences])
    btn_save_word2story.click(fn=extract_english_story_from_text, inputs=output_story, outputs=[input_story_quest, input_story_shots])
    btn_regenerate_story.click(fn=words_to_story, inputs=[input_word, radio_grade, checkbox_interests, input_word_count], outputs=output_story)
    btn_regenerate_sentences.click(fn=words_to_sentences, inputs=[input_word, radio_grade, checkbox_interests], outputs=output_sentences)

    # question area
    btn_run_all_question.click(fn=story_to_all_questions, inputs=[input_word, input_story_quest, radio_difficulty, input_qtype], outputs=[output_blank_questions, output_reading_questions])
    btn_regenerate_blank_question.click(fn=story_to_blank_questions, inputs=[input_word, input_story_quest, radio_difficulty], outputs=output_blank_questions)
    btn_regenerate_reading_question.click(fn=story_to_reading_questions, inputs=[input_story_quest, input_qtype], outputs=output_reading_questions)
    
    # image area
    btn_run_story2shots.click(fn=story_to_shots, inputs=input_story_shots, outputs=output_shots)
    btn_save_story2shots.click(fn=lambda x: x, inputs=output_shots, outputs=input_shots)
    btn_run_shots2prompts.click(fn=shots_to_prompts, inputs=input_shots, outputs=output_prompts)
    btn_save_shots2prompts.click(fn=lambda x: x, inputs=output_prompts, outputs=input_prompts)
    btn_run_prompts2image.click(fn=prompts_to_image, inputs=[input_prompts, input_shots], outputs=output_image)
    btn_save_prompts2image.click(fn=show_all_files, inputs=input_prompts, outputs=[input_prompts, output_files])

# launch the web app demo
demo.launch(server_port=6006)