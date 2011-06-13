from distutils.core import setup
import py2exe

setup(version = "0.1", name = "RCI", author = "Andre Simoes",data_files=[("rci.py")], console = ["rci.py"]  )

