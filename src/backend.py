#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入Flask类
from flask import Flask
from flask_restful import Api, Resource
# 实例化，可视为固定格式
app = Flask(__name__)
api = Api(app)

# 首页
class Main(Resource):
    def get(self):
        return {'hello': 'Main'}

# 用户管理
class UserApi(Resource):
    def get(self):
        return {'hello': 'UserApi'}

# 用例管理
class TestcaseApi(Resource):
    def get(self):
        return {'hello': 'TestcaseApi'}

# 任务管理
class TaskApi(Resource):
    def get(self):
        return {'hello': 'TaskApi'}

# 报告管理
class ReportApi(Resource):
    def get(self):
        return {'hello': 'ReportApi'}

# 添加路由
api.add_resource(Main, '/')
api.add_resource(UserApi, '/user')
api.add_resource(TestcaseApi, '/testcase')
api.add_resource(TaskApi, '/task')
api.add_resource(ReportApi, '/report')


if __name__ == '__main__':
    app.run(debug=True)