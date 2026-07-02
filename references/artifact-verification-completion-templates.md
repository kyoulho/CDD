# Artifact Verification and Completion Templates

> Access: Reference.
> `_artifact-templates.md`의 검증/완료 상세 예시를 분리한 reference다.
> 기본 읽기 경로 문서가 아니며, verification/completion 산출물의 상세 YAML 예시가 필요할 때만 연다.

이 문서는 검증 결과 metadata와 사용자-facing 완료 보고 예시를 담는다. 핵심 계약은 `_artifact-templates.md`의 `## 6. Verification Result Metadata Template`과 `## Completion Report Example`에 남아 있다.

## Verification Result Metadata Template

검증 결과의 metadata와 verification matrix를 함께 기록한다.

```yaml
artifact:
  id: VERIFY-TASK-000-001
  type: verification-result
  status: BLOCKED
  schemaVersion: cdd.v2.1
  projectId: project-id
  projectContextRef: PROJECT-CONTEXT-001
  taskId: TASK-000
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: verify-work
  sourceOfTruthSnapshot: SOT-SNAPSHOT-000
  requiredDocuments:
    - DOC-001
  dependsOnSnapshot:
    - taskId: TASK-001
      requiredStatus: COMPLETE
      actualStatus: COMPLETE
  approvalRefs:
    - APPROVAL-PROMPT-EXECUTION-000
  generatedFrom:
    - prompts/TASK-000.md
    - runs/TASK-000/check-result.yml
  knownConflicts: []
  supersedes: []
  supersededBy: null
  userFacingSummary: "TASK-000 구현 결과 검증 기록입니다."

verification:
  status: BLOCKED_BY_MISSING_CONTEXT
  verifiedAt: "2026-06-08T00:00:00Z"
  verifiedByRole: verification
  implementationRef: runs/TASK-000/implementation-summary.md
  promptRef: prompts/TASK-000.md
  taskContractRef: tasks/TASK-000.yml
  readinessRecheck:
    productSotMatched: true
    engineeringSotMatched: true
    implementationScopeRespected: true
    forbiddenScopeViolated: false
    archiveSupersededMaterialUsedAsActiveSot: false
    readinessWasNotReadyButImplementationOccurred: false
  legitimacyReportRefs:
    - LEGITIMACY-000
  matrix:
    - check: taskContractSatisfied
      result: PASS
      source: tasks/TASK-000.yml
      evidence: "acceptance criteria implemented"
    - check: requiredDocumentsFollowed
      result: PASS
      source: SOT-SNAPSHOT-000
      evidence: "no conflicting behavior found"
    - check: productSotMatched
      result: PASS
      source: PRODUCT-SOT-001
      evidence: "implemented behavior matches Product SOT"
    - check: engineeringSotMatched
      result: PASS
      source: ENGINEERING-SOT-001
      evidence: "implemented structure matches Engineering SOT"
    - check: readinessAllowedImplementation
      result: BLOCKED
      source: tasks/TASK-000.yml
      evidence: "Implementation Readiness was NOT_READY"
    - check: documentCoverageReady
      result: PASS
      source: tasks/TASK-000.yml
      evidence: "documentCoverage.status is READY"
    - check: interactionDesignAllowedBeforeInterfaceDesign
      result: BLOCKED
      source: tasks/TASK-000.yml
      evidence: "interface design appeared while interaction design was not approved"
    - check: storageIntentAllowedBeforeDbDesign
      result: BLOCKED
      source: tasks/TASK-000.yml
      evidence: "DB design appeared while Storage Intent Check was DB_DESIGN_BLOCKED"
    - check: behaviorContractAllowedBeforeApiDesign
      result: PASS
      source: tasks/TASK-000.yml
      evidence: "API design was backed by Behavior Contract Check"
    - check: stateMeaningAllowedBeforeStatusModel
      result: PASS
      source: tasks/TASK-000.yml
      evidence: "status model was backed by State Meaning Check"
    - check: operationalQualityAllowedBeforeDesign
      result: BLOCKED
      source: tasks/TASK-000.yml
      evidence: "performance/security/operation design appeared while operational quality criteria were not approved"
    - check: forbiddenApproachesViolated
      result: FAIL
      source: prompts/TASK-000.md
      evidence: "unapproved test profile introduced"
    - check: testRequirementsSatisfied
      result: BLOCKED
      source: tasks/TASK-000.yml
      evidence: "test strategy is missing"
  findings:
    - id: FINDING-001
      severity: high
      type: BLOCKED_BY_MISSING_CONTEXT
      summary: "Test strategy is not approved."
      requiredUserDecision: "Choose the test database/profile/migration strategy."
  allowedActions:
    - "ask Missing Context question"
  blockedActions:
    - "revision"
    - "complete"
  userFacingSummary: "구현 결과를 바로 완료 처리할 수 없습니다. 먼저 테스트 방식을 정해야 합니다."
```

목적:

- Verification Agent가 Task, 기준 문서, requiredDocuments, forbiddenApproaches, testRequirements를 같은 matrix로 검증하게 한다.
- 검증 결과별 허용 행동과 금지 행동을 산출물에 남긴다.

## Completion Report Example

사용자에게 보여주는 완료 보고는 verification 결과와 바로 완료 가능한지 여부를 자연어로 짧게 요약한다. 내부 completion record나 에이전트 간 전달물에는 `readinessCheck`, `Product SOT`, `Engineering SOT` 같은 내부 필드를 사용할 수 있지만, 기본 사용자 보고의 제목으로 먼저 쓰지 않는다.

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

사용자 선택이 필요한 경우에는 다음 블록을 포함한다.

```text
다음에 할 일:
아직 직접 진행하면 안 됩니다. 먼저 아래 중 하나를 선택해야 합니다.

선택지:
1. ...
2. ...
3. ...

제 추천:
- ...

바로 답할 수 있는 문장:
"..."
```

사용자 개입 없이 진행 가능한 경우에는 다음 블록을 포함하고, 실제로 다음 단계까지 진행한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
현재 기준으로 안전하게 진행할 수 있으므로, 요청 범위 안에서 다음 작업까지 진행합니다.

진행할 작업:
- ...

진행하지 않을 작업:
- ...
```

완료한 경우에는 다음 블록을 포함한다.

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

cleanup/delete 작업은 `cleanup-delete.md`의 완료 보고 형식을 우선할 수 있지만, 바로 완료 가능한지와 남은 결정은 생략하지 않는다.
