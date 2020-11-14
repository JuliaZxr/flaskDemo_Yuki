# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    jenkins = Jenkins(
        # 'http://10.6.7.171:8080/',
        'http://192.168.1.21:8080/',
        username='Momo',
        password='11f0b9a6d7c7ac4c6082911f2981b0144e'
    )
    print(jenkins.version)
    # keys()代表jenkins里所有的job任务：['20201029_iSelenium_jenkins', 'iSelenium_git_jenkins', 'lagou3_yuki_testcase']
    print(jenkins.keys())
    # 打印对应jenkins job的最后一次构建的结果集：{'lagou3.txt': <jenkinsapi.artifact.Artifact http://192.168.1.21:8080/job/lagou3_yuki_testcase/5/artifact/lagou3.txt>}中的lagou3_yuki_testcase/5代表最后一次构建数是5
    print(jenkins["lagou3_yuki_testcase"].get_last_build().get_artifact_dict())
    # 使用构建，因为设置了构建参数testcase_id，手动构建的时候要填参，所以这里调用时需要配置参数
    jenkins['lagou3_yuki_testcase'].invoke(
        build_params={'testcase_id': 1},
        block=True
    )
    # 调用完成后再次打印最后一次构建的结果集，确认是否调用构建成功
    print(jenkins["lagou3_yuki_testcase"].get_last_build().get_artifact_dict())
