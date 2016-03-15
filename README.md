# P-Shell
A shell implemented as a python package

## The `shell` Function

A system command can be called as follows:

```python
shell('cat abc.txt').run()
```

A python function can also be shelled:

```python
shell(function).run()
```

A shell function can be defined using `@` syntax:

```python
@shell
def f():
    for x in range(100):
        print (x)
```

## How to pipe

Piping functions into each other is accomplished as follows:

```python
shell('cat abc.txt').pipe('stdout', 'stdin', shell('sort').pipeToFile('stdout', 'stdin', 'def.txt')).run()
result = shell('cat u.txt').pipeToString('stdout', 'stdin', 'a')['a']
```

which is the equivalent of:

```sh
cat abc.txt | sort > def.txt
```

This format can also be used to redirect other streams:

```python
value = shell('cat abc.txt').pipeToString('stdout', 'a').pipeToString('stderr', 'b')
a, b = value['a'], value['b']
```

## Pipe syntax

Multiple-output redirection is really the only reason to use `.pipe`. If you just want to redirect standard output from one command to the standard output of another, you can use the following syntax:

```python
(shell('cat abc.txt') | shell('sort') | toFile('def.txt')).run()
```
