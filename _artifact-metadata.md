# Artifact Metadata Standard

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 문서는 CDD V2의 공통 artifact metadata를 정의한다.

목표는 파일 존재 여부가 아니라, artifact가 어떤 조건과 승인으로 생성되었는지 추적하는 것이다.

V2.1의 실제 YAML 골격은 `_artifact-templates.md`의 `Artifact Metadata Template`을 우선 사용한다. 이 문서는 필드 의미와 판단 원칙을 설명한다.

## 대상 Artifact

다음 artifact는 가능한 한 공통 metadata를 포함한다.

- source-of-truth document
- project-context
- document-registry
- change-request
- plan
- task-contract
- implementation-prompt
- verification-result
- revision-prompt
- completion-record
- approval-record
- harness-evaluation-note
- harness-test-log
- harness-experiment-plan

`harness-evaluation-note`, `harness-test-log`, `harness-experiment-plan`은 harness operation artifact다. Project source of truth 문서가 아니다.

## 공통 Metadata

```yaml
artifact:
  id: PROMPT-TASK-002-001
  type: implementation-prompt
  status: DRAFT
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: write-implementation-prompt
  taskId: TASK-002
  projectId: example-project
  projectContextRef: PROJECT-CONTEXT-001
  sourceOfTruthSnapshot: SOT-SNAPSHOT-001
  requiredDocuments:
    - PRODUCT-SOT-001
    - ENGINEERING-SOT-001
  dependsOnSnapshot:
    - taskId: TASK-001
      requiredStatus: COMPLETE
      actualStatus: BLOCKED_BY_MISSING_CONTEXT
  approvalRefs: []
  generatedFrom:
    - tasks/TASK-002.yml
    - docs/architecture/api-contract.md
  knownConflicts: []
  supersedes: []
  supersededBy: null
```

## 필드 의미

- `artifact.id`: artifact의 안정적인 식별자
- `artifact.type`: artifact 종류
- `artifact.status`: `_status-machine.md`의 상태
- `artifact.schemaVersion`: 적용한 harness artifact schema 버전
- `artifact.createdAt`: 생성 시각
- `artifact.createdByRole`: 생성한 role 또는 skill
- `artifact.taskId`: 관련 Task
- `artifact.projectId`: 프로젝트 식별자
- `artifact.projectContextRef`: 산출물이 참조한 Project Context artifact
- `artifact.sourceOfTruthSnapshot`: 생성 당시 기준 문서 snapshot
- `artifact.requiredDocuments`: 생성 근거 문서
- `artifact.dependsOnSnapshot`: 생성 당시 선행 Task 상태
- `artifact.approvalRefs`: 관련 승인 기록
- `artifact.generatedFrom`: 생성 입력 파일
- `artifact.knownConflicts`: 생성 시점에 알려진 충돌
- `artifact.supersedes`: 이 artifact가 대체한 artifact
- `artifact.supersededBy`: 이 artifact를 대체한 artifact
- `artifact.userFacingSummary`: 사용자에게 보여줄 쉬운 요약

## 규칙

- metadata가 없는 기존 artifact는 자동 invalid가 아니다.
- 하지만 legitimacy 판단이 불가능하면 사용자 확인 또는 quarantine 후보로 보고한다.
- 새 artifact는 가능한 한 metadata를 포함한다.
- 새 artifact의 metadata는 가능한 한 `_artifact-templates.md`의 템플릿 형식을 따른다.
- metadata는 "파일 존재"가 아니라 "생성 조건"을 설명해야 한다.
- metadata는 artifact legitimacy check의 입력이지, 단독 승인 근거가 아니다.
- projectContextRef는 프로젝트 현실을 가리키는 참조다. 하네스 검증 목적을 projectContext에 강제로 넣는 근거가 아니다.

## Legitimacy와의 관계

metadata가 있더라도 다음이 맞지 않으면 정상 baseline으로 사용할 수 없다.

- 필요한 approval reference가 없다.
- 생성 당시 `dependsOn` 상태가 조건을 만족하지 않는다.
- 생성 당시 `documentCoverage`가 READY가 아니다.
- 생성 당시 source of truth가 VALIDATED가 아니다.
- Missing Context 또는 Policy Conflict가 unresolved 상태였다.
- 이후 source of truth 변경으로 superseded 되었다.

metadata가 없거나 불충분하면 다음 중 하나로 처리한다.

- 사용자에게 생성 근거 확인
- `QUARANTINED` 후보 보고
- `SUPERSEDED` 후보 보고
- gate를 다시 통과한 새 artifact 생성 제안
