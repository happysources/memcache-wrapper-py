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

	def __init__(self, hostname='127.0.0.1', port=11211, prefix='', debug=0):
		""" init """

		# prefix
		self.prefix = ''
		if prefix:
			self.prefix = '%s.' % (prefix,)

		# memcache init
		self.__mc = memcache.Client(['%s:%s' % (hostname, port)], debug=debug)

		log.info('cache INIT host="%s:%s", prefix="%s*"', (hostname, port, self.prefix,), 1)


	def __key(self, key=None):
		""" key """

		return '%s%s' % (self.prefix, key)


	def incr(self, key=None, delta=1):
		""" incr """

		key_name = self.__key(key)

		try:
			ret = self.__mc.incr(key_name, delta)
		except BaseException as emsg:
			log.error('cache INCR key="%s", err="%s"', (key_name, emsg), 3)
			return None

		log.debug('cache INCR key="%s", delta=%s, ret="%s"', (key_name, delta, ret), 4)
		return ret


	def decr(self, key=None, delta=1):
		""" decr """

		key_name = self.__key(key)

		try:
			ret = self.__mc.decr(key_name, delta)
		except BaseException as emsg:
			log.error('cache DECR key="%s", err="%s"', (key_name, emsg), 3)
			return None

		log.debug('cache DECR key="%s", delta=%s, ret="%s"', (key_name, delta, ret), 4)
		return ret


	def get(self, key=None):
		""" get """

		key_name = self.__key(key)

		try:
			data = self.__mc.get(key_name)
		except BaseException as emsg:
			log.error('cache GET key="%s", err="%s"', (key_name, emsg), 3)
			return None

		data_len = -1
		if data and isinstance(data, six.string_types):
			data_len = len(data)

		log.info('cache GET key="%s", data=%s, len=%s', (key_name, data, data_len), 1)
		return data


	def delete(self, key=None):
		""" delete """

		key_name = self.__key(key)

		try:
			ret = self.__mc.delete(key_name)
		except BaseException as emsg:
			log.info('cache DEL key="%s", err="%s"', (key_name, emsg), 2)
			return None

		log.debug('cache DEL key="%s"', (key_name,), 4)
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
			log.error('cache SET key="%s" [MemoryError], data len=%s, mtime=%s, err="%s"',\
				(key_name, data_len, mtime, emsg), 3)
			return None

		except BaseException as emsg:
			log.error('cache SET key="%s" [BaseException], data len=%s, mtime=%s, err="%s"',\
				(key_name, data_len, mtime, emsg), 3)
			return None

		log.info('cache SET key="%s", data=%s, len=%s, mtime=%s',\
			(key_name, data, data_len, mtime), 2)

		return ret


	def cache(self, key=None, data=None, mtime=3600):
		""" cache (get/set) """

		ret_get = self.get(key=key)
		if ret_get:
			return ret_get

		return self.set(key=key, data=data, mtime=mtime)
