# -*- coding: UTF-8 -*-
# Author: Junbin Zhang
# E-mail: p78083025@ncku.edu.tw
# Update time: 2021.02.27

from __future__ import print_function

class PS():
    def __init__(self):
        # self.route_num = route_num
        # self.content_num = content_num
        self.ps = []

    # Producer generates unique content name
    def Creat_ps(self, route_ID, route_num, content_num, producer_content):
        '''
        ps = [content_name,...]
        '''
        ps = producer_content
        return ps

    def Get_ps(self):
        return self.ps

    # Check if there is data matching the content name in ps
    def Search_ps_interest(self, ps, content_name):
        '''
        ps = [content_name,...]
        '''
        #self.ps = ps
        for i in range(len(ps)):
            if content_name == ps[i]:
                return True
        # No data for content name found in ps
        return False
