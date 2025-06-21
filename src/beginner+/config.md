# 구성 파일 사용

구성 파일은 워크플로의 _규칙_과 워크플로의 _구성_을 분리하는 데 사용할 수 있는 snakemake 기능입니다. 예를 들어, 여러 다른 샘플에 대해 동일한 시퀀스 트리밍 워크플로를 실행한다고 가정해 보겠습니다. 지금까지 본 기술로는 Snakefile을 매번 변경해야 합니다. 구성 파일을 사용하면 Snakefile을 동일하게 유지하고 새 샘플마다 다른 구성 파일을 제공하기만 하면 됩니다. 구성 파일은 특정 프로그램에 대한 매개변수를 정의하거나 기본 매개변수를 재정의하는 데에도 사용할 수 있습니다.

## 첫 번째 예 - 단일 샘플 ID로 규칙 실행

샘플 ID를 기반으로 출력 파일을 만드는 이 Snakefile을 고려하십시오. 여기서 샘플 ID는 구성 파일에서 가져와 `config`라는 Python 사전을 통해 제공됩니다.
```python
{{#include ../../code/examples/config.basic/snakefile.one_sample}}
```

기본 구성 파일은 `config.one_sample.yml`이며, `config['sample']`을 `XYZ_123` 값으로 설정하고 `one_sample.XYZ_123.out`을 만듭니다.
```yml
{{#include ../../code/examples/config.basic/config.one_sample.yml}}
```

그러나 Snakefile의 `configfile:` 지시문은 `--configfile`을 사용하여 명령줄에서 재정의할 수 있습니다. `config.one_sample_b.yml` 파일을 고려하십시오.
```yml
{{#include ../../code/examples/config.basic/config.one_sample_b.yml}}
```
이제 `snakemake -s snakefile.one_sample --configfile config.one_sample_b.yml -j 1`을 실행하면 샘플 값은 `ABC_456`으로 설정되고 `one_sample.ABC_456.out` 파일이 생성됩니다.

(CTB: 적절한 출력 파일이 생성되었는지 확인하십시오.)

## 구성 파일에 여러 샘플 ID 지정

이전 예제는 한 번에 하나의 샘플만 처리하지만 YAML 목록을 사용하여 여러 개를 제공하지 못할 이유는 없습니다. 이 Snakefile, `snakefile.multi_samples`를 고려하십시오.
```python
{{#include ../../code/examples/config.basic/snakefile.multi_samples}}
```

그리고 이 구성 파일, `config.multi_samples.yml`:
```yml
{{#include ../../code/examples/config.basic/config.multi_samples.yml}}
```

여기서는 더 복잡한 설정을 사용하여 여러 출력 파일을 만들고 있습니다.

먼저 구성 파일의 `samples`를 사용합니다. `config['samples']` 값은 이전 샘플에서와 같이 Python 문자열이 아닌 Python 문자열 목록입니다. 이는 구성 파일이 `config.multi_samples.yml` 파일에서 `samples`를 목록으로 지정하기 때문입니다.

