#!/bin/sh

# Have yet to look into Ansible tests
set -x
ansible-playbook main.yml
CI=1 ansible-playbook main.yml
CI=1 ANSIBLE_CALLBACK_GHA_GROUP_PER_PLAY=True ansible-playbook main.yml
CI=1 ANSIBLE_CALLBACK_GHA_DISABLED=1 ansible-playbook main.yml
