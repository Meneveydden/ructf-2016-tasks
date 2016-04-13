#!/usr/bin/env python3

import os
import os.path
import random
import subprocess
import sys
import tempfile

from taskutils import BaseTask


ABC = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'

def classify(text):
    if not text.startswith('RUCTF'):
        return None

    text = text[len('RUCTF'):]
    if len(text) != 8:
        return None

    vector = [ABC.find(ch) for ch in text]
    if -1 in vector:
        return None

    text = "0 {}".format(' '.join("{}:{}".format(i + 1, v)
                                  for (i, v) in enumerate(vector)))

    (_, fn1) = tempfile.mkstemp()
    (_, fn2) = tempfile.mkstemp()
    with open(fn1, 'w') as f:
        print(text, file=f)

    try:
        subprocess.check_output(["svm-predict", fn1, "model", fn2])
    except Exception:
        return None

    try:
        with open(fn2) as f:
            return f.read().strip()
    finally:
        os.unlink(fn1)
        os.unlink(fn2)


class Task(BaseTask.create(
    NAME='classify', CATEGORY='ppc', SCORE=50, DB_FILE='flags.db',
    TASK_FILE=os.path.join(
        'static', 'ab83919b22c9a05b9ccb297efff3ecd5', 'task.tgz'),
    HTML_EN='Find vector for {} class',
    HTML_RU='Найдите вектор для класса {}')):

    @BaseTask.cmd("create")
    def cmd_create(self, dump_dir, team_id):
        klass = str(random.randint(1, 10))

        os.makedirs(dump_dir, exist_ok=True)
        quid = self.store_flag(os.path.join(dump_dir, Task.DB_FILE), klass)

        print("ID:{}".format(quid))
        print("html[en]:{}".format(Task.HTML_EN.format(klass)))
        print("html[ru]:{}".format(Task.HTML_RU.format(klass)))
        print("file:{}".format(Task.TASK_FILE))

    @BaseTask.cmd("user")
    def cmd_user(self, dump_dir, quid):
        answer = sys.stdin.readline().strip()
        flag = classify(answer)
        if flag is None:
            print('Wrong')
            return 1

        code = Task.check_task(dump_dir, quid, flag)
        return (0 if code else 1)


def main(args):
    sys.stdout = open(1, 'w', encoding='utf-8', closefd=True)
    return Task().run(*args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
