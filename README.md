# bandori-wiki-story-writer
Python code for turning transcripts of event/card stories from the Bandori game into wiki-code (for use on [Bandori Wikia](https://bandori.fandom.com)).

#### Example
The following is a valid transcript:

```
CiRCLE - Studio/
/sayo
Today's the day...
 
Imai-san, I love you!
/Ako, Rinko, and Yukina
...!
```

The following is the wiki-code that the above transcript is converted into:

```
{{loc|CiRCLE - Studio}}
{{dialog|sayo|Today's the day...}}
<br />
{{dialog|sayo|Imai-san, I love you!}}
{{dialog|Ako, Rinko, and Yukina|...!}}
```
### Dependencies
- pathlib (built-in for recent versions of Python)
- PyQt5 (optional)

### Example Usage
Suppose you have a transcript already written. As long as it is in the same location as the file containing the code and it is titled "transcript", simply run `python bwsw.py`. To loosen these restrictions, pass any of the following optional arguments: 
- `-path myfolder` sets the directory represented by `myfolder` as the directory where the transcript file is to be read from and where the output file is to be saved. The path can be either absolute (e.g. `C:\Users\ursul\Desktop`) or relatative to the current working directory (e.g. `Documents\myfolder`). The default is the parent directory of the file containing the code (so if you don't pass this argument, then again, make sure the transcript and the code are in the same folder).
- `-readname file_name` tells the program the name of the transcript file to read. The default is "transcript".
- `-writename file_name` tells the program what to name the output file. The default is "wikicode".

You can pass the following optional arguments to access additional features:
- `-expand` includes wiki-code that will put the story inside a collapsible frame. On the wikia, this looks like a button that says `Expand` which hides the story before being clicked and displays the story after being clicked.
- `-abbrev ABBREVIATION NAME` updates the default dictionary of character name abbreviations with a new key-value pair given by `{ABBREVIATION:CHARACTER}`. See below for the default abbreviations.

There is a version of the code with a label "\_gui" at the end of its name. It opens a window with a graphical user interface. If you do this, you don't need to pass any of the 5 arguments above because they will be handled by the GUI. The GUI requires the PyQt5 package. The GUI does not support custom abbreviations.

### Writing a transcript file
Transcript files are text files. They hold all the dialogue of an event/card story and use minimal syntax to indicate location banners, a change of speaker, or blank space.
- **Blank space:** to insert `<br />`, simply write an empty line (it may also contain spaces). For example, this can represent when the story skips a brief moment of time.
- **Locations:** to create a location banner such as `{{loc|CiRCLE}}`, start a new line and write the location name followed by a slash (`/`).
- **Dialogue:** to insert a dialogue box, such as `{{dialog|sayo|Good morning.}}`, indicate a change of speaker if necessary (see below) and start a new line. Then type the dialogue text exactly as is, nothing added. The speaker does not have to be indicated before every line of dialogue, only when there is a change of speaker.
- **New speaker:** to indicate a change of speaker, start a new line and write either a single or double slash (`/` or `//`) followed by the speaker's name.
  - Single slash is for most situations. It doesn't matter if the name is capitalized or not. It can also be an abbrevation of the speaker's name. See below for the default abbreviations. Abbreviations do not apply universally, i.e. your transcript can be a mix of abbreviated and non-abbreviated names, even for the same character. A single character may have multiple abbreviations as well.
  - Double slash can be used in rare situations but is mainly for style. When you make a dialogue box on the wiki, either the speaker is one of the main characters (from among the 5 bands or Marina) or the speaker is not (for example, "Ran's Dad", or when multiple main characters speak at once). In the first case, a round icon with a sprite of the character will show next to the dialogue box. In the second case, no icon will show. It used to be that if the speaker is not a main character, you have to use the construction `{{dialog|other|what they say|their name}}`. If you don't do so, the spacing between the surrounding dialogue boxes gets messed up, and they will overlap with each other on the screen. Now, this issue has been fixed. The regular `{{dialog|their name|what they say}}` will automatically handle both cases. But there are situations where you might want to purposely remove the icon even when a main character is speaking (for example, when a main character is speaking on the phone) and to do so, you can take advantage of this legacy code. I include this functionality just in case someone wants to use it. In this situation, the capitalization of names do matter.
- **Mentions of the player character:** whenever the player character's name is mentioned, replace it, including the "-san" suffix after it, with `[you]`. In the wiki-code output file, this will become `{{USERNAME}}-san`.

#### Errors

Be careful that slashes doesn't appear in any of the dialogue lines, names of speakers, or names of locations. If they do, there is some clunky error handling that I tried to incorporate, which asks for user input to directly tell the program what to do. Also be wary of special symbols, such as those in the emotes that Rinko uses when typing. The program might not recognize them and raise an error. If a slash-error can't be resolved or there is a UnicodeError, the following will show up in the output file:

`----------SKIPPED LINE----------`

The number of times it appears will be displayed.

#### Abbreviations

The default abbreviations are implemented by the dictionary below. You can change these to whatever you like.
```
{'kas':'kasumi', 'tae':'tae', 'rim':'rimi', 'say':'saaya', 'ari':'arisa',
'y':'yukina', 's':'sayo', 'l':'lisa', 'a':'ako', 'r':'rinko',
'aya':'aya', 'hin':'hina', 'chi':'chisato', 'may':'maya', 'eve':'eve',
'ran':'ran', 'moc':'moca', 'him':'himari', 'tom':'tomoe', 'tsu':'tsugumi',
'kok':'kokoro', 'kao':'kaoru', 'hag':'hagumi', 'kan':'kanon', 'mis':'misaki',
'mar':'marina'}
```
You can probably tell which band is my favorite.
