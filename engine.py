#!/usr/bin/env python
from works.trees import Trees
from works.crossings import Crossings
from website import app
from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    app.run()
    # tr = Crossings()
    # req = tr.request()
    # tr.update(req)
    # tr.output()
