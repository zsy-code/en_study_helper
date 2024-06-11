
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import random
import json
import config

# 加载本地RAG base 数据集
prefix_dict = json.load(open('dataset/word_formation_rules/prefix.json', 'r', encoding='utf-8'))
suffix_dict = json.load(open('dataset/word_formation_rules/suffix.json', 'r', encoding='utf-8'))
root_dict = json.load(open('dataset/word_formation_rules/root.json', 'r', encoding='utf-8'))


llm = ChatOpenAI(
    temperature=0.5,
    top_p=0.95,
    )

select_methods = Agent(
    role='英语单词学习助手',
    goal="""
    你将要尽最大努力辅助学生进行英语单词的记忆学习，你需要从以下几个角度来进行分析：
    1. 词根(如词根tele-（远距离）:telegraph（电报）、television（电视）,词根bio-（生命）:biology（生物学）、biography（传记）)
    2. 词缀(如否定词前缀un-:unhappy（不快乐）、unable（不能的）, 名词后缀-ion/-tion:information（信息）association（协会）)
    3. 词源
    4. 助记联想
    5. 同源词辨析(给出每个单词的**中文释义**, 单词之间逗号分隔)
    6. 例句(1-2个, 给出中文释义)
    
    注意:
    1. 词根一般需要你从单词中提取出来, 是当前单词的一部分, 也是一个独立的单词, 且**包含单词的核心含义**, 只有一个(一般不是方位或程度词)
    2. 需要区分词缀是前缀还是后缀, 前缀出现在单词开头, 后缀出现在单词结尾, 在其他一些同性词中可找到相同前后缀
    3. 同源词一定是单词而不是短语, 且不要出现输入单词本身, 一般由词根派生而来
    4. 检查助记联想模块的单词拆分是否和原单词一致, 不要多字母或少字母
    5. 词根中不要出现前后缀
    6. 词缀一定完整出现在单词开头或结尾, 没有中间词缀
    7. 不要混淆词根和词缀, 词根一定更包含单词的核心含义或更可能扩展到当前单词的含义
    8. 如果单词没有词根词缀请填“无”, 不要强行拆分, 注意去除词缀后单词剩余部分一定是有意义的
    9. 用中文回答问题
    10. 严格检查词缀是否出现在词首尾!!!

    请你再三思索并**逐条验证**你输出的结果是否符合要求, 如果出现上述任何一处错误, 你将被扣分

    示例:
    input word: information
    output:
    ##词根##\n
    form - 来自拉丁语forma,意为"形状、形式"
    ##词缀##\n
    in- 前缀,含"进入"之意
    -ation 名词后缀,表示"行为/状态"
    ##词源##\n
    information一词源自拉丁语informare,源自in(进入)和formare(形状、塑造),原指"将事物塑造成某种形式"的行为。
    ##助记联想##\n
    可将information拆分为"in-form-ation",联想为"通过一定形式进入(输入)某种状态"、"形成某种认知"。
    ##同源词辨析##\n
    form(形式), reform(改革), formation(形成), formality(正式), informal(非正式的), formula(公式), transform(转变)
    ##例句##\n
    1. Can you give me some information about the project? (你能告诉我一些关于这个项目的信息吗?)
    2. I need more information before making a decision. (在做决定之前,我需要更多的信息。)
  
    """,
    verbose=True,
    backstory=(''),
    tools=[],
    allow_delegation=False, 
    # max_iter=10,
    llm=llm
)

sm_task = Task(
    description=(
    "请对单词 {word}, 生成记忆辅助相关内容。"
    "{word_exp_from_dict}"
    ),
    expected_output='你必须严格按照如下标准输出结果:\n ##词根##\n##词缀##\n##词源##\n##助记联想##\n##同源词辨析##\n##例句##',
    tools=[],
    agent=select_methods,
)

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
    

crew_word_spelling = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    # word = 'euphonious'
    # prompt = search_word_from_localdataset(word)
    # print(prompt)
    # result = crew_word_spelling.kickoff(inputs={'word': word, 'word_exp_from_dict': prompt})
    # print(result)
    intersection = set(prefix_dict.keys()) & set(suffix_dict.keys()) & set(root_dict.keys())
    print(intersection)
    
    # print(prefix_dict['euphonious'])
    # print(suffix_dict['euphonious'])
    # print(root_dict['euphonious'])
    