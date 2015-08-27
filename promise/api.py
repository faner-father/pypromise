__author__ = 'faner'


def check_callable(target):
    if not (target and callable(target)):
        raise TypeError('target is not callable!')


class PromiseRunner(object):
    def __init__(self, promiseObj, run):
        self._promiseObj = promiseObj
        from threading import Thread

        def _run_wrap():
            try:
                self._result = run()
                self._promiseObj.do_then()
            except Exception, e:
                self._promiseObj.do_fail()

        self._runner = Thread(target=_run_wrap)
        self._runner.start()


class Promise(object):
    def __init__(self, call):
        pr = self._pr = PromiseRunner(self, call)
        self._result = None
        self._success = True
        self._completed = False

    @property
    def completed(self):
        return self._completed

    @property
    def result(self):
        return self._result

    @property
    def success(self):
        return self._success

    def do_then(self):
        self._result = self._success_callback()
        self._success, self._completed = True, True

    def do_fail(self):
        self._result = self._fail_callback()
        self._success, self._completed = False, True

    def then(self, success_callback):
        check_callable(success_callback)
        self._success_callback = success_callback
        return self

    def fail(self, fail_callback):
        check_callable(fail_callback)
        self._fail_callback = fail_callback
        return self


def PromiseWrapper(target, *args, **kwargs):
    return Promise(lambda: target(*args, **kwargs))
