import json

dic = {
'ambulance': '俺不能死=救护车',
'ambition': '俺必胜=雄心',
'agony': '爱过你=痛苦',
'admire': '我的妈啊=羡慕',
'addict': '爱得嗑它=上瘾',
'ail': '哎哟=疼痛',
'appall': '我跑=惊骇',
'bale': '背哦=灾祸',
'bachelor': '白吃了=学士/单身汉',
'blush': '不拉屎（憋得脸红）=脸红',
'camel': '楷模（沙漠之舟骆驼是动物之中的楷模）=骆驼',
'coffin': '靠坟=棺材',
'custom': '卡死他们=海关',
'economy': '依靠农民=经济',
'flee': '飞离=逃跑',
'gauche': '狗屎=粗鲁的',
'hermit': '何处觅=隐士',
'impediment': '一拍就蒙=阻碍',
'landlord': '懒得劳动=地主',
'lynch': '凌迟 =私刑处死',
'lawer': '捞呀=律师',
'morbid': '毛病的=病态',
'newbie': '牛比 =新手/菜鸟',
'obtuse': '我不吐死=愚笨',
'pregenant': '扑来个男的=怀孕',       
'pest': '拍死它=害 虫',
'putrid': '飘臭的=腐烂',
'ponderous': '胖的要死=肥胖的',
'shun': '闪=闪躲',   
'sting': '死盯=蛰',   
'shabby': '傻比=卑鄙的',
'tantrum': '太蠢=脾气发作',
'temper': '太泼=脾气',
}

open('dataset/homophones/homophones.json', 'w').write(json.dumps(dic, ensure_ascii=False))