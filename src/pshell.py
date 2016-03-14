import sys

def default_pipes():
    return {'stdin' : sys.stdin, 'stdout' : sys.stdout, 'stderr' : sys.stderr}

pipes = default_pipes()

class shell:
    def __init__(self, base_function):
        self.command = generate_shell(base_function)
        self.pipes = default_pipes()
    def run(self):
        global pipes
        old_pipes = pipes
        pipes = self.pipes
        retnotinoriginally = 'ret' not in pipes
        if retnotinoriginally:
            pipes['ret'] = WritableBuffer()
        self.command.execute()
        if retnotinoriginally:
            retval = pipes['ret'].text
            del pipes['ret']
        else:
            retval = ''
        pipes = old_pipes
        return retval
    def __call__(self, *args, **kwargs):
        shell2 = shell(lambda x:x)
        shell2.command = self.command(*args, **kwargs)
        shell2.pipes = self.pipes
        return shell2

class WritableBuffer:
    def __init__(self):
        self.text = ""
    def write(self, string):
        self.text += str(string)

def get_descriptor(descriptor):
    if descriptor in pipes:
        return pipes[descriptor]
    raise Exception(
        "%s is not a valid file descriptor in this context: available pipes = %s"
            % (descriptor, set(pipes.keys())))

def read(descriptor, *other_args):
    get_descriptor(descriptor).read(*other_args)

def write(descriptor, *other_args):
    get_descriptor(descriptor).write(*other_args)

class system_cmd:
    def __init__(self, command):
        self.command = command
    def execute(self):
        subprocess.call(
            self.command,
            shell   = True,
            stdin   = get_descriptor('stdin'),
            stdout  = get_descriptor('stdout'),
            stderr  = get_descriptor('stderr'))

class python_fn_cmd:
    def __init__(self, func):
        self.func = func
        self.args = ()
        self.kwargs = {}
    def execute(self):
        write('ret', self.func(*self.args, **self.kwargs))
    def __call__(self, *args, **kwargs):
        newkwargs = dict(self.kwargs)
        newkwargs.update(kwargs)
        val = python_fn_cmd(self.func)
        val.args = self.args + args
        val.kwargs = newkwargs
        return val

def generate_shell(base_function):
    if isinstance(base_function, str):
        return system_cmd(base_function)
    if callable(base_function):
        return python_fn_cmd(base_function)
