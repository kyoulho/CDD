# Artifact Templates V2.1

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 문서는 CDD V2.1 산출물 템플릿을 정의한다.

목표는 규칙을 추가하는 것이 아니라, 기존 V2의 metadata, status, approval, legitimacy 기준을 실제 산출물에 일관되게 붙일 수 있게 하는 것이다.

사용자-facing 보고에서는 내부 필드명을 먼저 보여주지 않고 "이 파일을 지금 기준으로 써도 되는지 확인했습니다"처럼 쉬운 표현을 우선 사용한다. 내부 YAML은 artifact 판단과 감사 기록에 사용한다.

## 1. Artifact Metadata Template

모든 주요 산출물의 공통 머리말이다.

```yaml
artifact:
  id: ARTIFACT-ID
  type: implementation-prompt
  status: DRAFT
  schemaVersion: cdd.v2.1
  projectId: project-id
  projectContextRef: PROJECT-CONTEXT-001
  taskId: TASK-000
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: write-implementation-prompt
  sourceOfTruthSnapshot: SOT-SNAPSHOT-000
  requiredDocuments:
    - DOC-001
  dependsOnSnapshot:
    - taskId: TASK-001
      requiredStatus: COMPLETE
      actualStatus: COMPLETE
  approvalRefs: []
  generatedFrom:
    - path/to/input.yml
  placement:
    checkedProjectStructure:
      - docs/README.md
      - document-registry.yml
      - existing task artifacts
    existingPattern: task-per-file
    targetFiles:
      - path/to/existing-or-target.md
    newFiles: []
    indexUpdatesRequired: []
    newFileReason: null
    structureChangeRequired: false
  knownConflicts: []
  supersedes: []
  supersededBy: null
  userFacingSummary: "이 산출물은 TASK-000을 진행하기 위한 초안입니다."
```

목적:

- 파일 존재 여부가 아니라 생성 조건, 승인, 기준 문서, 선행 작업 상태를 기록한다.
- 대상 프로젝트의 기존 문서 배치 구조와 저장 위치 결정 근거를 함께 기록한다.
- legitimacy check의 입력으로 사용한다.
- `projectContextRef`는 프로젝트 자체의 목적과 운영 전제를 참조한다. 하네스 평가 목적을 Project Context에 섞는 용도로 사용하지 않는다.

## Document Placement Check Template

작업 기준서, 구현 지시서, 검증 결과, 완료 기록을 만들거나 수정하기 전에 사용한다. 이 확인은 산출물 내부 형식보다 먼저 수행한다.

```yaml
documentPlacementCheck:
  checkedAt: "2026-06-08T00:00:00Z"
  checkedByRole: plan-task
  checkedProjectStructure:
    - docs/README.md
    - document-registry.yml
    - existing task artifacts
  existingPattern: single-accumulated-document
  existingPatternEvidence:
    - "docs/tasks.md contains multiple task entries"
  targetFilesToModify:
    - docs/tasks.md
  newFilesToCreate: []
  newFileReason: null
  readmeOrIndexUpdatesRequired:
    - docs/README.md
  readCostCheck:
    hotPathDocuments:
      - path: docs/tasks.md
        lines:
        bytes:
        role: active-index
        readFrequency: every-task
        recommendation: keep
    splitCandidates: []
    keepCandidates:
      - docs/tasks.md
    thresholds:
      hotPathSplitCandidate: "400 lines or 40KB"
      accumulatedHistorySplitCandidate: "1000 lines"
  currentWorkPointer:
    path: docs/project/current-work.md
    exists: false
    requiredFields:
      - currentGate
      - nextTask
      - activeTasks
      - requiredReadDocuments
      - excludedHistoricalRecords
      - currentConflicts
      - readmeOrIndexUpdatesRequired
    missingFields: []
    updateRequired: false
  readPathContract:
    requiredReadDocuments: []
    excludedHistoricalRecords: []
    excludedNonSotReferences: []
    oversizedRequiredReadDocuments: []
    activeHistoryMixedDocuments: []
    decisionLogSplitCandidates: []
  baselineRoleCheck:
    activeCriteriaDocuments: []
    historicalRecords: []
    nonSotReferences: []
    currentVsHistoryConflicts: []
  matchesExistingStructure: true
  structureChangeRequired: false
  userApprovalRequired: false
  userFacingSummary: "기존 작업 기준서가 단일 문서에 누적되는 구조이므로 같은 문서에 추가합니다."
```

