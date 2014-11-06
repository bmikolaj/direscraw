#!/usr/bin/env python
def nform(input, *args):
    alist = []
    for i in args:
        alist.append(i)

    if len(alist) > 2:
        raise ValueError('{} arguments specified: Maximum is 2.'.format(len(alist)))
    elif len(alist) == 1:
        alist.append(None)
    elif len(alist) == 0:
        alist.append(None)
        alist.append(None)

    if alist[1] and not isinstance(alist[1], int):
        raise ValueError('Argument must be an integer.')

    if isinstance(alist[0], int):
        f = alist[0]
    elif isinstance(alist[1], int):
        f = alist[1]
    else:
        f = 2

    formatted = '{{:.{}f}}'.format(f).format(input).rstrip('0').rstrip('.')
    if alist[0] and not isinstance(alist[0], int):
        formatted = formatted + alist[0]

    return formatted
    #print(formatted)

nform(34.4445, 4)