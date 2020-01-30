#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example
"""

import sys
from logni import log

#pylint: disable=wrong-import-position
sys.path.append('memcachewrapper')
sys.path.append('../../memcachewrapper')
import memcachewrapper

# set log
log.mask('ALL')
log.stderr(1)

# memcache init
CACHE = memcachewrapper.MemcacheWrapper(prefix='test', debug=9)

print('set/get:')
print("err get A:", CACHE.get('A'))
print("ok  set A:", CACHE.set('A', 'aaaa'))

print("ok  get A:", CACHE.get('A'))
print("ok  set A:", CACHE.set('A', 'bbb'))

print("ok  get A:", CACHE.get('A'))
print("ok  del A:", CACHE.delete('A'))

print()
print('incr/decr:')
print("ok  set no:", CACHE.set('noX', 10))
print("ok  incr no:", CACHE.incr('noX'))
print("ok  incr no:", CACHE.incr('noX'))
print("ok  incr no:", CACHE.incr('noX'))
print("ok  decr no:", CACHE.decr('noX'))
print("ok  incr no:", CACHE.incr('noX'))
print("ok  decr no:", CACHE.decr('noX'))
print("ok  decr no:", CACHE.decr('noX'))

print()
print('delete:')
print(CACHE.delete('noX'))
print(CACHE.delete('noX'))

print()
print('cache:')
print(CACHE.cache('A', 'cccc'))
print()
print(CACHE.cache('A', 'ddd'))
