#! /usr/bin/env python
"""
cmdrun 및 'diff' 강조 표시와 함께 사용할 두 파일 간의 통합 diff를 표시합니다.
"""
import sys
import argparse
from difflib import unified_diff


def main():
    p = argparse.ArgumentParser()
    p.add_argument('file1')
    p.add_argument('file2')
    p.add_argument('-o', '--output')
    args = p.parse_args()

    data1 = open(args.file1, 'rt').readlines()
    data2 = open(args.file2, 'rt').readlines()

    outfp = sys.stdout
    if args.output:
        outfp = open(args.output, 'wt')

    x = list(unified_diff(data1, data2))
    for i in x[3:]:
        outfp.write(i)


if __name__ == '__main__':
    sys.exit(main())
