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
        old_stdinstdout = _setup_stdinout()
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
        _reset_stdinout(old_stdinstdout)
        return retval
    def copy(self):
        shell2 = shell(lambda x:x)
        shell2.command = self.command
        shell2.pipes = dict(self.pipes)
        return shell2
    def __call__(self, *args, **kwargs):
        shell2 = self.copy()
        shell2.command = self.command(*args, **kwargs)
        return shell2
    def add_pipe(self, name, descriptor):
        new_shell = shell(lambda x:x)
        new_shell.command = self.command
        new_shell.pipes = dict(self.pipes)
        new_shell.pipes[name] = descriptor
        return new_shell
    def redirect(self, *args):
        def compact():
            str_prev = None
            for arg in args:
                if isinstance(arg, str):
                    if str_prev is None:
                        str_prev = arg
                    else:
                        yield str_prev, arg
                        str_prev = None
                else if len(arg) == 2:
                    yield arg[0], arg[1]
                else:
                    raise TypeError("Argument is not a string or a two-element tuple of strings: " + arg)
            if str_prev is not None:
                raise Exception("Odd number of non-string arguments")
        shell_current = 
        for pipe_in, pipe_out in compact():

def _setup_stdinout():
    old_stdinstdout = sys.stdin, sys.stdout, sys.stderr
    if 'stdin' in pipes:
        sys.stdin = pipes['stdin']
    if 'stdout' in pipes:
        sys.stdout = pipes['stdout']
    if 'stderr' in pipes:
        sys.stderr = pipes['stderr']
    return old_stdinstdout

def _reset_stdinout(old_stdinstdout):
    sys.stdin, sys.stdout, sys.stderr = old_stdinstdout

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

def readline(descriptor, *other_args):
    get_descriptor(descriptor).readline(*other_args)

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
