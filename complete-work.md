# Complete Work Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: 검증과 사용자 review approval 뒤 Task 완료 조건을 확인할 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

## 핵심 용어

- 이번 작업 기준 묶음: 이번 작업에서 따라야 할 승인된 기준 문서 묶음.
- 검증: 구현 결과가 기준 문서, 작업 기준서, 구현 지시서와 맞는지 확인하는 절차.
- 완료 기록: 검증과 review approval 또는 후속 작업 전환 연계 조건 확인 뒤 남기는 완료 기록.

이 skill은 Task 완료 조건을 확인하고 완료 기록을 남긴다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 completion record를 생성하거나 수정하지 않는다. 완료 가능 여부와 남은 조건만 분석 보고서로 제공한다.

verification과 사용자 review approval 없이는 complete하지 않는다. 단, 검증 완료된 선행 작업 뒤에 사용자가 후속 작업을 명확히 요청했고 `_approval-reference.md`의 후속 작업 전환 연계 조건을 모두 만족하면 completion record와 문서 상태 정합성 정리에 한해 같은 요청 범위 안에서 완료로 이어갈 수 있다.

Completion record artifact는 `_artifact-metadata.md`, `_artifact-templates.md`의 `Artifact Metadata Template`, `_status-machine.md`를 따른다. 완료 승인은 `_approval-reference.md`의 REVIEW_APPROVAL, COMPLETION_APPROVAL, 또는 후속 작업 전환 연계 조건과 연결한다.

사용자-facing 완료 보고는 기본적으로 확인한 기준과 verification 결과를 기준으로 짧게 작성한다. cleanup/delete 작업은 `cleanup-delete.md`의 기존 cleanup-delete 완료 보고 형식을 우선할 수 있다.

완료 불가는 내부 status로만 보고하지 않고, 완료 조건 중 무엇이 남았는지로 설명한다.

완료 불가 시 내부 진단표보다 "완료하려면 남은 일"을 먼저 말한다. 상세 진단은 사용자가 요청했을 때 제공한다.

기본 완료 보고에서는 `SOT`, `Product Readiness`, `Engineering Readiness`, `Implementation Readiness`, `READY`, `NOT READY`, `Storage Intent Check`, `Behavior Contract Check`, `State Meaning Check`를 제목이나 결론으로 먼저 쓰지 않는다. 내부 용어는 completion record metadata나 사용자가 요청한 상세 판정표에만 그대로 둔다.

## 완료 조건

다음 조건이 모두 만족되어야 한다.

- prompt approved
- implementation done
- check passed
- verification VERIFIED
- user review approved
- pending Source of Truth Change Request 없음
- 작업 기준 묶음과 실제 변경 범위가 일치
- known source of truth conflict 없음
- 작업 기준서와 source of truth 정합
- 모든 dependsOn Task COMPLETE
- 미확정 결정 없음
- prompt execution이 명시적으로 승인됨
- completion 근거 artifact가 legitimacy check 통과
- invalid/quarantined/superseded artifact 없음

## 역할

- 완료 전 IDE diff review 또는 동등한 review를 사용자에게 요청한다.
- check result가 통과했는지 확인한다.
- verification status가 VERIFIED인지 확인한다.
- 사용자 review approval이 있는지 확인한다. 단, 후속 작업 전환 연계 조건을 모두 만족하는 경우에는 completion record와 status 정합성 정리를 먼저 수행하고 후속 작업으로 이어간다.
- 완료 기록을 남긴다.

## 규칙

