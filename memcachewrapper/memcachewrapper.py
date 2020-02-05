#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Memcache wrapper
"""

import six
import memcache
from logni import log

class MemcacheWrapper:
	""" Memcache object """

	def __init__(self, host='127.0.0.1', port=11211, prefix='', debug=0):
		""" init """

		# prefix
		self.prefix = ''
		if prefix:
			self.prefix = '%s.' % (prefix,)

		self.__name = '%s:%s' % (host, port)

		# memcache init
		self.__mc = memcache.Client(['%s:%s' % (host, port)], debug=debug)

		log.info('memcache INIT host="%s:%s" -> %s, prefix="%s*"',\
			(host, port, self.__name, self.prefix,), priority=2)


	def __key(self, key=None):
		""" key """

		return '%s%s' % (self.prefix, key)


	def incr(self, key=None, delta=1):
		""" incr """

		key_name = self.__key(key)

		try:
			ret = self.__mc.incr(key_name, delta)
		except BaseException as emsg:
			log.error('memcache %s INCR key="%s", err="%s"',\
				(self.__name, key_name, emsg), 2)
			return None

		log.info('memcache %s INCR key="%s", delta=%s, ret="%s"',\
			(self.__name, key_name, delta, ret), priority=1)

		return ret


	def decr(self, key=None, delta=1):
		""" decr """

		key_name = self.__key(key)

		try:
			ret = self.__mc.decr(key_name, delta)
		except BaseException as emsg:
			log.error('memcache %s DECR key="%s", err="%s"',\
				(self.__name, key_name, emsg), 2)
			return None

		log.info('memcache %s DECR key="%s", delta=%s, ret="%s"',\
			(self.__name, key_name, delta, ret), priority=1)

		return ret


	def get(self, key=None):
		""" get """

		key_name = self.__key(key)

		try:
			data = self.__mc.get(key_name)
		except BaseException as emsg:
			log.error('memcache %s GET key="%s", err="%s"',\
				(self.__name, key_name, emsg), 2)
			return None

		data_len = -1
		if data and isinstance(data, six.string_types):
			data_len = len(data)

		log.info('memcache %s GET key="%s", data=%s, len=%s',\
			(self.__name, key_name, data, data_len), priority=1)

		return data


	def delete(self, key=None):
		""" delete """

		key_name = self.__key(key)

		try:
			ret = self.__mc.delete(key_name)
		except BaseException as emsg:
			log.error('memcache %s DEL key="%s", err="%s"',\
				(self.__name, key_name, emsg), 2)
			return None

		log.info('memcache DEL key="%s"', (key_name,), priority=1)

		return ret


	def set(self, key=None, data=None, mtime=3600):
		""" set """

		key_name = self.__key(key)

		data_len = -1
		if data and isinstance(data, six.string_types):
			data_len = len(data)

		try:
			ret = self.__mc.set(key_name, data, mtime)

		except MemoryError as emsg:
			log.error('memcache %s SET key="%s" [MemoryError], data len=%s, mtime=%s, err="%s"',\
				(self.__name, key_name, data_len, mtime, emsg), 2)
			return None

		except BaseException as emsg:
			log.error('memcache %s SET key="%s" [BaseException], data len=%s, mtime=%s, err="%s"',\
				(self.__name, key_name, data_len, mtime, emsg), 2)
			return None

		log.info('memcache %s SET key="%s", data=%s, len=%s, mtime=%s',\
			(self.__name, key_name, data, data_len, mtime), 1)

		return ret


	def cache(self, key=None, data=None, mtime=3600):
		""" cache (get/set) """

		ret_get = self.get(key=key)
		if ret_get:
			return ret_get

		return self.set(key=key, data=data, mtime=mtime)
