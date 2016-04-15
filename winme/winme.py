#!/usr/bin/python3

ERR_OK = 0
ERR_UNKNOWN_METHOD = 1
ERR_CHECKER_ERROR = 2
ERR_WRONG_ANSWER = 3

TASK_ID = "winme"
TASK_SCORE = 1
TASK_NAME = "Win me!"

TASK_HTML_EN_PATTERN = "Try to win this <a href=/static/winme.exe>game</a> and you'll get the flag!"

TASK_HTML_RU_PATTERN = "Попробуйте выиграть в эту<a href=/static/winme.exe>игру</a> и получите флаг!"

import hashlib
import sys
import datetime

def create_task(dump_dir, user_id):
	task = \
		"ID: " + user_id + "\n" + \
		"html[en]: " + TASK_HTML_EN_PATTERN + "\n" + \
		"html[ru]: " + TASK_HTML_RU_PATTERN + "\n"
	sys.stdout.write(task);

def check_answer(dump_dir, user_id, answer):
	try:
		jury_answer_bytes = "".join(user_id, "winme.exe", "Saturday").encode("utf-8")
		jury_answer = md5.new(jury_answer).hexdigest()
		if jury_answer.lower() != answer.lower():
			sys.stderr.write("Wrong answer, expected {0} got {1}\n".format(jury_answer, answer))
			sys.exit(ERR_WRONG_ANSWER)
		sys.exit(ERR_OK)
	except Exception as e:
		sys.stderr.write("Exception during checking answer: {0}\n".format(e))
		sys.exit(ERR_WRONG_ANSWER)


if __name__ == "__main__":
	method = sys.argv[1]

	if method == "id":
		sys.stdout.write("{0}:{1}\n".format(TASK_ID, TASK_SCORE))
	elif method == "series":
		sys.stdout.write("{0}\n".format(TASK_ID))
	elif method == "name":
		sys.stdout.write("{0}\n".format(TASK_NAME))
	elif method == "create":
		create_task(sys.argv[2], sys.argv[3])
	elif method == "user":
		check_answer(sys.argv[2], sys.argv[3], input())
	else:
		sys.stderr.write("Invalid method: {0}".format(method))
		exit(ERR_UNKNOWN_METHOD)