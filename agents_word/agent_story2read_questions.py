
from crewai import Agent, Task, Crew
import config

select_methods = Agent(
    role='英文命题老师',
    goal="""
    提供一篇阅读理解英文文章和题型列表, 请你根据文章为每个题型拟一道题目。

    请注意: 题型列表中的每个题型都对应一个英文选择题, 如果所出题目和题目列表中的对应题型不对应, 将会被判为错误。

    输出示例:
    [("question": "What will the man-made island serve as?", "choices": ["A．An energy center.", "B．A living center.", "C．A research center. ", "D．A tour center."], "answer": "A", "explanation": "细节理解题。由文章第二段“The country has promised to stop oil production within the next 30 years, but that means it’s going to need to get its energy from somewhere else. To that end, Denmark has planned to build a man-made island off its coast. (该国已承诺在未来30年内停止石油生产，但这意味着它需要从其它地方获得能源。为此，丹麦计划在其海岸外建造一座人造岛屿。)”可知，丹麦计划在其海岸外建造一座人造岛屿是为了将它作为能源中心。故选A项。", "qtype": "细节理解题")]
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
    "文章:"
    "{article}"
    "题型列表:"
    "{qtype_list}"
    ),
    expected_output='Final Answer请务必按照下面的格式进行输出: [("question": "题目", "choices": [选项列表], "answer": "答案", "explanation": "解析", "qtype": "题型"), ...]',
    tools=[],
    agent=select_methods,
)

crew_auto_question = Crew(
  agents=[select_methods],
  tasks=[sm_task]
)


if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    article = """
    Once upon a time, in a small village nestled between two great mountains, there lived a group of intelligent and confident friends named Alex, Emma, Jack, Kate, and Mike. They were all passionate about playing badminton, but they wanted to make their games more exciting by exploring new ways to play on stage.
    One moment changed everything for them when they stumbled upon an old theater that was abandoned for years. The theater had a big, empty stage with no audience seats, but it still had the potential to become a unique playground for badminton. They decided to transform their passion into a creative project and started brainstorming ideas on how to turn the theater stage into a badminton court.
    Their exploration led them to discover that the old theater was actually an impressive building with a beautiful design, but it needed some renovation before they could play there. The friends worked together using their confidence and intelligence to repair the stage, and after weeks of hard work, their effort paid off.
    The moment of truth arrived when they invited everyone in the village to watch them play on the newly renovated badminton court at the theater. The debate on whether this was a good idea or not continued among the villagers, but Alex, Emma, Jack, Kate, and Mike were determined to prove that their creative project could work.
    The day of the big event arrived, and the friends took center stage, ready to show off their impressive skills in badminton. The atmosphere was tense as they started playing, but the more they played, the more mesmerized the audience became by the way the ball bounced on the stage, creating a unique moment that none had ever seen before.
    The event turned out to be an enormous success, and from that day forward, the old theater became known as the Badminton Theater. The friends continued exploring new ways to play badminton on stage, inspiring others in the village to embrace their creativity and confidence.
    """
    qtype_list = ['细节理解题', '推理判断题', '词义猜测题', '主旨大意题']
    result = crew_auto_question.kickoff(inputs={'article': article, 'qtype_list': str(qtype_list)})
    print(result)