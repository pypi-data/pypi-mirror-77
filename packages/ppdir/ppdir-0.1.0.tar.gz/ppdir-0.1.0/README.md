# mkignore
**Pretty print a directory structure as a tree**

### Installation
`pip install ppdir`

### Usage
```shell script
usage: ppdir [-h] [-a, --all] [-c, --color] [DIR]

Pretty print a directory structure as a tree

positional arguments:
  DIR

optional arguments:
  -h, --help   show this help message and exit

  -a, --all    Include hidden files

  -c, --color  Colorize output
```
  
### Example
`ppdir -a -c .`

Output:
![Example](./screenshot.png)