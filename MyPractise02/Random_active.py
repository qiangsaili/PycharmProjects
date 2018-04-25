#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/4/25 22:33
'''
import random
import string

def Random_Active(lenght,num):
	with open('random_code.txt', 'w') as file:
		i = 1
		while i < num:
			random_code = ''.join(random.sample(string.ascii_uppercase + string.digits + string.ascii_lowercase, lenght))
			print(random_code)
			if not jude_repeat(random_code):
				print(jude_repeat(random_code))
				file.write(random_code + '\n')
			else:
				i = i - 1
			i = i + 1
	file.close()
	
def jude_repeat(context):
	file_read = open('random_code.txt', 'r')
	file_read_line = file_read.readlines()
	if context in file_read_line:
		return True
	else:
		return False
	
Random_Active(12,200)