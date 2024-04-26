#!/bin/python3
from sys import argv
from os import path, listdir, system
from subprocess import run


def post(mes):
	print('=={}=='.format(mes.upper()))


def getLast(ext):
	n = len(ext)
	files = filter(path.isfile, listdir())
	files = filter(lambda x: x[-n:] == ext and x != 'make.py', files)
	files = sorted(files, key=lambda x: path.getmtime(x), reverse=True)
	if not files:
		post('directory is empty')
		exit()
	return files[0]


def algo(*par):
	if 'a' in par:
		tar = getLast('.out')
		post('running')
		print()
		system('./{}'.format(tar))
		return

	if 'p' in par:
		tar = getLast('.py')
		post('running')
		print()
		system('pypy3 "{}"'.format(tar))
		return

	debug = '-std=c++17 -Wall -Wextra -Wshadow -g -fsanitize=address -fsanitize=undefined -D_GLIBCXX_DEBUG'
	com = ['g++']
	
	if 'd' in par:
		com.extend(debug.split())

	tar = getLast('.cpp')
	com.append(tar)
	print(' '.join(com))
	make = run(com)
	if make.returncode:
		post('error during compilation')
		return
	post('compilation complete')

	if 'r' in par:
		post('running')
		print()
		system('./a.out')


if __name__ == '__main__':
	algo(*argv[1:])
