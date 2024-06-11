
from crewai import Agent, Task, Crew, Process
import json
import os
# os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"]="http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"]="lm-studio"


homo_dict = json.load(open('dataset/homophones/homophones.json', 'r', encoding='utf-8'))
def search_exp_in_dict(word):
    prompt = ""
    if word in homo_dict:
        search_ho_res = homo_dict[word]
        ho_key = search_ho_res.split('->')[0]
        ho_exp = search_ho_res.split('->')[1]
        prompt = f"参考谐音: {ho_key} 原词义: {ho_exp}"
    return prompt

select_methods = Agent(
    role='单词记忆助手',
    goal="""
    帮助中文学生利用谐音梗记忆单词,用中文回答问题
    现给定一个单词，请你首先判断其是否适合以谐音梗的方式辅助记忆，如果是，请你编写对应的谐音梗内容（中文短语或句子），如果不是，请说明理由
    一个好的谐音梗,最好是能用有内在联系的短语或句子来对应单词的读音,这样不仅容易记住发音,而且句子或短语本身也更易记忆。
    注意如果满足以下条件之一拒绝谐音梗创作：
    1.生成的中文词组连贯起来过于牵强
    2.英文发音与中文词组发音不相符, 特别注意发音
    3.谐音梗的短语连在一起太生硬或不容易理解

    如果找不到合适的谐音梗,务必不要强行创作
    示例1:
    input word: ambulance
    ##谐音梗##
    am（俺）bu（不）lan（能）ce（死）
    ##说明##
    俺不能死，**救护车**还没来
    示例2:
    input word: revolution
    ##谐音梗##
    无
    ##说明##
    该单词找不到合适的中文发音短语与之对应

    你给出的说明一定是对前面谐音梗的解释, 并联系到实际单词含义
    """,
    verbose=True,
    backstory=(''),
    tools=[],
    allow_delegation=True, 
    # max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现给定单词: {word}, 请进行谐音梗创作."
    "{prompt_from_local_dataset}"
    ),
    expected_output='Final Answer请务必按照下面的格式进行输出: ##谐音梗##\n##说明##\n',
    tools=[],
    agent=select_methods,
)

crew_homophonic = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    word = "blush"
    prompt = search_exp_in_dict(word)
    result = crew_homophonic.kickoff(inputs={'word': word, 'prompt_from_local_dataset': prompt})
    print(result)