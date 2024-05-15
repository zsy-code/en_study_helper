# -*- encoding: utf-8 -*-
# -------------------------------------------------
# Deployment of the task agents
# -------------------------------------------------
# Shiyuan Zhao

from flask import Flask, request, jsonify
from agents.agent_word2story import crew_word2story
from agents.agent_storyboard import crew_story2shots
from agents.agent_sd_prompt import crew_shots2prompts
from agents.agent_word_spelling import crew_word_spelling, search_word_from_localdataset
from agents.agent_homophonic import crew_homophonic, search_exp_in_dict

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