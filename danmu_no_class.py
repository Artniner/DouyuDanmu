# -*- coding:utf-8 -*-

#import multiprocessing
import socket
import threading
import time
import re
import codecs

#礼物ID
GIFTS = {'191':'鱼丸','192':'赞','193':'弱鸡','519':'呵呵','520':'稳','712':'棒棒哒','713':'辣眼睛','714':'怂','1027':'药丸',
		'195':'飞机','196':'火箭','536':'笔记本','750':'办卡','824':'荧光棒','1005':'超级火箭',
		'1541':'星光棒','1563':'节日鱼丸','1564':'节日赞','1566':'办卡','1567':'庆典飞机','1569':'庆典火箭','1571':'超大鱼丸',
		'1':'初级酬勤','2':'中级酬勤','3':'高级酬勤'}
	
#房间ID	
ROOMS = {'女流66':'156277','超级小桀':'74751','寅子':'71415','十三三三':'69752','只有十五岁的涛妹':'32892','衣锦夜行':'48699','wtybill':'57321','妃凌雪':'78561',
		'冯提莫':'71017','逆风笑':'216906'}

#服务器信息
HOST = 'openbarrage.douyutv.com'
PORT = 8601
CODE = 689
RID = ROOMS['寅子']

#消息格式
LOGIN_INFO = 'type@=loginreq/username@=visitor/password@=123456/roomid@='+str(RID)+'/\0'
JOIN_GROUP = 'type@=joingroup/rid@='+str(RID)+'/gid@=-9999/\0'
KEEP_LIVE = 'type@=mrkl/\0'
#KEEP_LIVE = 'type@=keeplive/tick@='
LOGOUT = 'type@=logout/\0'


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

#发送请求
def send_request_msg(req_msg):
	encode_msg = req_msg.encode('utf-8')
	msg_length = len(encode_msg)+12
	msg_head = int.to_bytes(msg_length-4, 4, 'little') \
		+ int.to_bytes(msg_length-4, 4, 'little') + \
		int.to_bytes(CODE, 4, 'little')
	msg = msg_head+encode_msg
	client.send(msg)

#登陆服务器	
def login():
	send_request_msg(LOGIN_INFO)
	send_request_msg(JOIN_GROUP)

#发送心跳包	
def keep_live():
	while True:
		#timeStamp = int(time.time())
		#KEEP_MSG = KEEP_LIVE + str(timeStamp) + '/\0'
		send_request_msg(KEEP_LIVE)
		time.sleep(45)		

#获取弹幕		
def get_barrage():
	#分散
	#re_user = re.compile(b'type@=chatmsg.*?nn@=(.*?)/')
	#re_content = re.compile(b'type@=chatmsg.*?txt@=(.*?)/')
	#re_rid = re.compile(b'type@=chatmsg.*?rid@=(.*?)/gid@=(.*?)/')
	
	#综合
	re_barrage = re.compile(b'type@=chatmsg.*?nn@=(.*?)/.*?txt@=(.*?)/')
	
	while True:	
		#分散
		#data = client.recv(1024)
		#user = re_user.findall(data)
		#content = re_content.findall(data)
		
		#综合
		data = client.recv(1024)
		data_barrage = re_barrage.findall(data)
		
		if not data:
			print('--------------------------------------------------------------------')
			break
		elif not data_barrage:
			continue
		else:
			for i in data_barrage:
				user = i[0].decode('utf-8','ignore')
				content = i[1].decode('utf-8','ignore')
				print(user+':'+content)
				print('')
				
#获取礼物数据（包括酬勤）				
def get_data():
	#分散
	#re_user = re.compile(b'type@=dgb.*?nn@=(.*?)/')
	#re_gfid = re.compile(b'type@=dgb.*?gfid@=(.*?)/')
	#re_gfcnt = re.compile(b'type@=dgb.*?gfcnt@=(.*?)/')
	#re_hits = re.compile(b'type@=dgb.*?hits@=(.*?)/')
	#re_gs = re.compile(b'type@=dgb.*?gs@=(.*?)/')
	
	#综合
	re_gift = re.compile(b'type@=dgb.*?gfid@=(.*?)/.*?nn@=(.*?)/.*?(?:hits@=(.*?)/|ct)')
	re_deserve = re.compile(b'type@=bc_buy_deserve.*?hits@=(.*?)/lev@=(.*?)/sui@=(.*?)/')
	
	while True:
		#分散
		#data = client.recv(1024)
		#user = re_user.findall(data)
		#gfid = re_gfid.findall(data)
		#hits = re_hits.findall(data)
		#gfcnt = re_gfcnt.findall(data)
		
		#综合
		data = client.recv(1024)
		data_gifts = re_gift.findall(data)
		data_deserve = re_deserve.findall(data)

		if not data:
			print('-------------------------------------------------------------')
			break
		else:
			get_gift(data_gifts)
			get_deserve(data_deserve)

#礼物数据处理（不包括酬勤）
def get_gift(data_gifts):
		#elif not data_gifts:
		#	continue		
		#else:
	if data_gifts:
		for i in data_gifts:
			user = i[1].decode('utf-8','ignore')
			giftID = i[0].decode('utf-8','ignore')
			if not i[2]:
				hits = '1'
			else:
				hits = i[2].decode('utf-8','ignore')
			print_gift(user,giftID,hits)

#酬勤数据处理		
def get_deserve(data_deserve):
	if data_deserve:
		re_user = re.compile(b'nick@=(.*?)/')
		for i in data_deserve:
			user_data = i[2].decode('utf-8','ignore')
			user = re_user.findall(user_data)[0].decode('utf-8','ignore')
			lev = i[1].decode('utf-8','ignore')
			hits = i[0].decode('utf-8','ignore')
			print(i)
		print_gift(user,lev,hits)

#礼物数据输出（包括酬勤）
def print_gift(user,giftID,hits):
	file = codecs.open('gift.txt','a','GBK')
	if giftID in GIFTS:	
		return
		#print(user+':'+GIFTS[giftID]+'×'+hits)
		#file.write(user+':'+GIFTS[giftID]+'×'+hits+'\r\n')
	else:
		print(user+':'+giftID+'×'+hits)
		file.write(user+':'+giftID+'×'+hits+'\r\n')
	file.close()

login()
t_barrage = threading.Thread(target = get_barrage)
t_gift = threading.Thread(target = get_data)
t_keeplive = threading.Thread(target = keep_live)

#t_barrage.start()
t_gift.start()
t_keeplive.start()

#if __name__ == '__main__':
#	p_danmu = multiprocessing.Process(target=get_barrage)
#	p_gift = multiprocessing.Process(target=get_gift)
#	p_keep = multiprocessing.Process(target=keep_live)
#	p_danmu.start()
#	#p_gift.start()
#	p_keep.start()