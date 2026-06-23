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
- 단, 사용자가 이미 실제 구현, 수정, 정리까지 명확히 요청했고 구현 지시서 작성이 내부 실행 기준을 만드는 절차일 뿐이면, 아래 "초안 작성 후 실행 연계" 조건을 모두 만족할 때 같은 사용자 요청을 실행 승인 근거로 사용할 수 있다.

### REVIEW_APPROVAL

- 구현 결과 또는 diff review 승인
- completion 전 필요하다.

### COMPLETION_APPROVAL

- 완료 기록을 남겨도 된다는 승인
- review approval과 별개로 요구될 수 있다.

### FOLLOW_UP_CONTINUATION_APPROVAL

- 검증 완료된 선행 작업 뒤에 사용자가 후속 Task 작성, 후속 구현, 다음 단계 진행을 명확히 요청한 경우의 제한적 연계 승인
- 현재 사용자의 후속 작업 요청이 선행 작업 결과를 전제로 하는 것이 명확하면, 조건 충족 시 review/completion intent의 보조 근거로 기록할 수 있다.
- 선행 작업의 완료 기록, status, 실행 전 문구 정리처럼 artifact 정합성 보정에만 사용할 수 있다.
- 새 코드 수정, source of truth 변경, 정책 결정, 위험 변경, 검증되지 않은 결과 완료에는 사용할 수 없다.
- 아래 "후속 작업 전환 연계" 조건을 모두 만족할 때만 completion approval 보조 근거로 기록할 수 있다.

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
- "초안만", "먼저 보여줘", "검토 후 진행"처럼 사용자가 검토 단계를 요청했으면 실행 승인으로 해석하지 않는다.
- approval reference가 없는 artifact는 자동 invalid는 아니지만, legitimacy 판단이 불가능하면 사용자 확인 또는 quarantine 후보로 보고한다.

## 승인 요청 전 브리핑

작업 기준서, 구현 지시서, 기준 문서 변경안, 검증 결과, 완료 기록, 수정 지시서, cleanup/delete 분류안에 대한 사용자 승인을 요청할 때는 `_user-facing-language.md`의 "승인 전 브리핑 형식"을 먼저 출력해야 한다.

승인 문장은 브리핑 뒤에 둔다. CDD Agent는 승인 문장만 단독으로 제시하거나, 내부 상태값과 enum만 나열한 뒤 승인을 요구할 수 없다.

브리핑에는 최소한 이번 작업의 목적, 포함 범위, 제외 범위, 사용자가 승인해야 하는 핵심 결정, 위험/중단 조건, 승인 후 가능해지는 다음 단계가 있어야 한다. 이 정보가 없으면 approval text를 생성하지 말고 먼저 브리핑에 필요한 내용을 정리한다.

## 초안 작성 후 실행 연계

작업 지시서 초안 작성 승인과 실행 승인 사이에 새 사용자 결정을 요구하지 않아도 되는 경우가 있다. 이 경우 CDD Agent는 초안 작성 뒤 다시 실행 승인을 묻지 않고 요청 범위 안에서 실행 단계로 이어갈 수 있다.

연계 조건:

- 사용자가 실제 구현, 문서 수정, cleanup/delete 실행, revision 실행 중 하나를 명확히 요청했다.
- 사용자가 "초안만", "계획만", "먼저 보여줘", "수정하지 마"처럼 중간 검토나 분석 전용을 요구하지 않았다.
- 작업 지시서 작성 중 새 제품 판단이나 설계 판단이 발견되지 않았다.
- 저장, 동작, 상태, 상호작용, 운영 기준이 충분하다.
- 작업 범위, 금지 범위, 검증 방법이 명확하다.
- migration, 데이터 삭제, public API 제거, dependency 대량 변경, 되돌리기 어려운 cleanup/delete가 없다.
- 작업 지시서가 기존 기준 문서와 충돌하지 않는다.
- 실행 범위가 사용자의 원래 요청 범위를 넘지 않는다.

