#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
import requests


class TestUserApi:
    # 测试获取数据
    def test_user_get(self):
        r = requests.get(
            "http://127.0.0.1:5000/user"
        )
        print(r.json())
        assert r.status_code == 200
        assert len(r.json()) >= 0

    # 测试登录成功、失败
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

    # 测试注册
    def test_put(self):
        r = requests.put("http://127.0.0.1:5000/user", json={
            "username": "momo3",
            "password": "momo3",
            "email": "momo=3@yuki.com"
        })
        assert r.status_code == 200
        assert r.json()["msg"] == "register success"

        print(r.json())

        # 注册成功后要去获取所有的用户信息，进行断言，看注册新增的用户是否存在
        r = requests.get(
            "http://127.0.0.1:5000/user"
        )
        print(r.json())
        assert r.status_code == 200
        users = [u["name"] for u in r.json()]
        assert 'momo3' in users
