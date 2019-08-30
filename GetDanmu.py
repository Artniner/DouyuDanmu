# -*- coding:utf-8 -*-
import socket
import time
import re

class DouyuDanmu:
	HOST = 'openbarrage.douyutv.com'
	PORT = 8601
	CODE = 689
	RID = 74751
		
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	
	def connect_danmu():
		client.connect((HOST,PORT))
		
	def send_request_msg(req_msg):
		encode_msg = req_msg.encode('utf-8')
		msg_length = len(encode_msg)+12
		msg_head = int.to_bytes(msg_length-4, 4, 'little') \
			+ int.to_bytes(msg_length-4, 4, 'little') + \
			int.to_bytes(CODE, 4, 'little')

		msg = msg_head+encode_msg
		client.send(msg)
		
	def login(room_id):
		LOGIN_INFO = 'type@=loginreq/username@=visitor/password@=123456/roomid@='+str(room_id)+'/\0'
		JOIN_GROUP = 'type@=joingroup/rid@='+str(room_id)+'/gid@=-9999/\0'
		send_request_msg(LOGIN_INFO)
		send_request_msg(JOIN_GROUP)
	
	def keep_live():
		KEEP_LIVE = 'type@=mrkl/\0'
		while True:
			send_request_msg(KEEP_LIVE)
			time.sleep(15)
			
	def get_user_content():
		re_user = re.compile(b'type@=chatmsg.*?nn@=(.*?)/')
		re_content = re.compile(b'type@=chatmsg.*?txt@=(.*?)/')
		
		data = client.recv(1024)
		user = re_user.findall(data)
		content = re_content.findall(data)
			
		if not data:
			print('-------------------------------------------------------------')
			#client.close()
			#client.connect((HOST,PORT))
			#send_request_msg(LOGOUT)
			#send_request_msg(LOGIN_INFO)
			#send_request_msg(JOIN_GROUP)
			continue
		elif not user or not content:
			continue
		else:
			return user,content