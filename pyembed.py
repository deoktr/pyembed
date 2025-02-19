#!/usr/bin/env python3

import argparse
import logging
import sys


__version__ = "1.0.0"


def gen_python(input):
    out = ""

    for line in input.readlines():
        # skip comments
        if line.strip().startswith("#"):
            continue

        line = repr(line)

        # we want only double quotes for C source
        if not line.startswith('"'):
            line = line.replace('"', '\\"')
        line = line.replace("'", '"')
        out += line + "\n"

    return out


def gen(input):
    out = (
        """
#define PY_SSIZE_T_CLEAN
#include <python3.12/Python.h>

int main(int argc, char *argv[]) {
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\\n");
        exit(1);
    }
    Py_Initialize();

    PyRun_SimpleString(
"""
        + gen_python(input)
        + """
);

    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    PyMem_RawFree(program);
    return 0;
}
"""
    )
    return out


def _handle(args):
    if args.version:
        print(__version__)
        return 0

    out = gen(args.input)

    args.output.write(out)
    return 0


def _cli() -> int:
    parser = argparse.ArgumentParser(
        prog="pyembed",
        description="%(prog)s python C embed generator",
    )
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "input",
        nargs="?",  # required to be able to pipe to stdin
        help="input file",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )

    args = parser.parse_args()

    try:
        return _handle(args)
    except Exception as e:
        logging.error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(_cli())
