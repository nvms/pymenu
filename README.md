pymenu is a small utility to help easily build command line interfaces with the help of two decorators: `@initcommand()` and `@command()`.

![](http://i.imgur.com/1s8QgtD.png)

```python
from pymenu import *

m = PyMenu()
m.set_prompt('> ')

@initcommand()
def this_first():
    print(m.centrify('pymenu demo'))

@initcommand()
def this_second():
    print('Enter [help] to get help')

@command(r'help|h')
def help():
    print(helptext)

@command(r'quit|exit|q')
def goodbye():
    sys.exit('Goodbye')

m.run()
```