둘째, Snakefile에서 [와일드카드 규칙](wildcards.md)을 사용하는 것으로 전환했습니다. 왜냐하면 [여러 파일에 대해 하나의 규칙을 실행](wildcards.md#running-one-rule-on-many-files)하고 싶기 때문입니다. 이것은 많은 이점이 있습니다!

마지막으로, [단일 패턴과 하나의 값 목록으로 `expand` 함수를 사용하는](expand.md#using-expand-with-a-single-pattern-and-one-list-of-values) [기본 규칙](../chapter_10.md)을 제공하여 와일드카드 규칙이 만들 출력 파일 목록을 구성합니다.

이제 구성 파일에서 샘플 목록을 편집하거나 다른 샘플 목록이 있는 다른 구성 파일을 제공할 수 있습니다!

## 구성 파일을 통해 입력 스프레드시트 지정

## 구성 파일에 명령줄 매개변수 지정

구성 파일은 샘플 ID에만 국한되지 않습니다. 구성 파일에 거의 모든 것을 넣을 수 있습니다.

[섹션 1](../chapter_0.md)에서 개발한 워크플로에서 특정 k-mer 크기에서 게놈을 비교하는 `sourmash sketch` 명령을 고려하십시오. 예를 들어 [2장](../chapter_2.md)에서는 다음과 같습니다.

```python
rule sketch_genomes:
    output:
       "GCF_000017325.1.fna.gz.sig",
       "GCF_000020225.1.fna.gz.sig",
       "GCF_000021665.1.fna.gz.sig"
    shell: """
        sourmash sketch dna -p k=31 genomes/*.fna.gz --name-from-first
    """
```

여기서 `sketch dna`는 매개변수 `-p k=31`로 실행되어 비교를 위한 k-mer 크기를 k=31로 설정합니다. 이것은 구성 파일에 적합한 후보입니다!

[params 블록](params.md)과 구성 파일을 사용하여 이 규칙을 다음과 같이 다시 작성할 수 있습니다.
```python
rule sketch_genomes:
    output:
       "GCF_000017325.1.fna.gz.sig",
       "GCF_000020225.1.fna.gz.sig",
       "GCF_000021665.1.fna.gz.sig",
    params:
        ksize=config['ksize'],
    shell: """
        sourmash sketch dna -p k={params.ksize} genomes/*.fna.gz --name-from-first
    """
```

몇 가지 좋은 기능이 있습니다.

* 'params'를 사용하면 이것이 매개변수임을 독자에게 명확하게 보여줍니다!
* k-mer 크기를 구성할 수 있습니다!

CTB: k=21에서도 실제로 작동하는지 확인하십시오!

CTB: config.get 및 int/유형 유효성 검사에 대해 이야기하십시오.

CTB: 고급 사용법: compare에 대한 output=pdf와 같은 조건부 매개변수.

참고/위험, 출력 파일 이름의 매개변수에 대한 정보가 필요할 수 있습니다...

참고/위험, 구성 파일의 정보와 snakefile의 정보 간의 절충점에 대해 이야기하십시오. 예를 들어 실행할 프로그램과 사용할 매개변수입니다.

## 구성 파일 디버깅 및 `config` 사전 표시

snakemake를 실행할 때 구성이 실제로 무엇인지 알고 싶을 때가 많습니다. 이를 수행하는 편리한 방법은 `pprint`를 사용하는 것입니다. 예를 들어 `snakefile.multi_samples.pprint`를 참조하십시오.
```python
{{#include ../../code/examples/config.basic/snakefile.multi_samples.pprint}}
```
다음과 같은 출력을 생성합니다.
```
config is:
{'samples': ['DEF_789', 'GHI_234', 'JKL_567']}
SAMPLES is:
['DEF_789', 'GHI_234', 'JKL_567']
```

CTB: 파이썬 dict/list를 설명하거나 링크하십시오.

CTB: 디버깅에 링크하십시오.

CTB: -n과 Python 문 대 규칙에 대해 이야기하십시오...

print, pprint
키

.get/기본값 제공 사용

## 고급 사용법

### 명령줄에서 구성 변수 제공

명령줄에서 개별 구성 변수를 설정할 수도 있습니다.

```
snakemake -j 1 -s snakefile.one_sample -C sample=ZZZ_123
```

CTB: 목록에 대해 이 작업을 수행하는 방법, 여러 구성 변수에 대해 이 작업을 수행하는 방법.

### 여러 구성 파일 제공

`--configfiles`

## 요약

구성 파일을 사용하면 다음을 수행할 수 있습니다.

* 워크플로에서 구성 분리
* 동일한 워크플로에 대해 여러 다른 구성 파일 제공
* Snakefile 대신 YML 파일을 편집하여 샘플 변경
* 입력 구성 유효성 검사 용이 (논의)

## 남은 것들

* 공식 snakemake 문서 참조
* YAML 및 JSON 구문 가이드
