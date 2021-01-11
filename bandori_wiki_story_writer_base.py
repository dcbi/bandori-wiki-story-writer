import argparse
from pathlib import Path

parent_dir = str(Path(__file__).parent.absolute())

parser = argparse.ArgumentParser()

parser.add_argument('-path', help="parent directory of files to read and write, default="+parent_dir, default=parent_dir)
parser.add_argument('-readname', help='name of file to read from, default=transcript', default='transcript')
parser.add_argument('-writename', help='name of file to write to, default=wiki', default='wiki')

args = parser.parse_args()

f1 = open(args.path + '\\' + args.readname + '.txt', 'r')
f2 = open(args.path + '\\' + args.writename + '.txt', 'w')

write = ''

for line in f1:

	l = line.strip()
	if l == '':
		f2.write('<br />\n')
		continue
	elif '/' in l:
		tag = l.split('/')
		if tag[0] == '':
			if tag[1] == '':
				writeNew = '{{dialog|others|[line]|' + tag[2] + '}}\n'
			else:
				writeNew = '{{dialog|' + process(tag[1].strip().lower(), args.abbrev) + '|[line]}}\n'
		else:
			if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
		continue
	else:
		f2.write( write.replace('[line]', line.strip().replace('[you]', '{{USERNAME}}-san')) )

f1.close()
f2.close()
