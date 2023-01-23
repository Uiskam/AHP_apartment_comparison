import app as app
import sys

if __name__ == "__main__":
    if len(sys.argv) == 3:
        app.start()
    print('Wrong number of arguments, expected 2 (config.csv data.csv)')
