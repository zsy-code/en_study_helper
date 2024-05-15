from crewai import Agent, Task, Crew, Process
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

import os
# os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"]="http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"]="lm-studio"

llm = ChatOpenAI(
    model = "llama3",
    base_url = "http://localhost:11434/v1")

# llm = HuggingFaceHub(
#     repo_id="shenzhi-wang/Llama3-8B-Chinese-Chat",
#     huggingfacehub_api_token="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",
#     task="text-generation",
# )

select_methods = Agent(
    role='单词拼写记忆大师',
    goal='给指定学段的学生根据其兴趣爱好提供最恰当的单词拼写记忆方法，用中文回答所有问题',
    verbose=True,
    backstory=(
    "你是一名单词拼写记忆大师，你将要对给定的单词 {word} 提供最恰当的拼写记忆方法，针对的具体用户是 {grade} 学段的学生，他们对 {interest} 有浓厚的兴趣爱好。"
    "具体记忆方法包括："
    "1. 拼写规则分析: 分析单词的构词法则、词根词缀、语源等,揭示拼写规律,有助于记忆。"
    "2. 同源词对比: 生成与目标单词同源的其他单词,通过比较差异巩固拼写印象。"
    "3. 首字母记忆法: 创作与单词首字母相关的有趣短语或句子,将拼写融入其中。"
    "4. 谐音梗: 可以运用押韵、双关语等创作与目标单词谐音的有趣短句,激发声音联想。"
    "5. 拼写歌曲/rap: 将拼写规则制成简单的儿歌或rap,有节奏的记忆更容易。"
    "6. 视觉化拼写: 模型生成富有创意的单词拼写图像或动画,将文字形象化有助记忆。"
    "7. 拼写游戏场景: 设计一些拼写游戏场景,让模型根据游戏规则创作相关内容帮助拼写练习。"
    "8. 个性化例句: 针对学生感兴趣的话题,让模型生成包含目标单词的个性化例句,以此加深印象。"
    ),
    tools=[],
    allow_delegation=False, 
    max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现在针对一个给定的单词 {word}，你需要提供最恰当的拼写记忆方法。"
    "你将服务的是 {grade} 学段的学生，他们对 {interest} 有浓厚的兴趣爱好。请你用中文回答所有问题。"
    ),
    expected_output='输出最匹配的三类记忆方法名称',
    tools=[],
    agent=select_methods,
)

crew = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'word': 'information', 'grade': "初中", 'interest': '科技、体育'})
print(result)