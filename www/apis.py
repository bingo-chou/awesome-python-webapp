#!/usr/bin/env python
# -*- coding:utf-8

import re,json,logging,functools
from transwarp.web import ctx
'''
负责将函数返回结果序列化为JSON
'''

def dumps(obj):
	return json.dumps(obj)

class APIError(StandardError):
	'''
	自定义基础Error类，包含error,data和message
	'''
	def __init__(self,error,data='',message=''):
		super(APIError,self).__init__(message)
		self.error=error
		self.data=data
		self.message=message

class APIValueError(APIError):
	'''
	继承自APIError，处理输入值有问题或者无效
	'''
	def __init__(self,field,message=''):
		super(APIValueError,self).__init__('value:invalid',field,message)

class APIResourceNotFoundError(APIError):
	'''
	处理没有找到资源文件Error
	'''
	def __init__(self,field,message=''):
		super(APIResourceNotFoundError,self).__init__('value:notfound',field,message)

class APIPermissionError(APIError):
	'''
	处理权限Error
	'''
	def __init__(self,message=''):
		super(APIPermissionError,self).__init__('permission:forbidden','permission',message)

	
def api(func):
	'''
	@app.route('/api/test')
	@api
	def api_test():
		return dict(result='123',items=[])
	'''
	@functools.wraps(func)
	def _wrapper(*args,**kw):
		try:
			r=json.dumps(func(*args,**kw))
		except APIError,e:
			r=json.dumps(dict(error=e.error,data=e.data,message=e.message))
		except Exception,e:
			r=json.dumps(dict(errors='internalerror',date=e.__class__.__name__,message=e.message))
		ctx.response.content_type='application/json'
		return r
	return _wrapper

if __name__=='__main__':
	import doctest
	doctest.testmod()
