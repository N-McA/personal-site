#!/usr/bin/env python3

import subprocess
import shlex
import os
from pathlib import Path


def chdir_to_script_location():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def run(cmd, ignore_fail=False):
    check = not ignore_fail
    return subprocess.run(
        shlex.split(cmd), check=check, stdout=subprocess.PIPE
    ).stdout.decode("UTF-8")


def link_hook(file, hook_name):
  run('rm ./.git/hooks/{}'.format(hook_name), ignore_fail=True)
  cmd = "ln -s {relpath} .git/hooks/{hook_name}"
  run(cmd.format(
    relpath=os.path.relpath(file, '.git/hooks/'),
    hook_name=hook_name,
  ))


if __name__ == "__main__":
    chdir_to_script_location()
    link_hook('./hooks/no-commits-on-prod.py', 'pre-commit')

