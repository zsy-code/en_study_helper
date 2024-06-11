import json 
import os

word_path = "dataset/word_formation_rules"
import random

# 加载本地RAG base 数据集
prefix_dict = json.load(open('dataset/word_formation_rules/prefix.json', 'r', encoding='utf-8'))
suffix_dict = json.load(open('dataset/word_formation_rules/suffix.json', 'r', encoding='utf-8'))
root_dict = json.load(open('dataset/word_formation_rules/root.json', 'r', encoding='utf-8'))

def search_word_from_localdataset(word):
    prompt = ""
    word_meaning = None
    memory_list = []
    same_source_words = []

    if word in prefix_dict:
        prefix_item = prefix_dict[word]
        prefix_cont = prefix_item['prefix']
        prefix_expl = prefix_dict[prefix_cont]['exp']
        prompt += f'\n【前缀: {prefix_cont}, 说明: {prefix_expl}】'
        if word_meaning is None:
            word_meaning = prefix_item['exp']
        memory_list.append(prefix_item['memory'])
    else:
        prefix_item = None

    if word in suffix_dict:
        suffix_item = suffix_dict[word]
        suffix_cont = suffix_item['suffix']
        if suffix_cont is None:
            return f'{word} 一般用于单词后缀, {suffix_item["exp"]}'
        suffix_expl = suffix_dict[suffix_cont]['exp']
        prompt += f'\n【后缀: {suffix_cont}, 说明: {suffix_expl}】'
        if word_meaning is None:
            word_meaning = suffix_item['exp']
        memory_list.append(suffix_item['memory'])
    else:
        suffix_item = None
    
    if word in root_dict:
        root_item = root_dict[word]
        root_cont = root_item['root']
        root_expl = root_dict[root_cont]['exp']
        prompt += f'\n【词根: {root_cont}, 说明: {root_expl}】'
        if word_meaning is None:
            word_meaning = root_item['exp']
        memory_list.append(root_item['memory'])
        same_source_words = [key for key, value in root_dict.items() if value['root'] == root_cont]
        if len(same_source_words) > 5:
          same_source_words = random.sample(same_source_words, 5)
    else:
        root_item = None

    memory_list = [item for item in memory_list if item.strip() != ""]
    memory_prompt = ""
    if len(memory_list) > 0:
        if len(memory_list) == 1:
            memory_prompt = f'【记忆: {memory_list[0]}】'
        else:
            for i, item in enumerate(memory_list):
                memory_prompt += f'{i+1}. {item}\n'
            memory_prompt = f'【记忆: {memory_prompt.strip()}】'
    if word_meaning is not None:
        prompt = f'【词义: {word_meaning}】' + prompt
    prompt += '\n' + memory_prompt
    if len(same_source_words) > 0:
        prompt += f'\n【参考同源词: {", ".join(same_source_words)}】'
    prompt = prompt.strip()
    if prompt != '':
        prompt = '可参考词典查询结果:\n' + prompt
    return prompt


result = []
for file in os.listdir(word_path):
    with open(os.path.join(word_path, file), 'r') as f:
        data = json.load(f)
    for key in data:
        print(key, data[key])
        print(search_word_from_localdataset(key))
        print('-' * 20)