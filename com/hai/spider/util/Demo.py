#!-*-coding:utf-8-*-
__author__ = 'henryBee'


def main():
    a = "2019-01-07 16:38:39"
    a_nosplit = a.replace("-", "").replace(" ", "").replace(":", "")[6:12]
    print(a_nosplit)
    print(float(a_nosplit))


if __name__ == "__main__":
    main()