규칙:

- `docs/README.md`, 문서 index, document registry, 기존 작업 산출물 목록, 기존 파일명과 누적 방식을 먼저 확인한다.
- 기존 구조가 단일 작업 기준서에 task를 누적하는 방식이면 후속 phase/task도 같은 문서에 추가한다.
- 기존 구조가 task별 파일 분리 방식이면 후속 task도 같은 방식으로 분리한다.
- 기존 구조를 따르더라도 기본 읽기 경로의 문서가 400줄 또는 40KB를 넘으면 분리 후보로 보고한다.
- 1000줄 이상 누적 문서는 active index와 history 문서 분리 후보로 보고한다.
- 분리 우선순위는 매번 읽는 hot path 문서부터 잡는다.
- 짧고 응집된 문서는 파일 수를 늘리지 않고 기존 구조를 유지한다.
- 작업 기준서, ADR, 검증 결과, 완료 기록이 누적 문서로 커졌다면 active index와 history record 분리를 우선 검토한다.
- Product/Engineering 기준 문서는 너무 커질 때만 domain packet으로 나누고, 원래 기준 문서는 얇은 진입점과 index로 유지한다.
- 루트 `DESIGN.md`가 승인된 단일 디자인 기준이면 유지한다. 너무 커지면 root `DESIGN.md`는 전역 원칙과 index로 남기고 화면별 세부 기준만 분리 후보로 제안한다.
- 문서가 커졌거나 다음 작업 판단에 과거 완료 기록까지 읽어야 하면 현재 작업 포인터 역할을 확인한다. 파일명은 강제하지 않고 기본 후보는 `docs/project/current-work.md`다.
- 현재 작업 포인터에는 현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서, 읽지 않을 과거 기록, 현재 기준과 충돌하는 문서, README/index 갱신 필요 여부가 있어야 한다.
- 기본 읽기 경로 계약은 이번 작업에서 반드시 읽을 문서와 기본 읽기 경로에서 제외할 과거 기록/보조 자료를 분리한다.
- 큰 작업 기준서는 현재 진행 가능한 task만 담은 active index와 완료 기록을 담은 history로 분리하는 방식을 우선 검토한다.
- decision log가 커졌다면 현재 적용 중인 결정, 최근 변경 결정, 과거 결정 기록, superseded 결정을 나눠 읽게 한다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference는 기본적으로 `nonSotReferences`에 분류하고 기본 읽기 경로에서 제외한다.
- 과거 task completion, verification, prompt, old task 문서는 `historicalRecords`로 분류한다. active 기준으로 쓰려면 active 기준 문서나 registry의 승격 근거가 필요하다.
- 현재 기준과 과거 산출물이 충돌하면 `currentVsHistoryConflicts`에 기록하고, 저장 또는 후속 작업으로 진행하기 전에 사용자에게 정합성 정리 선택지를 제시한다.
- 새 문서 파일을 만들기 전에는 왜 기존 문서에 추가하지 않고 새 파일이 필요한지 사용자에게 보고한다.
- 기존 구조와 다른 파일 배치를 하려면 일부 파일만 다르게 만들지 말고 전체 문서 구조 변경안으로 제안하고 사용자 승인을 받는다.
- `matchesExistingStructure: false` 또는 `structureChangeRequired: true`이면 auto-stop하고 사용자 확인 전에는 저장하지 않는다.
- 저장 전 사용자 보고에는 수정할 파일, 새로 만들 파일, 기존 문서 구조와 맞는지, 현재 작업 포인터 갱신 필요 여부, 기본 읽기 경로 계약 변경 여부, 분리 후보, 유지 후보, 삭제/보존/비-SOT 분류 후보, README/index 갱신 필요 여부를 포함한다.

