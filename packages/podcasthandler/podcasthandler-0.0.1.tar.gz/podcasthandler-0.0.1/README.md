# Podcast Handler

A simple tool to play and keep track of your podcasts.

## Requirements

1. Python 3.0 or above
2. Music Player Daemon ([link](https://www.musicpd.org/))
3. Python library Python-Mpd2 ([link](https://pypi.org/project/python-mpd2/))

## Install

To clone the git repository:
```
	git clone https://gitlab.com/fnt400/podcast-handler.git
```
## Usage

## podcast-handler

A command line tool to play and automatically save position of a specific url.

> usage: podcast-handler [-h] [-H HOST] [-u URL] [-g] [-p POSITION] command
> 
> positional arguments:
>   command               play, stop, status, restart, gui
> 
> optional arguments:
>
>   -h, --help            show this help message and exit
>
>   -H HOST, --host HOST  set mpd host (default localhost)
>
>   -u URL, --url URL     set podcast episode url
>
>   -g, --gui             start with ncurses gui
>
>   -p POSITION, --position POSITION
>                         set start position (mm:ss)

Here's the available commands:

### Play

Play a specified url.
Without the URL argument, it continues the last played url.
With the POSITION argument, it starts playing from that position.

### Stop

Stop playing.

### Status

Display the current or the last played url.

### Restart

Restart from the beginning of the file.

### Gui

Start the ncurses gui.

# Known Bugs

- gui crashes on window resize
