# -*- encoding: utf-8 -*-
# -------------------------------------------------
# Deployment of the task agents
# -------------------------------------------------
# Shiyuan Zhao

from flask import Flask, request, jsonify
from agents_word.agent_word2story import crew_word2story
from agents_word.agent_words2story import crew_words2story
from agents_word.agent_storyboard import crew_story2shots
from agents_word.agent_sd_prompt import crew_shots2prompts
from agents_word.agent_word_spelling import crew_word_spelling, search_word_from_localdataset
# from agents_word.agent_homophonic import crew_homophonic, search_exp_in_dict
from agents_word.agent_word2sentence import crew_word2sentence
from agents_word.agent_story2read_questions import crew_auto_question
from agents_word.agent_story2blank_questions import crew_blank_question, questions
from utils import clean_response_text_to_json
import traceback
import config

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/word2story', methods=['POST'])
def word_to_story():
    """ input: word, grade, interest
        output: a word-association story
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    word = data.get('word', None)
    grade = data.get('grade', None)
    interest = data.get('interest', None)
    if None in [word, grade, interest]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'word': word, 'grade': grade, 'interest': interest}
        result = crew_word2story.kickoff(inputs=inputs)
        return {'story': result}
    

@app.route('/words2story', methods=['POST'])
def words_to_story():
    """ input: words, grade, interest
        output: a word-association story
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    words = data.get('words', None)
    grade = data.get('grade', None)
    interest = data.get('interest', None)
    word_count = data.get('word_count', None)

    if None in [words, grade, interest, word_count]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'words': words, 'grade': grade, 'interest': interest, 'word_count': word_count}
        result = crew_words2story.kickoff(inputs=inputs)
        return {'story': result}


@app.route('/story2shots', methods=['POST'])
def story_to_shots():
    """ input: a word-association story
        output: several groups of storyboards divided into stories
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    story = data.get('story', None)
    if None in [story]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'story': story}
        result = crew_story2shots.kickoff(inputs=inputs)
        return {'shots': result}


@app.route('/shots2prompts', methods=['POST'])
def shots_to_prompts():
    """ input: several groups of storyboards divided into stories
        output: several prompts for each group of storyboards   
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    shots = data.get('shots', None)
    if None in [shots]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'shots': shots}
        result = crew_shots2prompts.kickoff(inputs=inputs)
        return {'prompts': result}
    

@app.route('/word2sentence', methods=['POST'])
def word_to_sentence():
    """ input: several groups of storyboards divided into stories
        output: several prompts for each group of storyboards   
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    word = data.get('word', None)
    grade = data.get('grade', None)
    interest = data.get('interest', None)

    if None in [word, grade, interest]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'word': word, 'grade': grade, 'interest': interest}
        for _ in range(3):
            try:
                result = crew_word2sentence.kickoff(inputs=inputs)
                result = clean_response_text_to_json(result)
                assert result is not None, result
                break
            except:
                print(traceback.format_exc())
                
        return {'sentences': result}
    

@app.route('/story2read_questions', methods=['POST'])
def story_to_read_questions():
    """ input: several groups of storyboards divided into stories
        output: several prompts for each group of storyboards   
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    article = data.get('article', None)
    qtype_list = data.get('qtype_list', None)
    if None in [qtype_list, article]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'article': article, 'qtype_list': qtype_list}
        for _ in range(3):
            try:
                result = crew_auto_question.kickoff(inputs=inputs)
                result = clean_response_text_to_json(result)
                break
            except:
                print(traceback.format_exc())

        return {'questions': result}
    

@app.route('/story2blank_questions', methods=['POST'])
def story_to_blank_questions():
    """ input: several groups of storyboards divided into stories
        output: several prompts for each group of storyboards   
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    story = data.get('story', None)
    words = data.get('words', None)
    difficulty = data.get('difficulty', None)
    question_text = questions[difficulty]

    if None in [story, words, question_text]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'article': story, 'words': words, 'question_example': question_text}
        for _ in range(3):
            try:
                result = crew_blank_question.kickoff(inputs=inputs)
                result = clean_response_text_to_json(result)
                break
            except:
                print(traceback.format_exc())

        return {'questions': result}
    

@app.route('/word_spelling', methods=['POST'])
def word_spelling():
    """ input: word
        output: root, affix, etymology, memory point, etc.
    """
    request.environ['werkzeug.server.shutdown'] = 600
    data = request.json
    word = data.get('word', None)
    prompt_rag_spelling = search_word_from_localdataset(word)
    prompt_rag_homophones = search_exp_in_dict(word)
    if None in [word]:
        return jsonify({'error': 'missing parameters'})
    else:
        inputs = {'word': word, 'word_exp_from_dict': prompt_rag_spelling}
        result_spelling = crew_word_spelling.kickoff(inputs=inputs)
        inputs = {'word': word, 'prompt_from_local_dataset': prompt_rag_homophones}
        result_homophones = crew_homophonic.kickoff(inputs=inputs)
        return {'content': result_spelling + '\n\n' + result_homophones}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)