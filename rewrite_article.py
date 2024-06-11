
source_article = """
《Astronomers are enlisting AI to prepare for a data downpour》

In deserts across Australia and South Africa, astronomers are planting forests of metallic detectors that will together scour the cosmos for radio signals. When it boots up in five years or so, the Square Kilometer Array Observatory will look for new information about the universe’s first stars and the different stages of galactic evolution. 

But after synching hundreds of thousands of dishes and antennas, astronomers will quickly face a new challenge: combing through some 300 petabytes of cosmological data a year—enough to fill a million laptops. 

It’s a problem that will be repeated in other places over the coming decade. As astronomers construct giant cameras to image the entire sky and launch infrared telescopes to hunt for distant planets, they will collect data on unprecedented scales. 

“We really are not ready for that, and we should all be freaking out,” says Cecilia Garraffo, a computational astrophysicist at the Harvard-Smithsonian Center for Astrophysics. “When you have too much data and you don’t have the technology to process it, it’s like having no data.”

In preparation for the information deluge, astronomers are turning to AI for assistance, optimizing algorithms to pick out patterns in large and notoriously finicky data sets. Some are now working to establish institutes dedicated to marrying the fields of computer science and astronomy—and grappling with the terms of the new partnership.

In November 2022, Garraffo set up AstroAI as a pilot program at the Center for Astrophysics. Since then, she has put together an interdisciplinary team of over 50 members that has planned dozens of projects focusing on deep questions like how the universe began and whether we’re alone in it. Over the past few years, several similar coalitions have followed Garraffo’s lead and are now vying for funding to scale up to large institutions.

Garraffo recognized the potential utility of AI models while bouncing between career stints in astronomy, physics, and computer science. Along the way, she also picked up on a major stumbling block for past collaboration efforts: the language barrier. Often, astronomers and computer scientists struggle to join forces because they use different words to describe similar concepts. Garraffo is no stranger to translation issues, having struggled to navigate an English-only school growing up in Argentina. Drawing from that experience, she has worked to put people from both communities under one roof so they can identify common goals and find a way to communicate. 

Astronomers had already been using AI models for years, mainly to classify known objects such as supernovas in telescope data. This kind of image recognition will become increasingly vital when the Vera C. Rubin Observatory opens its eyes next year and the number of annual supernova detections quickly jumps from hundreds to millions. But the new wave of AI applications extends far beyond matching games. Algorithms have recently been optimized to perform “unsupervised clustering,” in which they pick out patterns in data without being told what specifically to look for. This opens the doors for models pointing astronomers toward effects and relationships they aren’t currently aware of. For the first time, these computational tools offer astronomers the faculty of “systematically searching for the unknown,” Garraffo says. In January, AstroAI researchers used this method to catalogue over 14,000 detections from x-ray sources, which are otherwise difficult to categorize.

Another way AI is proving fruitful is by sniffing out the chemical composition of the skies on alien planets. Astronomers use telescopes to analyze the starlight that passes through planets’ atmospheres and gets soaked up at certain wavelengths by different molecules. To make sense of the leftover light spectrum, astronomers typically compare it with fake spectra they generate based on a handful of molecules they’re interested in finding—things like water and carbon dioxide. Exoplanet researchers dream of expanding their search to hundreds or thousands of compounds that could indicate life on the planet below, but it currently takes a few weeks to look for just four or five compounds. This bottleneck will become progressively more troublesome as the number of exoplanet detections rises from dozens to thousands, as is expected to happen thanks to the newly deployed James Webb Space Telescope and the European Space Agency’s Ariel Space Telescope, slated to launch in 2029. 

Processing all those observations is “going to take us forever,” says Mercedes López-Morales, an astronomer at the Center for Astrophysics who studies exoplanet atmospheres. “Things like AstroAI are showing up at the right time, just before these faucets of data are coming toward us.”

Last year López-Morales teamed up with Mayeul Aubin, then an undergraduate intern at AstroAI, to build a machine-learning model that could more efficiently extract molecular composition from spectral data. In two months, their team built a model that could scour thousands of exoplanet spectra for the signatures of five different molecules in 31 seconds, a feat that won them the top prize in the European Space Agency’s Ariel Data Challenge. The researchers hope to train a model to look for hundreds of additional molecules, boosting their odds of finding signs of life on faraway planets. 

AstroAI collaborations have also given rise to realistic simulations of black holes and maps of how dark matter is distributed throughout the universe. Garraffo aims to eventually build a large language model similar to ChatGPT that’s trained on astronomy data and can answer questions about observations and parse the literature for supporting evidence. 

“There’s this huge new playground to explore,” says Daniela Huppenkothen, an astronomer and data scientist at the Netherlands Institute for Space Research. “We can use [AI] to tackle problems we couldn’t tackle before because they’re too computationally expensive.” 

However, incorporating AI into the astronomy workflow comes with its own host of trade-offs, as Huppenkothen outlined in a recent preprint. The AI models, while efficient, often operate in ways scientists don’t fully understand. This opacity makes them complicated to debug and difficult to identify how they may be introducing biases. Like all forms of generative AI, these models are prone to hallucinating relationships that don’t exist, and they report their conclusions with an unfounded air of confidence. 

“It’s important to critically look at what these models do and where they fail,” Huppenkothen says. “Otherwise, we’ll say something about how the universe works and it’s not actually true.”

Researchers are working to incorporate error bars into algorithm responses to account for the new uncertainties. Some suggest that the tools could warrant an added layer of vetting to the current publication and peer-review processes. “As humans, we’re sort of naturally inclined to believe the machine,” says Viviana Acquaviva, an astrophysicist and data scientist at the City University of New York who recently published a textbook on machine-learning applications in astronomy. “We need to be very clear in presenting results that are often not clearly explicable while being very honest in how we represent capabilities.”

Researchers are cognizant of the ethical ramifications of introducing AI, even in as seemingly harmless a context as astronomy. For instance, these new AI tools may perpetuate existing inequalities in the field if only select institutions have access to the computational resources to run them. And if astronomers recycle existing AI models that companies have trained for other purposes, they also “inherit a lot of the ethical and environmental issues inherent in those models already,” Huppenkothen says.

Garraffo is working to get ahead of these concerns. AstroAI models are all open source and freely available, and the group offers to help adapt them to different astronomy applications. She has also partnered with Harvard’s Berkman Klein Center for Internet & Society to formally train the team in AI ethics and learn best practices for avoiding biases. 

Scientists are still unpacking all the ways the arrival of AI may affect the field of astronomy. If AI models manage to come up with fundamentally new ideas and point scientists toward new avenues of study, it will forever change the role of the astronomer in deciphering the universe. But even if it remains only an optimization tool, AI is set to become a mainstay in the arsenal of cosmic inquiry. 

“It’s going to change the game,” Garraffo says. “We can’t do this on our own anymore.” 

"""

