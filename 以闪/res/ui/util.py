# 工具函数
from collections import namedtuple
from random import randint
from time import sleep, time

from ascript.android.action import click
from ascript.android.screen import FindColors, Ocr
from ascript.android import action
from ascript.android.system import R
from ascript.android.screen import FindImages

from .data import *

Point = namedtuple("Point", ["x", "y"])
# 获取参数名
loc = locals()
def get_variable_name(variable):
	for key in loc:
		if loc[key] == variable:
			return key


def e(text = '返回',code = 1):
	if code == 0:
		# error
		p = action.catch_click("程序出错，点击屏幕结束")
		quit()
	elif code == 1:
		# pass
		p = action.catch_click(f"{text}出错，\n点击屏幕手动继续(5s)")
		sleep(5)
	elif code == 2:
		# success
		p = action.catch_click("程序完成，点击结束")
	else:
		pass

	

def check_page():
	while True:
		re = Ocr.mlkitocr_v2(rect =[99,1079,527,1216],pattern = '恭喜获得')
		if re:
			click_blank()
			return 1
		close_x()
		close_back()
		if check_t(COLLECTION, "收集",1):
			return 2

# 点击区域（区域，等待时间）->1
def click_a(rect, wait = 0.5):
	x = randint(rect[0], rect[2])
	y = randint(rect[1], rect[3])
	text = get_variable_name(rect)
	click(x,y)
	print(f"{text}:Click Point({x},{y})")
	sleep(wait)
	return 1

# 点击点（点坐标x，y，范围长度，等待时间）->1
def click_p(px,py, l = 5, wait = 0.5):
	x = randint(px - l, px + l)
	y = randint(py - l, py + l)
	click(x, y)
	print(f"点击({x},{y})")
	sleep(wait)
	return 1

#   识别文字_次数(范围，文本，次数，结束后等待，识别间隔)->0 or (x,y)
def check_t(rect, text,count = 5,wait = 0.5,interval = 0.5):
	i = 0
	print(f"识别：“{text}”...")
	while i < count:
		i+=1
		res = Ocr.paddleocr_v2(rect=rect, pattern=text)
		if not res:
			res = Ocr.mlkitocr_v2(rect=rect, pattern=text)

		if not res:
			print(f"第({i})次未找到“{text}”")
			sleep(interval)

		else:
			print(f"检测到{text}:{res}")# 测试
			x = res[0].center_x
			y = res[0].center_y
			sleep(wait)
			return Point(x,y)

	print(f"未找到“{text}”（{count}）")
	return 0

#   c
def check_t_wait(rect, text, timeout = 30, wait = 0.5, interval = 0.5):
	i = 0
	start_time = time()
	print(f"识别：“{text}”...")
	while time() - start_time > timeout:
		i+=1
		res = Ocr.paddleocr_v2(rect=rect, pattern=text)
		if not res:
			res = Ocr.mlkitocr_v2(rect=rect, pattern=text)
		if not res:
			print(f"第({i})次未找到“{text}”")
			sleep(interval)

		else:
			print(f"检测到{text}:{res}")# 测试
			x = res[0].center_x
			y = res[0].center_y
			sleep(wait)
			return Point(x,y)

	print(f"未找到“{text}”(超时)")
	return 0

#   识别文字_次数(范围，文本，次数，结束后等待，识别间隔)->0 or (x,y)
def identify_t(rect, text='',count = 5,wait = 0.5,interval = 0.5):
	i = 0
	print(f"识别：“{text}”")
	while i < count:
		i+=1
		res = Ocr.paddleocr_v2(rect=rect, pattern=text)
		if not res:
			res = Ocr.mlkitocr_v2(rect=rect, pattern=text)

		if not res:
			print(f"第({i})次未找到“{text}”")
			sleep(interval)

		else:
			print(f"检测到{text}:{res}")# 测试
			t = res[0].text
			sleep(wait)
			return t

	print(f"未找到“{text}”（{count}）")
	return 0

# 点击文字(rect,text，范围长度，等待时间，间隔，随机范围）->01
def click_t(rect, text,count = 5,wait = 0.5,interval = 0.5,l = 5):
	res = check_t(rect, text, count, wait, interval)
	if res:
		click_p(res.x, res.y,l, wait)
		return 1
	else:
		e(text = text)
		return 0


# 检测多色返回(多色描述，范围，描述文本，次数，相似度，结束后等待，识别间隔)->0 or (x,y)
def check_allColor(color_detail, rect, text, count = 1, diff=0.9, wait = 0.5, interval = 0.5):
	i = 0
	print(f"寻找“{text}”中。。。")
	while i < count:
		res = FindColors.find(color_detail, rect = rect, diff = diff)
		i += 1
		if not res:
			print(f"第({i})次未找到“{text}”")
			sleep(interval)

		else:
			print(f"检测到{text}:{res}")# 测试
			x = res.x
			y = res.y
			sleep(wait)
			return Point(x, y)

	print(f"未找到“{text}”（{count}）")
	return 0

# 检测图片(图名，范围，描述文本，次数，相似度，结束后等待，识别间隔)->0 or [x1,y1,x2,y2]
def check_img(img_path, rect, text,count = 1, confidence=0.95, wait = 0.5, interval = 0.5):
	i = 0
	print(f"寻找“{text}”中。。。")
	while i < count:
		res = FindImages.find_all_template([R.img(img_path+".png"),],rect= rect ,confidence= confidence)
		i += 1
		if not res:
			print(f"第({i})次未找到“{text}”")
			sleep(interval)

		else:
			print(f"检测到{text}:{res}")# 测试
			r = res[0]['rect']
			sleep(wait)
			return r

	print(f"未找到“{text}”（{count}）")
	return 0

def click_img(img_path, rect, text,count = 3, confidence=0.95, wait = 0.5, interval = 0.5):
	res = check_img(img_path, rect, text,count, confidence, wait, interval)
	if res:
		click_a(res)
		return 1
	else:
		e(text = text)
		return 0


def click_blank(rect = X_CLOSE):
	click_a(rect)
	return 1

# x检测(次数)->0 or (x,y)
def check_x(count = 1):
	text = "x键"
	res = check_allColor(X_CLOSE_color_detail, X_CLOSE, text,count,0.95)
	if res:
		return Point(res.x,res.y)
	else:
		e(text = text)
		return 0

# x关闭(次数)->01
def close_x(count = 5):
	text = "x键"
	res = check_allColor(X_CLOSE_color_detail, X_CLOSE, text,count,0.95)
	if res:
		click_p(res.x,res.y)
		return 1
	else:
		e(text = text)
		return 0

# 左上角关闭(次数)->01
def close_back():
	text = "返回键"
	res = check_allColor(BACK_CLOSE_color_detail, BACK_CLOSE, text,diff=0.9)
	if res:
		click_p(res.x,res.y)
		return 1
	else:
		e(text = text)
		return 0

# 弹窗关闭()->01
def close_pop():
	text = "x键_弹窗"
	res = check_allColor(X_CLOSE_color_detail, X_CLOSE, text, diff=0.95)
	if res:
		click_p(res.x, res.y)
		return 1
	else:
		e(text = text)
		return 0