## Read-only Audit Tool Contract

`bin/cdd-audit`는 문서 정합성 반복 점검을 위한 보조 도구다. CDD 판단을 대신하지 않고, 파일 write, git write, agentmemory write, 네트워크 호출, 자동 분리, 자동 삭제, 과거 기록 자동 승격, 현재 기준 자동 확정을 수행하지 않는다.

명령:

```text
cdd-audit docs [--root <path>] [--config <path>] [--format text|json] [--fail-on blocking|never]
```

입력:

- project root. 없으면 현재 위치에서 위로 올라가며 marker를 찾는다.
- optional config: `.cdd-audit.json`, `cdd-audit.json`, `.cdd/audit.json`.
- 읽을 문서 후보: `*.md`, `*.yml`, `*.yaml`.
- 제외 directory 후보: `.git`, `node_modules`, `.venv`, `dist`, `build`, `.next`, `.cache`, `__pycache__`.

출력:

- 현재 작업 포인터와 누락 필드
- 현재 gate, 다음 task, active task
- 반드시 읽을 문서와 제외할 과거 기록
- 400줄 또는 40KB를 넘는 기본 읽기 경로 문서
- 1000줄 이상 누적 문서
- active/history 혼재 후보
- 비-SOT 자료 혼입 후보
- README/index 갱신 필요 여부

exit code:

- `0`: 실행 성공, 차단 항목 없음
- `2`: 실행 성공, 차단 항목 있음
- `1`: 실행 실패

`--fail-on never`는 automation에서 사용할 수 있다. 이 옵션은 차단 finding을 숨기지 않고 exit code만 `0`으로 바꾼다.

## Harness Operation Artifact Types

하네스 평가 목적을 추적해야 한다면 project source of truth가 아닌 별도 harness operation artifact를 사용한다.

```text
harness-evaluation-note
harness-test-log
harness-experiment-plan
```

These are not project source of truth documents.

## 2. Approval Record Template

승인 기록은 모호한 자연어를 권한으로 확대 해석하지 않기 위한 독립 기록이다.

```yaml
approval:
  id: APPROVAL-000
  type: PATCH_APPROVAL
  targetArtifactId: ARTIFACT-ID
  targetArtifactType: skill-layer
  approvedScope:
    - start-here.md
    - _authority-boundary.md
  approvedBy: user
  approvedAt: "2026-06-08T00:00:00Z"
  approvalText: "CDD skill 파일 수정을 승인합니다."
  authorityLevel: patch
  preconditions:
    - "Target project files must not be modified."
    - "CLI/tools implementation is forbidden."
  expiresWhen:
    - "approvedScope changes"
    - "new files outside approvedScope are required"
  notes: []
```

목적:

- Direction, Draft, Patch, Apply, Prompt Execution, Review, Completion 승인을 분리한다.
- 승인 범위 밖 파일을 수정하지 않도록 한다.

## 3. Legitimacy Report Template

기존 artifact를 baseline으로 사용하기 전에 작성하는 판정 기록이다.

