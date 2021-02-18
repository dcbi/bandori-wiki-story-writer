import argparse
from pathlib import Path

parent_dir = str(Path(__file__).parent.absolute())

parser = argparse.ArgumentParser()

parser.add_argument('-path', help="parent directory of files to read and write, default="+parent_dir, default=parent_dir)
parser.add_argument('-writename', help='name of file to write to, default=transcript', default='transcript')
parser.add_argument('-readname', help='name of file to read from, default=wikicode', default='wikicode')
parser.add_argument('-abbrev', help='turn on using abbreviations of character names', action=store_true)

args = parser.parse_args()

long = {'kasumi': 'kas', 'tae': 'tae', 'rimi': 'rim', 'saaya': 'say', 'arisa': 'ari', 'yukina': 'y', 'sayo': 's', 'lisa': 'l', 'ako': 'a', 'rinko': 'r', 'aya': 'aya', 'hina': 'hin', 'chisato': 'chi', 'maya': 'may', 'eve': 'eve', 'ran': 'ran', 'moca': 'moc', 'himari': 'him', 'tomoe': 'tom', 'tsugumi': 'tsu', 'kokoro': 'kok', 'kaoru': 'kao', 'hagumi': 'hag', 'kanon': 'kan', 'misaki': 'mis', 'marina': 'mar'}

def mystrip(line):
	return line.strip().strip('{').strip('}')

def speaker(name, abb):
	if name in list(long.keys()) and abb:
		return long[name]
	else:
		return name

def main(line, abb):
	markup = line.split('|')
	if markup[0] == 'CharTalk' or markup[0] == 'dialog':
		if markup[1] == 'others' or markup[1] == 'Array':
			return '/'*2 + markup[3] + '\n' + markup[2] + '\n'
		else:
			return '/' + speaker(markup[1],abb) + '\n' + markup[2] + '\n'
	elif markup[0] == 'loc':
		return markup[1] + '/\n'
	else:
		return line + '\n'

with open(args.path + '\\' + args.readname + '.txt', 'r') as f1, open(args.path + '\\' + args.writename + '.txt', 'w') as f2:
	for line in f1: f2.write(  main( mystrip(line), args.abbrev )  )