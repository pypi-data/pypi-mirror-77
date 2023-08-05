#!/usr/bin/env python


import argparse
import io
import logging

import ply.lex

logger = logging.getLogger(__name__)


# Usage
# python stripcomments.py input.tex > output.tex
# python stripcomments.py input.tex -e encoding > output.tex

def strip_comments(source, extremely_verbose=False):
    tokens = (
        'PERCENT', 'BEGINCOMMENT', 'ENDCOMMENT', 'BACKSLASH',
        'CHAR', 'BEGINVERBATIM', 'ENDVERBATIM', 'NEWLINE', 'ESCPCT',
    )
    states = (
        ('linecomment', 'exclusive'),
        ('commentenv', 'exclusive'),
        ('verbatim', 'exclusive')
    )

    # Deal with escaped backslashes, so we don't think they're escaping %.
    def t_BACKSLASH(t):
        r"\\\\"
        logger.debug('in backslash {}'.format(t))
        return t

    # One-line comments
    def t_PERCENT(t):
        r"\%"
        t.lexer.begin("linecomment")
        logger.debug('in linecomment {}. removing.'.format(t))
        # keep the % sign for clarity
        return t

    # Escaped percent signs
    def t_ESCPCT(t):
        r"\\\%"
        return t

    # Comment environment, as defined by verbatim package
    def t_BEGINCOMMENT(t):
        r"\\begin\s*{\s*comment\s*}"
        logger.debug('entering a comment environment at line {}'.format(t.lexer.lineno))
        t.lexer.begin("commentenv")

    # Verbatim environment (different treatment of comments within)
    def t_BEGINVERBATIM(t):
        r"\\begin\s*{\s*verbatim\s*}"
        t.lexer.begin("verbatim")
        return t

    # Any other character in initial state we leave alone
    def t_CHAR(t):
        r"."
        logger.debug('in CHAR {}. keeping.'.format(t))
        return t

    def t_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        logger.debug('in NEWLINE {}. keeping.'.format(t))
        return t

    def t_error(t):
        logger.critical("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # End comment environment
    def t_commentenv_ENDCOMMENT(t):
        r"\\end\s*{\s*comment\s*}"
        # Anything after \end{comment} on a line is ignored!
        t.lexer.begin('linecomment')

    # Ignore comments of comment environment
    def t_commentenv_CHAR(t):
        r"."
        pass

    def t_commentenv_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_commentenv_error(t):
        logger.critical("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # End of verbatim environment
    def t_verbatim_ENDVERBATIM(t):
        r"\\end\s*{\s*verbatim\s*}"
        t.lexer.begin('INITIAL')
        return t

    # Leave contents of verbatim environment alone
    def t_verbatim_CHAR(t):
        r"."
        return t

    def t_verbatim_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    def t_verbatim_error(t):
        logger.critical("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # End a % comment when we get to a new line
    def t_linecomment_ENDCOMMENT(t):
        r"\n"
        t.lexer.lineno += len(t.value)
        t.lexer.begin("INITIAL")
        logger.debug('in linecomment::NEWLINE {}. keeping.'.format(t))
        # keep the newline at the end of a line comment to handle tests/linecomment.txt correctly
        return t

    # Ignore anything after a % on a line
    def t_linecomment_CHAR(t):
        r"."
        if extremely_verbose:
            logger.debug('in linecomment CHAR {}'.format(t))

    def t_linecomment_error(t):
        logger.critical("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    lexer = ply.lex.lex()
    lexer.input(source)

    return u"".join([tok.value for tok in lexer])


def strip_comments_from_files(infile, outfile):
    with io.open(infile, encoding='utf-8') as f:
        source = f.read()

    with io.open(outfile, mode='w', encoding='utf-8') as f:
        f.write(strip_comments(source))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the file to strip comments from')
    parser.add_argument('--encoding', '-e', default='utf-8')
    parser.add_argument('--output', '-o', default=None)
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    with io.open(args.filename, encoding=args.encoding) as f:
        source = f.read()

    stripped = strip_comments(source)
    if args.output:
        with io.open(args.output, mode='w', encoding=args.encoding) as f:
            f.write(stripped)
    else:
        import sys

        sys.stdout.write(stripped)
