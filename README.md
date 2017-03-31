# Flask Todo Demo

## 环境与依赖

Flask Todo Demo 是一个 [LeanEngine][1] 的示例项目。它运行在 Python 3 上，依赖 [flask][2] 和 [LeanCloud Python SDK][3]。你可以在 [这里][11] 查看在线 demo。

## 在开始之前

Flask Todo Demo 是一个 [LeanCloud][4] 应用。在部署上线之前，需要先做一些准备工作。

1. 在 [LeanCloud 控制台][5] 新建一个应用，并设置一个二级域名。
2. 在控制台中新增一个名为 `SECRET_KEY` 的环境变量。（关于如何创建一个好的密钥，请参考 [这个 gist][6]）
3. 安装最新版的 [LeanCloud 命令行工具][7]。如果你无法访问 GitHub，请移步 [国内镜像](http://releases.leanapp.cn/#/leancloud/lean-cli/releases)。

## 部署方法

首先将 Flask Todo Demo 的代码克隆到本地。在终端中打开项目所在目录，输入 `lean login`，然后 `lean checkout`，根据提示操作，就可以将本地的项目与刚刚在 LeanCloud 上创建的应用链接起来。

使用 [virtualenv][8] 来为这个应用创建一个隔离的 Python 运行环境。激活虚拟环境，然后用 `pip` 来安装所需的依赖。

用 `lean deploy` 命令将代码部署到 LeanCloud 上。部署完成之后，就可以在浏览器中输入刚才设置的域名，打开线上运行的网站了。

简单来讲：

```bash
$ git clone https://github.com/leancloud/flask-todo-demo.git && cd flask-todo-demo
$ virtualenv venv --python=python3 && source venv/bin/activate
$ (venv) pip install -r requirements.txt
$ (venv) lean login
$ (venv) lean checkout
$ (venv) lean deploy
```

## 如何调试？

在本地调试，请使用 `lean up` 命令，然后在 `http://localhost:3000` 查看本地运行实例。如果你使用了虚拟环境，请先激活对应的虚拟环境。

## 高级技巧

### Hook 函数

在 `cloud.py` 中有一个 `before_todo_save` 函数，它的上一行是 `@engine.before_save('Todo')`，说明这是一个 Hook 函数。当一个新的 `Todo` 将要被保存到数据之前，LeanCloud 会自动调用这个函数，你可以利用它来检查数据的有效性。

在现在这个函数里，当一个 todo 的 `content` 超过 240 个字，我们就会将其截断，并在最后加上「...」。这显然不是最好的办法；如果你有兴趣，可以尝试 fork 代码之后自己修改成更好的处理方法。

除了在对象保存之前进行预处理，你还可以调用很多其他 Hook。想要了解更多，可以参考 [Hook 函数文档][13]。

### 定时任务

`cloud.py` 中的另一个函数是 `empty_trash`，它会筛选出 `status` 为 `-1` 且最后一次更新时间是 30 天之前的 todo 并删除。

这是一个云函数，你可以在项目中通过 `leancloud.cloudfunc.run('empty_trash')` 来手动调用它，但显然自动化是更好的方案。

为了实现自动化，我们可以在 LeanCloud 控制台设置一个定时任务，让这个函数每天凌晨都自动运行一次。

将代码部署到云引擎之后，你就可以前往 LeanCloud 控制台，在云引擎 > 定时任务中创建一个定时器。定时器的运行规则用 cron 表达式来定义，这里我们希望它每天凌晨 12 点运行一次，那么 cron 表达式就应当写作 `0 0 0 * * ?`。

定时任务可以帮你自动做很多事情，想要了解更多，可以参考 [定时任务文档][14]。

## 其他语言的 Demo

请参考 [LeanCloud 开源 Demo][12]

## Miscellaneous

* License: [MIT][9]
* Author: GUAN Xiaoyu ([guanxy@me.com][10])

[1]: https://leancloud.cn/docs/leanengine_overview.html
[2]: http://flask.pocoo.org
[3]: https://github.com/leancloud/python-sdk
[4]: https://leancloud.cn/
[5]: https://leancloud.cn/dashboard/applist.html#/apps
[6]: https://gist.github.com/nervouna/cd58fb09c22826eaaff996793de72d85
[7]: https://github.com/leancloud/lean-cli/releases/latest
[8]: https://github.com/pypa/virtualenv
[9]: https://github.com/leancloud/flask-todo-demo/blob/master/LICENSE
[10]: mailto:guanxy@me.com
[11]: https://flask-todo-demo.leanapp.cn
[12]: https://leancloud.cn/docs/demo.html#/web
[13]: https://leancloud.cn/docs/leanengine_cloudfunction_guide-python.html#Hook_函数
[14]: https://leancloud.cn/docs/leanengine_cloudfunction_guide-python.html#定时任务