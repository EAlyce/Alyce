"""
PagerMaid 插件兼容装饰器
支持 @on_command, @on_message 等
"""
from core.dispatcher import Dispatcher
from core.command import CommandRegistry

dispatcher = Dispatcher()
commands = CommandRegistry()

import inspect
from functools import wraps

def on_command(name, admin_only=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 自动注入 message, client, args
            sig = inspect.signature(func)
            params = sig.parameters
            inject_args = []
            # 约定参数顺序: message, client, args
            if 'message' in params:
                inject_args.append(kwargs.get('message'))
            if 'client' in params:
                inject_args.append(kwargs.get('client'))
            if 'args' in params:
                inject_args.append(kwargs.get('args', []))
            # 权限校验
            if admin_only and hasattr(kwargs.get('message'), 'from_user'):
                user = kwargs['message'].from_user
                if not getattr(user, 'is_admin', False):
                    return  # 非管理员不执行
            return await func(*inject_args)
        commands.register(name, wrapper)
        return wrapper
    return decorator

def on_message(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 自动注入 message, client
        sig = inspect.signature(func)
        params = sig.parameters
        inject_args = []
        if 'message' in params:
            inject_args.append(kwargs.get('message'))
        if 'client' in params:
            inject_args.append(kwargs.get('client'))
        return await func(*inject_args)
    dispatcher.register("message", wrapper)
    return wrapper