연계하면 안 되는 경우:

- 사용자가 초안 검토를 명시했다.
- 지시서 작성 중 미확정 결정, 정책 충돌, 기준 문서 변경 필요가 발견됐다.
- 위험 변경 또는 사람 확인 지점이 있다.
- 실행하려면 사용자 요청 범위를 넓혀야 한다.
- 기존 artifact legitimacy가 불명확하다.

사용자-facing 보고에서는 이렇게 말한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
작업 지시서는 내부 실행 기준으로 작성하고, 새로 결정할 사항이 없으므로 같은 요청 범위 안에서 바로 실행합니다.
```

## 확인 질문 예시

```text
"A로 하자"는 변경 방향 승인으로 이해했습니다. 아직 파일 적용 승인은 아닙니다.
먼저 변경 목적, 포함 범위, 제외 범위, 고정되는 결정, 위험/중단 조건, 승인 후 가능해지는 일을 브리핑합니다.
실제로 파일 묶음을 바꾸려면 다음처럼 승인해 주세요:
"CR-001의 Files Proposed for Apply 전체 적용을 승인합니다."
```

```text
이번 요청은 초안 검토까지만으로 이해했습니다. 이 지시서로 실제 구현을 시작하려면 별도 실행 승인이 필요합니다.
```

## 후속 작업 전환 연계

선행 Task가 완료 기록만 뒤처져 있고 사용자가 후속 Task 작성이나 구현을 명확히 요청한 경우, CDD Agent는 승인 문구를 다시 요구하기 전에 후속 작업 전환 연계 조건을 먼저 확인한다. 조건을 모두 만족하면 선행 Task 완료 정합성 정리를 수행하고 같은 요청 범위 안에서 후속 작업으로 이어간다.

연계 조건:

- 사용자가 후속 Task 작성, 후속 구현, 다음 단계 진행 중 하나를 명확히 요청했다.
- 선행 Task의 구현 결과가 이미 사용자에게 보고되었고, 현재 후속 요청이 그 결과를 전제로 한다.
- 선행 Task의 verification status가 `VERIFIED`이고 check 결과가 통과했다.
- 선행 Task의 실제 변경 범위와 작업 기준 묶음이 일치한다.
- 선행 Task에 남은 미확정 제품 판단, 설계 판단, 정책 충돌, source of truth 변경 요청이 없다.
- 남은 작업이 completion record 생성, status 전환, 실행 전 문구 제거, predecessor snapshot 갱신 같은 artifact 정합성 정리에 한정된다.
- artifact legitimacy check가 통과하고 invalid/quarantined/superseded 충돌이 없다.
- 후속 작업으로 넘어가는 것이 사용자의 원래 요청 범위를 넘지 않는다.

연계하면 안 되는 경우:

- 선행 Task 검증이 없거나 `VERIFIED`가 아니다.
- 사용자가 선행 작업 결과를 보류하거나 검토만 하겠다고 했다.
- 변경 결과가 사용자에게 보고되지 않았거나, 현재 후속 요청이 그 결과를 전제로 한다고 볼 근거가 없다.
- 완료 정리 과정에서 source of truth 변경, 정책 결정, 위험 변경, 데이터 삭제, public API 제거, migration, dependency 대량 변경이 필요하다.
- 선행 Task artifact의 DRAFT 상태가 실제 미실행을 의미하는지 단순 문구 누락인지 판별할 수 없다.
- 후속 작업을 시작하려면 새로운 제품 판단이나 설계 판단을 정해야 한다.

사용자-facing 보고에서는 이렇게 말한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
선행 작업은 검증이 끝났고 남은 것은 완료 기록 정합성 정리뿐입니다.
먼저 완료 기록과 문서 상태를 맞춘 뒤, 같은 요청 범위 안에서 다음 작업으로 이어갑니다.
```
