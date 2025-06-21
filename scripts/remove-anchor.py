#! /usr/bin/env python
"""
cmdrun과 함께 사용하기 위해 ANCHOR 하위 문자열이 포함된 줄을 제거합니다.
"""
import sys
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp')
    p.add_argument('-o', '--output')
    args = p.parse_args()

    data = open(args.inp, 'rt').readlines()

    outfp = sys.stdout
    if args.output:
        outfp = open(args.output, 'wt')

    for i in data:
        if 'ANCHOR' not in i:
            outfp.write(i)


if __name__ == '__main__':
    sys.exit(main())
