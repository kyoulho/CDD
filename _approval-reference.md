# Approval Reference Standard

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 문서는 CDD V2의 승인 종류와 approval reference 형식을 정의한다.

승인은 모호한 자연어를 권한으로 확대 해석하지 않기 위한 기록이다.

V2.1의 실제 YAML 골격은 `_artifact-templates.md`의 `Approval Record Template`을 우선 사용한다. 이 문서는 승인 종류와 해석 규칙을 설명한다.

## 승인 종류

### DIRECTION_APPROVAL

- 변경 방향 선택
- 예: A/B/C 중 A 선택
- 파일 수정 권한 없음
- prompt 생성 또는 실행 권한 없음

### DRAFT_REVIEW_APPROVAL

- DRAFT 변경안을 검토했다는 승인
- 아직 파일 수정 권한 없음
- 다음 단계 적용 승인과 분리한다.

### APPLY_APPROVAL

- 지정된 artifact와 `approvedScope` 전체에 대해 실제 파일 수정을 허용
- 반드시 명시적이어야 한다.
- 대상 artifact와 파일 묶음이 명확해야 한다.

### PATCH_APPROVAL

- 분석/제안 결과를 기준으로 지정된 파일 범위의 패치를 허용
- source of truth Change Request APPLY와 구분한다.
- 반드시 수정 범위가 명확해야 한다.
- 예: "위 분석에 따라 skill 파일 수정을 승인합니다."
- 예: "CDD skill 파일 수정을 승인합니다."

### PROMPT_DRAFT_APPROVAL

- 구현 지시서 초안 작성 또는 검토 승인
- prompt execution 권한이 아니다.

### PROMPT_EXECUTION_APPROVAL

- 구현 Agent가 해당 구현 지시서로 실제 구현을 시작해도 된다는 승인
- prompt draft approval과 분리한다.

### REVIEW_APPROVAL

- 구현 결과 또는 diff review 승인
- completion 전 필요하다.

### COMPLETION_APPROVAL

- 완료 기록을 남겨도 된다는 승인
- review approval과 별개로 요구될 수 있다.

### DEPENDENCY_CHANGE_APPROVAL

- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library 변경 승인
- 승인 범위와 목적이 명확해야 한다.

## Approval Record 형식

산출물에 승인 기록을 붙일 때는 가능한 한 `_artifact-templates.md`의 `Approval Record Template`을 사용한다.

```yaml
approval:
  id: APPROVAL-CR-001-APPLY
  type: APPLY_APPROVAL
  targetArtifactId: CR-001
  approvedScope:
    - docs/architecture/api-contract.md
    - docs/architecture/data-model.md
    - tasks/TASK-002.yml
  approvedBy: user
  approvedAt: "2026-06-08T00:00:00Z"
  approvalText: "CR-001 정합 묶음 적용을 승인합니다."
```

## 승인 해석 규칙

- "A로 하자"는 `DIRECTION_APPROVAL` 이상으로 해석하지 않는다.
- "좋아", "진행해", "추천대로", "알아서 반영해", "빨리 해"는 모호하면 확인 질문을 한다.
- "분석만", "수정하지 마", "원인만", "검토만", "제안만"이 있으면 어떤 approval도 파일 수정 권한으로 해석하지 않는다.
- 분석/제안에서 패치로 전환하려면 `PATCH_APPROVAL` 또는 동등한 명시 승인이 필요하다.
- `APPLY_APPROVAL`은 반드시 대상 artifact와 파일 묶음이 명확해야 한다.
- `PROMPT_DRAFT_APPROVAL`과 `PROMPT_EXECUTION_APPROVAL`을 분리한다.
- prompt 초안 승인만으로 구현을 시작하면 안 된다.
- approval reference가 없는 artifact는 자동 invalid는 아니지만, legitimacy 판단이 불가능하면 사용자 확인 또는 quarantine 후보로 보고한다.

## 확인 질문 예시

```text
"A로 하자"는 변경 방향 승인으로 이해했습니다. 아직 파일 적용 승인은 아닙니다.
실제로 파일 묶음을 바꾸려면 다음처럼 승인해 주세요:
"CR-001의 Files Proposed for Apply 전체 적용을 승인합니다."
```

```text
구현 지시서 초안은 만들 수 있습니다. 다만 이 지시서로 실제 구현을 시작하려면 별도 실행 승인이 필요합니다.
```
