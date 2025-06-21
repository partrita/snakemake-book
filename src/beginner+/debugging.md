# 워크플로 실행 디버깅 기술 (그리고 문제 해결!)

## 몇 가지 초기 지혜의 말

복잡한 컴퓨터 상황을 디버깅하는 것은 예술입니다. 적어도 쉽게 체계화되지 않습니다. 디버깅에는 지침과 규칙조차 있지만 작동이 보장되는 단일 절차나 접근 방식은 없습니다.

이 장에서는 snakemake 워크플로를 *디버깅하는 방법*에 중점을 둡니다. 이 장을 읽고 있다면 무언가를 작동시키기 위해 열심히 노력하고 있을 가능성이 큽니다. 젠장, 당신은 아마도 절박하기 때문에 이 문장만 읽고 있을 것입니다.

아래는 현재 snakemake 여정에서 디버깅에 대해 제공할 수 있는 가장 유용한 조언입니다.

첫째, 워크플로를 가능한 한 단순화하여 빠르게 실행할 수 있도록 합니다. 예를 들어 샘플 수를 1개 또는 2개로 줄이고(@@) 입력 파일을 하위 샘플링하여 작게 만듭니다. 이렇게 하면 실행 속도가 빨라지고 결과를 테스트하는 사이의 시간이 줄어듭니다.

둘째, 한 번에 하나의 규칙에 집중합니다. 원하는 대로 작동하지 않는 규칙을 찾을 때까지 각 규칙을 하나씩 실행합니다. 그런 다음 해당 규칙을 수정하는 데 집중합니다. 이렇게 하면 snakemake 규칙을 통해 점점 더 견고한 경로를 제공할 수 있습니다.

셋째, 실행 중인 명령을 인쇄하고(-p 사용) snakemake 출력에서 와일드카드를 주의 깊게 검사합니다. 명령과 와일드카드 값이 모두 예상한 대로인지 확인합니다. 그렇지 않은 첫 번째 규칙을 찾아 해당 규칙을 수정합니다. 이렇게 하면 각 단계에서 와일드카드가 ...

## snakemake 디버깅의 세 단계

snakemake 워크플로를 만들거나 수정할 때 접하게 될 세 가지 일반적인 디버깅 단계가 있습니다.

첫째, 일치하지 않는 들여쓰기 및 공백, 일치하지 않는 따옴표로 인해 구문 오류가 발생합니다. 이러한 오류로 인해 snakemake가 Snakefile을 읽지 못하게 됩니다.

둘째, 규칙을 연결하고 와일드카드를 채우는 데 문제가 발생합니다. 이로 인해 snakemake가 작업을 실행하지 못하게 됩니다.

그리고 셋째, 특정 규칙이나 작업이 실패하게 만드는 실제 실행 오류가 발생합니다. 이러한 오류로 인해 워크플로가 완료되지 못하게 됩니다.

이 장에서는 이러한 오류의 가장 일반적인 유형의 원인을 다루고 이러한 오류 중 상당수를 피하거나 수정하기 위한 팁과 기술도 제공합니다.

* 중간 대상
* 디버그-dag
* 로그
* Snakefile에서 인쇄 (file= 사용)
* 오류 메시지 찾기 및 읽기 - 침묵, 종료됨 등
* 단일 CPU 모드에서 실행
* 공백
* 와일드카드 채우기
* `--until`을 사용하여 이동할 규칙 지정
* 한 번에 하나의 와일드카드에 집중
* 생각: 디버깅 세트에 대해 실제로 자세히 살펴보는 것을 할 수도 있습니다.

@@ 구문 이후 제안된 절차: 먼저 -j big 및 -k로 실행합니다. 그런 다음 남은 모든 것이 차단 오류가 됩니다.


~~~admonish info title='구문 오류 후: snakemake 워크플로 실행'

snakemake 워크플로에서 실행 오류를 디버깅하려고 할 때 사용할 수 있는 간단한 전략 목록입니다. 즉, snakemake가 Snakefile을 읽지 못하게 하는 구문 오류를 해결한 _후_입니다.

1. `-n/--dry-run`으로 snakemake를 실행하고 출력을 검사합니다. 이렇게 하면 snakemake 워크플로가 규칙을 실행하고 실제로 관심 있는 출력을 생성하는지 알 수 있습니다.
2. `-j/--cores 1`로 snakemake를 실행합니다. 이렇게 하면 작업이 직렬 모드로 차례로 실행됩니다. 이렇게 하면 한 번에 하나의 작업만 실행되므로 snakemake 작업의 출력이 덜 혼란스러워집니다.
3. `-p/--printshellcmds`로 snakemake를 실행합니다. 이렇게 하면 실행 중인 실제 셸 명령이 인쇄됩니다.
4. 명령줄에서 규칙 이름이나 파일 이름을 지정하여 디버깅하려는 규칙만 실행합니다([명령줄에서 규칙 실행 및 대상 선택](targets.md) 참조).

~~~

## 구문 오류 찾기, 수정 및 방지.

### 공백 및 들여쓰기 오류: 찾기, 수정 및 방지.

vscode 또는 다른 텍스트 편집기와 같은 좋은 편집기를 사용하십시오. snakemake 모드 또는 Python 모드로 설정하십시오(공백 등).

### 구문 오류, 줄 바꿈 및 따옴표.

세겹 따옴표 대 작은따옴표

줄 삭제.

## Snakefile 워크플로 선언/사양 디버깅 @@

### `MissingInputException`

새 워크플로를 작성할 때 발생하는 가장 일반적인 오류 중 하나는 `MissingInputException`입니다. 이는 snakemake가 세 가지를 말하는 방식입니다. 첫째, 특정 파일이 _필요하다_는 것을 알아냈습니다. 둘째, 해당 파일이 아직 존재하지 않습니다. 셋째, 해당 파일을 _만드는_ 방법을 모릅니다(즉, 해당 파일을 생성하는 규칙이 없습니다).

예를 들어, 이 매우 간단한 워크플로 파일을 고려하십시오.
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.missing-input}}
```

실행하면 다음이 표시됩니다.
```
MissingInputException in rule example in file /Users/t/dev/2023-snakemake-book-draft/code/examples/errors.simple-fail/snakefile.missing-input, line 1:
Missing input files for rule example:
    affected files:
        file-does-not-exist
```

이 오류는 두 가지 일반적인 상황에서 발생합니다. 워크플로에 제공해야 했지만 누락된 입력 파일이 있는 경우(예: 누락된 FASTQ 파일) 또는 이 파일을 (출력으로) 생성해야 하는 규칙이 제대로 일치하지 않는 경우입니다.

### `MissingOutputException` 및 `--latency-wait` 증가

때때로 `MissingOutputException`을 언급하고 `--latency-wait`로 대기 시간을 늘리도록 제안하는 오류 메시지가 표시될 수 있습니다. 이는 예상 출력 파일을 제대로 만들지 않는 규칙의 증상인 경우가 가장 많습니다.

예를 들어 다음을 고려하십시오.
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.missing-output}}
```

여기에는 출력 블록에 `file-does-not-exist`라는 파일을 만들 것이라고 지정하지만 (셸 명령의 오타로 인해) 대신 잘못된 파일을 만드는 간단한 규칙이 있습니다. 이를 실행하면 다음 메시지가 표시됩니다.

```
Waiting at most 5 seconds for missing files.
MissingOutputException in rule example in file /Users/t/dev/2023-snakemake-book-draft/code/examples/errors.simple-fail/snakefile.missing-output, line 3:
Job 0 completed successfully, but some output files are missing. Missing files after 5 seconds. This might be due to filesystem latency. If that is the case, consider to increase the wait time with --latency-wait:
file-does-not-exist
```

먼저 `output:` 블록은 지시문이 아니라 단순히 _주석_이라는 점을 기억합시다. 이 규칙이 _만들어야 하는_ 것을 snakemake에 알려주지만 실제로 만들지는 않습니다 @@ (여기서 input-output에 링크). 파일을 _만드는_ 규칙의 부분은 일반적으로 `shell:` 블록이며, 여기서는 셸 블록에서 실수를 하여 잘못된 파일을 만들고 있습니다.

**셸 블록에서 실제로 어떤 파일이 만들어졌는지 snakemake가 알 수 있는 간단한 방법은 없으므로** snakemake는 시도하지 않습니다. 이 규칙을 실행하면 특정 파일이 만들어질 것이라고 _말했지만_ 실행했을 때 해당 파일이 _만들어지지 않았다_고 간단히 불평합니다. 이것이 일반적으로 `MissingOutputException`이 의미하는 바입니다.

이를 수정하려면 셸 명령을 살펴보고 원하는 파일을 만들지 않는 이유를 이해해야 합니다. 복잡해질 수 있지만 일반적인 수정 사항 중 하나는 파일 이름을 중복으로 작성하지 않고 대신 셸 블록에서 `{output}` 패턴을 사용하여 `output:` 블록과 `shell:` 블록에서 실수로 다른 이름을 사용하지 않도록 하는 것입니다.

그렇다면 누락된 파일에 대해 5초 동안 기다리거나 `--latency-wait`를 늘리라는 이 메시지는 무엇일까요? 이것은 여러 시스템에서 실행되는 작업에서 공유 네트워크 파일 시스템에 쓸 때 발생할 수 있는 고급 상황(@@나중에 논의됨)을 나타냅니다. 단일 시스템에서 snakemake를 실행하는 경우 이것은 절대 문제가 되지 않아야 합니다! 이에 대한 논의는 나중에 미루겠습니다.

### `WorkflowError` 및 와일드카드

또 다른 일반적인 오류는 `WorfklowError: Target rules may not contain wildcards."입니다. 이는 와일드카드가 포함된 규칙을 실행하도록 snakemake에 요청할 때 발생합니다.

다음을 고려하십시오.
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.wildcard-error}}
```

다음을 생성합니다.
```
WorkflowError:
Target rules may not contain wildcards. Please specify concrete files or a rule without wildcards at the command line, or have a rule without wildcards at the very top of your workflow (e.g. the typical "rule all" which just collects all results you want to generate in the end).
```

이 경우 이 오류는 snakemake 워크플로에 규칙이 하나만 있고 `snakemake`를 실행하면 기본적으로 해당 규칙을 대상으로 실행하기 때문에 발생합니다. 그러나 해당 규칙은 출력 블록에서 [와일드카드](wildcards.md)를 사용하므로 대상이 될 수 없습니다.

규칙 이름을 명시적으로 지정할 때도 이 오류가 발생할 수 있습니다. 이름으로 실행하도록 snakemake에 요청한 규칙의 출력 블록에 와일드카드가 포함되어 있으면 규칙을 직접 실행할 수 없습니다. 대신 snakemake가 와일드카드를 유추하는 데 사용할 수 있는 파일 이름을 제공해야 합니다.

두 경우 모두 해결책은 snakemake에 파일 이름을 빌드하도록 요청하거나 와일드카드가 포함되지 않은 대상을 snakemake에 제공하는 것입니다. 예를 들어, 디렉터리에 `XYZ.input` 파일이 있는 경우 여기서는 명령줄에서 `XYZ.output`을 지정하거나 `XYZ.output`이라는 이름을 의사 대상으로 지정하는 새 기본 규칙을 작성할 수 있습니다.
```python
rule all:
    input:
        "XYZ.output"
```
두 솔루션 모두 `name` 와일드카드를 대체할 값을 `example` 규칙에 제공하는 효과가 있습니다.

자세한 내용은 [와일드카드를 사용하여 규칙 일반화](wildcards.md#all-wildcards-used-in-a-rule-must-match-to-wildcards-in-the-output-block) 및 [대상](targets.md)을 참조하십시오.

## 실행 중인 snakemake 워크플로 디버깅


## 규칙을 한 번에 하나씩 실행합니다.

## 규칙을 한 번에 하나의 작업으로 실행합니다.

## 오류 메시지 찾기 및 해석

### 실패한 명령에 대한 오류 메시지 표시

## `-k/--keep-going`으로 실행할 수 있는 모든 규칙 실행

Snakemake는 셸 명령의 오류 메시지를 약간 혼란스럽게 표시합니다. 메시지는 규칙이 실패했다는 알림 _위에_ 나타납니다.

다음 Snakefile을 고려하십시오.
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.shell-fail}}
```

`file-does-not-exist`라는 파일이 포함되지 _않은_ 디렉터리에서 이를 실행하면 다음 출력이 표시됩니다.

```
[Fri Apr 14 14:59:29 2023]                 
rule hello_fail:
    jobid: 0
    reason: Rules with neither input nor output files are always executed.
    resources: tmpdir=/var/folders/6s/_f373w1d6hdfjc2kjstq97s80000gp/T

ls: cannot access 'file-does-not-exist': No such file or directory
[Fri Apr 14 14:59:29 2023]
Error in rule hello_fail:
    jobid: 0
    shell:
        
        ls file-does-not-exist
    
        (one of the commands exited with non-zero exit code; note that snakemake uses bash strict mode!)
```

이 출력에는 세 부분이 있습니다.

* 첫 번째 부분은 `rule hello_fail:`에서 시작하여 snakemake가 이 규칙을 실행할 것이라고 선언하고 그 이유를 알려줍니다.
  
* 두 번째 부분에는 해당 명령을 실행한 오류 메시지가 포함됩니다. 여기서 `ls`는 해당 파일이 존재하지 않기 때문에 실패하므로 `ls: cannot access 'file-does-not-exist': No such file or directory`를 출력합니다. **이것은 실패한 명령에서 출력된 오류입니다.**
  
* 세 번째 부분은 "Error in rule hello_fail"에서 시작하여 실패한 규칙을 설명합니다. 이름 `hello_fail`, 작업 ID 및 실행된 셸 명령(`ls file-does-not-exist`)과 함께 실패가 감지된 방법(0이 아닌 종료 코드 @@) 및 셸 명령이 실행된 방법("엄격 모드" @@라고 함)에 대한 일부 정보가 함께 제공됩니다.
  
여기서 다소 직관적이지 않은 부분은 실패한 규칙에 특정한 오류 메시지(해당 파일이 존재하지 않음)가 실패 알림 _위에_ 나타난다는 것입니다.

이에 대한 몇 가지 좋은 이유가 있으며(@@ stdout 캡처와 관련된 내용) 이 동작을 변경하는 다양한 방법이 있지만(@@ 로깅) _기본적으로_ 이것이 snakemake가 셸 명령의 오류를 보고하는 방식입니다.

실제로 이것이 의미하는 바는 실패한 셸 명령을 디버깅할 때 snakemake 오류를 찾아야 할 곳이 실패 알림 _위_라는 것입니다!
  
@@ bash 엄격 모드 설명

@@ (간단히) 로깅 설명

@@ -j를 1보다 크게 실행할 때

### 메모리 부족 오류: "Killed".

CTB: 소문자인가요, 대문자인가요?

때때로 snakemake에서 "규칙 실패" @@ 오류가 표시되고 찾을 수 있는 유일한 오류 메시지는 "killed"입니다. 이것은 무엇일까요?

이는 일반적으로 셸 명령(또는 셸 프로세스)이 운영 체제에서 피할 수 없는 신호에 의해 종료되었음을 의미하며, 가장 일반적인 신호는 메모리 부족 오류입니다.

프로세스가 너무 많은 메모리를 사용하면 운영 체제의 기본 동작은 즉시 종료하는 것입니다. 달리 할 수 있는 일이 많지 않습니다. 안타깝게도 이를 설명하는 기본 오류 메시지는 다소 부족합니다.

안타깝게도 이 문제를 _해결_할 수 있는 단일 방법은 없습니다. 몇 가지 일반적인 전략은 다음과 같습니다.

* 메모리가 더 많은 시스템으로 전환하거나 (slurm과 같은 대기열 시스템을 사용하는 경우) 작업에 더 많은 메모리를 요청합니다.
* 사용할 메모리 양을 지정하도록 요청하는 프로그램(예: 일부 어셈블러 또는 모든 java 프로그램)을 사용하는 경우 명령줄에서 요청하는 메모리 양을 줄일 수 있습니다.
* 데이터 세트의 크기를 줄일 수도 있습니다. 아마도 하위 분할하거나 하위 샘플링하여 @@.

[end of src/beginner+/debugging.md]

[start of src/beginner+/expand.md]
# `expand`를 사용하여 파일 이름 생성

[Snakemake 와일드카드](./wildcards.md)를 사용하면 규칙을 여러 파일에 쉽게 적용할 수 있지만, 원하는 모든 파일 이름을 생성하는 방법이라는 새로운 과제도 발생합니다.

이러한 과제의 예로, [8장](../chapter_8.md)의 `compare_genomes` 규칙에 필요한 게놈 목록을 고려해 보겠습니다.

```python
rule compare_genomes:
    input:
        "GCF_000017325.1.fna.gz.sig",
        "GCF_000020225.1.fna.gz.sig",
        "GCF_000021665.1.fna.gz.sig",
        "GCF_008423265.1.fna.gz.sig",
