DTQ
===

Fire and forget commands, linearized.

Demo
----

It's vanilla Python >=3.5, no packages needed.

In a first shell

    python dtq/server.py

In another shell

    python dtq/client.py 'date && sleep 10'
    python dtq/client.py 'echo "beuha"'

Licence
-------

GPLv3 © Mathieu Lecarme
