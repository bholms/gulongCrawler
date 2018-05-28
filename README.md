This commandline tool crawls through www.gulongbbs.com and generate ebooks so users can put on their kindles for easy read.

```
usage: glScrap.py [-h] bookURL

Process arguments

positional arguments:
  bookURL     Book page URL from www.gulongbbs.com

  optional arguments:
    -h, --help  show this help message and exit
```

example: 流星蝴蝶剑

`python glScrap.py https://www.gulongbbs.com/book/lxhdj/`

A new directory called "lxhdj" should be created and all chapters should be listed in there. Now use Sigil to generate the epub and use Calibre to convert to MOBI format.