```yaml
legitimacyReport:
  id: LEGITIMACY-000
  checkedAt: "2026-06-08T00:00:00Z"
  checkedByRole: start-here
  targetArtifact:
    id: ARTIFACT-ID
    type: implementation-prompt
    path: prompts/TASK-000.md
    status: DRAFT
  result: BLOCKED
  checks:
    metadataPresent:
      result: PASS
      reason: "artifact metadata exists"
    statusAllowed:
      result: FAIL
      reason: "DRAFT is reviewable but not executable"
    approvalRefsValid:
      result: FAIL
      reason: "Prompt execution approval is missing"
    dependenciesSatisfied:
      result: PASS
      reason: "dependsOn snapshot is complete"
    documentCoverageReady:
      result: PASS
      reason: "documentCoverage is READY"
    sourceOfTruthSnapshotValid:
      result: PASS
      reason: "snapshot references approved documents"
    missingContextResolved:
      result: PASS
      reason: "no unresolved Missing Context recorded"
    policyConflictsResolved:
      result: PASS
      reason: "knownConflicts is empty"
    superseded:
      result: PASS
      reason: "not superseded"
  allowedActions:
    - "ask user for execution approval"
    - "continue execution if draft-to-execution continuation conditions are satisfied"
  blockedActions:
    - "implementation"
  userFacingSummary: "지시서 파일은 있지만 실행 승인 기록이나 초안 작성 후 실행 연계 조건을 확인해야 바로 구현할 수 있습니다."
```

목적:

- "파일이 있다"를 "지금 기준으로 사용할 수 있다"와 분리한다.
- invalid, quarantined, superseded 후보를 판단한다.

## 4. Source Of Truth Snapshot Template

산출물이 생성될 당시 참조한 기준 문서 묶음을 기록한다.

```yaml
sourceOfTruthSnapshot:
  id: SOT-SNAPSHOT-000
  projectId: project-id
  projectContextRef: PROJECT-CONTEXT-001
  capturedAt: "2026-06-08T00:00:00Z"
  capturedByRole: document-readiness
  registryPath: tools/cdd/projects/project-id/document-registry.yml
  documents:
    - id: DOC-001
      path: docs/architecture/api-contract.md
      type: API_CONTRACT
      status: APPROVED
      versionRef: "sha-or-version"
      owns:
        - api.request
        - api.response
      requiredFor:
        - TASK-000
  currentCriteria:
    hotPathDocuments:
      - docs/product/product-sot.md
    activeIndexes: []
    domainPackets: []
  historicalRecords:
    - path: docs/tasks/history.md
      role: historical-record
      reason: "과거 작업 완료 기록이며 현재 기준 문서가 아니다."
  nonSotReferences:
    - path: .codesight/wiki/index.md
      role: generated-map
      reason: "탐색 보조 자료이며 현재 기준이 아니다."
  readCost:
    splitCandidates: []
    keepCandidates: []
    readmeOrIndexUpdatesRequired: []
  currentVsHistoryConflicts: []
  coverageSummary:
    status: READY
    missing: []
  knownConflicts: []
  userFacingSummary: "필요한 기준 문서가 준비된 상태입니다."
```

목적:

- prompt, verification, completion이 어떤 기준 문서 버전을 참조했는지 추적한다.
- 이후 기준 문서 변경 시 supersede 여부를 판단한다.
- 현재 기준, 과거 기록, 보조 자료를 분리해 후속 작업이 과거 산출물을 현재 기준처럼 읽지 않게 한다.
- 기본 읽기 경로가 커졌을 때 active index, history, domain packet 분리 후보를 추적한다.

## Design Intent Checks Template

저장 구조, API, 상태 모델을 산출물에 넣기 전에 의미 확인 결과를 기록한다.

