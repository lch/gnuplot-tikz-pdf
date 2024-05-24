import gnuplot_tikz_pdf
import sys
from pathlib import Path


def main():
	argv_len = len(sys.argv)
	sp = Path(sys.argv[0])

	if argv_len == 3:
		gnuplot_tikz_pdf.draw_script(sys.argv[1], sys.argv[2])
	elif argv_len == 2:
		gnuplot_tikz_pdf.draw_script(sys.argv[1])
	else:
		print(f'usage: {sp.name} [gnuplot script] ([output filename or path])')
		sys.exit(1)


if __name__ == '__main__':
	main()
