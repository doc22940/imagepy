from imagepy.core.engine import Free
import numpy as np
import pandas as pd
from imagepy import IPy

'''
生成：
  随机数
  正太随机
  日历
  单位矩阵
基础：
  添加字段
  删除字段
  字段运算
  赋值
  截取
  转置
统计：
  平均数，最大值，最小值，方差
  频率统计
筛选：
  ：
图表：
  折线图
  条形图
  饼状图
信号：
  高斯
  差分
关联：
  聚合
  分组
'''
class One(Free):
	title = 'Unit Matrix'
	para = {'size':3}
	view = [(int, (1,1024), 0, 'size', 'size', '')]

	def run(self, para=None):
		data = np.eye(para['size'])
		dataframe = pd.DataFrame(data)
		IPy.table('Eye[%s,%s]'%data.shape, dataframe)

class Random01(Free):
	title = 'Uniform Random'
	para = {'row':3, 'col':5, 'low':0, 'high':1}
	view = [(float, (-1024,1024), 0, 'low', 'low', ''),
			(float, (-1024,1024), 0, 'high', 'high', ''),
			(int, (1,1024), 0, 'row', 'row', ''),
			(int, (1,1024), 0, 'col', 'col', '')]

	def run(self, para=None):
		data = np.random.rand(para['row'], para['col'])
		data *= para['high']-para['low']
		data -= para['low']
		dataframe = pd.DataFrame(data)
		IPy.table('Random01[%s,%s]'%data.shape, dataframe)

class RandomN(Free):
	title = 'Gaussian Random'
	para = {'row':3, 'col':5, 'mean':0, 'std':1}
	view = [(float, (-1024,1024), 0, 'mean', 'mean', ''),
			(float, (-1024,1024), 0, 'std', 'std', ''),
			(int, (1,1024), 0, 'row', 'row', ''),
			(int, (1,1024), 0, 'col', 'col', '')]

	def run(self, para=None):
		data = np.random.randn(para['row'], para['col'])
		data *= para['std']
		data += para['mean']
		dataframe = pd.DataFrame(data)
		IPy.table('RandomN[%s,%s]'%data.shape, dataframe)

class Calendar(Free):
	title = 'Calendar'
	para = {'year':2018, 'month':2}
	view = [(int, (-9999,9999), 0, 'year', 'year', ''),
			(int, (1,12), 0, 'month', 'month', '')]

	def run(self, para=None):
		import calendar
		ls = calendar.month(para['year'], para['month']).split('\n')
		title = ls[0].strip()
		titles = ls[1].split(' ')
		table = []
		for i in ls[2:-1]:
			a = i.replace('   ', ' None ').strip()
			table.append(a.replace('  ', ' ').split(' '))
		dataframe = pd.DataFrame(table, columns=titles)
		IPy.table(ls[0].strip(), dataframe)

plgs = [One, Random01, RandomN, Calendar]