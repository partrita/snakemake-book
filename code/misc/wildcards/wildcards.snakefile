# ANCHOR: 모든 파일
files, = glob_wildcards('letters-only-{word}.txt')
# ANCHOR_END: 모든 파일
print(files)
assert files == ['abc2', 'abc-xyz', 'abc']

# ANCHOR: 문자만
letters_only, = glob_wildcards('letters-only-{name,[a-zA-Z]+}.txt')
# ANCHOR_END: 문자만
print(letters_only)

assert 'abc' in letters_only
assert not 'abc2' in letters_only, letters_only

# ANCHOR: 문자만-2
letters_only, = glob_wildcards('letters-only-{name,[^0-9]+}.txt')
# ANCHOR_END: 문자만-2
print(letters_only)

assert 'abc' in letters_only
assert 'abc-xyz' in letters_only
assert not 'abc2' in letters_only

# ANCHOR: 모든-txt
all_txt_files, = glob_wildcards('{filename}.txt')
# ANCHOR_END: 모든-txt

assert 'data/datafile' in all_txt_files

# ANCHOR: 하위 디렉터리 없음
this_dir_only, = glob_wildcards('{filename,[^/]+}.txt')
# ANCHOR_END: 하위 디렉터리 없음

assert 'data/datafile' not in this_dir_only
