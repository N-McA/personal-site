#!/usr/bin/env python3

import subprocess
import shlex


def run(cmd):
    return subprocess.run(
        shlex.split(cmd), check=True, stdout=subprocess.PIPE
    ).stdout.decode("UTF-8")


branch_name = run("git rev-parse --abbrev-ref HEAD").strip()

if branch_name == 'prod':
    raise ValueError('Do not commit on prod, rebase from master instead.')
