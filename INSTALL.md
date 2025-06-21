# 이 책을 빌드하고 테스트하기 위한 소프트웨어 설치

## 기본 소프트웨어로 conda 환경 만들기

```
mamba create -n mdbook -y rust snakemake-minimal pandas sourmash
```

그리고 활성화:
```
mamba activate mdbook
```

## 저장소 복제

```
cd ~/
git clone https://github.com/ngs-docs/2023-snakemake-book-draft
cd 2023-snakemake-book-draft
```

## mdbook 및 플러그인 설치:

[mdbook](https://github.com/rust-lang/mdBook)과 [mdbook-admonish](https://github.com/tommilligan/mdbook-admonish) 및 [mdbook-cmdrun](https://crates.io/crates/mdbook-cmdrun)을 사용합니다.

```
cargo install mdbook mdbook-admonish mdbook-cmdrun
```

## 책 빌드

```
make
```

## snakemake 테스트 실행

```
make test
```
