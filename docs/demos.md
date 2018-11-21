* `file_upload` 模块

    * [上传文件](/upload/)：上传文件到服务器、从上传文件夹删除文件

* `myutils` 模块

    * [系统信息](/utils/pyinfo/)：列举全部系统信息
    * [浏览文件](/utils/files/)：浏览从根目录开始的任意文件
    * [hosts](/utils/hosts/)：显示系统 `/etc/hosts` 文件
    * [用户和用户组](/utils/users/)：显示 Linux 系统的 `/etc/passwd` 和 `/etc/group` 文件
    * [创建超级用户](/utils/createsuperuser/)：类似于执行 `manage.py createsuperuser`，仅在数据库没有超级管理员时才可以使用
    * [重置数据库](/utils/reset_db/)：输入超级管理员的用户名和密码，删除全部表，重新执行 migrate

* `golang` 模块

    * [执行 Go 程序](/go/)：同步执行 Go 程序，在程序运行结束之后返回输出结果
    * [流式响应](/go/stream/)：前端使用 `EventSource`，后端使用 `event-stream`，实现流式响应，返回输出结果
    * [直接返回 PID](/go/nowait/)：异步执行 Go 程序，仅返回 PID，不管输出结果

* `celery_test` 模块

    * [计数器](/celery/)：一个基于 Celery 的计数器，每分钟自动触发一次 Period Task，使计数器 +1
    * [计数器 +1](/celery/add/)：手动新建一个 Task，使计数器 +1，与周期性任务不冲突

* `send_mail` 模块

    * [SMTP 发送邮件](/mail/)：使用 SMTP 协议发送邮件

* Django Admin

    * [后台管理](/admin/)：Django Admin
