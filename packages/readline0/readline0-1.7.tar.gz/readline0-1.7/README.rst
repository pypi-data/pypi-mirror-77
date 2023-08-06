Read lines of data with an arbitrary delimiter, like a null, newline or even an x.

It passes pylint, passes pycodestyle, passes pydocstyle, is thoroughly unit tested, and runs on CPython 2.7, CPython 3.x,
Pypy 7.3.1, and Pypy3 7.3.1.

It gains a lot of speed by eschewing single-character reads.

Usage looks like:
   .. code-block:: python

      import readline0
      file_ = open('/etc/shells', 'r')
      for line in readline0.readline0(file_=file_, separator=b'\n'):
      ...     print(line)
      ...
      b'# /etc/shells: valid login shells'
      b'/bin/sh'
      b'/bin/dash'
      b'/bin/bash'
      b'/bin/rbash'

Of course separator need not be a newline; it defaults to a null byte.
Also ``file_`` defaults to sys.stdin.
And there's a blocksize argument as well, which defaults to 64K.
