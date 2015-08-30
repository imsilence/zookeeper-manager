#!/usr/bin/env python
#encoding: utf-8

import json

from django.shortcuts import render, redirect

from django.core.urlresolvers import reverse

from models import ZKClient, ZKException

def _get_client(request):
    _kafkaserver = request.POST.get('kafkaserver', None)
    if _kafkaserver is None:
        _kafkaserver = request.session.get('kafkaserver', '127.0.0.1:2181')
    else:
        request.session['kafkaserver'] = _kafkaserver

    _client = None
    try:
        _client = ZKClient(_kafkaserver)
    except ZKException, e:
        pass

    return _kafkaserver, _client

def index(request):
    _kafkaserver, _client = _get_client(request)
    if _client:
        _root_node = _client.get_node()
        _tree_data = [] if _root_node is None else [_root_node]
        return render(request, 'index.html', {'kafkaserver' : _kafkaserver, 'treedata' : json.dumps(_tree_data)})
    else:
        return render(request, 'error.html', {'kafkaserver' : _kafkaserver})

def detail(request):
    _kafkaserver, _client = _get_client(request)
    if _client:
        _path = request.POST.get('path')
        _detail = {} if _path is None else _client.get_value(_path)
        return render(request, 'detail.html', {'detail': _detail})
    else:
        return render(request, 'error.html', {'kafkaserver' : _kafkaserver})

def update(request):
    _kafkaserver, _client = _get_client(request)
    if _client:
        _path = request.POST.get('path')
        _value = request.POST.get('value', '')
        _path is None or _client.set_value(_path, _value)
        return redirect(reverse('zookeeper:index'))
    else:
        return render(request, 'error.html', {'kafkaserver' : _kafkaserver})

def create(request):
    _kafkaserver, _client = _get_client(request)
    if _client:
        _ppath = request.POST.get('path')
        _name = request.POST.get('name')
        _value = request.POST.get('value')
        _ppath is None or _name is None or _client.create_node(_ppath, _name.split('/')[0], _value)
        return redirect(reverse('zookeeper:index'))
    else:
        return render(request, 'error.html', {'kafkaserver' : _kafkaserver})

def delete(request):
    _kafkaserver, _client = _get_client(request)
    if _client:
        _path = request.POST.get('path')
        _path is None or _client.delete_node(_path)
        return redirect(reverse('zookeeper:index'))
    else:
        return render(request, 'error.html', {'kafkaserver' : _kafkaserver})
