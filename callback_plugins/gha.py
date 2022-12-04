from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
  callback: gha
  type: stdout
  short_description: Group role/play output in Github Actions
  version_added: 0.1.0
  description:
    - A default callback wrapper for improving the reading experience of Ansible logs in Github ACtions output.
  author: Steffen Poulsen (@raunow)
  extends_documentation_fragment:
    - default_callback
  notes:
    - Enable plugin by defining the CI environment variable, it is defined by default in Github Actions
  seealso:
    - name: default – default Ansible screen output
      description: The official documentation on the B(default) callback plugin.
      link: https://docs.ansible.com/ansible/latest/plugins/callback/default.html
  requirements:
    - Configure `stdout_callback` in ansible.cfg
  options:
    group_per_play:
      description: Group Plays instead of roles.
      ini:
        - section: callback_gha
          key: group_per_play
      env:
        - name: ANSIBLE_CALLBACK_GHA_GROUP_PER_PLAY
      type: bool
    disabled:
      description: Disable plugin.
      env:
        - name: ANSIBLE_CALLBACK_GHA_DISABLED
      type: bool
'''

import os
from ansible.plugins.callback.default import CallbackModule as Default

class CallbackModule(Default):
    '''
    Wrap output in Github Actions groups
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'gha'

    def _display_end_group(self):
        if self.print_end_group:
            self._display.display('::endgroup::')
            self.print_end_group = False

    def _display_group(self, title):
        if self.print_group:
            self._display.display(("::group::%s" % (title)))
            self.print_end_group = True
    
    def __init__(self):
        self.print_group = ('CI' in os.environ and 'ANSIBLE_CALLBACK_GHA_DISABLED' not in os.environ)
        self.print_end_group = False
        self.last_role = ""
        super(CallbackModule, self).__init__()

    def v2_playbook_on_play_start(self, play):
        self._display_end_group()
        if self.get_option("group_per_play"):
            self._display_group("PLAY [%s]" % (play.name))
        super(CallbackModule, self).v2_playbook_on_play_start(play)

    def v2_playbook_on_task_start(self, task, is_conditional):
        if not self.get_option("group_per_play"):
            role_name = task._role.get_name(include_role_fqcn=True) if task._role else ""

            if self.last_role != role_name:
                if self.last_role != "":
                    self._display_end_group()

                if role_name != "":
                    self._display_group("ROLE [%s]" % (role_name))

                self.last_role = role_name
        super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_stats(self, stats):
        self._display_end_group()
        super(CallbackModule, self).v2_playbook_on_stats(stats)
