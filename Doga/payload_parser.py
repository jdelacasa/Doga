# -*- coding: utf-8 -*-

"""
Doga.payload_parser

This module parse payload string and collect information from it
these involves method, host, resource path, section, http_type, useragent.
"""

import re
import sys

from log_generator import LogGenerator


class PayloadParser:

    def __init__(self):
        self.log_generator = LogGenerator()

        self.method = '(GET|HEAD|POST|PUT|DELETE|TRACE|OPTIONS|CONNECT|PATCH)'
        self.path = '(\/.*)'
        self.http_type = '(HTTP\/1.[0-1])'

        self.req_regex = "%s\s%s\s%s" % (self.method, self.path, self.http_type)
        self.host_regex = "Host:\s(.*)\r"
        self.useragent_regex = "User-Agent:\s(.*)\r"

    def parse(self, data, addr, ports):
        """ Parse request method, path, host, useragent, httptype etc.

        param: data(str) : packet payload string
        param: addr(list) : list object having source and destination IP address
        param: ports(list) : list object having source and destination ports
        """

        req_str = re.search(self.req_regex, data)
        host_str = re.search(self.host_regex, data)
        useragent_str = re.search(self.useragent_regex, data)

        try:
            method = req_str.group(1)
            path = req_str.group(2)
            http_type = req_str.group(3)
            host = host_str.group(1)
            useragent = useragent_str.group(1)
            section = path.split('?')[0]

            self.log_generator.generate(method, path, http_type, host, useragent, section)
        except:
            #print req_str.groups()
            print host_str.groups()
            print useragent_str.groups()
            print 'unable to parse packet payload'
            sys.exit()
