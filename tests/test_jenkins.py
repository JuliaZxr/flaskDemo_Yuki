#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    jenkins = Jenkins('http://10.6.7.171:8080/')
    print(jenkins.version)