- verification 없이 complete 하지 마라.
- 사용자가 review 승인하지 않으면 complete 하지 마라.
- 테스트 통과만으로 complete 하지 마라.
- verification status가 BLOCKED_BY_MISSING_CONTEXT 또는 BLOCKED_BY_POLICY_CONFLICT이면 complete 하지 마라.
- verification status가 NEEDS_SOURCE_OF_TRUTH_CHANGE이면 complete 하지 마라.
- 미확정 결정이 해결되기 전에는 complete로 진행하지 마라.
- Git commit은 이 skill의 필수 기능이 아니다.
- source of truth 변경이 섞여 있으면 complete하지 말고 verification 또는 policy conflict로 되돌린다.
- source of truth 변경 요청이 APPLIED 후 VALIDATED 되지 않았으면 complete하지 마라.
- Known Conflicts After Apply가 비어 있지 않으면 complete하지 마라.
- source of truth 문서 일부만 변경되어 다른 APPROVED 문서와 충돌하면 complete하지 마라.
- 작업 기준서가 변경된 source of truth와 불일치하면 complete하지 마라.
- dependsOn Task가 COMPLETE가 아니면 complete하지 마라.
- 현재 Task 또는 선행 Task의 미확정 결정을 "나중에"로 미루고 complete하지 마라.
- Prompt Draft Approval을 Prompt Execution Approval로 해석해 complete하지 마라.
- invalid/quarantined/superseded artifact가 있으면 complete하지 마라.
- legitimacy check를 통과하지 못한 prompt, verification result, completion record를 완료 근거로 사용하지 마라.
- 후속 작업 전환 요청을 검증되지 않은 선행 작업 완료 승인으로 해석하지 마라.
- 남은 일이 completion record, status, 실행 전 문구 정리 같은 artifact 정합성 보정뿐이고 후속 작업 전환 연계 조건을 모두 만족하면 승인 문구를 요구하지 말고 정리 후 다음 단계로 진행하라.

## Verification 결과별 허용 행동

- VERIFIED: user review approval 요청 가능. 승인 후 complete 가능. 후속 작업 전환 연계 조건을 모두 만족하면 completion record와 문서 상태 정합성 정리 후 다음 단계로 이어갈 수 있다.
- NEEDS_REVISION: complete 금지. revision-prompt 생성과 사용자 승인 후 revision으로 이동.
- BLOCKED_BY_MISSING_CONTEXT: complete 금지. 미확정 결정 질문만 가능. 코드 수정과 revision 금지.
- BLOCKED_BY_POLICY_CONFLICT: complete 금지. 충돌 보고와 사용자 정책 결정 또는 source of truth 수정 승인 필요.
- NEEDS_SOURCE_OF_TRUTH_CHANGE: complete 금지. Source of Truth Change Request와 사용자 승인 절차 필요.
- known source of truth conflict가 남아 있으면 모든 상태에서 complete 금지.
- BLOCKED_BY_PREDECESSOR: complete 금지. 선행 Task 완료와 미확정 결정 해결 필요.
- BLOCKED_BY_INVALID_ARTIFACT: complete 금지. artifact 격리/폐기/복구 방향 결정 필요.

## 완료 기록에 포함할 내용

- artifact metadata
- status
- approvalRefs
- projectId
- taskId
- completedAt
- prompt approval 여부
- check result
- verification result
- review approval 여부
- pending Source of Truth Change Request 여부
- known source of truth conflict 여부
- dependsOn Task 완료 여부
- 미확정 결정 여부
- artifact legitimacy check 결과
- invalid/quarantined/superseded artifact 여부
- archive/superseded 문서 참조 여부와 참조 목적
- generated/index/memory/recall/previous-report 자료를 source of truth로 사용하지 않았다는 확인
- cleanup/delete Task인 경우 keep list, delete list, archive 보존 여부, 삭제하지 않은 항목과 이유, 남은 legacy 후보
- 변경 요약
- 남은 suggestions

## 짧은 기본 완료 보고 형식

기본 완료 보고는 검증 중심으로 다음 항목을 우선 작성한다.

```text
확인한 기준:
- ...

현재 판단:
- 바로 완료 가능 / 아직 결정 필요 / 수정 필요

이유:
- ...

변경 범위:
- ...

검증 결과:
- ...

남은 위험:
- ...

다음에 할 일:
- ...
```

필요하면 "먼저 정할 것", "내 추천", "내가 물어볼 것"을 추가한다. 내부 readiness 결과를 사용자에게 보여줘야 할 때도 "제품 방향", "설계 준비 상태", "지금 바로 만들 수 있는지"로 바꿔 말한다.

