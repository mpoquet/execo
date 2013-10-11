# Copyright 2009-2013 INRIA Rhone-Alpes, Service Experimentation et
# Developpement
#
# This file is part of Execo.
#
# Execo is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Execo is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Execo.  If not, see <http://www.gnu.org/licenses/>

from config import configuration
import pipes, subprocess, os

def comma_join(*args):
    return ", ".join([ arg for arg in args if len(arg) > 0 ])

def compact_output(s):
    thresh = configuration.get('compact_output_threshold')
    if thresh == 0 or len(s) <= thresh: return s
    return s[:thresh/2] + "\n[...]\n" + s[(thresh/2)-thresh:]

def nice_cmdline(cmdline):
    if hasattr(cmdline, '__iter__'):
        return " ".join([ pipes.quote(arg) for arg in cmdline ])
    else:
        return cmdline

def find_files(*args):
    """run find utility with given path(es) and parameters, return the result as a list"""
    find_args = "find " + " ".join([pipes.quote(arg) for arg in args])
    p = subprocess.Popen(find_args, shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    p.wait()
    return [ p for p in stdout.split("\n") if p ]

def which(name):
    """return full path of executable on the $PATH"""
    p = subprocess.Popen("which " + name, shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    p.wait()
    stdout = stdout.rstrip()
    if len(stdout) > 0:
        return stdout
    else:
        return None

def find_exe(name):
    """search an executable in whole execo directory. If not found, get it on the $PATH."""
    path = None
    for exe_path in find_files(os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "..", ".."), "-name", name):
        path = exe_path
        break
    if not path:
        path = which(name)
    return path
