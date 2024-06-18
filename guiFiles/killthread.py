import threading
import ctypes
import time
from guiFiles.configmgr import ConfigMgr
import guiFiles.initinstruments as init


class KillableThread(threading.Thread):
    def __init__(self, name='', target=None, *args, **kwargs):
        threading.Thread.__init__(self)
        self.name = name
        self.target = target

    def run(self):
        try:
            self.target()
        except:
            if eval(ConfigMgr.instr['loadOnOff']):
                load = init.eload()
                load.output(state='OFF')
            print('Test Killed!')
        return

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if resu > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Failure in raising exception')


if __name__ == '__main__':
    x = twe('Thread A')
    x.start()
    count = 0
    while(count < 10):
        print(count)
        count += 1
        if count == 5:
            x.raise_exception()
            x.join()
        time.sleep(2)
