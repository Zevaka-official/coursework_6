import json
import logging

import redis
from hashlib import sha1

from django.conf import settings


class BackgroundTaskManager:
    logger = logging.getLogger(__name__)

    @staticmethod
    def _get_args_pair(data):
        data_str = json.dumps(data)
        data_hash = sha1(data_str.encode('utf-8')).hexdigest()
        return data_hash, data_str

    @classmethod
    def _execute_bg_func(cls, func, s_arg):
        kwargs = json.loads(s_arg)
        retry = kwargs['__retry'] - 1
        args = kwargs['__args']
        del kwargs['__retry']
        del kwargs['__args']
        try:
            func(*args, **kwargs)
            return True, None, None
        except Exception as e:
            cls.logger.exception(e)
            kwargs['__retry'] = retry
            kwargs['__args'] = args
            return False, retry, json.dumps(kwargs)

    def __init__(self, hostname, port, db_id):
        self._bg_methods = {}
        self._redis_conn_pool = redis.ConnectionPool(host=hostname, port=port, db=db_id)

    def schedule(self, retry_count, ttl: int = 5 * 60):
        """
        Add task to background task list
        :param retry_count:
        :param ttl: time to live..
        :return:
        """
        def _decorator(func):
            method_name = func.__name__
            self._bg_methods[method_name] = func

            def _wrap(*args, **kwargs):
                with redis.Redis(connection_pool=self._redis_conn_pool) as db:
                    kwargs['__retry'] = retry_count
                    kwargs['__args'] = args
                    key, data = self._get_args_pair(kwargs)

                    db.set(f'{method_name}_{key}', data, ex=ttl)

            return _wrap

        return _decorator

    def run_scheduled_methods(self):
        """
        Go to the Moon!.. khm.. execute scheduled tasks
        :return:
        """
        with redis.Redis(connection_pool=self._redis_conn_pool) as db:
            for func_name, func in self._bg_methods.items():
                kk = db.keys(f'{func_name}_*')
                for key in kk:
                    is_success, retry_cnt, arg = self._execute_bg_func(func, db.get(key))
                    if is_success or retry_cnt <= 0:
                        db.delete(key)
                    else:
                        db.set(key, arg, ex=db.ttl(key))


background_task_manager = BackgroundTaskManager(**settings.BACKGROUND_TASK_MANAGER["redis"])

run_scheduled = background_task_manager.run_scheduled_methods
