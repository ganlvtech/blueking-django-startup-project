它提供的只是一个 Django 的 Docker 容器！你可以做你想做的一切。

根目录中必须有 `settings.py`，因为 `DJANGO_SETTINGS_MODULE` 在容器的环境变量中设置为 `settings`。

静态文件在容器外部提供。所以你必须将静态文件放在 `/static/` 下并将 `/static/` 通过 SVN 上传到服务器。将它们放在每个应用程序的目录下，想通过 Django 提供它们是不可行的。

Blueking Django Framework 提供了许多帮助 DevOps 的模块，例如流量分析器，邮件程序，短信发送，日志记录，QQ 登录，权限控制和 Mako 模板引擎等。它们太沉重了。普通的 Web 应用程序可能不需要它们。

如果你是 Django 的新手，这个简单的 `settings.py` 不会让你感到困惑。只需在项目中添加一个文件，修改几行配置，就可以是 Blueking 平台运行 Django 官方教程的项目了。希望它可以帮到你。

当你对 Django 足够了解之后，你可以自己实现它们。
