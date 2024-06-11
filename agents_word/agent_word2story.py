
from crewai import Agent, Task, Crew, Process
import config

select_methods = Agent(
    role='英文单词记忆联想大师',
    goal='你将为学生拟定某个单词的英文联想小故事, 仅可能简短精炼200词左右, 该单词要重复出现至少3次, 同时你要给出全文的中文翻译方便学生记忆, 并用中文总结出故事主题。',
    verbose=True,
    backstory=(
    "请帮我针对单词 {word} 写一篇辅助单词记忆的故事, 故事的主题可以是 {interest} 中的一种, 故事要适合 {grade} 学段的学生阅读"
    ),
    tools=[],
    allow_delegation=False, 
    max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现在针对一个给定的单词 {word}，你需要写一篇辅助单词记忆的故事。"
    "故事的主题可以是 {interest} 中的一种, 故事要适合 {grade} 学段的学生阅读。"
    ),
    expected_output='你必须严格按照如下标准输出结果:\n ##english story##\n##chinese translation##\n##story theme##',
    tools=[],
    agent=select_methods,
)

crew_word2story = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    result = crew_word2story.kickoff(inputs={'word': 'information', 'grade': "小学", 'interest': '自然'})
    print(result)
