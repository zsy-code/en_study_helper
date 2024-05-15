# -*- encoding: utf-8 -*-
# ------------------------------------------------------
# A simple gradio interface for word spelling memory aid
# ------------------------------------------------------
# Shiyuan Zhao

import gradio as gr
import requests

def process_text(word):
    data = {'word': word}
    print('starting process word spelling memory aid: ', data)
    result = requests.post('http://127.0.0.1:9000/word_spelling', json=data)
    if 'content' not in result.json():
        return 'ERROR!'
    print('finished process word2story: ', result.json())
    return result.json()['content']


interface = gr.Interface(process_text, 
                         inputs="text",
                         outputs="text",
                         title="Word Spelling Memory Aid Demo",
                         description="Start typing words and click Run button to see the result")

interface.launch()