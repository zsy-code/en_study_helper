
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
    role='英文命题老师',
    goal="""
    现在需要你对给定的一篇文章和已有的n个题目进行改写或仿照题目命题点重新命题, 以帮助学生更好的理解文章和做题方法。
    你需要充分理解题目的题型和考点, 重新命题并且用中文给出答案和解析。
    你首先需要确定你要出的题型是什么, 然后确定你要出的题目考点/方向是什么, 最后再考虑题目内容。
    你要充分理解各种考查点的特性和区别。

    请注意:
    1. 你给出的新题目必须要和原题目考点一样: 如主旨大意题、推理判断题、词义猜测题等
    2. 你给出的新题目必须和原题目题型一样: 如单选题、多选题、填空题等

    输出格式示例:
    ##新题目##
    Plank exercise can help improve ___________ according to the passage.
    A. your metabolism
    B. your balance
    C. your mood
    D. All of the above
    ##答案##
    D
    ##解析##
    A选项"your metabolism",文中提到"Performing plank exercise as a daily home exercise before or after school will not only speed up your metabolism,but also keep your metabolic rate high all day long."
    B选项"your balance",文中说"Doing plank exercise regularly will improve your balance."
    C选项"your mood",文中写到"As a result, it can have a powerful and positive effect on our mood."
    综合原文内容,平板支撑运动可以提高新陈代谢,改善平衡能力,并能给人积极正面的情绪体验,所以D选项"All of the above"是正确答案。
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
    "原文:"
    "{article}"
    "问题:"
    "{question}"
    "答案及解析:"
    "{answer}"
    ),
    expected_output='Final Answer请务必按照下面的格式进行输出: ##新题目##\n##答案##\n##解析##',
    tools=[],
    agent=select_methods,
)

crew_auto_question = Crew(
  agents=[select_methods],
  tasks=[sm_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   cache=True,
#   max_rpm=100,
#   share_crew=True
)

if __name__ == "__main__":
    # Starting the task execution process with enhanced feedback
    article = """
    The world is warming up and humans are the cause, and that means it’s up to us to stop it. The burning of oil and coal is one huge cause, and clean energy (能源) sources are needed greatly if we’re going to make any meaningful changes. But where is all of this clean energy going to come from? Denmark seems to have an idea.
    In Europe, Denmark provides more oil than any other country, but that’s going to change. The country has promised to stop oil production within the next 30 years, but that means it’s going to need to get its energy from somewhere else. To that end, Denmark has planned to build a man-made island off its coast.
    As Fast Company reports, the plan will include the building of the island itself as well as up to 600 wind turbines (涡轮机) to pick up ocean winds and change them into electricity (电). The island will have a size of 20 football fields and will have turbines around it and send power to huge batteries (电池) that can store power for whenever it’s needed. All told, the island should be able to provide power for as many as three million homes, but as more batteries are added, that stored power could be provided for even more homes and businesses.
    “The island is expected to cost about HXDOLLAR34 billion, which is really a lot of money. However, as countries begin to use more green energy, the ones that produce more of it will have the chance to sell it to other countries. As oil and coal burning is not allowed worldwide, those that don’t produce enough green energy might be forced to buy up power from their greener neighbors,” said Fast Company.
    """

    question = """
    What will the man-made island serve as?
    A．An energy center. B．A living center.
    C．A research center. D．A tour center.
    """

    answer = """
    答案: A
    解析: 细节理解题。由文章第二段“The country has promised to stop oil production within the next 30 years, but that means it’s going to need to get its energy from somewhere else. To that end, Denmark has planned to build a man-made island off its coast. (该国已承诺在未来30年内停止石油生产，但这意味着它需要从其它地方获得能源。为此，丹麦计划在其海岸外建造一座人造岛屿。)”可知，丹麦计划在其海岸外建造一座人造岛屿是为了将它作为能源中心。故选A项。
    """
    result = crew_auto_question.kickoff(inputs={'article': article, 'question': question, 'answer': answer})
    print(result)
    