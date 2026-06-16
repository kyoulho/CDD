# Artifact Status Machine

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 문서는 CDD V2의 공통 artifact 상태와 전이를 정의한다.

## 공통 상태

### DRAFT

- 검토 가능
- 실행 불가
- 기준 artifact로 사용 불가
- 다음 단계 입력으로 쓰려면 review 또는 approval이 필요하다.

### PENDING_REVIEW

- 사용자 또는 reviewer 검토 대기
- 실행 불가
- 승인 전에는 기준 artifact로 사용 불가

### APPROVED

- 다음 단계 입력으로 사용 가능
- 단, `dependsOn`, source of truth, known conflict, superseded 여부를 재검사해야 한다.
- 승인 범위 밖 행동에는 사용할 수 없다.

### APPLIED

- 승인된 변경이 파일에 반영된 상태
- 아직 기준 artifact로 확정된 것은 아니다.
- validation이 필요하다.

### VALIDATED

- 기준 artifact로 사용 가능
- 단, 이후 source of truth 변경, Task 변경, dependency 상태 변경 시 invalidation 판단이 필요하다.

### NEEDS_REVISION

- 승인된 기준 안에서 수정이 필요한 상태
- revision prompt 생성 가능
- 사용자 승인 후에만 revision 실행 가능

### BLOCKED

- 필요한 결정, 승인, 선행 작업, 또는 기준 문서 정합성이 부족한 상태
- 후속 단계 진행 불가

### INVALID

- 사용 금지
- 후속 작업 근거로 사용 금지
- completion 근거로 사용 금지

### QUARANTINED

- 사용 보류
- 사용자 결정 필요
- 격리, 폐기, 재생성, 복구 중 하나를 결정해야 한다.

### SUPERSEDED

- 과거 기록
- 실행, 구현, completion 근거로 사용 금지
- 새 artifact 또는 새 source of truth 기준으로 대체되었다.

### COMPLETE

- 완료 조건이 충족된 상태
- completion record와 review approval이 있어야 한다.

### REJECTED

- 사용자 또는 reviewer가 거부한 상태
- 다음 단계 입력으로 사용하지 않는다.

## 상태 전이

```text
DRAFT -> PENDING_REVIEW -> APPROVED
APPROVED -> APPLIED -> VALIDATED
VALIDATED -> SUPERSEDED
DRAFT -> REJECTED
PENDING_REVIEW -> REJECTED
APPROVED -> NEEDS_REVISION
NEEDS_REVISION -> DRAFT
ANY -> INVALID
ANY -> QUARANTINED
BLOCKED -> DRAFT
VALIDATED -> COMPLETE
```

## 상태별 Gate

- `DRAFT`: 사용자 검토만 가능하다.
- `APPROVED`: 다음 단계 입력으로 쓸 수 있지만 legitimacy check를 다시 수행한다.
- `APPLIED`: validation 전까지 기준으로 사용하지 않는다.
- `VALIDATED`: 기준으로 사용할 수 있다.
- `INVALID`: 어떤 후속 작업에도 사용하지 않는다.
- `QUARANTINED`: 사용자 결정 전 사용하지 않는다.
- `SUPERSEDED`: 기록으로만 보존한다.
- `COMPLETE`: 후속 Task의 dependency gate를 통과하는 근거가 될 수 있다.

## Status와 User-Facing 표현

내부 status를 사용자에게 그대로 노출하지 않는다. 사용자-facing 표현은 `_user-facing-language.md`를 따른다.

예:

- `BLOCKED`: "아직 진행에 필요한 조건이 부족합니다."
- `QUARANTINED`: "이 파일은 잠시 보류하고 처리 방향을 정해야 합니다."
- `SUPERSEDED`: "이 파일은 이전 기준이라 더 이상 사용하면 안 됩니다."
- `VALIDATED`: "기준 문서와 작업 지시가 서로 맞는 상태입니다."
