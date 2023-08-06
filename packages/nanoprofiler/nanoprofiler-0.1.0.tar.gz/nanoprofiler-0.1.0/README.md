[![Code: GPL v3](https://img.shields.io/badge/Code-GPLv3-green.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![Documentation: CC BY-SA 4.0](https://img.shields.io/badge/Documentation-CC%20BY--SA%204.0-blue.svg?style=flat-square)](https://creativecommons.org/licenses/by-sa/4.0/) [![Release: v0.1.0](https://img.shields.io/static/v1?label=Release&message=v0.1.0&color=7E4798&style=flat-square)](https://gitlab.com/nanogennari/nanoprofiler/-/tree/master)

A small python profiler using cProfile, pstats, Pandas and matplotlib.

## Instalation

Clone the repository

    https://gitlab.com/nanogennari/nanoprofiler.git

Install setuptools (if not installed)

    sudo apt install python-setuptools

And run sertup script

    cd nanoprofiler
    python setup.py install

## Usage

Usage example

    from nanoprofiler import Profiler

    pr = Profiler()

    pr.start(name="exec1")
    your_code()
    pr.stop()

    pr.start(name="exec2")
    another_code()
    pr.stop()

    pr.plot_top_time(time="cumtime")
    pr.plot_function(time="tottime")
    pr.save_data("folder/to/save/results")