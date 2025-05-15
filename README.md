# Trick Surf Data Recap
## About
This project is all about a tiny script for generating recaps of TrickSurf API data.
Some of the information it uses are number of players, number of maps, number of servers,
number of events, number of triggers, number of teleports, number of tricks, number of jumps,
and number of sprays.

## Running Script
The script is located in the [/src/](./src) directory & named [main.py](./src/main.py).
The script supports several flags that you can pass to it — `--license`, `--first-hash`,
and `--last-hash`.
To gather more information & make yourself familiar w/ the utility,
execute the [main.py](./src/main.py) file w/ `--help` flag attached.
```text
usage: main.py [-h] [-l] --first-hash FIRST_HASH --last-hash LAST_HASH

optional arguments:
  -h, --help            show this help message and exit
  -l, --license         show the project license and exit
  --first-hash FIRST_HASH
                        set the first commit hash
  --last-hash LAST_HASH
                        set the last commit hash
```
The script depends on one python package that you can install using \`pip\`.
Run `pip install -r requirements.txt` in the root of this project and it will recursively install
all needed packages to run the [main.py](./src/main.py) file.

## Setting Development Environment
Follow this [documentation](https://docs.python.org/3/library/venv.html) to
setup a virtual python environment. Then activate the environment you just set-up
and install required packages using the [requirements.txt](./requirements.txt) file placed in the root of this project.
Be sure that you use Python 3.9.


## License
Licensed under the [GPL-3.0 license](./COPYING).
