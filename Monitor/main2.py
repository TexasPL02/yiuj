import time
import requests
from psutil import net_io_counters
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

from load import SystemMonitor_net

# 设置初始值
last_upload, last_download, last_timestamp = 0, 0, time.time()


def get_network_speed():
	global last_upload, last_download, last_timestamp

	counter = net_io_counters()
	current_upload, current_download = counter.bytes_sent, counter.bytes_recv
	current_timestamp = time.time()

	upload_speed = (current_upload - last_upload) / (current_timestamp - last_timestamp)
	download_speed = (current_download - last_download) / (current_timestamp - last_timestamp)

	last_upload, last_download, last_timestamp = current_upload, current_download, current_timestamp

	return upload_speed, download_speed


def get_temperatures():
	response = requests.get("http://localhost:8085/data.json")
	data = response.json()

	cpu_temp, gpu_temp = None, None
	for hardware in data['Children']:
		if 'CPU' in hardware['Text']:
			cpu_temp = next(
				(sensor['Value'] for sensor in hardware['Children'] if sensor['SensorType'] == 'Temperature'), None)
		elif 'GPU' in hardware['Text']:
			gpu_temp = next(
				(sensor['Value'] for sensor in hardware['Children'] if sensor['SensorType'] == 'Temperature'), None)

	return cpu_temp, gpu_temp


def update_icon(icon):
	while icon.visible:
		upload_speed, download_speed = get_network_speed()
		cpu_temp, gpu_temp = get_temperatures()

		text = f"↑{upload_speed:.2f} kB/s ↓{download_speed:.2f} kB/s\nCPU: {cpu_temp}°C GPU: {gpu_temp}°C"
		image = create_image(text)
		icon.icon = image

		time.sleep(1)


def create_image(text):
	width = 200
	height = 50
	image = Image.new('RGB', (width, height), color=(255, 255, 255))
	dc = ImageDraw.Draw(image)
	dc.text((10, 10), text, fill=(0, 0, 0))
	image.save("img_show.png")
	return image


if __name__ == "__main__":
	# # 创建图标
	# icon = Icon('System Info', icon=create_image("Loading..."))
	#
	# # 添加菜单项
	# menu = Menu(MenuItem('Exit', lambda: icon.stop()))
	# icon.menu = menu
	#
	# # 启动更新线程
	# thread = Thread(target=update_icon, args=(icon,))
	# thread.daemon = True
	# thread.start()
	#
	# # 运行图标
	# icon.run()
	monitor = SystemMonitor_net()
	try:
		while True:
			monitor.refresh(None, None)
			time.sleep(1)
	except KeyboardInterrupt:
		print("监控已停止")