
from crewai import Agent, Task, Crew, Process
import config

questions = {
    "junior": """
    [("question": "Their exploration led them to discover that the old theater was actually an ____ building with a beautiful design, but it needed some renovation before they could play there.",
    "answer": "impressive",
    "explanation": "他们的探索使他们发现，旧剧院实际上是一座设计精美的令人印象深刻的建筑，但在他们可以在那里玩之前需要进行一些翻修。",
    "word": "impressive"),
    ("question": "The friends worked together using their ____ and intelligence to repair the stage, and after weeks of hard work, their effort paid off.",
    "answer": "confidence",
    "explanation": "朋友们共同努力，利用他们的信心和智慧修复舞台，经过几周的辛勤工作，他们的努力得到了回报。",
    "word": "confidence"),
    ("question": "The ____ on whether this was a good idea or not continued among the villagers, but Alex, Emma, Jack, Kate, and Mike were determined to prove that their creative project could work.",
    "answer": "debate",
    "explanation": "村民们对这是否是一个好主意的争论一直在继续，但亚历克斯、艾玛、杰克、凯特和迈克决心证明他们的创意项目可以成功。",
    "word": "debate"),
    ("question": "Once upon a time, in a small village nestled between two great mountains, there lived a group of ____ and confident friends named Alex, Emma, Jack, Kate, and Mike.",
    "answer": "intelligent",
    "explanation": "从前，在一个坐落在两座大山之间的小村庄里，住着一群聪明自信的朋友，名叫亚历克斯、艾玛、杰克、凯特和迈克。",
    "word": "intelligent")]

    ## 注意: 请从原文中摘取原句挖空作为题目, 挖空处作答线用“____”表示。
    """,
    "senior": """
    [("question": "The old theater, though abandoned, was an ____ building with a beautiful design.",
    "answer": "impressive",
    "explanation": "那座旧剧院虽然被废弃了，但它是一座设计精美的令人印象深刻的建筑。",
    "word": "impressive"),
    ("question": "The friends used their ____ and intelligence to renovate the stage.",
    "answer": "confidence",
    "explanation": "朋友们用他们的自信和智慧来改造舞台。",
    "word": "confidence"),
    ("question": "The ____ on whether the project would succeed intrigued the villagers.",
    "answer": "debate",
    "explanation": "那些认为项目是否成功的争论吸引了村民们。",
    "word": "debate"),
    ("question": "The friends were known in the village for their ____ solutions to various challenges they encountered.",
    "answer": "intelligent",
    "explanation": "这些朋友以他们对各种遇到的挑战所提出的聪明解决方案而闻名于村庄。")]

    ## 注意：请适当对原文做一些改写再进行挖空, 不要直接摘取原文, 挖空处作答线用“____”表示。
    """
}

select_methods = Agent(
    role='英文单词记忆出题专家',
    goal="""
    给你一篇英文短文和单元词列表, 你将为单词列表中的**每个单词**撰写一个挖空的练习题目, 填空位置即为对应的单词, 题干内容要依照英文短文来编写。
    示例:
    英文短文:
    Once upon a time, in a small village nestled between two great mountains, there lived a group of intelligent and confident friends named Alex, Emma, Jack, Kate, and Mike. They were all passionate about playing badminton, but they wanted to make their games more exciting by exploring new ways to play on stage.
    One moment changed everything for them when they stumbled upon an old theater that was abandoned for years. The theater had a big, empty stage with no audience seats, but it still had the potential to become a unique playground for badminton. They decided to transform their passion into a creative project and started brainstorming ideas on how to turn the theater stage into a badminton court.
    Their exploration led them to discover that the old theater was actually an impressive building with a beautiful design, but it needed some renovation before they could play there. The friends worked together using their confidence and intelligence to repair the stage, and after weeks of hard work, their effort paid off.
    The moment of truth arrived when they invited everyone in the village to watch them play on the newly renovated badminton court at the theater. The debate on whether this was a good idea or not continued among the villagers, but Alex, Emma, Jack, Kate, and Mike were determined to prove that their creative project could work.
    The day of the big event arrived, and the friends took center stage, ready to show off their impressive skills in badminton. The atmosphere was tense as they started playing, but the more they played, the more mesmerized the audience became by the way the ball bounced on the stage, creating a unique moment that none had ever seen before.
    The event turned out to be an enormous success, and from that day forward, the old theater became known as the Badminton Theater. The friends continued exploring new ways to play badminton on stage, inspiring others in the village to embrace their creativity and confidence.
    单元词列表:
    ['impressive', 'confidence', 'debate', 'intelligent']
    挖空题目:
    {question_example}

    请你仔细检查:
    1.题目中必须有做答空
    2,挖空答案必须能填入题目中
    3.挖空答案必须出现在单词列表中

    如果以上条件有任意一条不满足, 你将会收到巨大惩罚
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
    "下面是一个给定的英文短文:\n{article}\n以及对应的单词列表:\n{words}\n 请你为每个单词撰写对应的挖空题目, 并给出答案解析。"
    ),
    expected_output='你必须严格按照如下标准输出结果:\n [("question": "试题内容", "answer": "试题答案", "explanation": "试题解析", "word": "考查单词"), ...]',
    tools=[],
    agent=select_methods,
)

crew_blank_question = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    story = """
    Once upon a time in a small village nestled between two great mountains, there lived a curious young boy named Jack. He loved observing nature, studying insects, and exploring the forest nearby. Nowadays, he decided to take his passion for observing creatures to a higher level by becoming a professional wildlife biologist.
    Jack's career path was not without challenges. As he studied animals in their natural habitats, he realized that many species were disappearing due to human activities. He observed regularly how deforestation affected bird populations and how pollution harmed fish in rivers. His nation needed professionals like him to address these issues.
    One day, Jack discovered a hidden theme park near his village that was built on the ruins of an ancient forest. The management had not been observing their impact on the environment regularly, and Jack decided to act. He organized a team of local students, including himself, to observe the effects of human activities on the ecosystem.
    They collected data on the types of animals living in the forest, how many trees were cut down each year for new rides or attractions, and the amount of waste they produced daily. They even observed the regular bird migrations that took place seasonally.
    After conducting their research, Jack's team presented their findings to the park management, suggesting eco-friendly alternatives for their theme park. The nation was impressed with their hard work, dedication, and commitment to preserving nature. Jack realized that his career choice had a bigger impact than he ever imagined.
    """
    words = "['character', 'nowadays', 'career', 'professional', 'nation', 'theme', 'observe', 'regularly']"
    difficulty = 'junior'
    question_text = questions[difficulty]
    result = crew_blank_question.kickoff(inputs={'article': story, 'words': words, 'question_example': question_text})
    print(result)
