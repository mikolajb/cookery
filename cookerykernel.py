from ipykernel.kernelbase import Kernel
from sys import path as syspath
syspath.append('../cookerypy')
from cookery import Cookery


class CookeryKernel(Kernel):
    implementation = 'Cookery'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {'mimetype': 'text/plain'}
    banner = "Cookery banner"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.cookery = Cookery()

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not silent:
            res = self.cookery.execute_expression(code)

            stream_content = {'name': 'stdout', 'text': repr(res)}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}

    def do_inspect(self, code, cursor_pos, detail_level=0):
        self.log.debug(code)
        self.log.debug(cursor_pos)
        return {'status': 'ok', 'data': {}, 'metadata': {}, 'found': False}

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CookeryKernel)
