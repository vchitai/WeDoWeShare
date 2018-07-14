import os
from router import *


def main():
    app.secret_key = os.urandom(12)#, debug=True
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
