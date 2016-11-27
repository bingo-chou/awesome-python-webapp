#!/usr/bin/env python
# -*- coding:utf-8

import re,json,logging,functools
from transwarp.web import ctx
'''
负责将函数返回结果序列化为JSON
'''
class Page(object):
	'''
	用于显示blogs的page
	'''
	def __init__(self,item_count,page_index=1,page_size=10):
		'''
		
		>>> p1=Page(100,1)
		>>> p1.page_count
		10
		>>> p1.offset
		0
		>>> p2=Page(90,9,10)
		>>> p2.page_count
		9
		>>> p2.offset
		80
		>>> p2.limit
		10
		>>> p3=Page(91,10,10)
		>>> p3.page_count
		10
		>>> p3.offset
		90
		>>> p3.limit
		10
		'''
		self.item_count=item_count
		self.page_size=page_size
		self.page_count=item_count//page_size+(1 if item_count%page_size>0 else 0)
		if (item_count==0) or (page_index<1) or (page_index>self.page_count):
			self.offset=0
			self.limit=0
			self.page_index=1
		else:
			self.page_index=page_index
			self.offset=self.page_size*(page_index-1)
			self.limit=self.page_size
		self.has_next=self.page_index<self.page_count
		self.has_previous=self.page_index>1
	def __str__(self):
		return 'item_count:%s,page_count:%s,page_index:%s,page_size:%s,offset:%s,limit:%s'%(self.item_count,self.page_count,self.page_index,self.page_size,self.offset,self.limit)
	
	__repr__=__str__
	
		
def _dump(obj):
	if isinstance(obj,Page):
		return {
			'page_index':obj.page_index,
			'page_count':obj.page_count,
			'item_count':obj.item_count,
			'has_next':obj.has_next,
			'has_previous':obj.has_previous
		}
	raise TypeError('%s is not JSON serializable'%obj)

def dumps(obj):
	return json.dumps(obj,default=_dump)

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
			r=dumps(func(*args,**kw))
		except APIError,e:
			r=json.dumps(dict(error=e.error,data=e.data,message=e.message))
		except Exception,e:
			logging.exception(e)
			r=json.dumps(dict(errors='internalerror',data=e.__class__.__name__,message=e.message))
		ctx.response.content_type='application/json'
		return r
	return _wrapper

if __name__=='__main__':
	import doctest
	doctest.testmod()
