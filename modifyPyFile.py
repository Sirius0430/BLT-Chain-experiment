

if __name__ == '__main__':
    with open("static.py","r",encoding="utf8") as f:
        data = f.readlines()
        changedData = data[24].split("")
        print()