```yaml
designIntentChecks:
  interactionDesign:
    required: true
    result: "상호작용 설계 보류"
    actor:
    entryPoint:
    startingContext:
    input: []
    action: []
    successOutput:
    failureOutput:
    emptyStateOutput:
    permissionDeniedOutput:
    inProgressFeedback:
    keyCopyOrResult:
    missingDecisions:
      - "The user/operator interaction is not approved yet."
  frontendUx:
    required: true
    result: FRONTEND_UX_BLOCKED
    targetScreens: []
    userGoals: []
    implementationContract:
      layout:
      informationPriority:
      forbiddenPatterns: []
      responsive:
      browserVerification:
      currentViewportFirst: true
    requiredRoleCoverage:
      - FRONTEND_UX_CRITERIA
      - USER_FLOW_OR_INTERACTION_SPEC
      - DESIGN_SYSTEM_OR_UI_PATTERN
      - FRONTEND_ARCHITECTURE
    missingDecisions:
      - "The frontend UX implementation contract is not approved yet."
  storageIntent:
    required: true
    result: DB_DESIGN_BLOCKED
    stores:
    reason:
    readBack:
    notStored: []
    structuredFields: []
    freeTextFields: []
    retentionPolicy:
    ownershipScope:
    missingDecisions:
      - "What is being stored and why is not approved yet."
  behaviorContract:
    required: true
    result: API_DESIGN_BLOCKED
    expectedBehavior:
    input:
    successResult:
    failureResult:
    authorizationScope:
    idempotencyRetry:
    exposedRepresentation:
    missingDecisions:
      - "The behavior contract is not approved yet."
  stateMeaning:
    required: true
    result: STATE_MODEL_BLOCKED
    meaning:
    transitionEvents: []
    allowedActionsByState: []
    terminalFailureCancelMeaning:
    storedOrDerived:
    exposedExternally:
    missingDecisions:
      - "The state meaning is not approved yet."
  operationalQuality:
    required: true
    result: "설계 보류"
    expectedDataVolume:
    queryBehavior:
    sortSearchPagination:
    responseTimeExpectation:
    permissionValidation:
    sensitiveDataExposure:
    failureVisibility:
    validationLocation:
    retryIdempotencyDuplicatePrevention:
    loggingAudit:
    missingDecisions:
      - "Operational quality criteria are not approved yet."
```

Rules:

- `상호작용 설계 가능`이 아니면 화면, CLI 명령, API surface, 배치 실행 방식, 저장 구조를 기록하지 않는다.
- `FRONTEND_UX_ALLOWED`가 아니면 route, page, component, layout, styling, motion, visual QA 기준을 기록하지 않는다.
- 분석 결과를 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저/스크린샷 검증 기준으로 고정한 UI 구현 계약이 없으면 웹/모바일 UI 구현 범위를 기록하지 않는다.
- `DB_DESIGN_ALLOWED`가 아니면 table, column, migration, repository, API DTO를 기록하지 않는다.
- `API_DESIGN_ALLOWED`가 아니면 API path, method, route, controller, request/response shape를 기록하지 않는다.
- `STATE_MODEL_ALLOWED`가 아니면 status enum, status column, state transition을 기록하지 않는다.
- `설계 가능`이 아니면 performance, security, operation, sorting, search, pagination, permission, retry, logging, audit 정책을 기록하지 않는다.
- `required: false`이면 해당 작업이 그 구조를 다루지 않는다는 뜻이지, 필요한 check를 우회해도 된다는 뜻이 아니다.

## 5. Prompt Artifact Template

구현 지시서 또는 수정 지시서의 표준 골격이다.

