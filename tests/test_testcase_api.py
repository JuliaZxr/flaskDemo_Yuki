#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from unittest import TestCase
import requests


class TestTestCaseApi:
    url = "http://127.0.0.1:5000/testcase"

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
    def test_testcase_get(self):
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
    def test_testcase_post(self):
        # 添加数据使用post
        r = requests.post(
            self.url,
            headers={
                "Authorization": "Bearer " + self.token
            },
            json={
                "casename": "testcase_demo_name" + str(datetime.datetime.now()),
                "data": "click add"
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

        data = [testcase["data"] for testcase in r.json()]
        assert 'click add' in data

    # 测试修改数据， 此处使用的是post非put
    """
    严格的来说，新增使用post，修改使用put：
        /testcase post 表示新增
        /testcase?id=1 post 表示修改，即通过id=1告知修改具体数据
            · 在post中id=1使用params传递
            · 在post中需要修改的使用json传递
    """
    def test_testcase_put(self):
        # 添加数据使用post
        r = requests.post(
            self.url,
            headers={
                "Authorization": "Bearer " + self.token
            },
            params={
                "id": 1
            },
            json={
                "data": "click modify"
            }
        )
        print(r.text)
        assert r.status_code == 200

        # 修改后要先查询，查看是否新增数据成功
        r = requests.get(
            self.url,
            # 因为对应的TestcaseApi类中的方法get被@jwt_required装饰了，所以需要token（写在header中），否则访问提示无权
            headers={
                "Authorization": "Bearer " + self.token
            }
        )
        print(r.json())
        assert r.status_code == 200
        # 将修改后的data取出来，去断言存在修改后的特定单词 modify
        data = [testcase["data"] for testcase in r.json() if testcase["id"] == 1][0]
        # for testcase in r.json():
        #     if testcase.id == 1:
        #         data = testcase.data
        assert 'modify' in data