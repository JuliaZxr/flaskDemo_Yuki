#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入Flask类
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# 实例化，可视为固定格式
app = Flask(__name__)
api = Api(app)
# 配置数据库，连接地址
# 参数说明：
# app.config['SQLALCHEMY_DATABASE_URI'] = '数据库类型://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名字'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@127.0.0.1:3306/lagou3_yuki'
db = SQLAlchemy(app)

# 数据库结构
class User(db.Model):
    # id时integer类型，是主键
    id = db.Column(db.Integer, primary_key=True)
    # username是string类型，80字节，是唯一的，不可为空
    username = db.Column(db.String(80), unique=True, nullable=False)
    # password是string类型，80字节，不是唯一的，不可为空
    password = db.Column(db.String(80), unique=False, nullable=False)
    # email是string类型，120字节，是唯一的，不可为空
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# 首页
class Main(Resource):
    def get(self):
        return {'hello': 'Main'}

# 用户管理
class UserApi(Resource):
    def get(self):
        # 查看提取数据库中所有的用户
        users = User.query.all()
        # 返回一个列表：每个user的id
        return [{"id": u.id, "uname": u.username} for u in users]

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