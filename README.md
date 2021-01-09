# bandori-wiki-story-writer
Python script for turning (correctly formatted) transcripts of event/card stories from Bandori into wiki-code.

#### Example
The following transcript

```
CiRCLE - Studio/
/sayo
Today's the day...
 /
Imai-san, I love you!
//Ako, Rinko, and Yukina
...!
```

will turn into the following wiki-code

```
{{loc|CiRCLE - Studio}}
{{dialog|sayo|Today's the day...}}
<br />
{{dialog|sayo|Imai-san, I love you!}}
{{dialog|others|...!|Ako, Rinko, and Yukina}}
```
