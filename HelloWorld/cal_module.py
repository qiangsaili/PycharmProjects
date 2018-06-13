#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/5/16 6:05
'''

class Calculator():
	""" 实现两个数的加、减、乘、除"""
	def __init__(self, a, b):
		self.a = int(a)
		self.b = int(b)
		
	# 加法
	def add(self):
		return self.a + self.b
	# 减法
	def sub(self):
		return self.a - self.b

	# 乘法
	def mul(self):
		return self.a * self.b

	# 除法
	def div(self):
		if self.b:
			return self.a / self.b
		else:
			return 0