# -*- encoding: utf-8 -*-
# ------------------------------------------------------
# clean data from htmls
# ------------------------------------------------------
# Shiyuan Zhao

from bs4 import BeautifulSoup
import os, re, json


def clean_html_data(html_data):
    html_data = re.sub('<script((?<!</script)[\s\S])*?</script>', '', html_data)
    html_data = re.sub('<style((?<!</style)[\s\S])*?</style>', '', html_data)
    soup = BeautifulSoup(html_data, 'lxml')
    return soup

def check_is_prefix(text):
    if re.search('[A-Za-z]+\-', text):
        return True
    return False

def parse_pre_list_data(html_data, prefix_dict):
    """ parse prefix data from htmls
    """
    soup = clean_html_data(html_data)
    main_divs = soup.find_all('div', {'class': 'flashcard-row'})
    temp_words_list = []
    for item in main_divs:
        p_targets = item.select('p.scf-center, p.scf-body, p.scf-body-l')
        key, value = p_targets[0].text, p_targets[1].text
        temp_words_list.append([key, value])
    
    curr_prefix = None
    for item in temp_words_list:
        word, explanation = item[0], item[1]
        # 去除不需要的音标部分
        explanation = re.sub('/ [^/]*?/ ', '', explanation)
        # 获取记忆内容部分
        if re.search('［记］', explanation):
            exp, memory = explanation.split('［记］')[0], explanation.split('［记］')[1]
        else: 
            exp, memory = explanation, ''

        if check_is_prefix(word):
            curr_prefix = word
            self_type = 'prefix'
        else:
            self_type = 'word'
        
        if self_type == 'prefix':
            prefix_dict[word] = {'exp': exp, 'memory': memory, 'type': self_type, 'prefix': None}
        else:
            prefix_dict[word] = {'exp': exp, 'memory': memory, 'type': self_type, 'prefix': curr_prefix}


def check_is_suffix(text):
    if re.search('\-[A-Za-z]+', text):
        return True
    return False

def parse_post_list_data(html_data, suffix_dict):
    """ parse suffix data from htmls
    """
    soup = clean_html_data(html_data)
    main_divs = soup.find_all('div', {'class': 'flashcard-row'})
    temp_words_list = []
    for item in main_divs:
        p_targets = item.select('p.scf-center, p.scf-body, p.scf-body-l')
        key, value = p_targets[0].text, p_targets[1].text
        temp_words_list.append([key, value])

    curr_suffix = None
    for item in temp_words_list:
        word, explanation = item[0], item[1]
        # 去除不需要的音标部分
        explanation = re.sub('/ [^/]*?/ ', '', explanation)
        # 获取记忆内容部分
        if re.search('［记］', explanation):
            exp, memory = explanation.split('［记］')[0], explanation.split('［记］')[1]
        else: 
            exp, memory = explanation, ''

        if check_is_suffix(word):
            curr_suffix = word
            self_type = 'suffix'
        else:
            self_type = 'word'
        
        if self_type == 'suffix':
            suffix_dict[word] = {'exp': exp, 'memory': memory, 'type': self_type, 'suffix': None}
        else:
            suffix_dict[word] = {'exp': exp, 'memory': memory, 'type': self_type, 'suffix': curr_suffix}
        

def check_is_root(text):
    if re.search('^＝', text.strip()):
        return True
    return False

def parse_root_list_data(html_data, root_dict):
    """ parse root data from htmls
    """
    soup = clean_html_data(html_data)
    main_divs = soup.find_all('div', {'class': 'flashcard-row'})
    temp_words_list = []
    for item in main_divs:
        p_targets = item.select('p.scf-center, p.scf-body, p.scf-body-l')
        key, value = p_targets[0].text, p_targets[1].text
        temp_words_list.append([key, value])
    
    curr_root = None
    for item in temp_words_list:
        word, explanation = item[0], item[1]
        # 去除不需要的音标部分
        explanation = re.sub('/ [^/]*?/ ', '', explanation)
        # 获取记忆内容部分
        if re.search('［记］', explanation):
            exp, memory = explanation.split('［记］')[0], explanation.split('［记］')[1]
        else:
            exp, memory = explanation, ''
        
        if check_is_root(explanation):
            curr_root = word
            self_type = 'root'
        else:
            self_type = 'word'
        
        if self_type == 'root':
            root_dict[word] = {'exp': exp, 'memory': memory, 'type': self_type, 'root': None}
        else:
            root_dict[word] = {'exp': exp, 'memory': memory, 'type': self_type, 'root': curr_root}
        

if __name__ == '__main__':
    prefix_dict = {}
    suffix_dict = {}
    root_dict = {}
    for root, dirs, files in os.walk("word_data_htmls"):
        for file in files:
            if 'pre_' in file:
                file_path = os.path.join(root, file)
                print(file_path)
                html_data = open(file_path, 'r', encoding='utf-8').read()
                parse_pre_list_data(html_data, prefix_dict)
            if 'post_' in file:
                file_path = os.path.join(root, file)
                print(file_path)
                html_data = open(file_path, 'r', encoding='utf-8').read()
                parse_post_list_data(html_data, suffix_dict)
            if 'root_' in file:
                file_path = os.path.join(root, file)
                print(file_path)
                html_data = open(file_path, 'r', encoding='utf-8').read()
                parse_root_list_data(html_data, root_dict)

    print('prefix_dict', len(prefix_dict))
    print('suffix_dict', len(suffix_dict))
    print('root_dict', len(root_dict))

    dataset_path = 'dataset_wfr'
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    
    prefix_path = os.path.join(dataset_path, 'prefix.json')
    suffix_path = os.path.join(dataset_path, 'suffix.json')
    root_path = os.path.join(dataset_path, 'root.json')
    open(prefix_path, 'w', encoding='utf-8').write(json.dumps(prefix_dict, ensure_ascii=False))
    open(suffix_path, 'w', encoding='utf-8').write(json.dumps(suffix_dict, ensure_ascii=False))
    open(root_path, 'w', encoding='utf-8').write(json.dumps(root_dict, ensure_ascii=False))