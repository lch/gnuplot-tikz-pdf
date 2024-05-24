from PyGnuplot import gp
import tempfile
import subprocess
import os
import os.path
from pathlib import Path
import shutil


def create_tmp_dir():
	td = tempfile.TemporaryDirectory(prefix='gnuplot-tikz-pdf-')
	print(f'created tmp dir {td.name}')
	return td


def create_tikz(workdir: str):
	tf = tempfile.NamedTemporaryFile(
		suffix='.tikz', dir=workdir, delete=False, delete_on_close=False
	)
	print(f'created tmp tikz file {tf.name}')
	return tf


def gen_deps(tmpdir: str):
	prev_wd = os.getcwd()
	os.chdir(tmpdir)
	script_path = '/usr/share/gnuplot/5.4/lua/gnuplot-tikz.lua'
	if not os.path.isfile(script_path):
		raise FileNotFoundError(f'script not found: {script_path}')
	try:
		subprocess.run(['lua', script_path, 'style'])
	except subprocess.SubprocessError:
		raise RuntimeError
	os.chdir(prev_wd)


def gen_tex(workdir: str, tikzfile: str, output_name: str):
	tex_content = r"""\documentclass[tikz, margin=0]{standalone}
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{gnuplot-lua-tikz}
\begin{document}"""
	tex_content += f'\\input{{{tikzfile}}}\n'
	tex_content += r'\end{document}'
	with open(f'{workdir}/{output_name}.tex', 'w') as f:
		f.write(tex_content)


def gen_pdf(workdir: str, texfile: str):
	prev_wd = os.getcwd()
	os.chdir(workdir)
	tex_filename = texfile.removesuffix('.tex')
	try:
		subprocess.run(['pdflatex', f'{tex_filename}'])
	except subprocess.SubprocessError:
		raise RuntimeError
	if not os.path.isfile(f'{tex_filename}.pdf'):
		raise FileNotFoundError('no result pdf')
	else:
		shutil.move(f'{tex_filename}.pdf', f'{prev_wd}/{tex_filename}.pdf')
	os.chdir(prev_wd)


def draw_script(path: str, output: str = '.'):
	output_path = Path(output)
	output_filename = output_path.stem
	if output_path.stem == '':
		output_filename = 'result'

	td = create_tmp_dir()
	tf = create_tikz(td.name)
	gen_deps(td.name)
	gen_tex(td.name, tf.name, output_filename)

	fig = gp()
	fig.a('set terminal tikz')
	fig.a(f'set output "{tf.name}"')
	fig.a(f'load "{path}"')

	gen_pdf(td.name, output_filename)

	tf.close()
	td.cleanup()
