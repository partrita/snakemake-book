# 리소스, 제약 조건 및 작업 관리

## 만들 지점 / 개요

* 정확히 예측하는 것의 불가능성; 전략
* 벤치마크, slurm, top (??)으로 측정하는 방법; 관리할 핵심 사항으로서의 RSS
* CPU 활용률, 컨텍스트 전환, 오버헤드; 스레드, 프로세스
* 병렬 처리에 대한 고려 사항 (아마도 [parallel](parallel.md) 참조).

표준 리소스: mem, disk, runtime 및 tmpdir

자체 정의 리소스: 기타 사항.

## 예시

* 다양한 메모리 제약 작업을 설정하고 다양한 최대 메모리로 실행합니다. 중첩을 보여줍니다. 사용된 총 메모리를 보여주는 그림을 만듭니다.
