import argparse
import pathlib
import sys, os.path

directory = os.path.dirname(sys.argv[0])

parser = argparse.ArgumentParser(description='Reads transcript file and writes file for wiki.')

parser.add_argument('-path', help="path of file to read from, default='RUNNING FILE DIRECTORY'", default=directory)
parser.add_argument('-readname', help='name of file to read from, default=transcript', default='transcript')
parser.add_argument('-writename', help='name of file to write to, default=wiki', default='wiki')

args = parser.parse_args()

f1 = open(args.path + '\\' + args.readname + '.txt', 'r')
f2 = open(args.path + '\\' + args.writename + '.txt', 'w')

write = ''

for line in f1:

	if '/' in line:
		tag = line.split('/')
		if tag[0] == ' ':
			f2.write('<br />\n')
		elif tag[0] == '':
			if tag[1] == '': write = '{{dialog|others|[line]|' + tag[2].strip() + '}}\n'
			else: write = '{{dialog|' + tag[1].strip().lower() + '|[line]}}\n'
		else:
			f2.write('{{loc|' + tag[0] + '}}\n')
		continue

	else:
		f2.write( write.replace('[line]', line.strip().replace('[you]', '{{USERNAME}}-san')) )

f1.close()
f2.close()
