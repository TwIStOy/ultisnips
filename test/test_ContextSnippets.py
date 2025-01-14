from test.constant import *
from test.vim_test_case import VimTestCase as _VimTest


class ContextSnippets_SimpleSnippet(_VimTest):
    files = {
        "us/all.snippets": r"""
        snippet a "desc" "True" e
        abc
        endsnippet
        """
    }
    keys = "a" + EX
    wanted = "abc"


class ContextSnippets_ExpandOnTrue(_VimTest):
    files = {
        "us/all.snippets": r"""
        global !p
        def check_context():
            return True
        endglobal

        snippet a "desc" "check_context()" e
        abc
        endsnippet
        """
    }
    keys = "a" + EX
    wanted = "abc"


class ContextSnippets_DoNotExpandOnFalse(_VimTest):
    files = {
        "us/all.snippets": r"""
        global !p
        def check_context():
            return False
        endglobal

        snippet a "desc" "check_context()" e
        abc
        endsnippet
        """
    }
    keys = "a" + EX
    wanted = keys


class ContextSnippets_Before(_VimTest):
    files = {
        "us/all.snippets": r"""
        context "len(snip.before) >= 5 and snip.before"
        snippet dup "desc" i
        [`!p snip.rv = snip.context[:-3]`]
        endsnippet
        """
    }
    word = 'Süßölgefäß'
    keys = "adup" + EX + '\n' + word + 'dup' + EX
    wanted = "adup" + EX + '\n' + word +'[' + word + ']'


class ContextSnippets_UseContext(_VimTest):
    files = {
        "us/all.snippets": r"""
        global !p
        def wrap(ins):
            return "< " + ins + " >"
        endglobal

        snippet a "desc" "wrap(snip.buffer[snip.line])" e
        { `!p snip.rv = context` }
        endsnippet
        """
    }
    keys = "a" + EX
    wanted = "{ < a > }"


class ContextSnippets_SnippetPriority(_VimTest):
    files = {
        "us/all.snippets": r"""
        snippet i "desc" "regex.search('err :=', snip.buffer[snip.line-1])" e
        if err != nil {
            ${1:// pass}
        }
        endsnippet

        snippet i
        if ${1:true} {
            ${2:// pass}
        }
        endsnippet
        """
    }

    keys = (
        r"""
        err := some_call()
        i"""
        + EX
        + JF
        + """
        i"""
        + EX
    )
    wanted = r"""
        err := some_call()
        if err != nil {
            // pass
        }
        if true {
            // pass
        }"""


class ContextSnippets_PriorityKeyword(_VimTest):
    files = {
        "us/all.snippets": r"""
        snippet i "desc" "True" e
        a
        endsnippet

        priority 100
        snippet i
        b
        endsnippet
        """
    }

    keys = "i" + EX
    wanted = "b"


class ContextSnippets_ReportError(_VimTest):
    files = {
        "us/all.snippets": r"""
        snippet e "desc" "Tru" e
        error
        endsnippet
        """
    }

    keys = "e" + EX
    wanted = "e" + EX
    expected_error = r"NameError: name 'Tru' is not defined"


class ContextSnippets_ReportErrorOnIndexOutOfRange(_VimTest):
    # Working around: https://github.com/neovim/python-client/issues/128.
    skip_if = lambda self: "Bug in Neovim." if self.vim_flavor == "neovim" else None
    files = {
        "us/all.snippets": r"""
        snippet e "desc" "snip.buffer[123]" e
        error
        endsnippet
        """
    }

    keys = "e" + EX
    wanted = "e" + EX
    expected_error = r"IndexError: line number out of range"


class ContextSnippets_CursorIsZeroBased(_VimTest):
    files = {
        "us/all.snippets": r"""
        snippet e "desc" "snip.cursor" e
        `!p snip.rv = str(snip.context)`
        endsnippet
        """
    }

    keys = "e" + EX
    wanted = "(2, 1)"


class ContextSnippets_ContextIsClearedBeforeExpand(_VimTest):
    files = {
        "us/all.snippets": r"""
        pre_expand "snip.context = 1 if snip.context is None else 2"
        snippet e "desc" w
        `!p snip.rv = str(snip.context)`
        endsnippet
        """
    }

    keys = "e" + EX + " " + "e" + EX
    wanted = "1 1"


class ContextSnippets_ContextHasAccessToVisual(_VimTest):
    files = {
        "us/all.snippets": r"""
        snippet test "desc" "snip.visual_text == '123'" we
        Yes
        endsnippet

        snippet test "desc" w
        No
        endsnippet
        """
    }

    keys = (
        "123" + ESC + "vhh" + EX + "test" + EX + " zzz" + ESC + "vhh" + EX + "test" + EX
    )
    wanted = "Yes No"


class ContextSnippets_Header_ExpandOnTrue(_VimTest):
    files = {
        "us/all.snippets": r"""
        global !p
        def check_context():
            return True
        endglobal

        context "check_context()"
        snippet a "desc" e
        abc
        endsnippet
        """
    }
    keys = "a" + EX
    wanted = "abc"


class ContextSnippets_Header_DoNotExpandOnFalse(_VimTest):
    files = {
        "us/all.snippets": r"""
        global !p
        def check_context():
            return False
        endglobal

        context "check_context()"
        snippet a "desc" e
        abc
        endsnippet
        """
    }
    keys = "a" + EX
    wanted = keys


class ContextSnippets_ContextHasAccessToReMatch(_VimTest):
    files = {
        "us/all.snippets": r"""
        context "match.group(1) != 'no'"
        snippet "(\w*) xxx" "desc" r
        HERE
        endsnippet
        """
    }
    negative = "no xxx"
    positive = "yes xxx"
    keys = negative + EX + positive + EX
    wanted = negative + EX + "HERE"
