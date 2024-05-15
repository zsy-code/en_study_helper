
from crewai import Agent, Task, Crew, Process

import os
# os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"]="http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"]="lm-studio"

select_methods = Agent(
    role='分镜头设计大师',
    goal='给你一则英文小故事, 你需要为其创建四个分镜头和镜头中的角色映射, 每个镜头要将角色、动作、场景表达充分, 请注意一个镜头中可能出现的多个角色, 这些镜头内容要足以表达整个故事, 且保持逻辑连贯性',
    verbose=True,
    backstory=(
    "示例:"
    "input:"
    "story:##"
    """
    Little Timmy had a puppy named Info who just loved learning new things. One sunny day, Timmy was hunting for bugs under rocks when Info came bounding over.  "What're those cool critters?" Info barked eagerly.
    Timmy excitedly shared all the information he knew about roly-polies - their many legs, armored plates, and love for dark, damp places. Info listened intently, his tail wagging with every fascinating fact.
    From then on, whenever Info saw something new, he'd beg "Tell me the information!" His thirst for knowledge was insatiable. Timmy happily taught the curious pup about birds, flowers, even cloud shapes!
    The boy and his furry friend bonded over their shared love of learning. Asking questions and swapping information brought them endless fun and adventure.
    """
    "##\n"
    "output:"
    "##shot 1##\n"
    'Little Timmy is hunting for bugs under rocks on a sunny day when his puppy Info comes bounding over, curious about the "cool critters" Timmy has discovered.\n'
    "##shot 2##\n"
    'Timmy excitedly shares all the information he knows about roly-polies with the attentive Info, whose tail wags with every new fascinating fact he learns.'
    "##shot 3##\n"
    'From then on, Info constantly begs Timmy "Tell me the information!" about any new thing he encounters, developing an insatiable thirst for knowledge. Timmy happily teaches the curious pup about birds, flowers, clouds, and more.'
    "##shot 4##\n"
    'Timmy and Info form a special bond over their shared love of learning, asking questions and swapping information, which brings them endless fun and adventure together.'
    "##role mapping##\n"
    '["Timmy": "a little boy", "Info": "a dog"]\n'
    "请注意, 角色映射你只需要输出一次即可。"
    "请帮我针对故事 {story} 进行分镜是, 你需要创建 四-五 个分镜, 以及其中的角色映射, 每个分镜内容不多于50词。"
    ),
    tools=[],
    allow_delegation=False, 
    max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现在针对一个给定的故事 {story}, 请你给其进行分镜。"
    ),
    expected_output='你必须严格按照如下标准输出结果:\n ##shot 1##\n##shot 2##\n##shot 3##\n##shot 4##\n##role mapping##',
    tools=[],
    agent=select_methods,
)

crew_story2shots = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == '__main__':
    # Starting the task execution process with enhanced feedback
    story = """
    Once upon a time, in a dense forest, there was a curious squirrel named Nutmeg. She loved to explore and gather information about the world around her. One day, while collecting nuts for winter, Nutmeg stumbled upon a hidden clearing filled with colorful flowers.
    As she wandered through the field, she noticed that each flower had its own unique shape and color. Intrigued by these differences, Nutmeg decided to collect information on each flower's name, appearance, and scent.
    She met a friendly bee named Buzz who was happy to help her gather information about the flowers. Together, they visited many more clearings in the forest, discovering new varieties of flowers with fascinating details.
    With this wealth of information, Nutmeg created an extensive library in her cozy treehouse filled with books and notes on every type of flower she encountered. As time passed, her knowledge became a valuable resource for all the animals in the forest seeking information about nature's wonders.
    """
    result = crew_story2shots.kickoff(inputs={'story': story})
    print(result)
