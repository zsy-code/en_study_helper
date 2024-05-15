
from crewai import Agent, Task, Crew, Process

import os
# os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"]="http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"]="lm-studio"

select_methods = Agent(
    role='stable diffusion AI绘画文生图prompt设计专家',
    goal='给你一组分镜头和对应的角色映射表, 你需要给每个分镜头设计AI绘画的prompt, 以帮助AI生成尽可能符合故事场景的图片。',
    verbose=True,
    backstory=(
    "示例:"
    "input:"
    """
    ##shot 1##
    Little Timmy is hunting for bugs under rocks on a sunny day when his puppy Info comes bounding over, curious about the "cool critters" Timmy has discovered.
    ##shot 2##
    Timmy excitedly shares all the information he knows about roly-polies with the attentive Info, whose tail wags with every new fascinating fact he learns.
    ##shot 3##
    From then on, Info constantly begs Timmy "Tell me the information!" about any new thing he encounters, developing an insatiable thirst for knowledge. Timmy happily teaches the curious pup about birds, flowers, clouds, and more.
    ##shot 4##
    Timmy and Info form a special bond over their shared love of learning, asking questions and swapping information, which brings them endless fun and adventure together.
    ##role mapping##
    ["Timmy": "a little boy", "Info": "a dog"]
    """
    "output:"
    """
    ##shot 1##
    photorealistic painting, little boy examining bugs under rocks, curious puppy dog bounding over, natural garden setting with flowers and trees, warm sunlight and soft color palette
    ##shot 2##
    photorealistic painting, little boy showing roly-poly bugs to attentive puppy, dog's tail wagging, lush green grassy background, dreamy lighting, soft brushstrokes
    ##shot 3##
    photorealistic painting, little boy teaching curious puppy about birds and blooming flowers, dog begging "tell me the information!", blue cloudy sky visible, colorful garden, soft dreamy style
    ##shot 4##
    photorealistic painting, little boy and puppy sitting together reading book, swapping questions and knowledge, close bond over love of learning, dappled sunlight through trees, soft natural color palette
    """
    "单镜头prompt示例:"
    "photorealistic, children's picture books,crayon paintings,blush,white background,simple background,Outgoing, boy, wearing outdoor clothes, wearing a hat, skateboarding, backpack, dirty, a peaceful place"
    
    "请注意, 你需要为故事选择合适的图像风格(写实、动漫、儿童绘画、科技等等), 四个分镜头prompt中的(图像风格)必须一致, 但可以不和示例中的相同。"
    "你需要使用角色映射表中的角色描述(如a dog)来替代角色名(如Info), 比如上面例子中使用little boy替换Timmy, dog替换info, 产出的prompt中##不要出现角色名字##."
    "请帮我下面几个分镜, 撰写相应的stable diffusion prompt, 注意(充分利用role mapping)."
    "{shots}"
    ),
    tools=[],
    allow_delegation=True, 
    max_iter=1,
    # llm=llm
)

sm_task = Task(
    description=(
    "现在针对分镜 {shots}, 请你给每个分镜撰写相应的stable diffusion prompt."
    ),
    expected_output='你必须严格按照如下标准输出结果:\n ##shot 1##\n##shot 2##\n##shot 3##\n##shot 4##',
    tools=[],
    agent=select_methods,
)

crew_shots2prompts = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    shots = """
    ##shot 1##
    In a dense forest, Nutmeg, a curious squirrel, explores her surroundings while collecting nuts for winter. She stumbles upon a hidden clearing filled with colorful flowers, catching her attention.
    ##shot 2##
    Nutmeg notices the unique shape and color of each flower, sparking her curiosity. She decides to gather information on each flower's name, appearance, and scent.
    ##shot 3##
    Nutmeg meets Buzz, a friendly bee who is happy to help her collect information about the flowers. Together, they visit many more clearings in the forest, discovering new varieties of flowers with fascinating details.
    ##shot 4##
    With this wealth of information, Nutmeg creates an extensive library in her cozy treehouse filled with books and notes on every type of flower she encountered. As time passes, her knowledge becomes a valuable resource for all the animals in the forest seeking information about nature's wonders.
    ##role mapping##
    ["Nutmeg": "a curious squirrel", "Buzz": "a friendly bee"]
    """
    result = crew_shots2prompts.kickoff(inputs={'shots': shots})
    print(result)