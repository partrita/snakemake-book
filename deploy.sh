#! /bin/bash
set -e
set -x

# 임시 디렉터리를 만들고 그 안에 책을 빌드합니다.
tmpdir=$(mktemp -d /tmp/bookXXX)
mdbook build -d ${tmpdir}
echo "빌드 디렉터리: ${tmpdir}"

# 임시 디렉터리로 이동합니다.
cd ${tmpdir}

# GitHub이 이를 Jekyll 사이트로 해석해서는 안 됨을 나타냅니다. 즉,
# 정적 사이트입니다.
touch .nojekyll

# 새 git 저장소를 만듭니다.
git init

# emacs의 ~ 파일을 무시합니다.
echo '*~' > .gitignore

# 'main' 브랜치의 모든 파일을 추가합니다.
git add .
git branch -M main

# 커밋합니다.
git commit -m "latest"

# github 페이지로 푸시합니다.
git push -f https://github.com/ngs-docs/2023-snakemake-book-draft main:gh-pages
