#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit test
"""

import sys
import time
import unittest

#pylint: disable=wrong-import-position
sys.path.append('../../memcachewrapper/')
sys.path.append('memcachewrapper/')
import memcachewrapper

HOSTNAME = '127.0.0.1'
PORT = 11211
PREFIX = 'unit_%s' % int(time.time())
DEBUG = 9


def _init():
	""" memcache init """

	return memcachewrapper.MemcacheWrapper(HOSTNAME, PORT, PREFIX, DEBUG)


class TestMemcache(unittest.TestCase):
	""" Unit test """


	def __check_ret_ok(self, ret):
		""" ok response """

		self.assertTrue(ret, msg='return must be value')


	def __check_ret_err(self, ret):
		""" error response """

		self.assertFalse(ret, msg='return must be None')


	def __check_init(self):
		""" check init params """

		self.assertTrue(isinstance(PORT, int), msg='PORT must be integer')
		self.assertTrue(isinstance(DEBUG, int), msg='DEBUG must be integer')



	def test_get_ok(self):
		"""
		OK test for get()
		"""

		# init
		self.__check_init()
		cache = _init()

		cache.set('AAA', 10)
		ret = cache.get('AAA')
		self.__check_ret_ok(ret)


	def test_get_err(self):
		"""
		Error test for get()
		"""

		# init
		self.__check_init()
		cache = _init()

		ret = cache.get('AAA')
		self.__check_ret_err(ret)


	def test_set(self):
		""" set() """

		# init
		self.__check_init()
		cache = _init()

		ret = cache.set('AAA')
		self.__check_ret_ok(ret)


	def test_incr_decr(self):
		""" incr/desc() """

		# init
		self.__check_init()
		cache = _init()

		# incr ok
		cache.set('I1', 10)
		ret = cache.incr('I1')
		self.__check_ret_ok(ret)

		# incr err
		ret = cache.incr('I2')
		self.__check_ret_err(ret)

		# decr ok
		ret = cache.decr('I1')
		self.__check_ret_ok(ret)

		# decr err
		ret = cache.decr('I2')
		self.__check_ret_err(ret)


	def test_delete(self):
		""" delete """

		# init
		self.__check_init()
		cache = _init()

		# delete ok
		cache.set('D1')
		ret = cache.delete('D1')
		self.__check_ret_ok(ret)

		# delete err
		#ret = cache.delete('D2')
		#self.__check_ret_err(ret)

if __name__ == '__main__':
	unittest.main()
