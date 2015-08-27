__author__ = 'faner'

from unittest import TestCase
from promise import api


def long_wait_func(success=True):
    import time

    time.sleep(3)
    if not success:
        raise RuntimeError('test error')


@api.promise_decorator
def long_wait_func_2(success=True):
    import time

    time.sleep(3)
    if not success:
        raise RuntimeError('test error')

def success():
    print 'success'
    return 'success'


def fail():
    print 'fail'
    return 'fail'


class TestMain(TestCase):
    def testPromise(self):
        import time
        pr = api.PromiseWrapper(long_wait_func).then(success).fail(fail)
        while not pr.completed:
            time.sleep(1)
            print 'still wait ...'
        print 'wait over, result is ', pr.result
        assert pr.result == success()

        pr = api.PromiseWrapper(long_wait_func, False).then(success).fail(fail)
        while not pr.completed:
            time.sleep(1)
            print 'still wait ...'
        print 'wait over, result is ', pr.result
        assert pr.result == fail()

    def testPromise2(self):
        import time
        pr = long_wait_func_2().then(success).fail(fail)
        while not pr.completed:
            time.sleep(1)
            print 'still wait ...'
        print 'wait over, result is ', pr.result
        assert pr.result == success()

        pr = long_wait_func_2(False).then(success).fail(fail)
        while not pr.completed:
            time.sleep(1)
            print 'still wait ...'
        print 'wait over, result is ', pr.result
        assert pr.result == fail()

if __name__ == '__main__':
    from unittest import TestProgram

    TestProgram(defaultTest=TestMain).runTests()
