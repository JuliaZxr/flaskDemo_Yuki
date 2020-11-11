#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入Flask类
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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

# session加密设置
app.config['JWT_SECRET_KEY'] = 'yuki-secret'  # Change this!
jwt = JWTManager(app)

"""
对应不同的数据库表结构：User、Testcase、Task
"""

# user 用户 数据库结构
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

# testcase 用例 数据库结构
class Testcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    casename = db.Column(db.String(80), unique=True, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=True)

    def __repr__(self):
        return '<Testcase %r>' % self.casename

# task 任务 数据库结构
class Task(db.Model):
    # 表名
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    # log 是任务执行后的返回结果
    log = db.Column(db.String(1024), unique=False, nullable=True)

    """
    建立关联数据库：
        testcase_id作为testcase表的外键ForeignKey，
        testcase:数据库中不存在的字段，只是为了查找和反向查找。backref:在关系的另一模型中添加反向引用        
    """
    testcase_id = db.Column(db.Integer, db.ForeignKey('testcase.id'),nullable=False)
    testcase = db.relationship('Testcase',backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return '<Task %r>' % self.log


# 首页
class Main(Resource):
    def get(self):
        return {'hello': 'Main'}

# 用户管理
class UserApi(Resource):
    def get(self):
        # 查看提取数据库中所有的用户
        users = User.query.all()
        # 返回一个列表：每个user的id、name
        return [
            {
                "id": u.id,
                "name": u.username
            } for u in users
        ]

    # 用户登录
    def post(self):
        # 获取用户名和密码
        username=request.json.get("username")
        password=request.json.get("password")

        # 验证：通过数据库查询过滤符合条件的第一条数据，若用户存在，返回登录成功消息，否则返回登录失败消息
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # 登录成功后返回客户一个token
            access_token = create_access_token(identity=username)
            return {"msg": "login success", "access_token": access_token}
        else:
            return {"msg": "login fail"}

    # 用户注册
    def put(self):
        # 获取用户名、密码、邮箱
        username = request.json.get("username")
        password = request.json.get("password")
        email = request.json.get("email")

        # 新建user对象，设置参数
        user = User(username=username, password=password, email=email)
        # 通过db进行数据库新增
        db.session.add(user)
        # 提交db操作
        db.session.commit()

        return {"msg": "register success"}

    # 用户账户删除
    def delete(self):
        pass

# 用例管理
class TestcaseApi(Resource):
    # @jwt_required是个装饰器，添加后，对应方法就被自动加上token校验
    @jwt_required
    def get(self):
        # 查看提取数据库中所有的用例,并返回一个列表：每个用例的属性值
        return [
            {
                "id": case.id,
                "casename": case.casename,
                "data": case.data
            } for case in Testcase.query.all()
        ]

    @jwt_required
    def post(self):
        """
        /testcase post 表示新增
        /testcase?id=1 post 表示修改

        此例子新增和修改都使用post；所以用if判断区别，当request中的args参数含id---->对应测试用例方法中的参数params={"id": 1}；则执行修改命令；否则执行新增命令
        """
        if request.args.get("id"):
            # 查询所有用例，过滤测试用例里id=1的数据，取第一条，赋值给testcase
            testcase = Testcase.query.filter_by(id=request.args.get("id")).first()
            # 如果请求的参数中有casename或者data，再执行修改命令
            if request.json.get("casename"):
                testcase.casename = request.json.get("casename")
            if request.json.get("data"):
                testcase.data = request.json.get("data")
            # 修改数据使用flush
            db.session.flush()
            db.session.commit()
        else:
            # 新建一个对象，设置参数值后，添加到数据库，并提交
            testcase = Testcase()
            testcase.casename = request.json.get("casename")
            testcase.data = request.json.get("data")
            # 新增数据使用add
            db.session.add(testcase)
            db.session.commit()

    @jwt_required
    def put(self):
        pass

    @jwt_required
    def delete(self):
        pass

# 任务管理
class TaskApi(Resource):
    @jwt_required
    def get(self):
        # 查看提取数据库中所有的任务,并返回一个列表：每个任务的属性值
        return [
            {
                "id": task.id,
                "log": task.log,
                "testcase_id": task.testcase_id
            } for task in Task.query.all()
        ]

    @jwt_required
    def post(self):
        """
        /task post 表示新增任务，同时执行
        /task?id=1 post 表示结果回传
        """
        # 新建一个对象，设置参数值后，添加到数据库，并提交
        task = Task()
        task.log = request.json.get("log")
        task.testcase_id = request.json.get("testcase_id")
        # 新增数据使用add
        db.session.add(task)
        db.session.commit()

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