cleanup/delete 작업은 keep list, delete list, archive 보존 여부, 삭제하지 않은 항목과 이유, 남은 legacy 후보를 포함하는 cleanup-delete 완료 보고 형식을 우선할 수 있다. 이 경우에도 바로 완료 가능한지와 남은 결정을 짧게 요약한다.

## Completion Record Metadata 예시

```yaml
artifact:
  id: COMPLETE-TASK-002-001
  type: completion-record
  status: COMPLETE
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: complete-work
  taskId: TASK-002
  projectId: example-project
  sourceOfTruthSnapshot: SOT-SNAPSHOT-001
  requiredDocuments:
    - PRODUCT-SOT-001
  dependsOnSnapshot:
    - taskId: TASK-001
      requiredStatus: COMPLETE
      actualStatus: COMPLETE
  approvalRefs:
    - APPROVAL-TASK-002-REVIEW
    - APPROVAL-TASK-002-COMPLETE
  generatedFrom:
    - runs/TASK-002/verification-result.md
  knownConflicts: []
  supersedes: []
  supersededBy: null
  readinessCheck:
    productReadiness: READY
    engineeringReadiness: READY
    implementationReadiness: READY
    conclusion: IMPLEMENTATION_ALLOWED
```

## User-Facing Completion

사용자-facing 보고에서는 완료 조건을 쉬운 말로 설명한다.

예:

```text
아직 완료로 기록할 수 없습니다. 검증은 끝났지만 사용자 리뷰 승인이 남아 있습니다.
```

후속 작업 전환 연계 조건을 모두 만족하면 승인 문구를 요구하지 않고 다음 형식을 우선 사용한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
선행 작업은 검증이 끝났고 남은 것은 완료 기록 정합성 정리뿐입니다.
먼저 완료 기록과 문서 상태를 맞춘 뒤, 같은 요청 범위 안에서 다음 작업으로 이어갑니다.

진행할 작업:
- 선행 작업 완료 기록 정리
- 선행 작업 문서 상태 정합성 확인
- 다음 작업 지시서 작성 또는 요청된 다음 단계 진행

진행하지 않을 작업:
- 새 제품 판단이나 설계 판단 임의 결정
- 검증되지 않은 변경 완료 처리
- 요청 범위 밖 구현
```

완료할 수 없을 때는 다음 형식을 우선 사용한다.

```text
아직 완료로 기록할 수 없습니다.
완료 전에 다음이 필요합니다.
1. 남은 검증 문제를 정리해 주세요.
2. 변경 결과를 리뷰해 주세요.
3. 완료 기록을 남겨도 되는지 승인해 주세요.

다음에 할 일:
아직 직접 진행하면 안 됩니다. 먼저 아래 중 하나를 선택해야 합니다.

선택지:
1. 남은 검증 문제를 먼저 수정한다.
2. 변경 결과를 리뷰하고 승인한다.
3. 완료 기록 생성을 보류한다.

제 추천:
- 검증 문제가 없으면 변경 결과를 리뷰하고 완료 기록 생성을 승인합니다.

바로 답할 수 있는 문장:
"변경 결과를 승인한다. 완료 기록을 남겨라."
```

## 다음 단계

- 모든 조건 충족: 완료 기록을 남기고 Task를 complete 처리한다.
- 조건 미충족: 미충족 조건을 사용자에게 보고하고 해당 skill 단계로 되돌아간다.
- 사용자 개입 없이 완료 가능한 경우에는 완료 보고를 작성하고 다음 후보를 제시한다.
- 사용자 review approval이나 후속 작업 전환 연계 조건이 없고, 미확정 결정, 정책 충돌, 선행 Task 미완료가 있으면 완료하지 않고 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다.

완료한 경우에는 다음 형식으로 끝낸다.

```text
다음에 할 일:
이번 작업은 완료되었습니다.

다음 후보:
1. ...
2. ...
3. ...

제 추천:
- ...
```
