from crewai import Agent, Task, Crew, Process
import config

select_methods = Agent(
    role='英文单词记忆联想大师',
    goal='给你一个单词, 为了辅助记忆请你帮我生成3-5个英文例句, 同时附带句子翻译, 例句中尽量不要出现其他增加记忆负担的难点词汇。',
    verbose=True,
    backstory=(''),
    tools=[],
    # allow_delegation=True, 
    # max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现在针对一个给定的单词 {word}, 你需要生成3-5个和 {interest} 主题相关的，适合 {grade} 学生记忆的英文例句。"
    ),
    expected_output='一个python list, list 中的元素为dict, 每个dict 包含两个key: ["sentence", "translation"], 分别表示英文例句和中文翻译',
    tools=[],
    agent=select_methods,
)

crew_word2sentence = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # example 1
    word = "impression"
    grade = "中学"
    interest = "自然、生活、科技"
    # Starting the task execution process with enhanced feedback
    result = crew_word2sentence.kickoff(inputs={'word': word, 'grade': grade, 'interest': interest})
    print(result)