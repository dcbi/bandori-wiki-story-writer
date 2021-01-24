from pathlib import Path

dir = str(Path(__file__).parent.absolute())

with open(dir + '\\transcript.txt', 'r') as f1, open(dir + '\\wikicode.txt', 'w') as f2:

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
					writeNew = '{{dialog|' + tag[1].lower() + '|[line]}}\n'
			else:
				if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
			continue

		else:
			f2.write( write.replace('[line]', line.strip().replace('[you]', '{{USERNAME}}-san')) )
