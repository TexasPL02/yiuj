from time import time
from ascript.android import action
from ascript.android.node import Selector


from .util import *
from .data import *


def start():
	action.Key.home()
	action.Key.back()
	sleep(1)
	Selector().text("以闪亮之名").click().find()
	sleep(3)
	click_blank()
	if check_t(COLLECTION, "收集",1):
		return True
	timeout = 30
	sleep(8)
	start_time = time()
	# 判断是否有：点击开始 和：加载中
	while True:
		no_start = 1
		load = 0.2
		if time() - start_time > timeout:
			e("开始游戏超时")

		start_pos = check_t(click_Start,"点击开始",1,0,0)
		if not start_pos and no_start:
			sleep(no_start)
			continue

		load_pos = check_t(Load,"加载",1,0,0)
		if start_pos and load_pos:
			no_start = 0
			sleep(load)
			continue
		elif start_pos and not load_pos:
			print("进入游戏")
			click_p(start_pos.x,start_pos.y)
			sleep(3)
			# 内循环确认进入游戏并关闭弹窗
			while True:
				if time() - start_time > timeout:
					e("进入游戏超时",0)
					break

				res = check_t(COLLECTION, "收集",1)
				x = check_x()
				if not x and not res:
					sleep(1)
					continue
				elif x:
					click(x.x,x.y)
					continue
				elif res:
					print("开始任务")
					return 1

def 思绪漫步1():# bug 测试
	click_a(SHINING_JOURNEY)
	click_a(sixumanbu)
	if click_a(meirilianxi):
		click_blank()
		click_blank()
	close_back()
	close_back()

	if not check_t(COLLECTION, "收集"):
		e()

def 思绪漫步2():
	click_a(SHINING_JOURNEY)
	click_a(sixumanbu)
	click_t(meirilianxi_lingqu,"领取")
	click_blank()
	click_blank()

	close_back()
	close_back()

	if not check_t(COLLECTION, "收集"):
		e()

def 元气使用():
	click_a(ICON)
	click_t(yuanqishiyong,"使用")
	yuanqizhi = identify_t(yuanqishibie,count = 1).split("/")[0]
	if yuanqizhi != 0:
		for _ in range(20):
			click_a(yuanqiduihuan,wait=0.2)
			click_a(yuanqiduihuan,wait=0.2)
	close_x()
	close_back()

	if not check_t(COLLECTION, "收集"):
		e()

def 收集():
	if click_t(COLLECTION,"收集"):
		click_a(COLLECTION_JB)
		click_a(COLLECTION_JB)
		close_back()

	if not check_t(COLLECTION, "收集"):
		e()

def 盲盒():
	if click_t(BLINDBOX,"盒"):
		click_a(BLINDBOX2)
		click_a(BLINDBOX2_JB)
		click_blank()
		close_back()
		close_back()

	if not check_t(COLLECTION, "收集"):
		e()


def 好友():
	res = click_t(FRIEND, "好友")
	if res:
		if click_t(TALK_SUMMER,"时尚顾问"):
			try:
				click_t(TALK_SUMMER_LQ,"领取")
			except:
				check_page()
				好友()
			click_a(TALK_SUMMER_LQ)
			close_back()

		if click_t(TXL,"通讯录"):
			click_t(TXL_yijianzengsong,"送")
			click_t(TXL_LQtili,"领取体力")
			click_t(TXL_YJLQ,"取")
			click_blank()
			close_x()

		if click_t(wannashequ,"社区"):
			click_a(wannashequ_JB)
			click_a(wannashequ_JB)
			close_back()

		if not check_t(COLLECTION, "收集"):
			e()



def 礼物():
	if click_img("gift",GIFT,"全服礼物"):

		click_a(GIFT_LEFT)
		click_blank()
		click_t(GIFT_CANLE,"取消")

		click_a(GIFT_RIGHT)
		click_blank()
		click_t(GIFT_CANLE,"取消")

		click_a(GIFT_LEFT)
		click_blank()
		click_t(GIFT_CANLE,"取消")

		close_back()

		if not check_t(COLLECTION, "收集"):
			e()


def 协会():
	if click_t(UNION, "协会"):
		if click_a(lingganpengzhuang):
			for _ in range(5):
				click_t(TJ_1_SY,"提交")
				click_blank()
			click_a(qihua)
			click_blank()
			close_back()

		if click_a(yingyuan):
			for _ in range(3):
				click_t(likeyingyuan,"援")
				click_blank()
			close_back()
			close_back()

		if not check_t(COLLECTION, "收集"):
			e()


def 闪亮之旅():
	click_a(SHINING_JOURNEY)

def 日常事件簿():
	click_t(richangshijianbu, "事")
	if click_img("金币",richangshijianbu_JB_rect,"金币"):
		click_blank()

	click_img("一键领取",richangshijianbu_rect,"一键领取")
	click_t(richangshijianbu_LQ,"领取")
	click_blank()
	click_blank()

	for _ in range(4):
		if click_img("派遣",PQ_rect, "派遣"):
			click_t(YJPQ,"派遣")
			click_t(QRPQ,"派遣")
	close_back()
	#
def 代言女王():
	if click_t(daiyannvwang, "女"):
		click_a(meirixuanchuan)
	if click_t(kashixuanchuan, "宣传"):
		click_blank()
		click_blank()

	c = [SNE_1,WST_2,YNS_3,BBL_4]
	for f in c:
		click_a(f)
		if click_t(yijianshiqu, "拾取"):
			click_blank()
			click_blank()
			click_blank()
			if check_t(daiyan, "代言",1):
				click_a(yijianshiqu)
			close_back()

	close_back()

	if not check_t(COLLECTION, "收集"):
		e()

def 商业街():
	if click_t(shop, "商业街"):
		for _ in range(10):
			if click_img("每日福利礼盒",shop_rect,"每日福利礼盒",1):
				click_t(buy,"购买")
				click_blank()
				close_x()
				close_back()
				break
			else:
				action.Touch.down(600,2500)
				action.Touch.move(600,1600,200)
				action.Touch.up(600,1600,100)

		if not check_t(COLLECTION, "收集"):
			e()

def 追光():
	if click_t(zhuiguang, "追光"):
		click_a(zhuiguang_enter)
		click_a(zhuiguang_JB)
		click_blank()
		close_back()
		close_back()

	if not check_t(COLLECTION, "收集"):
		e()
		pass

