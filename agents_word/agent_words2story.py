
from crewai import Agent, Task, Crew, Process
import config

select_methods = Agent(
    role='英文单词记忆联想大师',
    goal='你将为学生拟定某些单词的英文联想小故事, 故事尽可能要包含单词列表中给到的所有单词, 且尽可能简短精炼 {word_count} 词左右, 同时你要给出全文的中文翻译方便学生记忆, 并用中文总结出故事主题。',
    verbose=True,
    backstory=(''),
    tools=[],
    allow_delegation=True, 
    # max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现在针对一个给定的单词列表 {words}, 你需要写一篇辅助单词记忆的 ##{word_count} 词##左右的英文文章(注意生成文章的单词数量)。"
    "故事的主题可以是 {interest} 中的一种, 如果该兴趣类型的主题在本单词列表形成的文章中过于违和, 可以随机主题, 故事要适合 {grade} 学段的学生阅读。"
    ),
    expected_output='你必须严格按照如下标准输出结果:\n ##english story##\n##chinese translation##\n##story theme##',
    tools=[],
    agent=select_methods,
)

crew_words2story = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # example 1
    words = "['impressive', 'moment', 'confidence', 'badminton', 'debate', 'stage', 'intelligent', 'explore']"
    word_count = "300"
    grade = "小学"
    interest = "自然、生活、科技"
    # example 2
    words = "['character', 'nowadays', 'career', 'professional', 'nation', 'theme', 'observe', 'regularly']"

    # Starting the task execution process with enhanced feedback
    result = crew_words2story.kickoff(inputs={'words': words, 'word_count': word_count, 'grade': grade, 'interest': interest})
    print(result)
