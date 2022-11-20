from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
  callback: gha
  type: stdout
  short_description: Wrap roles with ::group::role_name and ::endgroup
  version_added: 0.1.0
  description:
    - A default callback wrapper for improving the log reading experience of plays in Github Workflows.
  author: Steffen Poulsen (@raunow)
  extends_documentation_fragment:
    - default_callback
  notes:
    - Enable plugin by defining the CI environment variable, it is defined by default in Github Workflows
  seealso:
    - name: default – default Ansible screen output
      description: The official documentation on the B(default) callback plugin.
      link: https://docs.ansible.com/ansible/latest/plugins/callback/default.html
  requirements:
    - set as stdout_callback in configuration
  options:
    group_per_play:
      description: Group Plays instead of roles.
      ini:
        - section: callback_gha
          key: group_per_play
      vars:
        - name: ansible_callback_diy_on_any_msg
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
        self._display.display('::endgroup::')

    def _display_group(self, title):
        self._display.display(("::group::%s" % (title)))
    
    def __init__(self):
        self.print_group = ('CI' in os.environ)
        self.print_end_group = False
        self.last_role = ""
        super(CallbackModule, self).__init__()

    def v2_playbook_on_play_start(self, play):
        if self.print_end_group:
            self._display_end_group()
            self.print_end_group = False
            
        if self.get_option("group_per_play"):
            if self.print_group:
                self.print_end_group = True
                self._display_group("PLAY [%s]" % (play.name))

        super(CallbackModule, self).v2_playbook_on_play_start(play)

    def v2_playbook_on_task_start(self, task, is_conditional):
        if not self.get_option("group_per_play"):
            role_name = task._role.get_name(include_role_fqcn=True) if task._role else ""

            if self.last_role != role_name:
                if self.last_role != "" and self.print_end_group:
                    self._display_end_group()
                    self.print_end_group = False

                if self.print_group and role_name != "":
                    self._display_group("ROLE [%s]" % (role_name))
                    self.print_end_group = True
                self.last_role = role_name

        super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_stats(self, stats):
        if self.print_end_group:
            self._display_end_group()
        super(CallbackModule, self).v2_playbook_on_stats(stats)
