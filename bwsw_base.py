from pathlib import Path

dir = str(Path(__file__).parent.absolute())

names = ['kasumi', 'tae', 'rimi', 'saaya', 'arisa', 'yukina', 'sayo', 'lisa', 'ako', 'rinko', 'aya', 'hina', 'chisato', 'maya', 'eve', 'ran', 'moca', 'himari', 'tomoe', 'tsugumi', 'kokoro', 'kaoru', 'hagumi', 'kanon', 'misaki', 'marina']

with open(dir + '\\transcript.txt', 'r') as f1, open(dir + '\\wikicode.txt', 'w') as f2:

	writeNew = ''

	for line in f1:

		l = line.strip()

		if l == '':
			f2.write('<br />'*2 + '\n')
			continue

		elif '/' in l:
			tag = l.split('/')
			if tag[0] == '':
				if tag[1] in names:
					writeNew = '{{dialog|' + tag[1].lower() + '|'
				else:
					writeNew = '{{dialog|' + tag[1] + '|'
			else:
				if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
			continue

		else:
			f2.write( writeNew + l.replace('[you]', '{{USERNAME}}-san') + '}}\n' )
