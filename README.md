# 部署方法
1. 安装基础环境
pip install -r requirements.txt

2. 初始化数据库
python manage.py migrate

3. 运行项目
python manage.py runserver 0.0.0.0:8080

4. 浏览器打开
http://127.0.0.1:8080/chat



修改consumers.py的<br/>
<br/>
docker_ips = ["192.168.2.77","192.168.2.78"]<br/>
docker_image = "centos:7.9.2009"<br/>
docker_port = 2375<br/>
<br/>
异步多进程去多个服务器去拉取centos:7.9.2009镜像
