#!/usr/bin/env python3
# -*- coding: gbk -*-
import asyncio
#def consumer():
#    r = 'yield '
#    while True:
#        n = yield r
#        if not n:
#            return
#        print('consumer n = %s' % n)
#
#def produce(c):
#    c.send(None)
#    n = 0
#    while n < 5:
#        n = n+1
#        print('produce n is %s!' % n)
#        r = c.send(n)
#        print('Consumer return %s' % r)
#    c.close()
#
#c = consumer()
#produce(c)

#
#@asyncio.coroutine
#def hello():
#    print('hello world!')
#    r = yield from asyncio.sleep(1)
#    print('hello again!')
#
#loop = asyncio.get_event_loop()
#tasks = [hello(), hello()]
#loop.run_until_complete(asyncio.wait(tasks))
#loop.close()

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break;
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sohu.com', 'www.163.com', 'www.sina.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

