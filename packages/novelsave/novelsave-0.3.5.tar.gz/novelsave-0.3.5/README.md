# NovelSave

Tool to convert novels to epub

## Install

```
pip install novelsave
```

## Commandline

### Example
```
python3 -m novelsave https://www.webnovel.com/book/my-disciples-are-all-villains_16984011906162405 -u -p -c
```

#### Save directory

Novels are saved to folder `novels` in user home

### Help

```batch
usage: __main__.py [-h] [-t TIMEOUT] [-u] [-p] [-c] [--email EMAIL] [--pass PASSWORD] novel

tool to convert webnovel to epub

positional arguments:
  novel                 either id or url of novel

optional arguments:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        webdriver timeout

actions:
  -u, --update          update novel details
  -p, --pending         download pending chapters
  -c, --create          create epub from downloaded chapters

credentials:
  --email EMAIL         webnovel email
  --pass PASSWORD       webnovel password
```

## Manual

Access all the saved data using `novelsave.database.NovelData`

Manipulate the data using the accessors provided in the class

Creating an epub is easy as calling a function. `novelsave.Epub().create()`

## Sources

- [webnovel.com](https://www.webnovel.com)
- [wuxiaworld.co](https://www.wuxiaworld.co/)