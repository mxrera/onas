#! /usr/bin/python3

from onas import JPEG
from docopt import docopt
import sys

if __name__ == "__main__":
    usage = f"""
    Compress images using JPEG algorithm.

    Usage:
        {sys.argv[0]} compress [options] <input> <output>
        {sys.argv[0]} (-h | --help)
        {sys.argv[0]} --version
    
    Options:
        -h --help     Show this screen.
        --version     Show version.
        --factor=<f>  Compression factor [default: 1].
    """
    args = docopt(usage, help=True, version="0.1")

    configuration = {
        "Quantization Factor": float(args["--factor"]),
    }
    jpeg = JPEG()
    jpeg.configure(**configuration)
    jpeg(args["<input>"], args["<output>"])
