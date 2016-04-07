#!/usr/bin/env python3

import os
import os.path
import random
import sys

from taskutils import BaseTask, md5


class Task(BaseTask.create(
    NAME='damaged', CATEGORY='forensics', SCORE=100, DB_FILE='flags.db',
    FLAGS_FILE='flags.txt', IMAGE_FILE=os.path.join(
        'static', 'a51f3fa3525b6a5c59ea272096a2eee3', 'image.im.bz2'),
    HTML_EN='Flag in the file "{}". Got it',
    HTML_RU='Флаг в файле "{}". Получите его')):

    @classmethod
    def generate_flag(cls):
        with open(cls.FLAGS_FILE) as f:
            flag = random.choice(list(f)).strip()

        return flag.split(':')

    @BaseTask.cmd("create")
    def cmd_create(self, dump_dir, team_id):
        (fn, flag) = Task.generate_flag()
        flag_ = ':'.join((fn, flag))

        os.makedirs(dump_dir, exist_ok=True)
        quid = self.store_flag(os.path.join(dump_dir, Task.DB_FILE), flag_)

        print("ID:{}".format(quid))
        print("html[en]:{}".format(Task.HTML_EN.format(fn)))
        print("html[ru]:{}".format(Task.HTML_RU.format(fn)))
        print("file:{}".format(Task.IMAGE_FILE))

    @BaseTask.cmd("user")
    def cmd_user(self, dump_dir, quid):
        answer = ':' + sys.stdin.readline().strip()
        entry = None

        with open(Task.FLAGS_FILE) as f:
            for line in f:
                if answer in line:
                    entry = line.strip()
                    break

        if entry is None:
            print('Wrong')
            return 1

        return self.check_task(dump_dir, quid, entry)


def main(args):
    sys.stdout = open(1, 'w', encoding='utf-8', closefd=True)
    return Task().run(*args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
