# -*- encoding: utf-8 -*-
# -------------------------------------------------
# Some utility functions used to support the proj
# -------------------------------------------------
# Shiyuan Zhao

from datetime import datetime
import base64
import time
import zipfile
import os, re
import json
from PIL import Image, ImageDraw, ImageFont


def zip_files(file_path_list, zip_file_name):
    """ 从file list 压缩文件到zip file
    """
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for file_path in file_path_list:
            # 获取文件名
            file_name = os.path.basename(file_path)
            # 添加文件到 zip
            zipf.write(file_path, arcname=file_name)


def timestamp():
    """ 获取当前时间戳
    """
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


def encode_file_to_base64(path):
    """ 读取图片文件内容并编码为base64字符串
    """
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def decode_and_save_base64(base64_str, save_path):
    """ 将base64字符串解码并保存到本地
    """
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))


def calculate_text_position(text, font, max_width, padding_in_line):
    """ 计算文本在合并图像中的布局，基本要求：
        1. 文本不能超过最大宽度
        2. 自动换行
        3. 文本行高要保留一部分padding，否则会很难看
        4. 文本行要在图片行col center
    """
    padding_left = int(max_width * 0.1)
    padding_right = int(max_width * 0.1)
    max_width -= padding_left + padding_right
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        bbox = font.getbbox(current_line + word)
        if bbox[2] - bbox[0] <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    height = (bbox[3] - bbox[1] + 2 * padding_in_line) * len(lines)
    return lines, max_width, height


def merge_images(file_list, merge_file_path, shot_list):
    """ 合拼图像为m行n列, 每行后增加空白区域附加shot text说明
    """
    # 打开16张需要拼接的图像
    images = [Image.open(file) for row in file_list for file in row]

    # 计算图像的宽高
    width, height = images[0].size
    # 设置最大文本宽度
    max_text_width = 512
    padding_in_text_line = 2

    columns = len(file_list[0])
    rows = len(file_list)
    # 创建一个新的大图像
    new_image_width = columns * width + max_text_width
    new_image_height = rows * height
    new_image = Image.new('RGB', (new_image_width, new_image_height), (255, 255, 255))

    # 将16张图像拼接到新的大图像上
    for row in range(rows):
        for col in range(columns):
            image_index = row * columns + col
            left = col * width
            top = row * height
            right = left + width
            bottom = top + height
            new_image.paste(images[image_index], (left, top, right, bottom))

    # 添加文本
    draw = ImageDraw.Draw(new_image)
    font = ImageFont.load_default().font_variant(size=32)  # 使用Arial字体, 大小为36

    # 每行后添加文本
    for row in range(rows):
        text = shot_list[row]
        lines, box_width, box_height = calculate_text_position(text, font, max_text_width, padding_in_text_line)
        text_x_start = columns * width + int(max_text_width * 0.1)
        text_y_start = row * height + (height - box_height) // 2 + padding_in_text_line
        for line in lines:
            draw.text((text_x_start, text_y_start), line, font=font, fill=(0, 0, 0))  # 添加黑色文本
            text_y_start += box_height // len(lines) + padding_in_text_line

    # 保存拼接后的大图像
    new_image.save(merge_file_path)


def clean_response_text_to_json(text):
    """
    由于crewAI的expected output中并不能接受{}, 否则会被识别为待替换字段, 因此{} 都用() 代替, 先还原后验证
    """
    text = re.sub('\[\s*\(', lambda x: x.group().replace('(', '{'), text)
    text = re.sub('"\),\s*\("', lambda x: x.group().replace('(', '{').replace(')', '}'), text)
    text = re.sub('\)\s*\]', lambda x: x.group().replace(')', '}'), text)
    
    try:
        obj = json.loads(text)
        return obj
    except json.JSONDecodeError:
        print(text)
        return None


if __name__ == '__main__':
    # base_path = 'images_out/txt2img'
    # file_list = os.listdir(base_path)
    # file_list = [os.path.join(base_path, file) for file in file_list]
    # file_list = [file_list[i:i+4] for i in range(0, len(file_list), 4)]
    # shot_list = [
    #     'Benny asked the tree, "How do you hold so much information? Is it your age, size, or something else?" The tree replied, "It\'s not just about how old I am or how big I grow. It\'s all about collecting and sharing knowledge."',
    #     'One day, Benny decided to explore further, and he came across a stream that flowed with water rich in minerals. He asked the stream, "How do you hold so much information?" The stream replied, "I collect tiny pieces of rock and soil from far away lands and carry them with me, using my flow to distribute them."',
    #     'Benny continued his journey, meeting more creatures who shared their stories about holding information. He met a bird named Bella who had seen the world from high above and stored her experiences in her memory.',
    #     'As Benny gathered all this information, he realized that each living thing held its own unique knowledge. He learned that information was not just found in books but also in nature\'s wonders.'
    # ]
    # merge_images(file_list, 'merged.png', shot_list)

    response_text = """
    [("question": "What was the group of friends' passion?", "choices": ["A．Playing chess", "B．Learning languages", "C．Badminton", "D．Cooking"], "answer": "C", "explanation": "细节理解题。文章第一段提到‘They were all passionate about playing badminton…’，所以他们的热情是打羽毛球。", "qtype": "细节理解题"),
    ("question": "Why did the friends choose to transform their passion into a creative project?", "choices": ["A．To make more money", "B．To explore new ways to play on stage", "C．To repair the old theater", "D．To impress the villagers"], "answer": "B", "explanation": "推理判断题。根据文章第二段，他们决定将他们的热情转化为一个创意项目是为了‘探索新的在舞台上的玩法’。因此，选择正确的是B选项。", "qtype": "推理判断题"),
    ("question": "What is the word for a building designed to have performances or exhibitions?", "choices": ["A．Theater", "B．Museum", "C．Stadium", "D．Park"], "answer": "A", "explanation": "词义猜测题。文章提到‘an old theater that was abandoned for years’，所以这个词应对是‘theater’。", "qtype": "词义猜测题"),
    ("question": "What happened to the old theater after the friends renovated it?", "choices": ["A．It became a park", "B．It remained abandoned", "C．It became known as the Badminton Theater", "D．It was demolished"], "answer": "C", "explanation": "主旨大意题。文章最后提到‘从那一天起，旧剧院就成为了Badminton剧场’，所以正确答案是C选项。", "qtype": "主旨大意题")]
    """
    lst = clean_response_text_to_json(response_text)
    for item in lst:
        print(item)