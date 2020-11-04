#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
import requests


class TestUserApi(TestCase):
    def test_post(self):
        r = requests.post("http://127.0.0.1:5000/user", json={
            "username": "yuki",
            "password": "yuki"
        })
        assert r.status_code == 200
        assert r.json()["msg"] == "login success"
        print(r.json())