```

이 목록은 와일드카드 규칙으로 생성할 스케치를 지정하기 때문에 중요합니다. 그러나 이 목록을 작성하는 것은 모든 파일 이름의 일부가 동일하고 반복되기 때문에 성가시고 오류가 발생하기 쉽습니다.

더 나쁜 것은 이 목록을 여러 곳에서 사용해야 하거나 동일한 액세션으로 약간 다른 파일 이름을 생성해야 하는 경우 오류가 발생하기 쉽다는 것입니다. 목록의 요소를 추가, 제거 또는 편집하고 싶을 가능성이 높으며 여러 곳에서 변경해야 합니다.

[9장](../chapter_9.md)에서는 이를 Snakefile 상단의 액세션 목록으로 변경한 다음 `expand`라는 함수를 사용하여 목록을 생성하는 방법을 보여주었습니다.
```python
ACCESSIONS = ["GCF_000017325.1",
              "GCF_000020225.1",
              "GCF_000021665.1",
              "GCF_008423265.1"]

#...

rule compare_genomes:
    input:
        expand("{acc}.fna.gz.sig", acc=ACCESSIONS),

```

`expand`를 사용하여 파일 이름 목록을 생성하는 것은 Snakefile에서 일반적인 패턴이며, 이 장에서는 이에 대해 자세히 살펴보겠습니다!

## 단일 패턴과 하나의 값 목록으로 `expand` 사용

위의 예에서는 단일 패턴 `{acc}.fna.gz.sig`를 제공하고 `ACCESSIONS`의 각 요소에서 필드 이름 `acc`의 값을 채워 여러 파일 이름으로 확인하도록 `expand`에 요청합니다. (입력 및 출력 블록에서 값을 지정하는 키워드 구문 `acc=ACCESSIONS`를 인식할 수 있습니다.)

여기서 `expand('{acc}.fna.gz.sig', acc=...)`의 결과는 네 개의 파일 이름을 긴 형식으로 작성하는 것과 _동일합니다_.
```
"GCF_000017325.1.fna.gz.sig",
"GCF_000020225.1.fna.gz.sig",
"GCF_000021665.1.fna.gz.sig",
"GCF_008423265.1.fna.gz.sig"
```
즉, `expand`는 특별한 와일드카드 일치 또는 패턴 추론을 수행하지 않고 단순히 값을 채우고 결과 목록을 반환합니다.

여기서 `ACCESSIONS`는 모든 Python _iterable_일 수 있습니다. 예를 들어 리스트, 튜플 또는 사전입니다. 자세한 내용은 [Python 부록](../appendix/python.md)을 참조하십시오.

## 여러 값 목록으로 `expand` 사용

여러 필드 이름과 함께 `expand`를 사용할 수도 있습니다. 다음을 고려하십시오.
```
expand('{acc}.fna.{extension}`, acc=ACCESSIONS, extension=['.gz.sig', .gz'])
```
그러면 다음 8개의 파일 이름이 생성됩니다.
```
"GCF_000017325.1.fna.gz.sig",
"GCF_000017325.1.fna.gz",
"GCF_000020225.1.fna.gz.sig",
"GCF_000020225.1.fna.gz",
"GCF_000021665.1.fna.gz.sig",
"GCF_000021665.1.fna.gz",
"GCF_008423265.1.fna.gz.sig",
"GCF_008423265.1.fna.gz"
```
제공된 패턴에 `acc`와 `extension`의 _모든 가능한_ 조합을 대체하여.

## _모든_ 조합 생성 대 _쌍별_ 조합

위에서 본 것처럼 여러 패턴을 사용하면 `expand`는 가능한 모든 조합을 생성합니다. 즉,
```python
{{#include ../../code/examples/expand.combine/Snakefile:combinatorial}}
```
는 9개의 파일 이름(`1.by.a`, `1.by.b`, `1.by.c`, `2.by.a` 등)을 생성합니다. 그리고 `expand` 문자열에 세 번째 패턴을 추가하면 `expand`는 해당 패턴도 조합에 추가합니다!

그래서 여기서 무슨 일이 일어나고 있는 걸까요?

기본적으로 expand는 가능한 모든 조합을 포함하는 전체 확장을 수행합니다. (이를 데카르트 곱, 교차 곱 또는 외부 조인이라고도 합니다.)

하지만 항상 원하는 것은 아닙니다. 이 동작을 어떻게 변경할 수 있을까요?

`expand` 함수는 선택적 두 번째 인수인 조합기를 사용하며, 이는 뒤따르는 값 목록을 결합하는 방법을 `expand`에 알려줍니다. 기본적으로 `expand`는 모든 가능한 조합을 만드는 Python 함수인 `itertools.product`를 사용하지만 다른 함수를 제공할 수 있습니다.

특히, [와일드카드 예제](wildcards.md) 중 하나에서 수행한 것처럼 `zip`을 대신 사용하여 쌍별 조합을 만들도록 `expand`에 지시할 수 있습니다.

다음은 예입니다.

```python
{{#include ../../code/examples/expand.combine/Snakefile:zip}}
```
그러면 이제 세 개의 파일 이름만 생성됩니다: `1.by.a`, `2.by.b`, `3.by.c`.

여기서 큰 주의 사항은 `zip`이 가장 짧은 입력 목록 길이의 출력 목록을 만든다는 것입니다. 따라서 세 요소로 구성된 목록 하나와 두 요소로 구성된 목록 하나를 제공하면 첫 번째 목록에서 두 요소만 사용합니다.

예를 들어, 이 `Snakefile`의 `expand`에서
```python
{{#include ../../code/examples/expand.combine/Snakefile:zip_short}}
```
두 번째 목록에는 `3`에 대한 파트너가 없으므로 `1.by.a`와 `2.by.b`만 생성됩니다.

자세한 내용은 [제품 대신 zip을 사용하는 것에 대한 snakemake 설명서](https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do)를 참조하십시오.

## `expand`에서 사용할 식별자 목록 가져오기

`expand` 함수는 워크플로에서 여러 번 사용하는 식별자 목록이 있을 때 효과적인 솔루션을 제공합니다. 이는 생물정보학에서 일반적인 패턴입니다! 그러나 위의 예에서처럼 이러한 목록을 Snakefile에 작성하는 것이 항상 실용적인 것은 아닙니다. 수십에서 수백 개의 식별자가 있을 수 있습니다!

식별자 목록은 다양한 방법으로 _다른_ 파일에서 로드할 수 있으며, `glob_wildcards`를 사용하여 디렉터리의 실제 파일 집합에서 생성할 수도 있습니다.

## 파일 또는 디렉터리에서 액세션 목록을 로드하는 예

### 텍스트 파일에서 액세션 목록 로드

텍스트 파일 `accessions.txt`에 간단한 액세션 목록이 있는 경우 다음과 같습니다.

파일 `accessions.txt`:
```
{{#include ../../code/examples/load_idlist_from/accessions.txt}}
```

그러면 다음 코드는 텍스트 파일의 각 줄을 별도의 ID로 로드합니다.
```python
{{#include ../../code/examples/load_idlist_from/snakefile.load_txt}}
```

그리고 각 액세션에 대한 sourmash 서명을 빌드합니다.

### CSV 파일에서 특정 열 로드

텍스트 파일 대신 여러 열이 있는 CSV 파일이 있고 로드할 ID가 모두 한 열에 있는 경우 Python [pandas 라이브러리](https://pandas.pydata.org/)를 사용하여 CSV를 읽을 수 있습니다. 아래 코드에서 `pandas.read_csv`는 CSV를 pandas DataFrame 개체로 로드한 다음 `accession` 열을 선택하여 반복 가능한 것으로 사용합니다.

파일 `accessions.csv`:
```csv
{{#include ../../code/examples/load_idlist_from/accessions.csv}}
```

`accessions.csv`를 로드하는 Snakefile:
```python
{{#include ../../code/examples/load_idlist_from/snakefile.load_csv}}
```

### 구성 파일에서 로드

Snakemake는 또한 구성 파일 사용을 지원하며, 여기서 snakefile은 기본 구성 파일의 이름을 제공합니다(명령줄에서 재정의할 수 있음).

구성 파일은 액세션을 넣기에도 좋은 장소입니다. 다음을 고려하십시오.

```yaml
{{#include ../../code/examples/load_idlist_from/config.yml}}
```

다음 Snakefile에서 사용됩니다.
```python
{{#include ../../code/examples/load_idlist_from/snakefile.use_config}}
```

여기서 `config.yml`은 [YAML 파일](https://en.wikipedia.org/wiki/YAML)이며, 사람이 읽을 수 있는 형식으로 컴퓨터도 읽을 수 있습니다. 나중에 구성 파일에 대해 이야기하겠습니다! CTB.

### `glob_wildcards`를 사용하여 파일 집합에서 ID 또는 액세션 로드

[와일드카드에 대한 장](wildcards.md#renaming-files-by-prefix-using-glob_wildcards)에서 `glob_wildcards` 명령을 간략하게 소개했습니다. `glob_wildcards`는 _실제로 디렉터리에 있는_ 파일에 대한 패턴 일치를 수행합니다.

다음은 `glob_wildcards`를 사용하여 실제 파일 이름에서 네 개의 액세션을 가져오는 Snakefile입니다.
```python
{{#include ../../code/examples/load_idlist_from/snakefile.glob_wildcards}}
```

이것은 액세션 목록을 얻는 특히 편리한 방법이지만 사용하는 것은 위험할 수 있습니다. 특히 파일을 실수로 삭제하고 샘플이 누락된 것을 알아차리지 못하기 쉽습니다! 이러한 이유로 많은 상황에서 로드할 파일의 독립적인 목록을 제공하는 것이 좋습니다.

CTB:
* snakefile에서 acc 대 accession 참고
* INPUT에 대한 반복 패턴은 있지만 OUTPUT에는 없음 - 그러나 glob_wildcards 대 wildcard 대 expand!
* 샘플에 대한 사용 사례 논의, 레시피?
* 경고에 링크/경고 반복
* "glob_wildcards에 대해 더 자세히 논의합니다..." - 제약 조건, 와일드카드, 또 어디에 있습니까? 더 있습니까?
* multiext도 다루나요?

## 와일드카드와 `expand` - 몇 가지 마무리 생각

와일드카드와 결합된 `expand`는 매우 강력하고 유용합니다. 그러나 와일드카드와 마찬가지로 이 강력함에는 약간의 복잡성이 따릅니다. 다음은 이러한 기능이 결합되는 방식에 대한 간략한 설명입니다.

`expand` 함수는 패턴과 채울 값 목록에서 _만들 파일 목록_을 만듭니다.

규칙의 와일드카드는 이름이 패턴과 일치하는 파일을 만드는 _레시피_를 제공합니다.

일반적으로 Snakefile에서 `expand`를 사용하여 특정 패턴과 일치하는 파일 목록을 생성한 다음 와일드카드를 사용하여 해당 실제 파일을 생성하는 규칙을 작성합니다.

`expand`와 함께 사용할 값 목록은 텍스트 파일, CSV 파일 및 구성 파일을 포함하여 여러 곳에서 가져올 수 있습니다. 또한 실제로 있는 파일에서 값 목록을 _추출_하는 패턴을 사용하는 `glob_wildcards`에서도 가져올 수 있습니다.

## 링크 및 참고 자료

* [expand에 대한 snakemake 참조 문서](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#the-expand-function)
* [Python `itertools`](https://docs.python.org/3/library/itertools.html) 문서.

[end of src/beginner+/expand.md]

[start of src/beginner+/input-and-output-blocks.md]
# `input:` 및 `output:` 블록

@@ 이것들은 지시문이 아니라 주석이며, 이것이 `{output}`을 사용하도록 제안하는 이유라는 점을 어딘가에 메모하십시오.

@@ 하나의 출력을 원하면 규칙을 실행한다는 메모를 작성하십시오.

[2장](../chapter_2.md)에서 보았듯이 snakemake는 입력을 출력에 연결하여 규칙을 자동으로 "연결"합니다. 즉, snakemake는 원하는 출력을 생성하기 위해 _무엇을 실행해야 하는지_ 여러 단계가 걸리더라도 알아낼 것입니다.

[3장](../chapter_3.md)에서는 또한 snakemake가 `input:` 및 `output:` 블록의 내용을 기반으로 셸 명령에서 `{input}` 및 `{output}`을 채운다는 것을 보았습니다. 이는 [6장](../chapter_6.md)에서와 같이 규칙을 일반화하기 위해 와일드카드를 사용할 때 더욱 유용해지며, 여기서 와일드카드 값은 `{input}` 및 `{output}` 값으로 올바르게 대체됩니다.

입력 및 출력 블록은 snakemake 워크플로의 핵심 구성 요소입니다. 이 장에서는 입력 및 출력 블록의 사용에 대해 좀 더 포괄적으로 논의할 것입니다.

## 입력 및 출력 제공

이전에 보았듯이 snakemake는 쉼표로 구분된 목록을 통해 여러 입력 및 출력 값을 기꺼이 받아들이고 셸 블록의 문자열로 대체합니다.

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic}}
```

이것들이 `{input}` 및 `{output}`을 사용하여 셸 명령으로 대체되면 공백으로 구분된 순서 있는 목록으로 바뀝니다. 예를 들어 위의 셸 명령은 먼저 `file1.txt file2.txt`를 인쇄한 다음 `output file1.txt output file2.txt`를 인쇄한 후 `touch`를 사용하여 빈 출력 파일을 만듭니다.

이 예에서는 또한 `:q`를 사용하여 셸 명령에 대한 파일 이름을 따옴표로 묶도록 snakemake에 요청하고 있습니다. 즉, 공백, 작은따옴표나 큰따옴표와 같은 문자 또는 특수 의미를 가진 기타 문자가 있는 경우 [Python의 shlex.quote 함수](https://docs.python.org/3/library/shlex.html#shlex.quote)를 사용하여 올바르게 이스케이프됩니다. 예를 들어, 여기서 두 출력 파일 모두 공백을 포함하므로 `touch {output}`은 올바른 두 파일인 `output file1.txt` 및 `output file2.txt` 대신 `output`, `file1.txt`, `file2.txt`라는 세 개의 파일을 만듭니다.

**`{...:q}`로 파일 이름을 따옴표로 묶는 것은 셸 블록에서 실행되는 모든 항목에 항상 사용해야 합니다.** 해롭지 않으며 심각한 버그를 예방할 수 있습니다!

~~~admonish info title='쉼표를 어디에 (그리고 넣어야 할까요)?'

위의 코드 예제에서 `"file2.txt"`와 `"output file2.txt"` 뒤에 쉼표가 있는 것을 알 수 있습니다.

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic}}
```

이것들이 필수인가요? **아니요.** 위의 코드는 다음과 같습니다.

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic2}}
```

여기서 입력 및 출력의 마지막 줄 뒤에는 쉼표가 없습니다.

일반적인 규칙은 다음과 같습니다. 목록의 항목을 구분하려면 내부 쉼표가 필요합니다. 그렇지 않으면 문자열이 서로 연결됩니다. 즉, `"file1.txt" "file2.txt"`는 줄 바꿈이 있더라도 `"file1.txtfile2.txt"`가 됩니다! 그러나 마지막 파일 이름 뒤에 오는 쉼표는 선택 사항이며 무시됩니다.

왜죠!? 이것들은 _Python 튜플_이며 원하는 경우 후행 쉼표를 추가할 수 있습니다. `a, b, c,`는 `a, b, c`와 동일합니다. 해당 구문에 대한 자세한 내용은 [여기](../appendix/python.md)에서 읽을 수 있습니다(CTB 특정 섹션에 대한 링크).

그렇다면 왜 후행 쉼표를 추가할까요?! 후행 쉼표를 사용하는 것이 좋습니다. 쉼표를 추가하는 것을 잊지 않고 새 입력 또는 출력을 쉽게 추가할 수 있기 때문입니다. 이것은 제가 자주 저지르는 실수입니다! 이것은 (작고 간단하지만 여전히 유용한) _방어적 프로그래밍_의 예이며, 여기서 선택적 구문 규칙을 사용하여 일반적인 실수를 방지할 수 있습니다.

~~~

## 입력과 출력은 _정렬된 목록_입니다.

0부터 시작하는 대괄호를 사용하여 목록으로 인덱싱하여 개별 입력 및 출력 항목을 참조할 수도 있습니다.

```python
rule example:
   ...
   shell: """
       echo first input is {input[0]:q}
       echo second input is {input[1]:q}
       echo first output is {output[0]:q}
       echo second output is {output[1]:q}
       touch {output}
   """
```

그러나 **이것은 깨지기 쉽기 때문에 권장하지 않습니다.** 입력 및 출력의 순서를 변경하거나 새 입력을 추가하면 인덱스를 일치하도록 조정해야 합니다. 목록의 인덱스 수와 위치에 의존하는 것은 오류가 발생하기 쉽고 나중에 Snakefile을 변경하기 어렵게 만듭니다!

## 입력 및 출력 파일에 키워드 사용

_키워드_ 구문을 사용하여 특정 입력 및 출력을 명명한 다음 `input.` 및 `output.` 접두사를 사용하여 참조할 수도 있습니다. 다음 Snakefile 규칙은 이를 수행합니다.
```python
{{#include ../../code/examples/input_output.quoting/snakefile.names}}
```

여기서 입력 블록의 `a`와 `b`, 출력 블록의 `a`와 `c`는 입력 및 출력 파일의 키워드 이름입니다. 셸 명령에서 각각 `{input.a}`, `{input.b}`, `{output.a}`, `{output.c}`로 참조할 수 있습니다. 유효한 변수 이름을 사용할 수 있으며, 위에서 `input.a`와 `output.a`가 서로 다른 값인 것처럼 충돌 없이 입력 및 출력 블록에서 동일한 이름을 사용할 수 있습니다.

**이것은 특정 입력 및 출력 파일을 참조하는 권장 방법입니다.** 읽기 쉽고, 재정렬이나 추가에 강력하며, (아마도 가장 중요하게는) 각 입력 및 출력의 _목적_을 독자(미래의 자신 포함)에게 안내하는 데 도움이 될 수 있습니다.

셸 코드에서 잘못된 키워드 이름을 사용하면 오류 메시지가 표시됩니다. 예를 들어 다음 코드는
```python
{{#include ../../code/examples/input_output.quoting/snakefile.names.broken:content}}
```
다음 오류 메시지를 표시합니다.
```
AttributeError: 'InputFiles' object has no attribute 'z', when formatting the following:

       echo first input is {input.z:q}

```

## 예: 유연한 명령줄 작성

특정 입력을 참조할 수 있는 것이 특히 유용한 한 가지 예는 입력 파일 이름을 선택적 인수로 지정해야 하는 파일에서 프로그램을 실행할 때입니다. 이러한 프로그램 중 하나는 페어드 엔드 입력 읽기에서 실행될 때 `megahit` 어셈블러입니다. 다음 Snakefile을 고려하십시오.

```python
{{#include ../../code/examples/input_output.megahit/Snakefile:content}}
```

여기 셸 명령에서 입력 읽기를 두 개의 개별 파일로 제공해야 하며, 하나 앞에는 `-1`을, 두 번째 앞에는 `-2`를 붙여야 합니다. 보너스로 결과 셸 명령은 매우 읽기 쉽습니다!

## 입력 함수 및 고급 기능

Python 프로그래밍에 의존하는 입력 및 출력의 고급 사용법이 많이 있습니다. 예를 들어, 아래와 같이 동적으로 값을 _생성_하기 위해 호출되는 Python 함수를 정의할 수 있습니다.

```python
{{#include ../../code/examples/input_output.quoting/snakefile.func:content}}
```

`output5.txt`를 만들도록 요청하면 이 규칙은 입력으로 `file25.txt`를 찾습니다.

이 기능은 [와일드카드](wildcards.md)에 대한 지식과 Python에 대한 약간의 지식에 의존하므로 이에 대한 논의는 나중에 미루겠습니다!

## 참조 및 링크

* [규칙에 대한 Snakemake 매뉴얼 섹션](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-and-rules)

[end of src/beginner+/input-and-output-blocks.md]

[start of src/beginner+/params-blocks.md]
# `params:` 블록과 `{params}`

이전에 보았듯이 [입력 및 출력 블록](input-and-output-blocks.md)은 snakemake가 작동하는 방식의 핵심입니다. 이를 통해 snakemake는 원하는 출력을 만드는 데 필요한 입력을 기반으로 규칙을 자동으로 연결할 수 있습니다. 그러나 입력 및 출력 블록은 특정 방식으로 제한됩니다. 가장 구체적으로 입력 및 출력 블록의 모든 항목은 _반드시_ 파일 이름이어야 합니다. 그리고 snakemake가 작동하는 방식 때문에 입력 및 출력 블록에 지정된 파일 이름은 워크플로가 해당 규칙을 지나 진행하려면 존재해야 합니다.

셸 명령은 파일 이름 이외의 매개변수를 사용해야 하는 경우가 많으며 이러한 매개변수는 snakemake에서 계산할 수 있거나 계산해야 하는 값일 수 있습니다. 따라서 snakemake는 셸 블록에서 파일 이름이 _아닌_ 매개변수 문자열을 제공하는 데 사용할 수 있는 `params:` 블록도 지원합니다. 아래에서 볼 수 있듯이 이러한 블록은 사용자 구성 가능 매개변수뿐만 아니라 Python 코드로 자동으로 계산할 수 있는 매개변수를 포함하여 다양한 용도로 사용할 수 있습니다.

## params 블록의 간단한 예

다음을 고려하십시오.
```python
{{#include ../../code/examples/params.basic/snakefile.params}}
```

여기서 값 `5`는 `params:` 블록의 이름 `val`에 할당된 다음 `shell:` 블록의 이름 `{params.val}` 아래에서 사용할 수 있습니다. 이는 [입력 및 출력 블록에서 키워드 사용](input-and-output-blocks.md#using-keywords-for-input-and-output-files)과 유사하지만 입력 및 출력 블록과 달리 params 블록에서는 키워드를 _반드시_ 사용해야 합니다.

이 예에서는 기능상의 이득은 없지만 가독성에서는 약간의 이득이 있습니다. 구문을 통해 `val`이 셸 블록의 세부 정보를 이해하지 않고도 수정할 수 있는 조정 가능한 매개변수임을 명확하게 알 수 있습니다.

## Params 블록은 와일드카드에 액세스할 수 있습니다.

`input:` 및 `output:` 블록과 마찬가지로 와일드카드 값은 `wildcards` 접두사를 사용하지 않고 `params:` 블록에서 직접 사용할 수 있습니다. 예를 들어, 이는 표준 [문자열 서식 지정 작업](string-formatting.md)을 사용하여 문자열에서 사용할 수 있음을 의미합니다.

이는 셸 명령이 파일 이름 이외의 것을 사용해야 할 때 유용합니다. 예를 들어, `bowtie` 읽기 정렬 소프트웨어는 `-S`를 통해 출력 SAM 파일의 _접두사_를 사용하므로 `bowtie ... -S {output}`으로 파일 이름을 올바르게 지정할 수 없습니다. 대신 다음과 같이 `{params.prefix}`를 사용할 수 있습니다.
```python
{{#include ../../code/examples/params.basic/snakefile.params_wildcards:content}}
```
여기서 `-S {output}`을 사용하면 `reads.sam.sam`이라는 파일이 생성됩니다!

## Params 블록은 다양한 기타 기능도 지원합니다.

CTB는 여기 또는 나중에 확장됩니다.

* 구성 값 가져오기 (확장 시 언급됨)
* [입력 함수 및 params 함수](../recipes/params-functions.md)
* megahit의 예로 쉼표로 구분된 값 사용? 예: -r 1,2,3.

## 링크 및 참고 자료:

* Snakemake 문서: [규칙에 대한 파일이 아닌 매개변수](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#non-file-parameters-for-rules)

[end of src/beginner+/params-blocks.md]

[start of src/beginner+/string-formatting.md]
# 문자열 서식 지정 "미니언어"

알아야 할 약 5가지 사항;
Q: 이것이 `expand`와 어떻게 교차합니까?

파이썬에서/와 상호 작용하는 것에 대한 내용을 추가해야 할 수도 있습니다.
* snakemake의 f 문자열 대 템플릿
* 문자열 "상수" 등

https://docs.python.org/3/library/string.html#formatspec

* 인용
* 키에 대한 문자열 템플릿에서 따옴표 사용 (또는 그렇게 하지 않음)
* 작업
* `{` 및 `}` 이스케이프

[end of src/beginner+/string-formatting.md]

[start of src/beginner+/syntax.md]
# Snakefiles의 기본 구문 규칙

* 문자열 - `'`과 `"`은 동일하며 일치하는 것을 사용해야 합니다.
* 후행 ,는 괜찮습니다.
* 들여쓰기 및 공백
* 파이썬 리스트, 딕셔너리

[end of src/beginner+/syntax.md]

[start of src/beginner+/targets.md]
# 명령줄에서 규칙 실행 및 대상 선택

snakemake에서 대상을 지정하는 방법은 간단하지만 세부 사항에서 많은 복잡성을 유발할 수 있습니다.

* 핵심 사항: 명령줄에 입력하는 내용("대상")은 snakefile의 미러 이미지입니다.
* snakefile 구성은 이를 반영할 수 있거나 반영해야 합니다.
* 규칙 이름과 파일 이름의 차이, 와일드카드 규칙과 그렇지 않은 규칙.

언어 사용: "의사 규칙"

snakemake 문서 링크:
https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#targets-and-aggregation

설정:
```
default_target: True
```

## 기본 대상

`snakemake -j 1`만 실행하면 snakemake는 가장 먼저 만나는 규칙을 실행합니다. 이는 @@로 조정할 수 있습니다.

이를 사용하는 일반적인 방법은 Snakefile 상단에 다음과 같은 'all' 규칙을 제공하는 것입니다.
```python
rule all:
    input:
        ...
```
일반적으로 이 규칙에는 하나 이상의 입력 파일이 포함되며 다른 규칙 블록은 없습니다. 예를 들어, [11장](../chapter_11.md)에서 기본 규칙은 다음과 같습니다.

이는 출력이나 셸 명령이 없는 규칙의 경우 snakemake가 규칙 전제 조건(즉, 입력 파일 생성)을 충족하기 위해 작동하기 때문이며, 이는 기본 규칙에 필요한 전부입니다.

따라서 종종 `all`이라고 명명되는 기본 규칙에는 워크플로에서 생성해야 하는 모든 "기본" 출력 파일 목록이 있는 단일 입력 블록이 포함되어야 합니다.

## 구체적인 대상: 규칙 이름 사용 대 파일 이름 사용

snakemake는 명령줄에서 규칙 이름 및/또는 파일 이름을 어떤 혼합으로든 기꺼이 받아들입니다. 특정 순서로 실행하도록 보장하지는 않지만 일반적으로 명령줄에 지정된 순서대로 실행합니다.

예를 들어, [11장](../chapter_11.md)의 Snakefile의 경우 `snakemake -j 1 compare_genomes`를 실행하여 `compare_genomes` 규칙만 실행하거나 `plot_comparison`을 추가하여 `compare_genomes`와 `plot_comparison`을 모두 실행하거나, `plot_comparison`이 `compare_genomes`의 출력에 의존하므로 어쨌든 `compare_genomes`를 실행하는 `plot_comparison`만 실행할 수 있습니다.

## 파일 이름을 사용하여 와일드카드 대상 실행

와일드카드가 포함된 규칙은 규칙 이름으로 실행할 수 없습니다. 왜냐하면 snakemake가 와일드카드를 채울 충분한 정보가 없기 때문입니다.

따라서 `snakemake -j 1 sketch_genomes`를 실행할 수 없습니다. 왜냐하면 해당 규칙에는 와일드카드가 있기 때문입니다. 규칙을 실행하려면 snakemake가 `accession` 와일드카드를 채워야 하며, 규칙 이름만으로는 충분하지 않습니다.

그러나 파일 이름을 사용하여 와일드카드 대상을 실행할 수 있습니다! `snakemake -j 1 GCF_000017325.1.fna.gz.sig`를 실행하면 snakemake는 해당 형식의 출력 파일을 생성하는 규칙(이 경우 `sketch_genome` 규칙)을 찾아 지정된 출력 파일 이름에서 와일드카드를 채워 실행합니다.

따라서 snakemake는 와일드카드가 포함되지 않은 한 규칙 이름으로 규칙을 기꺼이 실행합니다. 또는 해당 파일을 생성하는 규칙을 찾을 수 있는 한 지정된 파일을 생성하는 데 필요한 규칙을 찾아 실행합니다. 또는 혼합하여 실행합니다.

## 여러 구체적인 대상으로 워크플로 구성

특정 파일 집합을 빌드하는 여러 구체적인 대상 이름을 제공할 수 있습니다. 이는 워크플로를 빌드하거나 디버깅할 때 유용합니다.

[11장](../chapter_11.md)의 Snakefile을 다시 고려하십시오. `sourmash compare`를 실행하는 규칙과 출력 플롯을 생성하는 규칙이 있지만 서명 파일_만_ 생성하는 규칙은 없습니다.

이러한 규칙을 쉽게 추가할 수 있습니다. `all` 규칙 아래 어딘가에 다음을 추가합니다.
```
rule build_sketches:
    input:
        expand("{acc}.fna.gz.sig", acc=ACCESSIONS)
```
그런 다음 `snakemake -j 1 build_sketches`를 실행하면 4개의 .sig 파일이 생성되고 다른 작업은 수행되지 않습니다.

이것과 `compare_genomes` 규칙의 차이점은 `compare_genomes`가 `sourmash compare`도 실행한다는 것입니다.

@CTB: 최상위 수준의 레시피

## snakefile 구성에 대한 조언

* 기본 규칙을 제공합니다.
* 이름이 잘 지정된 하나 이상의 구체적인 규칙을 제공합니다.
* 파일 이름 레이아웃이나 규칙 이름을 문서 없이 기억할 것이라고 (자신을 포함하여) 기대하지 마십시오 ;).

[end of src/beginner+/targets.md]

[start of src/beginner+/visualizing.md]
# 워크플로 시각화

[end of src/beginner+/visualizing.md]

[start of src/beginner+/wildcards.md]
# 와일드카드를 사용하여 규칙 일반화

[6장](../chapter_6.md)에서 보여주듯이, 입력과 출력 사이에 반복되는 하위 문자열이 있는 경우 이를 와일드카드로 추출할 수 있습니다. 즉, 특정 입력에서 특정 출력을 만드는 규칙에서 패턴과 일치하는 모든 입력/출력 집합에서 작동하는 규칙으로 전환할 수 있습니다.

예를 들어 다음 코드는 특정 게놈에서 단일 sourmash 스케치를 만듭니다.

```python
rule sketch_genomes_1:
    input:
        "genomes/GCF_000017325.1.fna.gz",
    output:
        "GCF_000017325.1.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} --name-from-first
    """
```

이 규칙은 `.fna.gz`로 끝나는 *모든* 게놈에 대해 동일한 작업을 수행합니다!

```python
rule sketch_genomes_1:
    input:
        "genomes/{accession}.fna.gz",
    output:
        "{accession}.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """
```

여기서 `{accession}`은 `genomes/` 디렉터리 아래에 있고 `.fna.gz`로 끝나는 모든 파일 이름에 대해 필요에 따라 "채워지는" 와일드카드입니다.

Snakemake는 간단한 _패턴 일치_를 사용하여 `{accession}`의 값을 결정합니다. `.fna.gz.sig`로 끝나는 파일 이름을 요청하면 snakemake는 접두사를 가져온 다음 일치하는 입력 파일 `genomes/{accession}.fna.gz`를 찾고 그에 따라 `{input}`을 채웁니다.

와일드카드는 매우 유용하며 이를 사용하면 많은 경우 수백 또는 수천 개의 파일을 생성할 수 있는 단일 규칙을 작성할 수 있습니다! 그러나 고려해야 할 몇 가지 미묘한 점이 있습니다. 이 장에서는 이러한 미묘한 점 중 가장 중요한 것을 다루고 자세한 내용을 배울 수 있는 링크를 제공합니다.

## 와일드카드 규칙

먼저 와일드카드에 대한 몇 가지 기본 규칙을 살펴보겠습니다.

### 와일드카드는 원하는 출력에 의해 결정됩니다.

와일드카드의 첫 번째이자 가장 중요한 규칙은 다음과 같습니다. snakemake는 생성하도록 요청받은 파일 이름을 기반으로 와일드카드 값을 채웁니다.

다음 규칙을 고려하십시오.

```python
{{#include ../../code/examples/wildcards.output/snakefile.output}}
```
출력 블록의 와일드카드는 `.a.out`으로 끝나는 _모든_ 파일과 일치하며 관련 셸 명령이 이를 만듭니다! 이것은 강력하면서도 제약적입니다. 접미사 `.a.out`으로 모든 파일을 만들 수 있지만 파일을 만들도록 _요청_해야 합니다.

이는 이 규칙을 사용하려면 `.a.out`으로 끝나는 파일이 필요한 입력으로 있는 다른 규칙이 있어야 함을 의미합니다. (명령줄에서 이러한 파일을 명시적으로 요청할 수도 있습니다. CTB 문서 링크.) snakemake가 와일드카드 값을 추측할 다른 방법은 없습니다. snakemake는 명시적인 것이 암시적인 것보다 낫다는 격언을 따르며 원하는 파일이 생성될 것이라고 추측하지 않습니다.

예를 들어, 위의 규칙은 `.a.out`으로 끝나는 하나 이상의 파일 이름을 요청하는 다른 규칙과 쌍을 이룰 수 있습니다.
```python
rule make_me_a_file:
    input:
        "result1.a.out",
        "result2.a.out",
```

이는 또한 규칙에 와일드카드를 넣으면 더 이상 규칙 이름으로 해당 규칙을 실행할 수 없음을 의미합니다. 대신 파일 이름을 요청해야 합니다. 와일드카드가 포함된 규칙을 실행하려고 하지만 만들려는 파일 이름을 알려주지 않으면 다음이 표시됩니다.
```
Target rules may not contain wildcards.
```

와일드카드 규칙으로 작업하는 일반적인 방법 중 하나는 `expand`를 사용하여 원하는 파일 목록을 구성하는 다른 규칙을 갖는 것입니다. 이는 종종 와일드카드 목록을 로드하기 위해 `glob_wildcards`와 쌍을 이룹니다. 아래의 접두사로 파일 이름 바꾸기 레시피 또는 [`expand`를 사용하여 파일 이름 생성](expand.md) 장을 참조하십시오.

### 규칙에 사용된 모든 와일드카드는 `output:` 블록의 와일드카드와 일치해야 합니다.

snakemake는 `output:` 블록의 와일드카드를 사용하여 규칙의 다른 곳에서 와일드카드를 채우므로 하나 이상의 출력에서 언급된 와일드카드만 사용할 수 있습니다.

이는 `input:` 블록에 사용된 모든 와일드카드가 `output:`에 있어야 함을 의미합니다. 다음 예제를 고려하십시오. 여기서 입력 블록에는 출력 블록에서 사용되지 않는 와일드카드 `analysis`가 포함되어 있습니다.

```python
# 이것은 작동하지 않습니다:

rule analyze_sample:
    input: "{sample}.x.{analysis}.in"
    output: "{sample}.out"
```

이는 snakemake가 _입력_ 블록에서 `analysis` 와일드카드를 채우는 방법을 모르기 때문에 작동하지 않으며 다음과 같은 오류가 발생합니다.
```
WildcardError in line 1 of ...
Wildcards in input files cannot be determined from output files:
'analysis'
```

이렇게 생각해보십시오. 이것이 작동한다면 동일한 출력에 대해 여러 다른 입력 파일이 있을 수 있으며 snakemake는 원하는 출력을 생성하는 데 사용할 입력 파일을 선택할 방법이 없을 것입니다. 또한 출력은 사용된 입력에 따라 달라지므로 재현 불가능성이 발생합니다.

`input:` 블록의 모든 와일드카드는 `output:` 블록에 있어야 합니다. 그러나 `output:` 블록의 와일드카드가 `input:` 블록에 있을 필요가 없는 상황이 있습니다. 아래의 "셸 블록에서 사용할 매개변수를 결정하기 위해 와일드카드 사용"을 참조하십시오. 셸 블록에 대한 매개변수를 결정하기 위해 와일드카드를 사용하는 것에 대해 설명합니다!

### 와일드카드는 각 규칙에 로컬입니다.

와일드카드 이름은 규칙 블록 _내에서만_ 일치하면 됩니다. 와일드카드는 규칙 간에 공유되지 않습니다. 일관성과 가독성을 위해 여러 규칙에서 동일한 와일드카드 이름을 사용할 _수 있지만_ snakemake는 이를 독립적인 와일드카드로 처리하며 와일드카드 값은 공유되지 않습니다.

따라서 예를 들어 다음 두 규칙은 두 규칙 모두에서 동일한 와일드카드 `a`를 사용합니다.

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"

rule analyze_that:
    input: "{a}.second.txt"
    output: "{a}.third.txt"
```

그러나 이것은 별도의 규칙에서 _다른_ 와일드카드 `a`와 `b`를 사용하는 다음 두 규칙과 동일합니다.

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"

rule analyze_that:
    input: "{b}.second.txt"
    #        ^-- 다른 것 - 첫 번째 규칙의 'a' 대신 'b'
    output: "{b}.third.txt"
    #        ^-- 다른 것 - 첫 번째 규칙의 'a' 대신 'b'
```

와일드카드가 독립적이라는 규칙에는 한 가지 예외가 있습니다. 와일드카드 이름으로 와일드카드 일치를 제한하기 위해 [전역 와일드카드 제약 조건](../reference/wildcard-constraints.md)을 사용하는 경우 제약 조건은 Snakefile에서 해당 와일드카드 이름의 모든 사용에 적용됩니다. 그러나 와일드카드의 _값_은 독립적으로 유지됩니다. 제약 조건만 동일한 이름의 모든 와일드카드에서 공유됩니다.

<!-- CTB: 전역 와일드카드 제약 조건으로 직접 가리키도록 링크 수정. -->

와일드카드는 값에서 독립적이며 모든 규칙에서 다른 와일드카드를 사용할 수 있지만, Snakefile 전체에서 동일한 의미 체계를 갖도록 와일드카드를 선택하는 것이 좋은 규칙입니다. 예를 들어 항상 `sample`을 샘플 식별자를 참조하는 데 일관되게 사용하거나 `accession`을 데이터베이스 ID를 참조하는 데 사용합니다. 이렇게 하면 Snakefile을 더 쉽게 읽을 수 있습니다!

흥미로운 추가 사항: 와일드카드는 각 규칙에 로컬이므로 다른 규칙에서 패턴의 다른 부분을 자유롭게 일치시킬 수 있습니다! 아래의 "와일드카드 혼합 및 일치"를 참조하십시오.

### 와일드카드 네임스페이스는 `input:` 및 `output:` 블록에서 암시적으로 사용할 수 있지만 다른 블록에서는 사용할 수 없습니다.

규칙의 `input:` 및 `output:` 블록 내에서 와일드카드를 이름으로 직접 참조할 수 있습니다. 규칙의 다른 대부분의 부분에서 와일드카드를 사용하려면 `wildcards` 접두사를 사용해야 합니다. 이 규칙의 유일한 예외는 `params:` 블록입니다([`params:` 블록 및 `{params}`](params-blocks.md) 장 참조). 여기서 `wildcards`는 나중에 자세히 설명할 _네임스페이스_입니다. (CTB)

이 Snakefile을 고려하십시오.

```python
# 이것은 작동하지 않습니다:

rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {a}"
```

여기서 오류가 발생합니다.
```
NameError: The name 'a' is unknown in this context. Did you mean 'wildcards.a'?
```

오류에서 제안하는 것처럼 셸 블록에서 `wildcards.a`를 대신 사용해야 합니다.

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {wildcards.a}"
```

### 와일드카드는 어떤 식으로든 제한되지 않는 한 가능한 한 광범위하게 일치합니다.

와일드카드 패턴 일치는 _모든_ 문자에 대해 _가능한 가장 긴_ 일치를 선택하므로 약간 혼란스러운 동작이 발생할 수 있습니다. 다음을 고려하십시오.

```python
{{#include ../../code/examples/wildcards.greedy/snakefile.1}}
```

`something` 규칙에서 원하는 출력 파일 `x.y.z.gz`에 대해 `{prefix}`는 현재 `x.y`이고 `{suffix}`는 `z`입니다. 그러나 `{prefix}`가 `x`이고 접미사가 `y.z`인 것도 마찬가지로 유효합니다.

더 극단적인 예는 탐욕스러운 일치를 더욱 명확하게 보여줍니다.
```python
{{#include ../../code/examples/wildcards.greedy/snakefile.2}}
```
여기서 `{suffix}`는 단일 문자 `e`로 축소되고 `{prefix}`는 `longer_filenam`입니다!

와일드카드 일치에 대한 두 가지 간단한 규칙은 다음과 같습니다.
* 모든 와일드카드는 하나 이상의 문자와 일치해야 합니다.
* 그 후 와일드카드는 _탐욕스럽게_ 일치합니다. 각 와일드카드는 다음 와일드카드가 고려되기 전에 가능한 모든 것과 일치합니다.

이것이 와일드카드 일치를 제한하기 위해 [와일드카드 제약 조건](../reference/wildcard-constraints.md)을 사용하는 것이 좋은 이유입니다. 몇 가지 예는 아래의 "하위 디렉터리 및/또는 마침표를 피하기 위해 와일드카드 제한"을 참조하고 자세한 내용은 [와일드카드 제약 조건](../reference/wildcard-constraints.md) 장을 참조하십시오!

## 와일드카드의 몇 가지 예

### 여러 파일에 하나의 규칙 실행

와일드카드는 여러 파일에 동일한 간단한 규칙을 실행하는 데 사용할 수 있습니다. 이는 snakemake의 가장 간단하고 강력한 용도 중 하나입니다!

여러 파일을 압축하는 이 Snakefile을 고려하십시오.

```python
{{#include ../../code/examples/wildcards.many/Snakefile}}
```

이 Snakefile은 생성하려는 압축 파일 목록을 지정하고 와일드카드를 사용하여 입력 파일을 찾고 셸 블록을 채우는 데 필요한 패턴 일치를 수행합니다.

이 강력한 패턴의 더 많은 예는 [Snakefile로 for 루프 대체](../recipes/replacing-for.md)를 참조하십시오!

그렇긴 하지만 이 Snakefile은 작성하기 불편하고 다소 오류가 발생하기 쉽습니다.

* 파일이 많은 경우 개별적으로 작성하는 것이 성가십니다!
* 파일 목록을 생성하려면 직접 이름을 변경해야 하므로 오류가 발생하기 쉽습니다!

Snakemake는 이러한 문제를 해결하는 데 도움이 되는 몇 가지 기능을 제공합니다. 텍스트 파일이나 스프레드시트에서 파일 목록을 로드하거나 `glob_wildcards`를 사용하여 디렉터리에서 직접 목록을 가져올 수 있습니다. 그리고 `expand`를 사용하여 대량으로 이름을 변경할 수 있습니다. 몇 가지 예를 보려면 계속 읽으십시오!

```admonish info title='이것이 gzip을 직접 사용하는 것보다 나은 이유는 무엇입니까?'

`gzip -k original/*`를 사용하여 동일한 작업을 수행할 수 있지만 파일을 최종 위치로 이동해야 합니다.

`gzip -k original/*`을 사용하는 것과 snakemake를 사용하는 것은 어떻게 다릅니까? 그리고 더 낫습니까?

첫째, 결과는 다르지 않지만(두 방법 모두 원하는 입력 파일 집합을 압축합니다!) `gzip -k` 명령은 *직렬*로 실행되며 *병렬*로 실행되지 않습니다. 즉, gzip은 기본적으로 한 번에 하나의 파일을 압축합니다. Snakefile은 `-j`로 지정한 만큼의 프로세서를 사용하여 `gzip_file` 규칙을 _병렬_로 실행합니다. 즉, 이러한 파일이 매우 많은 경우(생물정보학에서 일반적인 문제!) snakemake 버전은 잠재적으로 몇 배 더 빠르게 실행될 수 있습니다.

둘째, `gzip -k original/*`로 명령줄에서 많은 파일을 지정하는 것은 `gzip`에서는 작동하지만 모든 셸 명령에서 작동하는 것은 아닙니다. 일부 명령은 한 번에 하나의 파일에서만 실행됩니다. `gzip`은 하나 또는 여러 파일을 제공하든 관계없이 작동합니다. 다른 많은 프로그램은 여러 입력 파일에서 작동하지 않습니다. 예를 들어 FASTQ 파일을 전처리하기 위한 `fastp` 프로그램은 한 번에 하나의 데이터 세트에서 실행됩니다. (snakemake가 사용자 지정 명령줄을 유연하게 작성할 수 있는 방법을 제공한다는 점도 언급할 가치가 있습니다. 몇 가지 예는 [입력 및 출력 블록](input-and-output-blocks.md) 장을 참조하십시오.)

셋째, Snakefile에서는 규칙이 실행된 후 존재할 것으로 예상되는 파일을 명시적으로 지정하는 반면, `gzip -k original/*`만 실행하면 셸에 `original/`의 모든 파일을 압축하도록 요청하는 것입니다. `original` 하위 디렉터리에서 실수로 파일을 삭제한 경우 gzip은 이를 알지 못하고 불평하지 않지만 snakemake는 불평합니다. 이것은 반복적으로 나타나는 주제입니다. 가능한 실수를 경고받을 수 있도록 예상하는 파일을 명시적으로 지정하는 것이 더 안전한 경우가 많습니다.

그리고 넷째, Snakefile 접근 방식을 사용하면 출력 파일의 이름을 흥미로운 방식으로 바꿀 수 있습니다. `gzip -k original/*`을 사용하면 원래 파일 이름에 갇히게 됩니다. 이것은 다음 하위 섹션에서 살펴볼 기능입니다!
```

### `glob_wildcards`를 사용하여 접두사로 파일 이름 바꾸기

다음과 같이 이름이 지정된 파일 집합을 고려하십시오.

```
F3D141_S207_L001_R1_001.fastq
F3D141_S207_L001_R2_001.fastq
```
`original/` 하위 디렉터리 내에 있습니다.

이제 `.fastq` 앞에 있는 `_001` 접미사를 모두 제거하도록 이름을 바꾸고 싶다고 가정합니다. 와일드카드를 사용하면 매우 쉽습니다!

아래 Snakefile은 `glob_wildcards`를 사용하여 디렉터리에서 파일 목록을 로드한 다음 `renamed/` 하위 디렉터리 아래에 새 이름으로 복사본을 만듭니다. 여기서 `glob_wildcards`는 디렉터리에서 사용 가능한 파일 집합 _에서_ `{sample}` 패턴을 추출합니다.

```python
{{#include ../../code/examples/wildcards.renaming_simple/Snakefile}}
```

이 Snakefile은 또한 `expand`를 사용하여 로드된 목록을 원하는 파일 이름 집합으로 다시 작성합니다. 즉, 더 이상 파일 목록을 직접 작성할 필요가 없습니다. snakemake가 하도록 할 수 있습니다! `expand`에 대한 자세한 내용은 [`expand`를 사용하여 파일 이름 생성](expand.md)에서 설명합니다.

여기서 `cp` 대신 `mv`를 수행하면 실행 후 `glob_wildcards`가 더 이상 변경된 파일을 선택하지 않습니다.

이 Snakefile은 디렉터리 자체에서 파일 목록을 로드하므로 입력 파일이 실수로 삭제되면 snakemake가 불평하지 않습니다. 파일 이름을 바꿀 때 이것이 문제를 일으킬 가능성은 거의 없습니다. 그러나 워크플로를 실행할 때는 문제를 피하기 위해 텍스트 파일이나 스프레드시트에서 샘플 목록을 로드하는 것이 좋습니다.

<!-- (CTB 레시피를 가리킴). -->

또한 이 Snakefile은 `original/`의 모든 파일과 모든 하위 디렉터리를 찾아 이름을 바꿉니다! 이는 `glob_wildcards`가 기본적으로 모든 하위 디렉터리를 포함하기 때문입니다. 와일드카드 제약 조건을 사용하여 하위 디렉터리에서 로드하는 것을 방지하는 방법은 아래 다음 섹션을 참조하십시오.

### 하위 디렉터리 및/또는 마침표를 피하기 위해 와일드카드 제한

와일드카드는 '/'를 포함한 모든 문자열과 일치하므로 `glob_wildcards`는 하위 디렉터리의 파일을 자동으로 찾고 '.' 및 '-'와 같은 파일 이름의 일반적인 구분 기호와 일치하도록 "확장"됩니다. 이를 일반적으로 "탐욕스러운 일치"라고 하며 때로는 와일드카드가 원하는 것보다 훨씬 더 많은 파일 이름과 일치하게 됨을 의미합니다! 와일드카드 제약 조건을 사용하여 와일드카드 일치를 제한할 수 있습니다.

두 가지 일반적인 와일드카드 제약 조건이 아래에 개별적으로 그리고 조합하여 표시됩니다. 첫 번째 제약 조건은 하위 디렉터리의 파일을 피하고 두 번째 제약 조건은 마침표를 피합니다.

```python
{{#include ../../code/examples/wildcards.basic_constrain/Snakefile:constraints}}
```

자세한 내용과 세부 정보는 [와일드카드 제약 조건](../reference/wildcard-constraints.md)을 참조하십시오.

## 고급 와일드카드 예제

### 여러 와일드카드를 사용하여 파일 이름 바꾸기

위의 첫 번째 이름 바꾸기 예제는 파일의 접미사만 변경하고 단일 와일드카드를 사용할 수 있을 때 매우 잘 작동하지만 더 복잡한 이름 바꾸기를 수행하려면 여러 와일드카드를 사용해야 할 수 있습니다.

`F3D141_S207_L001_R1_001.fastq` 형식의 파일 이름을 `F3D141_S207_R1.fastq`로 바꾸고 싶다고 가정합니다. 안타깝게도 단일 와일드카드로는 그렇게 할 수 없지만 다음과 같이 두 개를 사용할 수 있습니다.


```python
{{#include ../../code/examples/wildcards.renaming/Snakefile}}
```

이 코드에서는 세 가지 새로운 기능을 사용하고 있습니다.

첫째, `glob_wildcards`는 여러 와일드카드와 일치하며 결과 값을 단일 결과 변수(여기서는 `files`)에 넣습니다.

둘째, 일치하는 값은 두 개의 정렬된 목록 `files.sample`과 `files.r`에 배치되어 파일 이름에서 추출된 값이 쌍으로 일치합니다.

셋째, `expand`를 사용할 때 기본값인 `product`로 가능한 모든 조합을 만드는 대신 두 와일드카드 목록을 함께 "압축"하도록 요청하고 있습니다. `zip` 대 `product`에 대한 자세한 내용은 [`expand`를 사용하여 파일 이름 생성](expand.md)을 참조하십시오.

또한 이전 예와 마찬가지로 이 Snakefile은 `original/`의 모든 파일과 모든 하위 디렉터리를 찾아 이름을 바꿉니다!

링크:

* [제품 대신 zip을 사용하는 것에 대한 snakemake 설명서](https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do)

### 문자열 혼합 및 일치

와일드카드가 규칙에 로컬이라는 다소 직관적이지 않지만 매우 유용한 결과는 영리한 문자열 일치를 수행하여 일반 규칙과 더 구체적인 규칙을 혼합하고 일치시킬 수 있다는 것입니다.

여러 샘플의 읽기를 여러 참조에 매핑하고(규칙 `map_reads_to_reference`) SAM 파일을 BAM 파일로 변환하는 이 Snakefile을 고려하십시오.

<!-- CTB: 기능적인 Snakefile로 이전할까요? -->

```python
rule all:
    input:
        "sample1.x.ecoli.bam",
        "sample2.x.shewanella.bam",
        "sample1.x.shewanella.bam"

rule map_reads_to_reference:
    input:
        reads="{sample}.fq",
        reference="{genome}.fa",
    output:
        "{reads}.x.{reference}.sam"
    shell: "minimap2 -ax sr {input.reference} {input.reads} > {output}"

rule convert_sam_to_bam:
    input:
        "{filename}.sam"
    output:
        "{filename}.bam"
    shell: "samtools view -b {input} -o {output}
```

여기서 snakemake는 각 규칙에서 다른 와일드카드를 기꺼이 사용하고 패턴의 다른 부분과 일치시킵니다! 따라서,

* 규칙 `convert_sam_to_bam`은 `.bam` 및 `.sam` 접미사만을 기반으로 모든 SAM 파일을 BAM 파일로 일반적으로 변환합니다.

* 그러나 `map_reads_to_references`는 `{sample}.x.{reference}` 패턴과 일치하는 매핑 파일만 생성하며, 이는 다시 `{reference}.fa` 및 `{sample}.fastq`의 존재에 따라 달라집니다.

이것은 궁극적으로 snakemake가 문자열만 일치시키고 일치시키는 문자열의 구조에 대해 아무것도 "알지" 못하기 때문에 작동합니다. 그리고 규칙 전체에서 와일드카드를 기억하지도 않습니다. 따라서 snakemake는 한 규칙에서 와일드카드 집합 하나를 기꺼이 일치시키고 다른 규칙에서 다른 와일드카드 집합을 일치시킵니다!

### 셸 블록에서 사용할 매개변수를 결정하기 위해 와일드카드 사용.

파일 이름에 따라 _생성_할 내용의 매개변수가 결정되는 출력 파일을 생성하는 규칙을 빌드하기 위해 와일드카드를 사용할 수도 있습니다. 예를 들어 FASTQ 파일의 하위 집합을 생성하는 다음 예제를 고려하십시오.

```python
{{#include ../../code/examples/wildcards.subset/Snakefile}}
```

여기서 와일드카드는 입력 파일 이름이 아닌 출력 파일 이름에 _만_ 있습니다. 와일드카드 값은 snakemake가 `head`가 파일에서 선택할 줄 수를 결정하는 방법을 결정하는 데 사용됩니다!

이는 셸 명령에 여러 다른 매개변수를 제공하여 파일을 생성하는 데 매우 유용할 수 있습니다. 이를 "매개변수 스윕"이라고 합니다. 이에 대해서는 나중에 자세히 설명하겠습니다!

<!-- CTB XXX 참조.

CTB 링크:
* params 함수, params 람다?
* 이것과 확장을 사용한 매개변수 스윕
-->

## 와일드카드에 대해 생각하는 방법

와일드카드(`expand` 및 `glob_wildcards`와 함께)는 snakemake에서 가장 강력하고 유용한 기능 중 하나입니다. 간단한 패턴만을 기반으로 임의의 수의 파일에 규칙을 일반적으로 적용할 수 있습니다.

그러나 그 강력함에는 상당한 복잡성이 따릅니다!

궁극적으로 와일드카드는 모두 *문자열*과 *패턴*에 관한 것입니다. Snakemake는 패턴 일치를 사용하여 원하는 출력 파일에서 패턴을 추출한 다음 규칙의 다른 곳에서 해당 일치 항목을 채웁니다. 뒤따르는 복잡성의 대부분은 패턴 일치 및 채우기의 모호성을 피하는 것과 실제로 만들려는 모든 파일의 이름을 구성하는 쌍을 이루는 과제에서 비롯됩니다.

## 추가 참고 자료

참조: [와일드카드에 대한 snakemake 문서](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-wildcards).

[end of src/beginner+/wildcards.md]

[start of src/chapter_0.md]
# 설치 및 설정!

## 설정 및 설치

새 디렉터리에서 작업하는 것이 좋습니다.

[snakemake 설치](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) 및 [sourmash 설치](https://sourmash.readthedocs.io/en/latest/#installing-sourmash)가 필요합니다. 이를 위해 [mamba, miniforge/mambaforge를 통해](https://github.com/conda-forge/miniforge#mambaforge) 사용하는 것이 좋습니다.

### 데이터 가져오기:

다음 세 개의 파일을 다운로드해야 합니다.

* [GCF_000021665.1_ASM2166v1_genomic.fna.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/021/665/GCF_000021665.1_ASM2166v1/GCF_000021665.1_ASM2166v1_genomic.fna.gz)
* [GCF_000017325.1_ASM1732v1_genomic.fna.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/017/325/GCF_000017325.1_ASM1732v1/GCF_000017325.1_ASM1732v1_genomic.fna.gz)
* [GCF_000020225.1_ASM2022v1_genomic.fna.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/020/225/GCF_000020225.1_ASM2022v1/GCF_000020225.1_ASM2022v1_genomic.fna.gz)

그리고 `genomes/` 하위 디렉터리에 다음 이름으로 이름을 바꿉니다.
```
GCF_000017325.1.fna.gz
GCF_000020225.1.fna.gz
GCF_000021665.1.fna.gz
```

참고로, 올바른 이름으로 저장된 사본을 여기에서 다운로드할 수 있습니다. [osf.io/2g4dm/](https://osf.io/2g4dm/).

[end of src/chapter_0.md]

[start of src/chapter_1.md]
# 1장 - snakemake가 프로그램을 실행합니다!

생물정보학은 종종 시퀀싱 데이터를 특성화하고 줄이기 위해 다양한 프로그램을 실행하는 것을 포함하며, 저는 이를 돕기 위해 snakemake를 사용합니다.

### 첫 번째 간단한 snakemake 워크플로

다음은 간단하고 유용한 snakemake 워크플로입니다.
```python
{{#include ../code/section1/simple1.snakefile}}
```
`Snakefile`이라는 파일에 넣고 `snakemake -j 1`로 실행합니다.

그러면 세 게놈의 유사성 행렬과 계통수를 포함하는 출력 파일 `compare.mat.matrix.png`가 생성됩니다(그림 1 참조).

![유사성 행렬 및 계통수](images/2023-snakemake-slithering-section-1-mat.png)

이것은 기능적으로 이 세 명령을 `compare-genomes.sh` 파일에 넣고 `bash compare-genomes.sh`로 실행하는 것과 동일합니다.

```shell
sourmash sketch dna -p k=31 genomes/*.fna.gz --name-from-first

sourmash compare GCF_000021665.1.fna.gz.sig \
            GCF_000017325.1.fna.gz.sig GCF_000020225.1.fna.gz.sig \
            -o compare.mat

sourmash plot compare.mat
```

snakemake 버전은 이미 약간 더 좋습니다. 명령이 성공적으로 실행되면 격려를 해주고(멋진 녹색 텍스트로 "1/1 단계(100%) 완료"라고 표시됨) 명령이 실패하면 빨간색 텍스트로 알려줍니다.

하지만! 셸 스크립트 버전보다 snakemake 버전을 더욱 개선할 수 있습니다!

### 불필요한 명령 재실행 방지: 두 번째 snakemake 워크플로

`snakemake -j 1`로 snakemake를 호출할 때마다 명령이 실행됩니다. 하지만 대부분의 경우 이미 원하는 출력 파일이 있으므로 다시 실행할 필요가 없습니다!

snakemake가 규칙을 다시 실행하지 않도록 하려면 어떻게 해야 할까요?

셸 블록 앞에 `output:` 블록을 추가하여 예상되는 출력을 snakemake에 알려주면 됩니다.
```diff
<!-- cmdrun ../scripts/diff-trunc.py ../code/section1/simple1.snakefile ../code/section1/simple2.snakefile -->
```
이제 `snakemake -j 1`을 한 번 실행하면 명령이 실행됩니다. 하지만 다시 실행하면 "수행할 작업 없음(요청된 모든 파일이 있고 최신 상태임)"이라고 표시됩니다.

```admonish info title='코드 예제를 어떻게 읽어야 할까요?'
위의 코드 예제는 약간 이상하게 보입니다. 두 줄 앞에 '+'가 있고 녹색으로 표시되어 있습니다. 무슨 일일까요?

이것은 `diff` 프로그램에서 생성된 두 소스 코드 파일의 줄 단위 비교인 "diff"의 예입니다. 여기서 diff는 원래 코드 목록에 두 줄을 추가했음을 보여줍니다. 즉, '+'로 시작하는 두 줄입니다. 또한 원래 코드에 추가된 위치를 더 쉽게 볼 수 있도록 추가된 줄 위아래에 일부 컨텍스트를 추가합니다.

아래에서는 제거된 줄을 사용하는 예도 보여줄 것이며, 이는 첫 번째 위치에 '-'로 식별되고 빨간색으로 강조 표시됩니다.
```

이는 원하는 출력 파일인 `compare.mat.matrix.png`가 이미 존재하기 때문입니다. 따라서 snakemake는 아무것도 할 필요가 없다는 것을 알고 있습니다!

`compare.mat.matrix.png`를 제거하고 `snakemake -j 1`을 다시 실행하면 snakemake가 파일을 다시 기꺼이 만들어줍니다.
```shell
$ rm compare.mat.matrix.png
$ snakemake -j 1
```

따라서 snakemake를 사용하면 이미 원하는 파일을 생성한 경우 일련의 명령을 다시 실행하지 않도록 쉽게 만들 수 있습니다. 이것이 생물정보학 워크플로를 실행하기 위해 snakemake와 같은 워크플로 시스템을 사용하는 가장 좋은 이유 중 하나입니다. 셸 스크립트는 자동으로 명령을 다시 실행하지 않습니다.

### 실행해야 하는 명령만 실행

위의 마지막 Snakefile에는 세 가지 명령이 있지만 `compare.mat.matrix.png` 파일을 제거하면 마지막 명령만 다시 실행하면 됩니다. 처음 두 명령으로 만든 파일은 이미 존재하며 다시 만들 필요가 없습니다. 그러나 snakemake는 이를 알지 못합니다. 전체 규칙을 하나의 규칙으로 처리하고 실행할 필요가 없는 것을 파악하기 위해 셸 명령을 조사하지 않습니다.

이미 존재하는 파일을 다시 만들지 않으려면 Snakefile을 약간 더 복잡하게 만들어야 합니다.

먼저 명령을 세 개의 개별 규칙으로 나눕니다.
```python
{{#include ../code/section1/simple3.snakefile}}
```

여기서는 그다지 복잡한 작업을 수행하지 않았습니다. 자체 이름을 가진 두 개의 새 규칙 블록을 만들고 각 셸 명령에 자체 규칙 블록이 있도록 셸 명령을 분할했습니다.

snakemake에 세 가지 모두 실행하도록 지시할 수 있습니다.
```shell
snakemake -j 1 sketch_genomes compare_genomes plot_comparison
```
그러면 모두 성공적으로 실행됩니다!

그러나 우리는 snakemake가 일부 명령을 매번 실행하도록 되돌아왔습니다. `compare.mat.matrix.png`가 존재하기 때문에 `plot_comparison`을 매번 실행하지는 않지만 `sketch_genomes`와 `compare_genomes`는 반복적으로 실행합니다.

이것을 어떻게 고칠까요?

### 각 규칙에 출력 블록 추가

*각* 규칙에 출력 블록을 추가하면 snakemake는 출력을 업데이트해야 하는 규칙만 실행합니다(예: 존재하지 않기 때문).

그렇게 해봅시다.

```python
{{#include ../code/section1/simple4.snakefile}}
```
그리고 지금
```shell
snakemake -j 1 sketch_genomes compare_genomes plot_comparison
```
출력 파일이 여전히 있는 한 각 명령을 한 번만 실행합니다. 만세!

하지만 이것을 실행하려면 여전히 세 규칙의 이름을 모두 올바른 순서로 지정해야 합니다. 성가시네요! 다음에 수정합시다.

[end of src/chapter_1.md]

[start of src/chapter_10.md]
# 10장 - 기본 규칙 사용

이 섹션에서 Snakefile에 적용할 마지막 변경 사항은 기본 규칙이라고 하는 것을 추가하는 것입니다. 이것은 무엇이며 왜 필요할까요?

'왜'가 더 쉽습니다. 위에서는 snakemake에 특정 규칙 이름이나 파일 이름을 제공하는 데 주의를 기울였습니다. 그렇지 않으면 Snakefile의 첫 번째 규칙을 실행하는 것이 기본값이기 때문입니다. (파일에서 규칙 순서가 중요한 다른 방법은 없지만, 명령줄에서 규칙 이름이나 파일 이름을 제공하지 않으면 snakemake는 파일의 첫 번째 규칙을 실행하려고 합니다.)

이것은 기억하고 입력해야 할 것이 하나 더 있기 때문에 그다지 좋지 않습니다. 일반적으로 원하는 파일이나 파일을 생성하기 위해 `snakemake -j 1`만 실행할 수 있도록 하는 "기본 규칙"이라고 하는 것을 갖는 것이 좋습니다.

이것은 간단하게 수행할 수 있지만 약간 다른 구문이 필요합니다. 즉, 셸이나 출력 블록 없이 _오직_ `input`만 있는 규칙입니다. 다음은 파일의 첫 번째 규칙으로 넣어야 하는 Snakefile에 대한 기본 규칙입니다.

```python
rule all:
    input:
        "compare.mat.matrix.png"
```

이 규칙이 의미하는 바는 "파일 `compare.mat.matrix.png`를 원합니다."입니다. 이를 수행하는 방법에 대한 지침은 제공하지 않습니다. 파일의 나머지 규칙이 바로 그것입니다! 그리고 셸 블록이 없기 때문에 아무것도 _실행_하지 않으며, 출력 블록이 없기 때문에 아무것도 _생성_하지 않습니다.

여기서 논리는 간단하지만 간단하지는 않습니다. 이 규칙은 해당 입력이 존재할 때 성공합니다.

Snakefile 상단에 배치하면 `snakemake -j 1`을 실행하면 `compare.mat.matrix.png`가 생성됩니다. 해당 파일을 생성하는 것 _이외의_ 작업을 수행하지 않는 한 더 이상 명령줄에 규칙 이름이나 파일 이름을 제공할 필요가 없습니다. 이 경우 명령줄에 입력하는 모든 내용은 `rule all:`을 무시합니다.

[end of src/chapter_10.md]

[start of src/chapter_11.md]
# 11장 - 최종 Snakefile - 검토 및 논의

다음은 네 가지 게놈을 비교하기 위한 최종 Snakefile입니다.

이 snakemake 워크플로는 다음과 같은 기능을 가지고 있습니다.

* Snakefile 상단에 단일 액세션 목록이 있어 파일의 한 곳만 변경하여 더 많은 게놈을 추가할 수 있습니다. 이에 대한 자세한 논의는 [단일 패턴과 하나의 값 목록으로 `expand` 사용](../beginner+/expand.md#using-expand-with-a-single-pattern-and-one-list-of-values)을 참조하십시오.

* 워크플로는 입력 파일만 포함하는 "의사 규칙"인 기본 규칙 `all`을 사용합니다. 이것은 명령줄에 대상 없이 실행될 경우 snakemake가 실행할 기본 규칙입니다. 대상 및 Snakefile 구성에 대한 논의는 [명령줄에서 규칙 실행 및 대상 선택](./beginner+/targets.md)을 참조하십시오.

* 워크플로는 하나의 와일드카드 규칙 `sketch_genome`을 사용하여 `.fna.gz`로 끝나는 _여러_ 게놈 파일을 sourmash 서명 파일로 변환합니다. 와일드카드에 대한 논의는 [와일드카드를 사용하여 규칙 일반화](./beginner+/wildcards.md)를 참조하십시오.

* 또한 `sourmash compare`를 실행하는 데 필요한 게놈 서명의 전체 목록을 구성하기 위해 `expand`를 사용하는 규칙 `compare_genomes`가 있습니다. 다시 말하지만, 이에 대한 자세한 논의는 [단일 패턴과 하나의 값 목록으로 `expand` 사용](../beginner+/expand.md#using-expand-with-a-single-pattern-and-one-list-of-values)을 참조하십시오.

* 마지막 규칙 `plot_comparison`은 `compare_genomes`의 출력을 가져와 제공된 셸 명령을 통해 `sourmash plot`을 통해 PNG 이미지로 변환합니다.

```python
{{#include ../code/section2/interm6.snakefile}}
```

다음 섹션에서는 이 Snakefile에서 사용된 snakemake의 핵심 기능을 더 철저히 다루고, 더 복잡한 생물정보학 워크플로와 유용한 패턴 및 재사용 가능한 레시피를 소개합니다.

[end of src/chapter_11.md]

[start of src/chapter_2.md]
# 2장 - snakemake가 규칙을 연결합니다!

## `input:` 블록으로 규칙 연결

규칙에 필요한 _입력_ 파일에 대한 정보를 제공하여 snakemake가 규칙을 자동으로 연결하도록 할 수 있습니다. 그런 다음 특정 입력이 필요한 규칙을 실행하도록 snakemake에 요청하면 해당 입력을 출력으로 생성하는 규칙을 자동으로 파악하고 자동으로 실행합니다.

`plot_comparison` 및 `compare_genomes` 규칙에 입력 정보를 추가해 보겠습니다.

```python
{{#include ../code/section1/simple5.snakefile}}
```

이제 마지막 규칙을 실행하도록 snakemake에 요청하기만 하면 됩니다.
```shell
snakemake -j 1 plot_comparison
```
그러면 snakemake는 해당 입력 파일이 존재하지 않고 만들어야 하는 경우에만 다른 규칙을 실행합니다.

## 한 걸음 물러서서 보기

Snakefile은 이제 훨씬 길어졌지만 _그렇게_ 복잡하지는 않습니다. 우리가 한 일은 셸 명령을 별도의 규칙으로 나누고 각 규칙에 생성하는 파일(출력)과 실행하는 데 필요한 파일(입력)에 대한 정보를 주석으로 단 것입니다.

이렇게 하면 불필요하게 명령을 다시 실행할 필요가 없다는 장점이 있습니다. 현재 워크플로에서는 sourmash가 매우 빠르기 때문에 이것은 작은 장점일 뿐입니다. 하지만 각 단계에 1시간이 걸린다면 불필요한 단계를 피하면 작업 속도를 훨씬 빠르게 만들 수 있습니다!

그리고 나중에 보겠지만 이러한 규칙은 각각 다른 파일을 생성하는 워크플로에 통합할 수 있는 재사용 가능한 빌딩 블록입니다. 따라서 셸 명령을 개별 규칙으로 나누는 데에는 다른 좋은 이유가 있습니다!

[end of src/chapter_2.md]

[start of src/chapter_3.md]
# 3장 - snakemake는 중복을 피하도록 도와줍니다!

## `{input}` 및 `{output}`을 사용하여 반복되는 파일 이름 방지

이전 Snakefile을 보면 몇 가지 반복되는 파일 이름이 표시됩니다. 특히 `compare_genomes` 규칙에는 입력 블록에 세 개의 파일 이름이 있고 셸 블록에서 반복되며 `compare.mat`는 `compare_genomes`와 `plot_genomes` 모두에서 여러 번 반복됩니다.

`{input}` 및 `{output}`을 사용하여 파일 이름을 재사용하도록 snakemake에 지시할 수 있습니다. `{` 및 `}`는 snakemake에 이를 리터럴 문자열이 아니라 `input` 및 `output`의 값으로 대체되어야 하는 템플릿 변수로 해석하도록 지시합니다.

한 번 해봅시다!
```python
{{#include ../code/section1/simple6.snakefile}}
```

이 접근 방식은 처음부터 입력을 덜 할 뿐만 아니라 파일 이름을 한 곳에서만 편집하면 됩니다. 이렇게 하면 한 곳에서 파일 이름을 추가하거나 변경하고 다른 곳에서는 변경하지 않아 발생하는 실수를 방지할 수 있습니다. 제가 여러 번 저지른 실수입니다!

## snakemake를 사용하면 워크플로를 쉽게 다시 실행할 수 있습니다!

최신 데이터 파일과 소프트웨어를 사용하고 있는지 확인하기 위해 전체 워크플로를 처음부터 다시 실행하고 싶을 때가 많습니다. Snakemake를 사용하면 이 작업을 쉽게 수행할 수 있습니다!

snakemake에 생성 방법을 알고 있는 모든 파일(그리고 _오직_ 해당 파일만)을 정리하도록 요청할 수 있습니다.
```shell
snakemake -j 1 plot_comparison --delete-all-output
```
그런 다음 snakemake에 결과를 다시 생성하도록 요청할 수 있습니다.
```
snakemake -j 1 plot_comparison
```

## snakemake는 만들 수 없는 경우 누락된 파일을 알려줍니다!

`compare_genomes`에 존재하지 않는 새 파일을 추가한다고 가정해 보겠습니다.

```python
{{#include ../code/section1/simple7.snakefile}}
```

여기서 `does-not-exist.sig`는 존재하지 않으며, snakemake에 이를 만드는 규칙도 제공하지 않았습니다. snakemake는 어떻게 할까요?

크고 명확하게 불평할 것입니다! 그리고 아무것도 실행하기 전에 그렇게 할 것입니다.

먼저 규칙이 의존하는 출력 파일을 강제로 제거합니다.
```shell
rm compare.mat
```

그런 다음 `snakemake -j 1`을 실행합니다. 다음이 표시되어야 합니다.

```
Missing input files for rule compare_genomes:
    output: compare.mat
    affected files:
        does-not-exist.sig
```

이것이 바로 원하는 것입니다. 워크플로가 실행되기 전에 무엇이 누락되었는지 명확하게 표시하는 것입니다.

# 다음 단계

기본적인 snakemake 워크플로를 소개했으며, 이를 통해 셸 명령을 올바른 순서로 실행하는 간단한 방법을 제공합니다. snakemake는 이미 셸 명령을 직접 실행하거나 셸 스크립트로 실행하는 것보다 몇 가지 좋은 개선 사항을 제공합니다.

* 필요한 모든 파일이 이미 있는 경우 셸 명령을 실행하지 않습니다.
* 동일한 파일 이름을 반복해서 입력하지 않아도 됩니다.
* 무언가 실패하면 간단하고 명확한 오류를 제공합니다.

이 기능은 좋지만 생물정보학의 효율성을 향상시키기 위해 할 수 있는 일이 훨씬 더 많습니다!

다음 섹션에서는 다음을 살펴보겠습니다.

- _와일드카드_를 사용하여 더 일반적인 규칙 작성
- 더 많은 템플릿을 사용하여 파일 이름 입력 줄이기
- 생성할 기본 출력 파일 목록 제공
- 단일 컴퓨터에서 병렬로 명령 실행
- 스프레드시트에서 파일 이름 목록 로드
- 입력 파일로 워크플로 구성

[end of src/chapter_3.md]

[start of src/chapter_4.md]
# 4장 - 규칙 병렬 실행

마지막 `Snakefile` 항목의 `sketch_genomes` 규칙을 살펴보겠습니다.

(@CTB 참고: 섹션 1은 이러한 명시적 파일 이름을 포함하도록 수정해야 합니다!)

```python
{{#include ../code/section2/interm1.snakefile}}
```

이 명령은 그대로 잘 작동하지만 약간 어색합니다. 왜냐하면 생물정보학이 생물정보학이기 때문에 어느 시점에서 비교에 더 많은 게놈을 추가하고 싶을 가능성이 높고, 지금은 각 추가 게놈을 입력과 출력 모두에 추가해야 하기 때문입니다. 많은 작업은 아니지만 불필요합니다.

또한 게놈을 _많이_ 추가하면 이 단계가 빠르게 병목 현상이 될 수 있습니다. `sourmash sketch`는 10개 또는 20개 게놈에서 빠르게 실행될 수 있지만 100개 또는 1000개를 제공하면 속도가 느려집니다! (실제로 `sourmash sketch`는 100개 게놈에서 1개 게놈보다 100배 더 오래 걸립니다.) 이를 빠르게 하는 방법이 있을까요?

예 - 각 게놈에 대해 실행할 수 있는 규칙을 작성한 다음 snakemake에 병렬로 실행하도록 요청할 수 있습니다!

참고: 때로는 모든 게놈을 처리하는 단일 규칙이 있어야 합니다. 예를 들어 `compare_genomes`는 _모든_ 게놈을 비교해야 하며 이를 간단하게 해결할 방법이 없습니다. 하지만 `sketch_genomes`를 사용하면 간단한 옵션이 있습니다!

이 하나의 규칙을 세 개의 _별도_ 규칙으로 나누는 것부터 시작하겠습니다.

```python
{{#include ../code/section2/interm2.snakefile}}
```

@CTB 특정 줄만 포함

말이 많지만 작동합니다. 실행:

```shell
snakemake -j 1 --delete-all plot_comparison
snakemake -j 1 plot_comparison
```

파일을 더 수정하기 전에 노력의 결실을 즐겨봅시다. 이제 snakemake에 한 번에 둘 이상의 규칙을 실행하도록 지시할 수 있습니다!

@CTB 참고: snakemake에 모든 것을 다시 실행하도록 요청하는 방법이 있습니까? 강제?

다음을 입력해 보십시오.
```shell
snakemake -j 1 --delete-all plot_comparison
snakemake -j 3 plot_comparison
```

자세히 보면 snakemake가 세 개의 `sourmash sketch dna` 명령을 모두 _동시에_ 실행하고 있음을 알 수 있습니다.

이것은 실제로 매우 멋지고 snakemake의 더 강력한 실제 기능 중 하나입니다. snakemake에 _무엇을 하고 싶은지_ (대상을 지정하여) 알려주고 snakemake에 _각 단계를 수행하는 방법_을 알려주는 레시피 집합을 제공하면 snakemake는 제공한 리소스로 필요한 모든 단계를 실행하는 가장 빠른 방법을 알아낼 것입니다.

이 경우 `-j 3`으로 한 번에 최대 세 개의 작업을 실행할 수 있다고 snakemake에 알렸습니다. 한 번에 더 많은 작업을 실행하도록 지시할 수도 있었지만 현재 동시에 실행할 수 있는 규칙은 `sketch_genomes_1`, `sketch_genomes_2`, `sketch_genomes_3` 세 개뿐입니다. 이는 `compare_genomes` 규칙이 실행되려면 이 세 규칙의 출력이 필요하고 마찬가지로 `plot_genomes`가 실행되려면 `compare_genomes`의 출력이 필요하기 때문입니다. 따라서 다른 규칙과 동시에 실행할 수 없습니다!

[end of src/chapter_4.md]

[start of src/chapter_5.md]
# 5장 - 워크플로 시각화

우리가 무엇을 하고 있는지 시각화해 봅시다.

@@ 플롯 및 DAG, graphviz 설치

![작업의 interm2 그래프](images/2023-snakemake-slithering-section-2-interm2-dag.png?raw=true)

[end of src/chapter_5.md]

[start of src/chapter_6.md]
# 6장 - 와일드카드를 사용하여 규칙을 더 일반화하기

`sketch_genomes_` 규칙 중 하나를 다시 살펴보겠습니다.
```python
rule sketch_genomes_1:
    input:
        "genomes/GCF_000017325.1.fna.gz",
    output:
        "GCF_000017325.1.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} --name-from-first
    """
```

거기에는 약간의 중복이 있습니다. 액세션 `GCF_000017325.1`이 두 번 나타납니다. 그것에 대해 뭔가 할 수 있을까요?

네, 할 수 있습니다! "와일드카드"라는 snakemake 기능을 사용하여 snakemake에 자동으로 채울 빈 공간을 제공할 수 있습니다.

와일드카드를 사용하면 입력 또는 출력 파일 이름의 특정 부분이 와일드카드 이름을 둘러싸는 `{` 및 `}`를 사용하여 대체 대상임을 snakemake에 알립니다. `accession`이라는 와일드카드를 만들고 규칙의 입력 및 출력 블록에 넣어 보겠습니다.

```python
rule sketch_genomes_1:
    input:
        "genomes/{accession}.fna.gz",
    output:
        "{accession}.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """
```

이것이 하는 일은 `.fna.gz.sig`로 끝나는 출력 파일을 원할 때마다 `genomes/` 디렉터리에서 해당 접두사(`.fna.gz.sig` 앞의 텍스트)를 가진 파일을 찾고 `.fna.gz`로 끝나며 **존재하는 경우** 해당 파일을 입력으로 사용하도록 snakemake에 지시하는 것입니다.

(예, 규칙에 여러 와일드카드가 있을 수 있습니다! 나중에 보여드리겠습니다!)

`sketch_genomes_2` 및 `sketch_genomes_3`에서 와일드카드를 사용하면 규칙이 _동일하게_ 보이는 것을 알 수 있습니다. 그리고 결국에는 하나의 규칙만 필요하며(실제로 가질 수 있음) 세 규칙을 다시 하나의 `sketch_genome` 규칙으로 축소할 수 있습니다.

전체 `Snakefile`은 다음과 같습니다.
```python
{{#include ../code/section2/interm3.snakefile}}
```

와일드카드를 사용하고 있다는 중요한 차이점을 제외하고는 우리가 시작한 Snakefile과 매우 유사해 보입니다.

여기서는 세 개의 게놈을 스케치하는 하나의 규칙이 있었던 마지막 섹션의 끝부분과 달리, 이제 한 번에 하나의 게놈을 스케치하는 하나의 규칙이 있지만 병렬로 실행할 수도 있습니다! 따라서 `snakemake -j 3`은 여전히 작동합니다! 그리고 더 많은 게놈을 추가하고 동시에 실행하려는 작업 수를 늘려도 계속 작동합니다.

그렇게 하기 전에 이제 워크플로를 다시 살펴보겠습니다. 모양은 같지만 약간 다르게 보이는 것을 알 수 있습니다! 이제 게놈을 스케치하는 세 규칙의 이름이 다른 대신 모두 동일한 이름을 갖지만 `accession` 와일드카드에 대해 다른 값을 갖습니다!

![작업의 interm3 그래프](images/2023-snakemake-slithering-section-2-interm3-dag.png?raw=true)

[end of src/chapter_6.md]

[start of src/chapter_7.md]
# 7장 - 규칙 이름 대신 파일 이름을 snakemake에 제공

새로운 게놈을 혼합에 추가하고 `.sig`로 끝나는 스케치 파일을 생성하는 것부터 시작하겠습니다.

[이 NCBI 링크](https://www.ncbi.nlm.nih.gov/assembly/GCF_008423265.1)에서 GCF_008423265.1에 대한 RefSeq 어셈블리 파일(`_genomic.fna.gz` 파일)을 다운로드하고 `genomes/` 하위 디렉터리에 `GCF_008423265.1.fna.gz`로 넣습니다. ([이 osf.io 링크](https://osf.io/7cdxn)에서 올바른 이름으로 저장된 사본을 다운로드할 수도 있습니다.)

이제 `sourmash sketch dna`를 실행하여 스케치를 만들고 싶습니다(snakemake를 통해).

이를 위해 `Snakefile`에 무언가를 추가해야 할까요? 아니요, 그럴 필요 없습니다!

이 새로운 게놈에 대한 스케치를 만들려면 다음과 같이 올바른 파일 이름을 만들도록 snakemake에 요청하기만 하면 됩니다.
```shell
snakemake -j 1 GCF_008423265.1.fna.gz.sig
```

왜 이것이 작동할까요? `genomes/`의 파일에서 `.sig` 파일을 빌드하기 위한 일반적인 와일드카드 규칙이 있기 때문에 작동합니다!

snakemake에 해당 파일 이름을 빌드하도록 요청하면 규칙의 모든 출력 블록을 살펴보고 일치하는 출력이 있는 규칙을 선택합니다. 중요하게도 이 규칙에는 와일드카드가 _있을 수 있으며_, 있는 경우 파일 이름에서 와일드카드를 추출합니다!

## 경고: `sketch_genome` 규칙이 변경되었습니다!

참고로 더 이상 `sketch_genome`이라는 이름으로 규칙을 실행하도록 snakemake에 요청할 수 없습니다. 이는 규칙이 와일드카드를 채워야 하고 파일 이름을 제공하지 않으면 `{accession}`이 무엇이어야 하는지 알 수 없기 때문입니다.

`snakemake -j 1 sketch_genome`을 실행하려고 하면 다음 오류가 발생합니다.
>WorkflowError:
>Target rules may not contain wildcards. Please specify concrete files or a rule without wildcards at the command line, or have a rule without wildcards at the very top of your workflow (e.g. the typical "rule all" which just collects all results you want to generate in the end).

이는 snakemake가 와일드카드를 채우는 방법을 모르고 있음을 알려주는 것입니다(그리고 아래에서 살펴볼 몇 가지 제안을 제공합니다).

이 장에서는 새로운 기능을 사용하기 위해 Snakefile을 전혀 수정할 필요가 없었습니다!

[end of src/chapter_7.md]

[start of src/chapter_8.md]
# 8장 - 새 게놈 추가

새로운 게놈을 얻었고 스케치를 만들 수 있습니다. 비교에 추가하여 세 개가 아닌 _네 개_ 게놈에 대한 비교 행렬을 만들어 보겠습니다!

이 새로운 게놈을 비교에 추가하려면 스케치를 `compare_genomes` 입력에 추가하기만 하면 됩니다. 그러면 snakemake가 자동으로 관련 게놈 파일을 찾아 이전 장에서와 같이 `sketch_genome`을 실행한 다음 `compare_genomes`를 실행합니다. 나머지는 snakemake가 알아서 처리합니다!

```python
{{#include ../code/section2/interm4.snakefile}}
```

이제 `snakemake -j 3 plot_comparison`을 실행하면 4x4 행렬이 포함된 `compare.mat.matrix.png` 파일이 생성됩니다! (그림 참조)

![게놈의 4x4 행렬 비교](images/2023-snakemake-slithering-section-2-4x4-mat.png)

워크플로 다이어그램이 이제 네 번째 게놈을 포함하도록 확장되었습니다!

![interm3 작업 그래프](images/2023-snakemake-slithering-section-2-interm4-dag.png?raw=true)

[end of src/chapter_8.md]

[start of src/chapter_9.md]
# 9장 - `expand`를 사용하여 파일 이름 만들기

`compare_genomes` 규칙의 파일 목록이 모두 동일한 접미사를 공유하고 모두 동일한 규칙을 사용하여 빌드된다는 점에 유의할 수 있습니다. 어떤 식으로든 사용할 수 있을까요?

네! `expand(...)`라는 함수를 사용하고 빌드할 템플릿 파일 이름과 해당 파일 이름에 삽입할 값 목록을 제공할 수 있습니다.

아래에서는 `ACCESSIONS`라는 액세션 목록을 만들고 `expand`를 사용하여 해당 목록에서 `{acc}.fna.gz.sig` 형식의 입력 파일 목록을 빌드하여 `ACCESSSIONS`의 각 값에 대해 하나의 파일 이름을 만듭니다.

```python
{{#include ../code/section2/interm5.snakefile}}
```

와일드카드와 `expand`는 동일한 구문을 사용하지만 상당히 다른 작업을 수행합니다.

`expand`는 템플릿과 템플릿에 삽입할 값 목록을 기반으로 파일 이름 목록을 생성합니다. 일반적으로 snakemake가 사용자를 위해 만들도록 하려는 파일 목록을 만드는 데 사용됩니다.

규칙의 와일드카드는 하나 이상의 파일이 실제로 생성될 규칙을 제공합니다. "이런 모양의 이름으로 파일을 만들고 싶을 때 저런 모양의 파일에서 그렇게 할 수 있으며, 그렇게 하기 위해 실행해야 할 내용은 다음과 같습니다."라고 말하는 레시피입니다.

`expand`는 snakemake에 무엇을 만들고 싶은지 알려주고, 와일드카드 규칙은 snakemake에 그것들을 만드는 방법을 알려줍니다.

CTB: 이것이 문자열 목록과 동일한 방식에 대한 논의를 추가합니다.
CTB: [추가 확장 문서](beginner+/expand.md)를 참조하십시오.

[end of src/chapter_9.md]

[start of src/complete/assembly.md]
# 박테리아 게놈 조립 및 평가

이 장에서는 박테리아 게놈에 대한 짧지만 완전한 조립 및 평가 워크플로를 제공합니다. 이 워크플로는 페어드 엔드 Illumina 읽기를 가져온 다음 다음을 수행합니다.

* megahit 어셈블러를 실행합니다.
* 조립된 게놈에 대한 quast 보고서를 생성합니다.
* prokka로 조립된 게놈에 주석을 답니다.

## 연습 문제

어셈블러로 매개변수 스윕.

[end of src/complete/assembly.md]

[start of src/complete/rnaseq.md]
# 완전한 RNAseq 예제

아래에서는 간단하면서도 완전한 RNAseq 분석 워크플로를 제공합니다. 처음부터 끝까지 이 워크플로는 4개의 효모 RNAseq 읽기 데이터 세트를 가져온 다음 다음을 수행합니다.

* 각 데이터 세트에 대한 FastQC 보고서를 생성합니다.
* Trimmomatic을 실행하여 품질이 낮은 RNAseq 읽기를 제거합니다.
* 트리밍된 읽기에 대해 FastQC를 실행합니다.
* salmon을 사용하여 각 읽기 데이터 세트에 표시된 코딩 시퀀스를 정량화합니다.
* DESeq2를 사용하여 샘플로 표시된 조건에서 유전자 발현을 로드, 정규화 및 대조합니다.

이 워크플로가 변이 호출 및 어셈블리 워크플로와 구별되는 새로운 특징은 상당량의 처리가 RMarkdown 파일의 R에서 수행된다는 것입니다.

CTB: FastQC/multiqc 내용을 자체 예제로 분리해야 할까요?

TODO:

* 저자에게 감사를 표합니다!
* 이것을 장 모음으로 작성해야 할까요, 아니면 단일 장으로 작성해야 할까요?
* 워크플로 다이어그램을 만듭니다.

## 연습

새 데이터 세트 추가
이름으로 특정 유전자를 가져오는 몇 가지 예 추가

[end of src/complete/rnaseq.md]

[start of src/complete/variant.md]
# 박테리아 게놈에 대한 완전한 변이 호출 예제

여기서는 박테리아 게놈에 대한 간단한 입문용 변이 호출 워크플로를 제공합니다. 반수체 게놈을 가정하며 필터링되지 않은 변이 호출과 품질 필터링된 변이 호출을 모두 생성합니다. 이 워크플로는 대장균 LTEE의 단일 말단 읽기 데이터 세트를 가져온 다음 다음을 수행합니다.

* minimap2를 사용하여 읽기를 참조 게놈에 정렬하고 SAM 파일을 생성합니다.
* SAM 파일을 BAM 파일로 변환합니다.
* BAM 파일을 정렬하고 인덱싱합니다.
* mpileup을 사용하여 이진 형식으로 변이 호출 집합을 생성합니다.
* 이진 형식을 텍스트 VCF 파일로 변환합니다.
* 커버리지 및 품질을 기준으로 호출을 필터링합니다.

## 완전한 Snakefile

할 일:
- Snakefile의 최종 버전을 추가하십시오!

```python
<!-- cmdrun ../../scripts/remove-anchor.py ../../code/complete/variant/Snakefile -->
```

## 주석이 달린 Snakefile

### 다운로드 규칙

* 입력 없음, 출력만 있음
* curl은 웹에서 파일을 검색합니다. 게놈 파일 등에 유용합니다. wget도 사용할 수 있습니다.
* 실제 데이터로 실제 워크플로를 수행하는 경우 일반적으로 이러한 규칙을 생략하고 대신 데이터를 로컬에 저장합니다.
* -o {output}은 올바른 파일 이름이 적용되도록 합니다.

```python
{{#include ../../code/complete/variant/Snakefile:download}}
```

## 초기 매핑 수행

```python
{{#include ../../code/complete/variant/Snakefile:mapping}}
```

## SAM을 BAM으로 변환

* 왜 한 번에 다 하지 않고 따로 하는가?
  * 너무 많은 작업을 하면 오류 메시지가 합쳐짐
  * 병렬 등을 위해 작업을 분리하는 것이 좋은 습관
* 형식 변환 외에 첫 번째 단계에서 매핑되지 않은 읽기 필터링
* 정렬은 CPU 집약적이므로 여기서 다중 스레딩을 사용할 수 있음

```python
{{#include ../../code/complete/variant/Snakefile:sam_to_bam}}
```

## 변이 호출

리팩터링 - 너무 많은 것들!
* 최소 세 가지로 분할 - gunzip, mpileup, call, view, filter?

논의:
* mpileup은 체계적인 차이가 있는 곳을 찾습니다.
* call은 일부 기본 매개변수에 따라 출력합니다.
* view는 bcf를 vcf로 변환합니다.

```python
{{#include ../../code/complete/variant/Snakefile:call}}
```

## 추가 작업:

* 추가 파일 추가!
* -n으로 테스트 가능하게 만들기!
* big으로 테스트 가능하게 만들기!
* 테스트 태그 제거!
* 출력을 해석하는 방법/무엇을 해야 하는지

[end of src/complete/variant.md]

[start of src/intro.md]
# 소개

안녕하세요! 이 (초안) 책에 오신 것을 환영합니다! 이것은 아직 진행 중인 작업입니다. 업데이트 및 릴리스는 [github 저장소](https://github.com/ngs-docs/2023-snakemake-book-draft)를 확인하십시오.

## 저작권, 라이선스 및 재사용

이 저작물은 C. Titus Brown 및 기타 기여자의 저작권 (C) 2023입니다.

아래와 같이 복사, 수정 및 재배포할 수 있습니다.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="크리에이티브 커먼즈 라이선스" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">초안: 생물정보학을 위한 Snakemake 소개</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/ngs-docs/2023-snakemake-book-draft" property="cc:attributionName" rel="cc:attributionURL">C. Titus Brown 외</a>는 <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">크리에이티브 커먼즈 저작자표시-동일조건변경허락 4.0 국제 라이선스</a>에 따라 라이선스가 부여됩니다.<br /><a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/ngs-docs/2023-snakemake-book-draft" rel="dct:source">https://github.com/ngs-docs/2023-snakemake-book-draft</a>의 저작물을 기반으로 합니다.

[end of src/intro.md]

[start of src/recipes/never-fail-me.md]
# 절대 실패하지 않음 - 셸 명령을 항상 성공하도록 만드는 방법

snakemake는 셸 명령이 성공했는지 여부를 결정하기 위해 유닉스 종료 코드를 사용합니다. 이것은 실행 중인 프로그램에서 반환되는 숫자 값입니다. 값 `0`(영)은 성공을 나타내고 0이 아닌 다른 값은 오류를 나타냅니다.


~~~admonish info title='유닉스 종료 코드를 어떻게 해석해야 할까요?'

유닉스 "종료 코드" 또는 "종료 상태"는 종료하는 하위 프로세스에서 호출 프로그램으로 반환되는 단일 숫자입니다. 이것은 셸이나 워크플로 프로그램이 실행한 하위 프로그램의 성공 또는 실패에 대한 정보를 받는 방식입니다.

일반적인 기본값은 종료 코드 0이 성공을 나타내는 것입니다. 이것은 Linux 및 Mac OS X와 같은 POSIX 시스템에서 항상 그렇습니다. 또한 많은 프로그램이 빌드되는 GNU libc 라이브러리에 의해 표준화되었습니다(아래 링크 참조).

유닉스용 bash 셸에서 이전 명령의 종료 상태는 `$?` 변수에 저장되며 다음과 같이 평가할 수 있습니다.
```shell
$ if [ $? -eq 0 ] ...
```
또는 `&&`를 사용하여 첫 번째 명령이 "성공"(종료 코드 0으로 종료)하는 경우에만 두 번째 명령을 실행할 수 있습니다.
```shell
$ program && echo success
```
그리고 `||`을 사용하여 첫 번째 명령이 실패하는 경우(0이 아닌 종료 코드로 종료)에만 두 번째 명령을 실행할 수 있습니다.
```shell
$ program || echo failed
```

왜 0이 성공을 나타낼까요? 답을 찾을 수 없었지만 추측해야 한다면 0이 눈에 띄는 좋은 단일 값이기 때문일 것입니다!

자세한 내용은 [종료 상태에 대한 Wikipedia 항목](https://en.wikipedia.org/wiki/Exit_status)과 [GNU libc 매뉴얼 섹션](https://www.gnu.org/software/libc/manual/html_node/Exit-Status.html)을 참조하십시오.
~~~

때로는 구성 방식 때문에 셸 명령이 _실패해야_ 할 수도 있습니다. 예를 들어, 명령의 출력을 잘라내기 위해 파이핑을 사용하는 경우 유닉스는 파이프의 수신단이 입력 수신을 중단하면 명령을 중지합니다. 압축된 파일에서 처음 1,000,000줄만 가져오는 다음 명령을 살펴보십시오.

```
gunzip -c large_file.gz | head -1000000
```

`large_file.gz`에 1백만 줄 이상이 있는 경우 이 명령은 실패합니다. `head`가 1백만 줄 후에 입력 수신을 중단하고 gunzip이 파이프에 쓸 수 없기 때문입니다.

CTB: 오류 메시지 예시를 추가합니다.

이러한 상황이 발생하는 다른 경우는 스크립트나 프로그램을 사용하고 있는데 어떤 이유로든 제어할 수 없는 이유로 상태 코드 0으로 종료되지 않는 경우입니다.

`shell:` 블록의 명령이 절대 실패하지 않도록 하려면 다음과 같이 작성할 수 있습니다.
```
shell command || true
```

이렇게 하면 `shell command`가 실행되고 종료 코드가 0이 아닌 경우(실패) 항상 종료 코드 0(성공)을 갖는 `true`가 실행됩니다!

이것은 약간 위험합니다. 셸 명령이 실패하면 오류 메시지를 읽는 것 외에는 알 수 없지만 때로는 필요합니다!

다음은 종료되지 않는 스크립트를 실행하려고 시도하여 이 접근 방식을 보여주는 간단한 snakemake 예제입니다! 해당 명령은 항상 실패하지만 `|| true`를 사용하기 때문에 전체 셸 블록은 어쨌든 성공합니다.

```python
{{#include ../../code/misc/never-fail-me/never-fail-me.snakefile}}
```

(또한 이 접근 방식의 위험성을 보여줍니다. 이것은 실제로 실패해야 하는 명령일 가능성이 높기 때문입니다!)

CTB: 하위 셸을 언급할까요?

[end of src/recipes/never-fail-me.md]

[start of src/recipes/params-functions.md]
# FASTQ 파일을 고정된 수의 레코드로 하위 집합화.

레벨: 중급

[하위 샘플링 파일 레시피](./subsampling-files.md)에서는 출력 파일 이름만을 기반으로 특정 줄 수를 가진 파일을 출력하는 방법을 보여주었습니다. FASTQ 파일에서 특정 수의 _레코드_를 샘플링하려면 어떻게 해야 할까요? 이렇게 하려면 레코드 수를 줄 수로 변환해야 합니다.

이를 위해 snakemake는 `params:` 블록에서 함수를 지원합니다(참조 CTB XXX params 블록). 다음 레시피에서는 `num_records` 와일드카드에 지정된 _레코드_ 수를 기반으로 샘플링할 줄 수를 계산합니다.

```python
{{#include ../../code/examples/params.subset/Snakefile}}
```

여기에는 두 가지 특별한 구성 요소가 있습니다.

* Python 함수 `calc_num_lines`는 와일드카드 객체를 매개변수로 사용하고 `wildcards.num_records`의 값을 기반으로 하위 집합화할 줄 수를 계산합니다.
* 그런 다음 `params:` 블록은 `calc_num_lines`를 적용하여 `params.num_lines`를 생성하며, 이는 셸 명령에서 사용할 수 있습니다.


참고 자료:
* CTB 매개변수
* CTB 네임스페이스
* CTB 파이썬 코드

## 람다 사용

위의 레시피는 꽤 깁니다. 익명 "람다" 함수를 사용하여 훨씬 짧지만 이해하기 어려운 Snakefile을 만들 수 있습니다.

```python
{{#include ../../code/examples/params.subset_lambda/Snakefile}}
```

여기서 `lambda`는 단일 매개변수 `wildcards`를 사용하고 `wildcards.num_records`에 4를 곱한 값을 반환하는 익명 함수를 만듭니다.

[end of src/recipes/params-functions.md]

[start of src/recipes/replacing-for.md]
# 여러 파일에 하나의 규칙 적용 - 셸 스크립트에서 for 루프 대체

[end of src/recipes/replacing-for.md]

[start of src/recipes/splitting-files.md]
# split을 사용하여 파일 분할

[end of src/recipes/splitting-files.md]

[start of src/recipes/subsampling-files.md]
# FASTQ 파일 하위 샘플링

레벨: 초급+

[와일드카드를 사용하여 규칙 일반화](../beginner+/wildcards.md)에서는 와일드카드를 사용하여 다음을 생성하는 방법을 소개했습니다.

```python
{{#include ../../code/examples/wildcards.subset/Snakefile}}
```

참조:
* 와일드카드

## 줄 대신 레코드 하위 샘플링

여기서 한 가지 잠재적인 문제는 레코드 수가 아닌 줄 수를 기준으로 하위 집합 파일을 생성한다는 것입니다. 일반적으로 FASTQ 파일에서는 네 줄이 하나의 레코드를 구성합니다. 이상적으로는 위의 레시피에서 생성된 하위 집합 FASTQ 파일의 파일 이름에 줄 수가 아닌 _레코드_ 수가 있어야 합니다! 그러나 이렇게 하려면 레코드 수에 4를 곱해야 합니다!

이를 위해 규칙에 Python 함수를 도입할 수 있는 [`params:` 함수](./params-functions.md)를 사용할 수 있습니다.

[end of src/recipes/subsampling-files.md]

[start of src/reference/namespaces.md]
# 네임스페이스

CTB 스텁:

`wildcards` 네임스페이스는 규칙 _내에서만_ 사용할 수 있습니다. 이는 와일드카드가 개별 규칙 내에만 존재하고 와일드카드가 규칙 간에 공유되지 않기 때문입니다!

code/examples/wildcards.namespace

[end of src/reference/namespaces.md]

[start of src/reference/wildcard-constraints.md]
# 와일드카드 제약 조건으로 와일드카드 일치 제한

와일드카드는 snakemake에서 가장 강력한 기능 중 하나입니다. 하지만 때로는 너무 광범위하게, 너무 많은 파일과 일치하여 문제를 일으키기도 합니다!

와일드카드에 대한 소개는 [와일드카드에 대한 섹션](../beginner+/wildcards.md)을 참조하십시오!

기본적으로 snakemake의 와일드카드는 하나 이상의 문자와 일치합니다. 즉, 빈 문자열과는 일치하지 않지만 _다른 모든 것_과는 일치합니다. 와일드카드 장에서 논의했듯이 이것은 문제를 일으킬 수 있습니다!

snakemake는 [와일드카드 제약 조건](https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#constraining-wildcards)이라는 기능을 사용하여 와일드카드 일치를 제한하는 것을 지원합니다. 와일드카드 제약 조건은 정규 표현식을 사용하여 특정 와일드카드가 일치할 수 있는 것과 일치할 수 없는 것을 지정하는 유연한 시스템입니다.

```admonish info title="정규 표현식"

정규 표현식(일반적으로 "regex" 또는 "regexp"로 약칭)은 유연한 문자열 일치를 위한 미니 언어입니다.

CTB: 여기에 더 추가하고 유용하거나 일반적인 몇 가지 예를 제공합니다. \d+, 영숫자 단어, ??

Python에는 정규 표현식의 고급 사용에 대한 좋은 참고 자료인 정규 표현식에 대한 친숙한 소개가 함께 제공됩니다. [정규 표현식 HOWTO](https://docs.python.org/3/howto/regex.html)를 참조하십시오.
```

할 일:

* 규칙에서 와일드카드 사용
* glob_wildcards에 사용
* 또 어디에?
* 명명된 와일드카드

## glob_wildcards에서 와일드카드 제약 조건 사용

`glob_wildcards`와 함께 와일드카드 제약 조건을 사용하는 것부터 살펴보겠습니다. 다음 파일이 포함된 디렉터리를 고려하십시오.
```
letters-only-abc-xyz.txt
letters-only-abc.txt
letters-only-abc2.txt
```
다음과 같이 세 파일을 모두 쉽게 일치시킬 수 있습니다.
```
files, = glob_wildcards('letters-only-{word}.txt')
```
그러면 `['abc2', 'abc-xyz', 'abc']`가 됩니다.

이제 와일드카드 패턴이 `letters-only-abc.txt`와만 일치하고 다른 파일과는 일치하지 않도록 하려면 어떻게 해야 할까요?

아래와 같이 숫자와 일치하지 않고 문자만 일치하도록 제약 조건을 지정할 수 있습니다.
```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:letters-only}}
```
그러면 `letters_only` 목록은 `['abc']`가 됩니다.

정규식 `^`(NOT) 문자를 사용하여 허용되는 문자와 반대로 피해야 할 문자를 지정할 수도 있습니다. 이렇게 하면 이전 예보다 더 광범위한 파일과 일치하지만 숫자가 포함된 단어는 여전히 무시됩니다.
```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:letters-only-2}}
```
여기서 `letters_only`는 숫자 _외에는_ 모든 것을 허용하기 때문에 `['abc-xyz', 'abc']`가 됩니다.

특정 문자를 피하는 것은 하위 디렉터리에서 일치하는 것을 피하고 싶을 때 특히 유용합니다. 기본적으로 `glob_wildcards`는 하위 디렉터리의 파일을 포함합니다. 예를 들어 `data/datafile.txt` 파일이 있는 경우 아래 `all_txt_files`는 `data/datafile.txt`를 나열합니다.

```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:all-txt}}
```

그러나 와일드카드 일치를 슬래시(`/`)를 피하도록 제한하면 하위 디렉터리의 파일은 일치하지 않습니다.

```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:no-subdir}}
```

CTB 확인

## 규칙에서 와일드카드 제약 조건 사용

* 와일드카드가 처음 언급된 곳에만 필요

## 전역 와일드카드 제약 조건

snakemake는 다음과 같은 _전역_ 와일드카드 제약 조건을 지원합니다.

```python
wildcard_constraints:
    sample="\w+" # {sample,\w+}와 동일 - 알파벳 문자로 제한
    num="[0-9]+" # {num,[0-9]+}와 동일 - 숫자로 제한
```

Snakefile에서 `sample` 또는 `num`이 사용되는 모든 곳에 이러한 제약 조건이 적용됩니다.

<!-- CTB: 확인, 로컬에서 재정의할 수 있습니까? -->

[end of src/reference/wildcard-constraints.md]

[start of src/section_2.md]
# 섹션 2 - 더욱 유용한 Snakefile 구축

섹션 2에서는 snakemake의 여러 중요한 기능을 살펴보겠습니다. 섹션 1과 함께 이 섹션에서는 snakemake를 효과적으로 활용하기 위해 알아야 할 핵심 snakemake 기능 집합을 다룹니다.

이 섹션이 끝나면 자신만의 워크플로 몇 개를 작성할 수 있는 좋은 위치에 있게 될 것이며, 그런 다음 필요에 따라 더 고급 기능을 살펴볼 수 있습니다.

@ 이전에 어디까지 갔는지 요약 추가

[end of src/section_2.md]

[start of src/section_3.md]
# 첫 번째 Snakefile 이후

이 섹션은 이미 snakemake를 사용해 본 적이 있고 이제 더 많은 snakemake 기능을 배우고 적용하려는 사람들을 위한 것입니다!

## 몇 가지 초기 동기 부여

아래 Snakefile을 고려해 봅시다.

```python
{{#include ../code/examples/wildcards.fastqc/Snakefile:content}}
```

이 Snakefile은 현재 디렉터리 아래에서 `.fastq`로 끝나는 모든 파일을 찾습니다. 그런 다음 snakemake는 각 파일에 대해 FASTQC를 실행하고 multiqc를 사용하여 요약 보고서를 작성합니다. 파일 수에 관계없이 작동하며 모든 하위 디렉터리 아래의 파일을 찾습니다. 단일 시스템에서 병렬로 실행하거나 클러스터의 여러 시스템에서 실행할 수 있으며, snakemake에 제공하는 계산 리소스에 의해서만 제한됩니다. 그리고 새 FASTQ 파일이 추가되면 snakemake는 자동으로 이를 감지하고 `fastqc`를 실행한 다음 `multiqc`를 다시 실행하여 요약 보고서를 업데이트합니다.

이 모든 강력한 기능에도 불구하고 컴퓨터 프로그램치고는 상당히 짧다고 말할 수 있습니다. 하지만 다소 간결하고 복잡해 보이기도 합니다!

이 섹션은 위의 기능을 지원하는 snakemake의 모든 기능(및 Snakefile에 작성하는 방법)을 설명하는 데 할애됩니다. 이 섹션이 끝나면 snakemake의 핵심 기능 중 80% 이상을 사용할 수 있게 될 것입니다! 그리고 필요에 따라 사용할 수 있는 나머지 20%의 snakemake 핵심 기능 세트에 대한 포인터도 갖게 될 것입니다.

## 이 섹션 요약

이 섹션은 처음 두 섹션의 점진적인 도입과 나중에 논의될 이 완전히 작동하는 워크플로 시스템의 전체 기능 및 [공식 snakemake 문서](https://snakemake.readthedocs.io/) 사이의 간극을 메우려고 시도합니다.

이 섹션에서는 입력 및 출력 블록, 와일드카드, params 블록, `glob_wildcards` 및 `expand`를 소개합니다. 또한 snakemake 워크플로 디버깅에 대한 일반적인 접근 방식을 논의하고 기본 구문 규칙을 다룹니다.

[end of src/section_3.md]

[start of src/section_3b.md]
# 섹션 3b - 전체 예제

[end of src/section_3b.md]

[start of src/section_4.md]
# 섹션 4 - Snakemake 패턴 및 레시피

[end of src/section_4.md]

[start of src/section_5.md]
# 섹션 5 - 고급 기능

[end of src/section_5.md]

[start of src/section_6.md]
# 섹션 5 - Snakemake 기능 참조 가이드

[end of src/section_6.md]