target_article = """
《Astronomers are enlisting AI to prepare for a data downpour》

In the deserts of Australia and South Africa, astronomers are setting up the Square Kilometer Array Observatory to search the universe for radio signals. This observatory, starting in five years, will collect data about the first stars and galaxy evolution. However, it will generate about 300 petabytes of data annually, creating a challenge for astronomers.

This problem of huge data is growing as astronomers build large cameras and launch infrared telescopes. Cecilia Garraffo, a computational astrophysicist, notes that without proper technology to process this data, it is like having no data at all. To handle this, astronomers are turning to AI, creating programs to help analyze the massive amounts of data.

Garraffo founded AstroAI in 2022 to combine astronomy and computer science. Her team of over 50 members is working on projects to understand the universe and search for extraterrestrial life. Other groups are also forming to seek funding and expand their research.

Astronomers have used AI for years to classify objects like supernovas. With new AI techniques, algorithms can now find patterns in data without specific instructions, helping researchers discover unknown phenomena. For example, AstroAI used AI to identify over 14,000 x-ray sources recently.

AI is also helping to study exoplanet atmospheres. Researchers analyze starlight passing through these atmospheres to find molecules like water and carbon dioxide. AI can speed up this process, which is crucial as the number of exoplanet discoveries increases. Last year, an AstroAI team built an AI model that quickly identified molecules in exoplanet spectra.

Despite the benefits, AI models can be hard to understand and might introduce errors. Scientists must critically evaluate AI results to avoid false conclusions. To ensure fairness, Garraffo’s team makes their AI tools open source and trains in AI ethics. AI is set to become essential in astronomy, changing how astronomers study the universe.
"""

translation_text = """
《天文学家正在利用人工智能来为数据暴雨做好准备》

在澳大利亚和南非的沙漠中，天文学家正在建造平方公里阵列天文台，以搜索宇宙中的无线电信号。这个天文台将在五年后开始运行，收集关于最早恒星和星系演化的数据。然而，它每年将生成约300拍字节的数据，给天文学家带来了巨大的挑战。

随着天文学家建造大型相机和发射红外望远镜，巨量数据的问题愈加严重。计算天体物理学家塞西莉亚·加拉弗说，如果没有合适的技术处理这些数据，就像没有数据一样。为了应对这一挑战，天文学家正在转向人工智能，创建程序帮助分析大量数据。

加拉弗在2022年创立了AstroAI，以结合天文学和计算机科学。她的团队有50多名成员，正在进行理解宇宙和寻找外星生命的项目。其他团队也在成立，寻求资金扩展他们的研究。

多年来，天文学家一直使用人工智能分类超新星等天体。通过新的人工智能技术，算法现在可以在没有特定指令的情况下找到数据中的模式，帮助研究人员发现未知现象。例如，AstroAI最近使用人工智能识别了14000多个x射线源。

人工智能也在帮助研究系外行星的大气层。研究人员通过分析穿过这些大气层的恒星光寻找水和二氧化碳等分子。人工智能可以加速这一过程，这对于不断增加的系外行星发现至关重要。去年，AstroAI团队构建了一个人工智能模型，能够快速识别系外行星光谱中的分子。

尽管有诸多好处，人工智能模型有时难以理解，可能会引入错误。科学家必须批判性地评估人工智能结果，以避免错误结论。为了确保公平，加拉弗的团队将他们的人工智能工具开放源码，并进行人工智能伦理培训。人工智能将在天文学中变得不可或缺，改变天文学家研究宇宙的方式。
"""

hard_words = """
Square Kilometer Array Observatory 平方公里阵列天文台(结合square + observatory + 上下文galaxy & stars 不难推测大意)
computational astrophysicist 计算天体物理学家
supernova 超新星
exoplanet 星系外行星
spectrum 光谱
molecule 分子（根据find molecules like water and carbon 可推知大意）
ethics 伦理
"""

print('input:')
print(source_article)

print('output:')
print(target_article)

print('translation:')
print(translation_text)