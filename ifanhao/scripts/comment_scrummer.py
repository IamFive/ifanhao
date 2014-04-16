# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-9-12
#
import requests
import traceback
from bs4 import BeautifulSoup


raw = '''7|0|10|http://www.regulations.gov/Regs/|E7AD0F3A49FC4EE68D88662704F5FEA7|com.gwtplatform.dispatch.shared.DispatchService|execute|java.lang.String/2004016611|com.gwtplatform.dispatch.shared.Action|ExB+SE4+8N7Re0KMBWG5I22c|gov.egov.erule.regs.shared.action.LoadDocumentDetailAction/3833214929|d|{0}|1|2|3|4|2|5|6|7|8|9|10|'''

def after(s, pat):
    # returns the substring after pat in s.
    # if pat is not in s, then return a null string!
    pos = s.find(pat)
    if pos != -1:
        return s[pos + len(pat):]
    return ""

def headers():
    return {
        'X-GWT-Module-Bas':'http://www.regulations.gov/Regs/',
        'X-GWT-Permutation' : 'B96D73F165C9A2A21002CA191E48E085',
        'Content-Type':'text/x-gwt-rpc; charset=UTF-8'
    }

def start():
    with open('Safety Comment Stats - Sheet1.csv', 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('http://www.regulations.gov'):
            splitted = line.strip().split(',')
            url = splitted[0]

            id = after(url, 'D=')

            try:
                response = requests.post('http://www.regulations.gov/dispatch/LoadDocumentDetail',
                                         data=raw.format('CPSC-2012-0050-0003'), headers=headers())
                if response.status_code != 200:
                    print 'Error occurs when getting: {0}'.format(url)

                print response.content
            except Exception:
                print 'Error occurs when getting: {0}'.format(url)
                print traceback.format_exc()

start()
