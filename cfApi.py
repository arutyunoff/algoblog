from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def userInfo(handle):
	req = get(f'https://codeforces.com/api/user.info?handles={handle}')
	if req:
		return req.json()['result'][0]


def getTitle(link):
	try:
		req = get(link, headers={'user-agent': UserAgent().random})
		bs = BeautifulSoup(req.content)
	except:
		return
	if not bs.title:
		return 'Файл'
	return bs.title.string


def getColor(user):
	r = user.get('rating')
	if r is None:
		return 'white'
	if r < 1200:
		return 'gray'
	if r < 1400:
		return 'green'
	if r < 1600:
		return '#03A89E'
	if r < 1900:
		return 'blue'
	if r < 2100:
		return '#a0a'
	if r < 2400:
		return '#FF8C00'
	return 'red'


def searchFunc(algo, flt):
	flt = flt.lower().strip().split()
	if not flt:
		return True
	text = (algo.name + ' ' + algo.other).lower()
	return any([x in text for x in flt])


def authorFunc(algo, flt):
	flt = flt.strip()
	return algo.user == flt


def sendMail(addr, code):
	smtp = SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	login, pwd = 'krasavdar@gmail.com', 'thle yzyl dekz vzld'
	smtp.login(login, pwd)
	msg = MIMEMultipart()
	message = 'Your code for authorization: #{}'.format(code)
	msg['From'] = login
	msg['To'] = addr
	msg['Subject'] = 'AlgoBlog login'
	msg.attach(MIMEText(message, 'plain'))
	smtp.sendmail(msg['From'], msg['To'], msg.as_string())
	smtp.quit()
