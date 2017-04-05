# coding: utf-8

from datetime import datetime
from datetime import timedelta

from leancloud import Object
from leancloud import ACL
from leancloud import Engine
from leancloud import LeanEngineError

from app import app


engine = Engine(app)


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')
    author = todo.get('author')
    if author:
        acl = ACL()
        acl.set_public_read_access(True)
        acl.set_read_access(author.id, True)
        acl.set_write_access(author.id, True)
        todo.set_acl(acl)


@engine.define
def empty_trash():
    deleted_todos = Object.extend('Todo').query.equal_to('status', -1).less_than('updatedAt', datetime.today() - timedelta(30)).find()
    if not deleted_todos:
        print('过去 30 天内没有被删除的 todo')
    else:
        print('正在清理{0}条 todo……'.format(len(deleted_todos)))
        for todo in deleted_todos:
            todo.destroy()
        print('清理完成。')
