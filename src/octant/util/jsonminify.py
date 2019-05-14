# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 23:59:24 2019

File: jsonminify.py

Different routines to minify a json file.

Minification consists of removing comments and empty lines.
The JSON format does not naturally permits comments, but
of course they are useful. A common two step approach is to first minimize
the file and then parse the JSON. Something like::

    JSON.parse(JSON.minify(my_str));


See:
    https://stackoverflow.com/questions/244777/can-comments-be-used-in-json
    http://crockford.com/javascript/jsmin

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 10-Mar-2019 | FOE    | - File created and methods jsonminify and            |
|             |        |   fastjsonminify copied from GitHub.                 |
+-------------+--------+------------------------------------------------------+




.. seealso:: None
.. note:: None
.. todo:: None.

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: The authors of the original code

"""

import re


def jsonminify(string, strip_space=True):
    """A port of the `JSON-minify` utility to the Python language.

       Based on JSON.minify.js: https://github.com/getify/JSON.minify
       Contributers:
       - Gerald Storer
         - Contributed original version
       - Felipe Machado
         - Performance optimization
       - Pradyun S. Gedam
         - Conditions and variable names changed
         - Reformatted tests and moved to separate file
         - Made into a PyPI Package
    """
    tokenizer = re.compile('"|(/\*)|(\*/)|(//)|\n|\r')
    end_slashes_re = re.compile(r'(\\)*$')

    in_string = False
    in_multi = False
    in_single = False

    new_str = []
    index = 0

    for match in re.finditer(tokenizer, string):

        if not (in_multi or in_single):
            tmp = string[index:match.start()]
            if not in_string and strip_space:
                # replace white space as defined in standard
                tmp = re.sub('[ \t\n\r]+', '', tmp)
            new_str.append(tmp)
        elif not strip_space:
            # Replace comments with white space so that the JSON parser reports
            # the correct column numbers on parsing errors.
            new_str.append(' ' * (match.start() - index))

        index = match.end()
        val = match.group()

        if val == '"' and not (in_multi or in_single):
            escaped = end_slashes_re.search(string, 0, match.start())

            # start of string or unescaped quote character to end string
            if not in_string or (escaped is None or len(escaped.group()) % 2 == 0):  # noqa
                in_string = not in_string
            index -= 1  # include " character in next catch
        elif not (in_string or in_multi or in_single):
            if val == '/*':
                in_multi = True
            elif val == '//':
                in_single = True
        elif val == '*/' and in_multi and not (in_string or in_single):
            in_multi = False
            if not strip_space:
                new_str.append(' ' * len(val))
        elif val in '\r\n' and not (in_multi or in_string) and in_single:
            in_single = False
        elif not ((in_multi or in_single) or (val in ' \r\n\t' and strip_space)):  # noqa
            new_str.append(val)

        if not strip_space:
            if val in '\r\n':
                new_str.append(val)
            elif in_multi or in_single:
                new_str.append(' ' * len(val))

    new_str.append(string[index:])
    return ''.join(new_str)




def fastjsonminify(s):
    """https://gist.github.com/WizKid/1170297

    Claimed to run faster than jsonminify above:
    https://stackoverflow.com/questions/244777/can-comments-be-used-in-json
    """
    inCommentSingle = False
    inCommentMulti = False
    inString = False

    t = []
    l = len(s)

    i = 0
    fromIndex = 0
    while i < l:
        c = s[i]

        if not inCommentMulti and not inCommentSingle:
            if c == '"':
                slashes = 0
                for j in range(i - 1, 0, -1):
                    if s[j] != '\\':
                        break

                    slashes += 1

                if slashes % 2 == 0:
                    inString = not inString

            elif not inString:
                if c == '#':
                    inCommentSingle = True
                    t.append(s[fromIndex:i])
                elif c == '/' and i + 1 < l:
                    cn = s[i + 1]
                    if cn == '/':
                        inCommentSingle = True
                        t.append(s[fromIndex:i])
                        i += 1
                    elif cn == '*':
                        inCommentMulti = True
                        t.append(s[fromIndex:i])
                        i += 1

        elif inCommentSingle and (c == '\n' or c == '\r'):
            inCommentSingle = False
            fromIndex = i

        elif inCommentMulti and c == '*' and i + 1 < l and s[i + 1] == '/':
            inCommentMulti = False
            i += 1
            fromIndex = i + 1

        i += 1

    if not inCommentSingle and not inCommentMulti:
        t.append(s[fromIndex:len(s)])

    return "".join(t)
