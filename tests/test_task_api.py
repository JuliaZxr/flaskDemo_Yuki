#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from unittest import TestCase
import requests


class TestTaskApi:
    url = "http://127.0.0.1:5000/task"

    def setup_class(self):
        r = requests.post("http://127.0.0.1:5000/user", json={
            "username": "yuki",
            "password": "yuki"
        })
        assert r.status_code == 200
        assert r.json()["msg"] == "login success"
        print(r.text)

        # 将access_token读取出来放入token
        self.token = r.json()["access_token"]

    # 测试获取数据
    def test_task_get(self):
        r = requests.get(
            self.url,
            # 因为对应的TestcaseApi类中的方法get被@jwt_required装饰了，所以需要token（写在header中），否则访问提示无权
            headers={
                "Authorization": "Bearer " + self.token
            }
        )
        print(r.json())
        assert r.status_code == 200
        assert len(r.json()) >= 0

    # 测试添加数据
    def test_task_post(self):
        # 添加数据使用post
        r = requests.post(
            self.url,
            headers={
                "Authorization": "Bearer " + self.token
            },
            json={
                "log": "task_demo_log" + str(datetime.datetime.now()),
                "testcase_id": 1
            }
        )
        assert r.status_code == 200

        # 新增后要先查询，查看是否新增数据成功
        r = requests.get(
            self.url,
            # 因为对应的TestcaseApi类中的方法get被@jwt_required装饰了，所以需要token（写在header中），否则访问提示无权
            headers={
                "Authorization": "Bearer " + self.token
            }
        )
        print(r.json())
        assert r.status_code == 200

        assert len(r.json()) >= 1
