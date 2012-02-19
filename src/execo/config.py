# Copyright 2009-2012 INRIA Rhone-Alpes, Service Experimentation et
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

import logging
import os
import sys

# _STARTOF_ configuration
configuration = {
    'log_level': logging.WARNING,
    'compact_output_threshold': 4096,
    'kill_timeout': 5,
    'color_mode': os.isatty(sys.stdout.fileno())
                  and os.isatty(sys.stderr.fileno()),
    'style_log_header': ('yellow',),
    'style_log_level' : ('magenta',),
    'style_object_repr': ('blue', 'bold'),
    'style_emph': ('magenta', 'bold'),
    'style_report_warn': ('magenta',),
    'style_report_error': ('red', 'bold'),
    }
# _ENDOF_ configuration
"""Global execo configuration parameters.

- ``log_level``: the log level (see module `logging`)

- ``compact_output_threshold``: only beginning and end of stdout /
  stderr are displayed when their size is greater than this
  threshold. 0 for no threshold

- ``kill_timeout``: number of seconds to wait after a clean SIGTERM
  kill before assuming that the process is not responsive and killing
  it with SIGKILL

- ``color_mode``: whether to colorize output (with ansi escape
  sequences)

- ``style_log_header``, ``style_log_level``, ``style_object_repr``,
  ``style_emph``, ``style_report_warn``, ``style_report_error``:
  iterables of ansi attributes identifiers (those found in
  `execo.log._ansi_styles`)

"""

# _STARTOF_ default_connexion_params
default_connexion_params = {
    'user':        None,
    'keyfile':     None,
    'port':        None,
    'ssh':         'ssh',
    'scp':         'scp',
    'taktuk':      'taktuk',
    'ssh_options': ( '-tt',
                     '-o', 'BatchMode=yes',
                     '-o', 'PasswordAuthentication=no',
                     '-o', 'StrictHostKeyChecking=no',
                     '-o', 'UserKnownHostsFile=/dev/null',
                     '-o', 'ConnectTimeout=20' ),
    'scp_options': ( '-o', 'BatchMode=yes',
                     '-o', 'PasswordAuthentication=no',
                     '-o', 'StrictHostKeyChecking=no',
                     '-o', 'UserKnownHostsFile=/dev/null',
                     '-o', 'ConnectTimeout=20',
                     '-rp' ),
    'taktuk_options': ( '-s', ),
    'taktuk_connector': 'ssh',
    'taktuk_connector_options': ( '-o', 'BatchMode=yes',
                                  '-o', 'PasswordAuthentication=no',
                                  '-o', 'StrictHostKeyChecking=no',
                                  '-o', 'UserKnownHostsFile=/dev/null',
                                  '-o', 'ConnectTimeout=20'),
    'ssh_scp_pty': False,
    'host_rewrite_func': lambda host: host
    }
# _ENDOF_ default_connexion_params
"""Default connexion params for ``ssh``/``scp``/``taktuk`` connexions.

- ``user``: the user to connect with.

- ``keyfile``: the keyfile to connect with.

- ``port``: the port to connect to.

- ``ssh``: the ssh or ssh-like command.

- ``scp``: the scp or scp-like command.

- ``taktuk``: the taktuk command.

- ``ssh_options``: options passed to ssh.

- ``scp_options``: options passed to scp.

- ``taktuk_options``: options passed to taktuk.

- ``taktuk_connector``: the ssh-like connector command for taktuk.

- ``taktuk_connector_options``: options passed to taktuk_connector.

- ``ssh_scp_pty``: allocate a pty for ssh/scp.

- ``host_rewrite_func``: function called to rewrite hosts addresses.
"""

default_default_connexion_params = default_connexion_params.copy()
"""An initial backup copy of `execo.config.default_default_connexion_params`

If needed, after modifying default_connexion_params, the ssh/scp
defaults are still available in default_default_connexion_params.
"""

def load_configuration(filename, dicts_confs):
    """Update dicts with those found in file.

    :param file: file to load dicts from
    
    :param dicts_confs: an iterable of couples (dict, string)

    Used to read configuration dicts. For each couple (dict, string),
    if a dict named string is defined in <file>, update
    dict with the content of this dict. Does nothing if unable to open
    <file>.
    """
    jailed_globals = {}
    try:
        execfile(filename, jailed_globals)
    except Exception: #IGNORE:W0703
        pass
    for (dictio, conf) in dicts_confs:
        if jailed_globals.has_key(conf):
            dictio.update(jailed_globals[conf])

def get_user_config_filename():
    _user_conf_file = None
    if os.environ.has_key('HOME'):
        _user_conf_file = os.environ['HOME'] + '/.execo.conf.py'
    return _user_conf_file
    
load_configuration(
  get_user_config_filename(),
  ((configuration, 'configuration'),
   (default_connexion_params, 'default_connexion_params')))
