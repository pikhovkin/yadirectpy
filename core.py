#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#-------------------------------------------------------------------------------
# Name:        core
# Purpose:
#
# Author:      Sergey Pikhovkin (s@pikhovkin.ru)
#
# Created:     01.06.2011
# Copyright:   (c) Sergey Pikhovkin 2011
# Licence:     MIT
#-------------------------------------------------------------------------------

import json

from client import APIClient


class APIException(Exception):
    def __init__(self, code, msg, detail):
        self.code = code
        self.msg = msg
        self.detail = detail

    def __str__(self):
        return repr('%d: %s' % (self.code, self.msg))


class JSON2Obj(object):
    def __init__(self, page):
        self.__dict__ = json.loads(page)


class Direct(object):
    _VersionAPI = 4
    HOST = 'https://soap.direct.yandex.ru/json-api/v4/'
    Locale = 'en'
    _UserAgent = 'yadirectpy'

    @property
    def UserAgent(self):
        return self._UserAgent

    @UserAgent.setter
    def UserAgent(self, user_agent):
        self._UserAgent = user_agent

    @property
    def VersionAPI(self):
        return self._VersionAPI

    @VersionAPI.setter
    def VersionAPI(self, version_api):
        self._VersionAPI = version_api
        self.HOST = 'https://soap.direct.yandex.ru/json-api/v%d/' % version_api

    def __init__(self, key_file=None, cert_file=None):
        self._client = APIClient(key_file, cert_file)
        self._client.UserAgent = self._UserAgent
        self._data = ''

    def _GetResponseObject(f):
        def wrapper(self):
            obj = JSON2Obj(self._data)
            if hasattr(obj, 'error_code'):
                raise APIException(
                    obj.error_code, obj.error_str, obj.error_detail)
            return f(self, obj)

        return wrapper

    def _GetHeaders(self):
        header = {
            'User-Agent': self._UserAgent,
            'Accept': 'application/json',
            'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive'}
        return header

    @_GetResponseObject
    def _ResponseHandle(self, obj):
        return obj

    def _GetData(self, method, uri, params={}):
        headers = self._GetHeaders()
        self._data = self._client.Request(method, uri, params=params,
            headers=headers)
        return self._ResponseHandle()

    def GetData(self):
        return self._data

    def _GetParams(self, method, params):
        return {'method': method, 'param': params, 'locale': self.Locale}

    def _Method(self, **kwargs):
        if kwargs.get('params'):
            params = self._GetParams(self.method, kwargs['params'])
        else:
            params = self._GetParams(self.method, kwargs)
        return self._GetData('POST', self.HOST,
            json.dumps(params, ensure_ascii=False))

    def __getattr__(self, attr):
        self.method = attr
        return self._Method


def main():
    direct = Direct('private.key', 'cert.crt')
    direct.Locale = 'ru'
    #direct.HOST = 'https://api-sandbox.direct.yandex.ru/json-api/v4/'
    #direct.GetAvailableVersions(login='login',
    #                            application_id='1234567890',
    #                            token='1234567890')
    direct.GetClientInfo()
    print direct.GetData()
    Keywords = ["keyword"]
    try:
        #suggestion = direct.GetKeywordsSuggestion(Keywords=Keywords)
        #direct.GetRegions()
        #print direct.GetData().decode('utf-8')
        '''
        suggA = [];
        suggB = direct.GetKeywordsSuggestion(Keywords=Keywords).data

        suggA.extend(suggB)
        while suggA:
            Keywords = Keywords + [kw.encode('utf-8') for kw in suggA[:8]]
            suggA = direct.GetKeywordsSuggestion(Keywords=Keywords).data

        print Keywords
        print suggB
        '''
        Phrases = ['keyword']
        GeoID = []
        #wrep = direct.CreateNewWordstatReport(Phrases=Phrases, GeoID=GeoID).data
        #wrep = direct.GetWordstatReportList().data
        '''
        StatusReport:
            Done - отчет готов;
            Pending - отчет еще готовится.
        '''
        #wrep = direct.GetWordstatReport(params=111).data
        #wrep = direct.DeleteWordstatReport(params=111).data
        wrep = direct.GetRegions()
    except APIException, e:
        print '[%d] %s (%s)' % (e.code, e.msg, e.detail)
    print direct.GetData()


if __name__ == '__main__':
    main()
