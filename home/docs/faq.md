### 在服务器上通过 pip 安装包

把需要的包和版本号写在 `requirements.txt` 中

服务器会自动运行 `pip install -r requirements.txt`

**注意：服务器的 setuptools 并不是最新版的，部分 pip 包安装时对 setuptools 的版本有要求，这些包不能被安装。**

### 关于 MySQL

在本地开发环境中，你不必使用原生的 `MySQL-python`，试试 `PyMySQL` 吧！

```bash
pip install PyMySQL
```

你不必将 `PyMySQL` 添加到 `requirements.txt` 中，因为服务器已经自带了 `MySQL-python`。

### 静态文件

服务器中并不通过 Django 提供静态文件，而是通过 Nginx 直接提供，所以 SVN Commit 必须包含 `/static/` 文件夹。

如果你把静态文件存放在每个子应用的 `static/` 文件夹下，那么你可以使用 Django `collectstatic` 将他们自动复制到 `/static/` 文件夹，然后执行 SVN Commit。

```bash
python manage.py collectstatic
```
