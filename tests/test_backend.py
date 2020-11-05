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

        r = requests.post("http://127.0.0.1:5000/user", json={
            "username": "yuki",
            "password": "yuki2"
        })
        assert r.json()["msg"] == "login fail"
        print(r.json())

    def test_put(self):
        r = requests.put("http://127.0.0.1:5000/user", json={
            "username": "momo1",
            "password": "momo1",
            "email": "momo1@yuki.com"
        })
        assert r.status_code == 200
        assert r.json()["msg"] == "register success"
        print(r.json())