```yaml
artifact:
  id: PROMPT-TASK-000-001
  type: implementation-prompt
  status: DRAFT
  schemaVersion: cdd.v2.1
  projectId: project-id
  projectContextRef: PROJECT-CONTEXT-001
  taskId: TASK-000
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: write-implementation-prompt
  sourceOfTruthSnapshot: SOT-SNAPSHOT-000
  requiredDocuments:
    - DOC-001
  dependsOnSnapshot:
    - taskId: TASK-001
      requiredStatus: COMPLETE
      actualStatus: COMPLETE
  approvalRefs:
    - APPROVAL-PROMPT-DRAFT-000
  generatedFrom:
    - tasks/TASK-000.yml
  knownConflicts: []
  supersedes: []
  supersededBy: null
  userFacingSummary: "TASK-000 구현을 위한 지시서 초안입니다."

prompt:
  goal: "Implement TASK-000."
  taskContractRef: tasks/TASK-000.yml
  readinessCheck:
    productReadiness:
      status: READY
      evidence:
        - "Approved Product SOT defines user problem, target users, scenario, scope, non-goals, success criteria, failure UX, and vertical slice boundary."
      missingDecisions: []
      interactionDesign: "상호작용 설계 가능"
      frontendUx: FRONTEND_UX_ALLOWED
    engineeringReadiness:
      status: READY
      evidence:
        - "승인된 기술 설계 기준 문서가 제품 판단을 저장 구조, 상태, API, 코드 구조로 표현할 기준을 정의한다."
      missingDecisions: []
      designIntentChecks:
        operationalQuality: "설계 가능"
        storageIntent: DB_DESIGN_ALLOWED
        behaviorContract: API_DESIGN_ALLOWED
        stateMeaning: STATE_MODEL_ALLOWED
    implementationReadiness:
      status: READY
      evidence:
        - "SOT Packet, Task Contract, allowedScope, forbiddenScope, verificationCommands, user approval gate, and predecessor Task status are ready."
      missingDecisions: []
    conclusion: IMPLEMENTATION_ALLOWED
  sotPacketRef: SOT-PACKET-TASK-000
  allowedScope: []
  forbiddenScope: []
  verificationCommands: []
  projectContextSummary:
    projectType: []
    primaryPurpose: null
    productionIntent: null
    dataConsistencyCriticality: null
    allowedSimplifications: []
    forbiddenSimplifications: []
  documentCoverage:
    status: READY
    missing: []
  designIntentChecks:
    interactionDesign:
      required: false
      result: "상호작용 설계 가능"
      missingDecisions: []
    frontendUx:
      required: false
      result: FRONTEND_UX_ALLOWED
      implementationContract:
        layout:
        informationPriority:
        forbiddenPatterns: []
        responsive:
        browserVerification:
        currentViewportFirst: true
      missingDecisions: []
    storageIntent:
      required: false
      result: DB_DESIGN_ALLOWED
      missingDecisions: []
    behaviorContract:
      required: false
      result: API_DESIGN_ALLOWED
      missingDecisions: []
    stateMeaning:
      required: false
      result: STATE_MODEL_ALLOWED
      missingDecisions: []
    operationalQuality:
      required: false
      result: "설계 가능"
      missingDecisions: []
  implementationConstraints: []
  forbiddenApproaches: []
  uiImplementationContract:
    required: false
    targetScreens: []
    layout:
    informationPriority:
    forbiddenPatterns: []
    responsive:
    browserVerification:
    currentViewportFirst: true
    screenLevelAcceptanceCriteria: []
  acceptanceCriteria: []
  testRequirements: []
  executionRules:
    requirePromptExecutionApproval: true
    stopOnMissingContext: true
    stopOnPolicyConflict: true
    doNotModifySourceOfTruth: true
  suggestions: []
```

목적:

- 구현 Agent가 실행 전에 requiredDocuments, approvalRefs, dependsOn, documentCoverage를 한 번에 확인하게 한다.
- prompt 초안 승인과 실행 승인을 분리하되, 사용자가 실제 실행까지 명확히 요청했고 새 결정이나 위험 변경이 없으면 초안 작성 후 실행 연계 조건으로 이어갈 수 있게 한다.
- `readinessCheck.conclusion`이 `IMPLEMENTATION_BLOCKED`이면 구현 prompt를 실행하지 않는다.

## Task Contract Template

Task Contract는 구현 가능성보다 먼저 readiness를 고정해야 한다.

