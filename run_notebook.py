#!/usr/bin/env python

import os
import sys

import os
import subprocess
import tempfile

import nbformat

kernel_name = os.environ.get("JUPYTER_KERNEL_NAME", "vor")

def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=-1",
                "--ExecutePreprocessor.kernel_name={}".format(kernel_name),
                "--output", fout.name, path]
        subprocess.check_call(args)
        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]
              if output.output_type == "error"]

    return nb, errors

if __name__ == '__main__':
    _notebook_run('./analysis-ca-covid19-v1.ipynb')
