from distutils.core import setup
import py2exe

setup(console = [{'script': "mainReport.py"}], options={"py2exe":{"includes":["sip"], 'bundle_files': 1, 'compressed': True}})