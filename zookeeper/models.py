#!/usr/bin/env python
#encoding: utf-8

import traceback

from django.db import models

from kazoo.client import KazooClient

class ZKException(BaseException):
    pass

class ZKClient(object):

    def __init__(self, hosts):
        self._hosts = hosts
        self._client = self._connect(hosts)

    def _connect(self, hosts):
        _client = None
        try:
            _client = KazooClient(hosts=hosts)
            _client.start()
        except BaseException, e:
            print traceback.format_exc()
            raise ZKException('连接zookeeper失败')
        return _client

    def get_node(self, ppath='/', cpath=''):
        _path = '%s/%s' % (ppath.rstrip('/'), cpath)
        _node = None
        if self._client.exists(_path):
            _node = {}
            _node['text'] = 'root' if '' == cpath else cpath
            _node['path'] = _path
            _nodes = []
            for _child in self._client.get_children(_path):
                _cnode = self.get_node(_path, _child)
                _cnode is None or (_nodes.append(_cnode))

            if len(_nodes) > 0:
                _node['nodes'] = _nodes
                _node['tags'] = [len(_nodes)]

        return _node

    def get_value(self, path):
        _detail = {}
        if self._client.exists(path):
            _name = path.split('/')[-1]
            _value, _stat = self._client.get(path)
            _detail['path'] = path
            _detail['name'] = 'root' if _name == '' else _name
            _detail['value'] = '' if _value is None else _value.decode('utf-8')
        return _detail

    def set_value(self, path, value):
        if self._client.exists(path):
            self._client.set(path, value.encode('utf-8'))

    def create_node(self, ppath, cpath, value):
        _path = '%s/%s' % (ppath.strip('/'), cpath)
        if self._client.exists(ppath) and not self._client.exists(_path):
            self._client.create(_path, value.encode('utf-8'))

    def delete_node(self, path):
        if self._client.exists(path):
            self._client.delete(path, recursive=True)
