# coding: utf-8
__author__ = 'cloud'

'''
promise model:

'''

# example 1:
'''
create vol and attach
'''


def vol_create(vol_arg):
    pass


def vol_wait_available(scope):
    pass


def vol_attach_get_lock(scope):
    pass


def vol_attach(scope):
    pass


def vol_attach_release_lock(scope):
    pass


def vol_create_fail(scope):
    pass


def vol_wait_available_fail(scope):
    pass


class Promise(object):
    '''
    有以下几种执行顺序:
        一条链:func->then-then
        多条链:func->then->branch->then
                        ->branch2(parallel)
        任意条链上节点异常则链停止,执行fail

    feeds产生多个promise,
        promise(func).then(func2).feeds([d1, d2])
        等同于
            promise(func).then(func2).feed(d1)
            promise(func).then(func2).feed(d2)
        由一个promise坐代理
    go方法用来启动执行,自动识别是单promise还是多个promise
    '''

    def __init__(self, func, fail):
        pass

    def then(self, func_or_promise, fail_callback=None):
        # do something
        return self

    def thenes(self, func_or_promises, *fail_callbacks, **kw_fail_callbacks):
        return self

    def branch(self, branch_func_or_promise, fail_callback=None):
        pass

    def branches(self, branch_func_or_promises, *fail_callbacks, **kw_fail_callbacks):
        pass

    def feed(self, initial_data):
        pass

    def feeds(self, initial_datas):
        pass

    def go(self, initial_data=None):
        pass

    @property
    def completed(self):
        pass

    @property
    def result(self):
        pass


def promise(func, fail):
    return Promise(func, fail)


# promise and go, create single vol
pr1 = promise(vol_create, vol_create_fail) \
    .then(vol_wait_available, vol_wait_available_fail) \
    .then(vol_attach_get_lock) \
    .then(vol_attach).then(vol_attach_release_lock).go(initial_data=vol_arg)
'''
pr1 = promise(vol_create, vol_create_fail) \
    .then(vol_wait_available, vol_wait_available_fail) \
    .then(vol_attach_get_lock) \
    .then(vol_attach).then(vol_attach_release_lock).feed(initial_data=vol_arg)
pr1.go()

'''

while not pr1.completed:
    time.sleep()
else:
    print pr1.result


# create multiple vols
pr_proxy = promise(vol_create, vol_create_fail) \
    .then(vol_wait_available, vol_wait_available_fail) \
    .then(vol_attach_get_lock) \
    .then(vol_attach).then(vol_attach_release_lock).goes(initial_datas=[vol_arg, vol_arg2])
'''
pr_proxy = promise(vol_create, vol_create_fail) \
    .then(vol_wait_available, vol_wait_available_fail) \
    .then(vol_attach_get_lock) \
    .then(vol_attach).then(vol_attach_release_lock).feeds(initial_datas=[vol_arg, vol_arg2])
pr_proxy.goes()
'''

while not pr_proxy.completed:
    time.sleep(1)
else:
    for p in pr_proxy:
        print p.result

'''
example 2:
create instance with create and attach volumes, create and attach port.
'''


def upload_image():
    pass


def instance_create(inst_data):
    pass


def port_create(port_data):
    pass


def port_attach(scope):
    pass


def get_inst_lock(inst_id):
    pass


def release_inst_lock(inst_id):
    pass


vol_pr_proxy = promise(vol_create, vol_create_fail) \
    .then(vol_wait_available, vol_wait_available_fail) \
    .then(vol_attach_get_lock) \
    .then(vol_attach).then(vol_attach_release_lock).feeds(initial_datas=[vol_arg, vol_arg2])

inst_pr = promise(instance_create).feed(initial_data=inst_data)

port_pr = promise(port_create).thenes([get_inst_lock, port_attach, release_inst_lock]).feed(initial_data=port_data)

promise(upload_image).then(inst_pr).branches([vol_pr_proxy, port_pr])
