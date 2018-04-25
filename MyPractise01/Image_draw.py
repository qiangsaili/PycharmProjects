#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/4/25 19:20
'''
from PIL import Image,ImageFont,ImageDraw

def image_draw(context):
	im = Image.open('F:\PycharmProjects\Image\picture1.jpg')
	draw_im = ImageDraw.Draw(im)
	xsize,ysize = im.size
	fontsize = min(xsize,ysize)
	print(fontsize)
	myfont = ImageFont.truetype("C:\Windows\Fonts\cambria.ttc",30)
	draw_im.text([0.85*xsize,0.05*ysize],context,(255,0,0),font = myfont)
	del draw_im
	im.show()
	
image_draw('99')

	


