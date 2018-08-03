import requests
from bs4 import BeautifulSoup
import urllib.request

import pytesseract
from PIL import Image
from PIL import ImageEnhance

def shibie(filepath):
	# 打开图片
	img = Image.open(filepath)

	img = img.convert('RGB')
	enhancer = ImageEnhance.Color(img)
	enhancer = enhancer.enhance(0)
	enhancer = ImageEnhance.Brightness(enhancer)
	enhancer = enhancer.enhance(2)
	enhancer = ImageEnhance.Contrast(enhancer)
	enhancer = enhancer.enhance(8)
	enhancer = ImageEnhance.Sharpness(enhancer)
	img = enhancer.enhance(20)

	# 处理图片，提高图片的识别率
	# 转化为灰度图片
	img = img.convert('L')
	# img.show()

	# 对图片进行二值化处理
	threshold = 140
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	out = img.point(table, '1')
	# out.show()

	# exit()

	# 将图片转化为RGB模式
	img = img.convert('RGB')
	print(pytesseract.image_to_string(img))

	return pytesseract.image_to_string(img)

i = 0
	
while 1:
	# 创建一个会话
	s = requests.Session()

	# 发送get请求
	deng_url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
	}
	r = s.get(deng_url, headers=headers)

	# 生产soup对象
	soup = BeautifulSoup(r.text, 'lxml')
	# 获取验证码的url
	image_src = 'https://so.gushiwen.org' + soup.find('img', id='imgCode')['src']
	# 将这个图片下载到本地
	r = s.get(image_src, headers=headers)
	with open('code1.png', 'wb') as fp:
		fp.write(r.content)

	# 获取页面中隐藏的两个数据
	view_state = soup.find('input', id='__VIEWSTATE')['value']
	view_generator = soup.find('input', id='__VIEWSTATEGENERATOR')['value']


	code = shibie('code1.png')

	# 抓包，抓取post请求，然后通过代码模拟发送post请求
	post_url = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
	data = {
		'__VIEWSTATE': view_state,
		'__VIEWSTATEGENERATOR':	view_generator,
		'from':	'http://so.gushiwen.org/user/collect.aspx',
		'email': 
		'pwd': 
		'code':	code,
		'denglu': '登录',
	}

	r = s.post(url=post_url, headers=headers, data=data)
	i += 1
	
	print('这是第%s次登录' % i)

	# print(r.text)
	if '退出登录' in r.text:
		break

print('登录成功')






















