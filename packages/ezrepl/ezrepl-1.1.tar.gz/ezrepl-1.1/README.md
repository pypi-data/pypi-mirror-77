# EZREPL (Python REPL Maker)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
## Description
A simple REPL maker. For python, made in python. Right now you can make a simple REPL and parse it by making a evaluator class. You can also hook up a HelpMenu class to the repl.

## Prerequisites
* [Requirements](requirements.txt)

## Installation
pip3 install ezrepl

## Contributing
Coming Soon

## License
MIT License [Here](LICENSE).

## Functionality
Simple Repl
```
import ezrepl

class MyRepl(ezrepl.Repl):
    def evaluator(self, ui):
        if ui == "hello":
            print("sup")

app = MyRepl(prefix="Hi: ", breaker="quit")
app.mainloop()
```

