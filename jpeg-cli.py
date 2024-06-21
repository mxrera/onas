#! /usr/bin/python3

import sys
from onas import JPEG
from docopt import docopt
import matplotlib.pyplot as plt

if __name__ == "__main__":
    usage = f"""
    Compress images using JPEG algorithm.

    Usage:
        {sys.argv[0]} show [options] <input>
        {sys.argv[0]} compress [options] <input> <output>
        {sys.argv[0]} (-h | --help)
        {sys.argv[0]} --version
    
    Options:
        -h --help             Show this screen.
        --version             Show version.
        -k <k>, --factor=<k>  Compression factor [default: 1].
    """
    args = docopt(usage, help=True, version="0.1")

    configuration = {
        "Quantization Factor": float(args["--factor"]),
    }
    jpeg = JPEG()
    jpeg.configure(**configuration)

    if args["show"]:
        image = jpeg(args["<input>"])
        plt.imshow(image, cmap="gray")
        plt.axis("off")
        plt.show()
    elif args["compress"]:
        jpeg(args["<input>"], args["<output>"])
