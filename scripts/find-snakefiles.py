#! /usr/bin/env python
"""
'Snakefile' 또는 'snakefile.*'과 일치하는 모든 파일을 찾아 실행할 셸 코드를 작성합니다. 아직 작업 중입니다.

TODO?
- bash foo 설정
- 개별 셸 스크립트 작성 => 병렬 지원??
- 격리된 빌드/기타 디렉터리 지원
"""
import sys
import os
import argparse
import subprocess
from pathlib import Path


PATH_FILTERS = []

remove_out = lambda p: str(p).endswith('.out')
PATH_FILTERS.append(remove_out)

remove_bak = lambda p: str(p).endswith('~') or str(p).endswith('.bak')
PATH_FILTERS.append(remove_bak)

remove_dot = lambda p: any(pp.startswith('.') for pp in p.parts)
PATH_FILTERS.append(remove_dot)


def read_snakefile_metadata(filename):
    d = {}
    with open(filename, 'rt') as fp:
        lines = []
        for line in fp:
            line = line.strip()
            if not line.startswith('#'):
                break

            line = line[1:].strip()
            lines.append(line)

    d['expect_fail'] = False
    if 'expect_fail' in lines:
        d['expect_fail'] = True

    d['ignore'] = False
    if 'ignore' in lines:
        d['ignore'] = True

    for x in lines:
        if x.startswith('targets:'):
            x = x[8:]
            d['targets'] = x.strip()

    return d


def main():
    p = argparse.ArgumentParser()
    p.add_argument('dirs', nargs='+')
    p.add_argument('-o', '--output', default=None)
    p.add_argument('-l', '--list-snakefiles', action='store_true')
    p.add_argument('-d', '--debug', action='store_true')
    p.add_argument('-q', '--quiet', action='store_true')
    p.add_argument('-k', '--keyword-limit-pattern', default=None,
                   help="실행할 파일 이름에 필요한 키워드 지정")
    args = p.parse_args()

    snakefiles = []
    for dirname in args.dirs:
        pp = Path(dirname)

        snakefiles.extend(pp.glob('**/Snakefile'))
        snakefiles.extend(pp.glob('**/snakefile.*'))

    # 필터:
    snakefiles_filtered = []
    for ss in snakefiles:
        if any(f(ss) for f in PATH_FILTERS):
            if args.debug:
                print(f"(필터로 인해 경로에서 '{str(ss)}' 제거 중)",
                      file=sys.stderr)
            continue

        if args.keyword_limit_pattern:
            if args.keyword_limit_pattern not in str(ss):
                continue

        # 유지!
        snakefiles_filtered.append(ss)

    snakefiles = snakefiles_filtered
        
    print(f"실행할 snakefile {len(snakefiles)}개 발견!", file=sys.stderr)

    if args.list_snakefiles:
        print("\n".join([ str(ss) for ss in snakefiles ]))

    if args.output:
        print(f"실행 스크립트를 '{args.output}'에 저장 중", file=sys.stderr)
        output = open(args.output, 'wt')

        print("#! /bin/bash", file=output)
        print("failed=0", file=output)

        for snakefile in snakefiles:
            targets = ''
            metadata = read_snakefile_metadata(snakefile)

            if 'ignore' in metadata and metadata['ignore']:
                if not args.quiet:
                    print(f"(메타데이터에 따라 '{snakefile}' 무시 중)",
                          file=sys.stderr)
                continue
            
            if 'targets' in metadata:
                targets = metadata['targets']
            dirname, filename = os.path.split(snakefile)

            if metadata['expect_fail']:
                print(f"""
cd {dirname} > /dev/null
snakemake -s {filename} -j 1 -p {targets} >& {filename}.out && {{ echo fail {snakefile}; failed=1; }} || echo success {snakefile}
cd - > /dev/null
""", file=output)
            else:
                print(f"""
cd {dirname} > /dev/null
snakemake -s {filename} -j 1 -p {targets} >& {filename}.out && echo success {snakefile} || {{ echo fail {snakefile}; failed=1; }}
cd - > /dev/null
""", file=output)

        print("exit $failed", file=output)


if __name__ == '__main__':
    sys.exit(main())
