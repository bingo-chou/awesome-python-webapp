#!/usr/bin/env python
# -*- coding:utf-8 -*-

import config_default

class Dict(dict):
	
	def __init__(self,names=(),values=(),**kw):
		super(Dict,self).__init__(**kw)
		for k,v in zip(names,values):
			self[k]=v
	
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'"%key)

	def __setattr__(self,key,value):
		self[key]=value

def merge(defaults,override):
	'''
	以覆盖配置为先，合并默认配置和覆盖配置
	'''
	r={}
	for k,v in defaults.iteritems():
		if k in override:
			if isinstance(v,dict):
				r[k]=merge(v,override[k])
			else:
				r[k]=override[k]
		else:
			r[k]=v
	return r

def toDict(d):
	'''
	将普通dict对象，转换成自定义的Dict对象
	'''
	
	D=Dict()
	for k,v in d.iteritems():
		D[k]=toDict(v) if isinstance(v,dict) else v
	return D

configs=config_default.configs

try:
	import config_override
	configs=merge(configs,config_override.configs)
except ImportError:
	pass

configs=toDict(configs)
