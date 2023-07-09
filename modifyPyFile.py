import re
import sys

if __name__ == '__main__':
    with open("module/static.py", "r", encoding="utf8") as f:
        param = str(sys.argv[1])
        regex = re.compile(r"\[.+\]")
        data = f.readlines()
        data[24] = regex.sub(param, data[24])

    with open("module/static.py", "w+", encoding="utf8") as f:
        f.writelines(data)
