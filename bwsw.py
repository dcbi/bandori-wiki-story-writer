import argparse
from pathlib import Path

dir = str(Path(__file__).parent.absolute())

short = {'kas':'kasumi', 'tae':'tae', 'rim':'rimi', 'say':'saaya', 'ari':'arisa', 'y':'yukina', 's':'sayo', 'l':'lisa', 'a':'ako', 'r':'rinko', 'aya':'aya', 'hin':'hina', 'chi':'chisato', 'may':'maya', 'eve':'eve', 'ran':'ran', 'moc':'moca', 'him':'himari', 'tom':'tomoe', 'tsu':'tsugumi', 'kok':'kokoro', 'kao':'kaoru', 'hag':'hagumi', 'kan':'kanon', 'mis':'misaki', 'mar':'marina'}

parser = argparse.ArgumentParser(epilog='Default abbreviations: '+str(short))

parser.add_argument('-path', help="parent directory of files to read and write, default="+dir, default=dir)
parser.add_argument('-readname', help='name of file to read from, default=transcript', default='transcript')
parser.add_argument('-writename', help='name of file to write to, default=wikicode', default='wikicode')
parser.add_argument('-abbrev', action='append', nargs=2, metavar=('ABBREVIATION','CHARACTER'), help='set a custom abbreviation for a name', default=list() )
parser.add_argument('-expand', action='store_true', help='inserts wikicode to put story inside collapsible frame')

args = parser.parse_args()

if any(args.abbrev):
    for x in args.abbrev:
        short[x[0]] = x[1]

def process(NAME):
    name = NAME.lower()
    if name in list(short.keys()):
        return short[name]
    elif name in list(short.values()):
        return name
    else:
        return NAME

class Slash(Exception): pass

with open(args.path + '\\' + args.readname + '.txt', 'r') as f1, open(args.path + '\\' + args.writename + '.txt', 'w') as f2:
    if args.expand: f2.write('<div class="mw-collapsible mw-collapsed">\n')

    skip = ['-'*10 + 'SKIPPED LINE' + '-'*10, 0]

    writeNew = ''

    for line in f1:
        l = line.strip()
        if l == '':
            f2.write('<br />' + '\n')
            continue

        elif '/' in l:
            try:
                tag = l.split('/')
                if tag[0] == '':
                    if tag[1] == '': writeNew = '{{dialog|other||[line]|' + tag[2] + '}}\n'
                    else: writeNew = '{{dialog|' + process(tag[1]) + '|[line]}}\n'
                else:
                    if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
                    else: raise Slash
                continue

            except Slash:
                print('\nDetected possible slash "/" in dialog or loc text.')
                print('LINE: ' + l)
                cont = input('Select: (0) neither, (1) loc, (2) dialog\n--> ')
                if cont == '0':
                    f2.write(skip[0])
                    skip[1] += 1
                elif cont == '1':
                    f2.write('{{loc|' + l[:len(line)-1] + '}}\n')
                elif cont == '2':
                    f2.write( writeNew.replace('[line]', l.replace('[you]', '{{USERNAME}}-san')) )
                else:
                    print('INVALID INPUT.')
                    f2.write(skip[0])
                    skip[1] += 1
                continue
        else:
            try:
                f2.write( writeNew.replace('[line]', l.replace('[you]', '{{USERNAME}}-san') ) )
            except UnicodeError:
                print('Possible special character. Check transcript file.')
                f2.write(skip[0])
                skip[1] += 1
                continue

    if args.expand: f2.write('</div><br />')

    if not skip[1] == 0: print(str(skip[1]) + ' line(s) skipped. Fix output file manually.')
