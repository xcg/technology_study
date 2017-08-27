#!/usr/bin/env python
#coding:utf-8

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import time

env.user = 'root'
env.hosts = ['172.16.10.54','172.16.10.53']
env.password = '123456'

# 开发机项目主目录
env.project_dev_source = '/data/dev/Lwebadmin/' 

# 开发机项目压缩包存储目录
env.project_tar_source = '/data/dev/releases/'

# 项目压缩包名前缀,文件名为release.tar.gz
env.project_pack_name = 'release' 

# 项目生产环境主目录
env.deploy_project_root = '/data/www/Lwebadmin/' 

# 项目发布目录,位于主目录下面
env.deploy_release_dir = 'releases'

# 对外服务的当前版本软链接
env.deploy_current_dir = 'current' 

# 版本号
env.deploy_version=time.strftime("%Y%m%d")+"v2" 

@runs_once
# 获得用户输入的版本号,以便做版本回滚操作
def input_versionid(): 
        return prompt("please input project rollback version ID:",default="")

# 打包本地项目主目录,并将压缩包存储到本地压缩包目录
@task
@runs_once
def tar_source(): 
        print yellow("Creating source package...")
        with lcd(env.project_dev_source):
                local("tar -czf %s.tar.gz ." % (env.project_tar_source + env.project_pack_name))
        print green("Creating source package success!")


# 上传任务函数
@task
def put_package(): 
        print yellow("Start put package...")
        with settings(warn_only=True):
                with cd(env.deploy_project_root+env.deploy_release_dir):
                        # 创建版本目录
                        run("mkdir %s" % (env.deploy_version)) 
        env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_version

        #上传项目压缩包至此目录
        with settings(warn_only=True): 
                result = put(env.project_tar_source + env.project_pack_name + ".tar.gz", env.deploy_full_path)
        if result.failed and no("put file failed, Continue[Y/N]？"):
                abort("Aborting file put task!")

        # 成功解压后删除压缩包
        with cd(env.deploy_full_path): 
                run("tar -zxvf %s.tar.gz" % (env.project_pack_name))
                run("rm -rf %s.tar.gz" % (env.project_pack_name))
        print green("Put & untar package success!")

# 为当前版本目录做软链接
@task
def make_symlink(): 
        print yellow("update current symlink")
        env.deploy_full_path=env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_version
        # 删除软链接,重新创建并指定软链源目录,新版本生效
        with settings(warn_only=True): 
                run("rm -rf %s" % (env.deploy_project_root + env.deploy_current_dir))
                run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir))
        print green("make symlink success!")

# 版本回滚任务函数
@task
def rollback(): 
        print yellow("rollback project version")
        # 获得用户输入的回滚版本号
        versionid = input_versionid() 
        if versionid == '':
                abort("Project version ID error,abort!")
        env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + versionid
        # 删除软链接,重新创建并指定软链源目录,新版本生效
        run("rm -f %s" % env.deploy_project_root + env.deploy_current_dir)
        run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir)) 
        print green("rollback success!")

# 自动化程序版本发布入口函数
@task
def go():
        tar_source()
        put_package()
        make_symlink()