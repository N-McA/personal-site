---
title: "No commits on prod"
date: 2019-02-01
draft: false
math: true
tags: ["#git"]
---

I have a couple of small web projects, and have recently taken to hosting them with [netlify](www.netlify.com). It's free, awesome for static sites, and connects to github for continuous deployment.

My usual workflow is to develop on `master` and then rebase `master` onto a branch `prod` for deployment. Yet I'd frequently find that I'd accidentally commit onto `prod` locally, and then have to untangle things later (even though my shell tells me what branch I'm on!).

On github, you can manage this sort of thing with a protected branch, but that's not very portable (and probably overkill). Instead, I use git-hooks to ensure that I get a friendly reminder whenever I accidentally try to commit on `prod`. 

```python
# ./hooks/no-commits-on-prod.py
#!/usr/bin/env python3

import subprocess
import shlex


def run(cmd, ignore_fail=False):
    check = not ignore_fail
    return subprocess.run(
        shlex.split(cmd), check=check, stdout=subprocess.PIPE
    ).stdout.decode("UTF-8")


if __name__ == '__main__':
    branch_name = run("git rev-parse --abbrev-ref HEAD").strip()

    if branch_name == 'prod':
        raise ValueError('Do not commit on prod, rebase from master instead.')
```

Because hooks allow for arbitrary code execution after git commands are run, they're not included in the working tree. Thus I have a second script to make it easy to install hooks on a new machine (which has been re-used between a lot of projects)

```python
# ./install-hooks.py
#!/usr/bin/env python3

import subprocess
import shlex
import os


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
```

I like this approach because it's simple, and if I need to scramble to fix anything ugly it's always possible to delete the local hook and re-enable commits on `prod`.

If you've got any opinions on how this should be done, feel free to comment on the [github gist](https://gist.github.com/N-McA/dfa5e9b4caa06706393c4ce284963855).