```yaml
taskContract:
  taskId: TASK-000
  title: "Task title"
  type: implementation
  status: DRAFT
  goal: "Observable task goal."
  readinessCheck:
    productReadiness:
      status: READY
      evidence:
        - "Approved Product SOT covers the user problem and vertical slice boundary."
      missingDecisions: []
      interactionDesign: "상호작용 설계 가능"
      frontendUx: FRONTEND_UX_ALLOWED
    engineeringReadiness:
      status: READY
      evidence:
        - "Approved Engineering SOT covers how product decisions map to storage structure, state, API, code structure, and test strategy."
      missingDecisions: []
      designIntentChecks:
        operationalQuality: "설계 가능"
        storageIntent: DB_DESIGN_ALLOWED
        behaviorContract: API_DESIGN_ALLOWED
        stateMeaning: STATE_MODEL_ALLOWED
    implementationReadiness:
      status: NOT_READY
      evidence: []
      missingDecisions:
        - "Prompt execution approval is not recorded yet."
    conclusion: IMPLEMENTATION_BLOCKED
  requiredDocuments:
    product:
      - id: PRODUCT-SOT-001
        path: docs/product/product-requirements.md
        reason: "Defines what and why."
    engineering:
      - id: ENGINEERING-SOT-001
        path: docs/engineering/architecture.md
        reason: "Defines how the product decision maps to code."
    crossCutting: []
  designIntentChecks:
    interactionDesign:
      required: false
      result: "상호작용 설계 가능"
      missingDecisions: []
    storageIntent:
      required: false
      result: DB_DESIGN_ALLOWED
      missingDecisions: []
    behaviorContract:
      required: false
      result: API_DESIGN_ALLOWED
      missingDecisions: []
    stateMeaning:
      required: false
      result: STATE_MODEL_ALLOWED
      missingDecisions: []
    operationalQuality:
      required: false
      result: "설계 가능"
      missingDecisions: []
  allowedScope: []
  forbiddenScope: []
  implementationConstraints: []
  forbiddenApproaches: []
  acceptanceCriteria: []
  testRequirements: []
  verificationCommands: []
  userApprovalRequiredFor:
    - prompt-execution
```

Rules:

- `IMPLEMENTATION_ALLOWED` is valid only when Product Readiness, Engineering Readiness, and Implementation Readiness are all `READY`.
- If any readiness status is `NOT_READY`, conclusion must be `IMPLEMENTATION_BLOCKED`.
- If any required design intent check is `*_BLOCKED`, Engineering Readiness must be `NOT_READY` and conclusion must be `IMPLEMENTATION_BLOCKED`.
- If required interaction design is not `"상호작용 설계 가능"`, Product Readiness must be `NOT_READY` and conclusion must be `IMPLEMENTATION_BLOCKED`.
- If required operational quality is not `"설계 가능"`, Engineering Readiness must be `NOT_READY` and conclusion must be `IMPLEMENTATION_BLOCKED`.
- Do not write an implementation prompt while the Task Contract is `IMPLEMENTATION_BLOCKED`.
- Missing decisions must be split into Product Missing Context, Engineering Missing Context, or Implementation Missing Context.

## SOT Packet Template

SOT Packet은 이번 작업에서 승인된 기준 묶음이다.

```yaml
sotPacket:
  taskName:
  workMode:
  objective:
  approvedSotDocuments:
    product:
      - id:
        path:
        reason:
    engineering:
      - id:
        path:
        reason:
    crossCutting:
      - id:
        path:
        reason:
  requiredDecisions:
    product: []
    engineering: []
    implementation: []
  allowedScope: []
  forbiddenScope: []
  uiImplementationContract:
    required: false
    targetScreens: []
    layout:
    informationPriority:
    forbiddenPatterns: []
    responsive:
    browserVerification:
    currentViewportFirst: true
    screenLevelAcceptanceCriteria: []
  verificationCommands: []
  userApprovalRequiredFor: []
```

Rules:

- Product SOT and Engineering SOT must be distinguishable even if they live in the same file.
- Archive, superseded, generated, index, memory, recall, and previous report materials are not SOT unless explicitly approved in the SOT Packet.
- If Product or Engineering evidence is missing from the SOT Packet, Implementation Readiness is `NOT_READY`.

## 6. Verification Result Metadata Template

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
