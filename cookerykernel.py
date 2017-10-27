from ipykernel.kernelbase import Kernel
from cookery.cookery import Cookery
from IPython.display import Image


class CookeryKernel(Kernel):
    implementation = 'Cookery'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {'name': 'cookery',
                     'mimetype': 'text/plain',
                     'file_extension': '.cookery'}

    banner = "Cookery kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.cookery = Cookery(jupyter=True)
        self.cookery.log = self.log.getChild(self.implementation)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not silent:
            res = self.cookery.execute_expression_interactive(code)

            stream_content = {'name': 'stdout', 'text': repr(res)}
            # self.send_response(self.iopub_socket, 'stream', stream_content)
            self.send_response(self.iopub_socket, 'stream', Image(url="https://www.google.de/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"))

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}

    def do_complete(self, code, cursor_pos):
        self.log.debug("Completing: {}, at cursor pos: {}".format(code,
                                                                  cursor_pos))
        self.log.debug("Sending: {}".format(code[0:cursor_pos]))
        result = self.cookery.complete(code[0:cursor_pos])
        return {'matches': result,
                'cursor_start': cursor_pos,
                'cursor_end': cursor_pos,
                'metadata': {},
                'status': 'ok'}

    def do_inspect(self, code, cursor_pos, detail_level=0):
        self.log.debug(code)
        self.log.debug(cursor_pos)
        return {'status': 'ok', 'data': {}, 'metadata': {}, 'found': False}

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CookeryKernel)
