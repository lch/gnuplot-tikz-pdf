import sys
from pathlib import Path

from .gnuplot import draw_script


def main():
	argv_len = len(sys.argv)
	sp = Path(sys.argv[0])

	if argv_len == 3:
		draw_script(sys.argv[1], sys.argv[2])
	elif argv_len == 2:
		draw_script(sys.argv[1])
	else:
		print(f'usage: {sp.name} [gnuplot script] ([output filename or path])')
		sys.exit(1)


if __name__ == '__main__':
	main()
