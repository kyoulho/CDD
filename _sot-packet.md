# SOT Packet

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이번 작업 기준 묶음은 Codex가 따라야 할 승인된 기준 묶음이다. 내부명은 `SOT Packet`이다.

저장소 전체 문서가 자동으로 기준 문서가 되는 것은 아니다. Codex는 이번 작업 기준 묶음에 포함된 approved SOT만 작업 기준으로 삼는다.

`archive/`, `superseded`, `generated`, `index`, `memory`, `recall`, previous report 자료는 이번 작업 기준 묶음에 명시적으로 포함되지 않으면 보조 자료다. 검색에 걸렸다는 이유만으로 active source of truth로 사용하지 않는다.

작업 기준 묶음이 없거나 작업 판단에 필요한 필드가 부족하면 구현, revision, cleanup/delete 실행으로 넘어가지 말고 `_missing-context.md`로 돌아간다.

## 빠른 탐색

- 기준 묶음에 들어갈 필드는 "필드"를 본다.
- 작업 시작 전에 사용자에게 선언할 내용은 "작업 시작 선언"을 본다.
- 기준 묶음을 active 기준으로 사용할 때의 제한은 "사용 규칙"을 본다.

## 필드

작업 기준 묶음은 최소한 다음 필드를 문서화한다.

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
  currentCriteria:
    hotPathDocuments: []
    activeIndexes: []
    domainPackets: []
  currentWorkPointer:
    path:
    currentGate:
    nextTask:
    activeTasks: []
    requiredReadDocuments: []
    excludedHistoricalRecords: []
    currentConflicts: []
    readmeOrIndexUpdatesRequired: []
  readPathContract:
    requiredReadDocuments: []
    excludedHistoricalRecords: []
    excludedNonSotReferences: []
    oversizedRequiredReadDocuments: []
    activeHistoryMixedDocuments: []
    decisionLogSplitCandidates: []
  historicalRecords:
    taskCompletions: []
    verificationResults: []
    oldTasks: []
    oldPrompts: []
  nonSotReferences:
    generatedMaps: []
    codesight: []
    agentmemory: []
    searchIndexes: []
    archiveBranchReferences: []
  readCost:
    splitCandidates: []
    keepCandidates: []
    readmeOrIndexUpdatesRequired: []
  currentVsHistoryConflicts: []
  requiredDecisions:
    product: []
    engineering: []
    implementation: []
  allowedScope: []
  forbiddenScope: []
  approvedArtifacts: []
  verificationCommands: []
  completionReportFormat:
  userApprovalRequiredFor: []
```

필드 의미:

- `taskName`: 이번 작업을 식별하는 짧은 이름.
- `workMode`: `_work-mode.md`로 판별한 작업 방식.
- `objective`: 이번 작업의 관찰 가능한 목표.
- `approvedSotDocuments.product`: 이번 작업의 제품 기준 문서. 무엇을 왜 만들 것인지에 대한 기준이다.
- `approvedSotDocuments.engineering`: 이번 작업의 기술 설계 기준 문서. 제품 판단을 코드 구조로 어떻게 표현할지에 대한 기준이다.
- `approvedSotDocuments.crossCutting`: 제품/기술 기준을 가로지르는 보안, 테스트, 의존성, 운영 같은 기준이다.
- `currentCriteria`: 이번 작업에서 현재 기준으로 읽을 hot path 문서, active index, 필요한 domain packet 목록이다.
- `currentWorkPointer`: 현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서, 읽지 않을 과거 기록, 충돌, README/index 갱신 필요 여부를 짧게 가리키는 문서 또는 섹션이다.
- `readPathContract`: 이번 작업에서 반드시 읽을 문서와 기본 읽기 경로에서 제외할 과거 기록/보조 자료를 고정하는 계약이다.
- `historicalRecords`: completion, verification, old task, old prompt처럼 그 시점의 사실 기록으로만 읽을 자료다.
- `nonSotReferences`: generated map, Codesight, agentmemory, search index, archive branch reference처럼 탐색 보조로만 쓰는 자료다.
- `readCost`: 기본 읽기 경로에서 크기 때문에 분리 후보 또는 유지 후보가 된 문서와 README/index 갱신 필요 여부다.
- `currentVsHistoryConflicts`: 현재 기준과 과거 기록 또는 보조 자료가 충돌하는 항목이다. 비어 있지 않으면 구현, 후속 지시서 작성, completion으로 넘어가지 않는다.
- `requiredDecisions.product`: 작업 전 확정되어야 하는 제품 결정 목록. 비어 있지 않은 미확정 결정은 제품 관련 질문으로 분리한다.
- `requiredDecisions.engineering`: 작업 전 확정되어야 하는 코드 설계 결정 목록. 비어 있지 않은 미확정 결정은 기술 설계 관련 질문으로 분리한다.
- `requiredDecisions.implementation`: 작업 전 확정되어야 하는 실행 승인, scope, command 결정 목록. 비어 있지 않은 미확정 결정은 구현 시작 관련 질문으로 분리한다.
- `allowedScope`: 수정, 생성, 삭제, 조사할 수 있는 파일과 행동 범위.
- `forbiddenScope`: 이번 작업에서 금지된 파일, 저장소, 행동, 판단 범위.
- `approvedArtifacts`: 기준으로 사용할 수 있는 Plan, 작업 기준서, prompt, verification result, completion record 등 승인된 artifact.
- `verificationCommands`: 이번 작업 후 실행하거나, 실행 불가 시 이유를 보고할 검증 명령.
- `completionReportFormat`: 완료 보고 형식. 기본은 `complete-work.md`의 짧은 완료 보고 형식이다.
- `userApprovalRequiredFor`: 진행 전 사용자 승인이 필요한 행동 목록.

## 작업 시작 선언

Codex는 작업 시작 전 이번 작업 기준 묶음을 기준으로 다음 형식을 선언한다.

```text
작업 방식:
이번 작업 기준:
가능한 작업:
금지된 작업:
진행 전 필요한 승인:
검증 방법:
```

시작 선언 규칙:

- `ANALYSIS_ONLY`이면 파일을 생성, 수정, 삭제하지 않는다.
- `CLEANUP_DELETE`이면 새 기능을 만들지 않는다.
- `IMPLEMENTATION`이면 작업 기준 묶음 없이 시작하지 않는다.
- `DOCUMENT_ONLY`이면 코드, 테스트, 설정 파일을 수정하지 않는다.
- 시작 선언의 `Allowed`와 `Forbidden`이 충돌하면 구현하지 말고 아직 필요한 결정으로 돌아간다.
- `User approval required before`에 남은 항목이 있는데 해당 행동을 수행해야 하면 멈추고 사용자 승인을 받는다.

## 사용 규칙

- 작업 기준 묶음은 전체 문서 탐색을 대체하는 작업 기준 요약이지, 승인되지 않은 문서를 승격하는 장치가 아니다.
- approved SOT 문서와 작업 기준 묶음이 충돌하면 구현하지 말고 SOT conflict로 보고한다.
- 제품 기준 문서와 기술 설계 기준 문서를 구분한다. 둘 중 하나의 근거가 없으면 구현 시작 가능 여부는 `NOT_READY`다.
- 현재 기준, 과거 기록, 보조 자료를 구분한다. 과거 completion/verification/task/prompt는 active 기준으로 승격된 근거가 없으면 현재 기준이 아니다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference는 `nonSotReferences`에 두고 기본 읽기 경로에서 제외한다.
- 다음 작업 판단에 과거 완료 기록까지 훑어야 한다면 `currentWorkPointer`와 `readPathContract`를 먼저 보강해야 한다.
- `currentWorkPointer`는 파일명을 강제하지 않는다. 다만 `path`, `currentGate`, `nextTask`, `activeTasks`, `requiredReadDocuments`, `excludedHistoricalRecords`, `currentConflicts`, `readmeOrIndexUpdatesRequired`를 채울 수 있어야 한다.
- `readPathContract.requiredReadDocuments`에는 이번 작업에 필요한 최소 문서만 둔다. 완료된 task history, 과거 verification, completion, old prompt, generated map, Codesight, agentmemory는 제외 목록으로 분리한다.
- 기본 읽기 경로의 문서가 400줄 또는 40KB를 넘으면 분리 후보를 기록한다. 1000줄 이상 누적 문서는 active index와 history 분리 후보를 기록한다.
- currentVsHistoryConflicts가 비어 있지 않으면 후속 구현, prompt, completion으로 넘어가지 않고 정합성 정리를 먼저 보고한다.
- 작업 기준 묶음 밖 작업은 현재 Task의 suggestions 또는 다음 후보로 분리한다.
- 보조 자료를 참고했다면 verification 또는 completion에서 active SOT로 사용하지 않았음을 밝힌다.
- 작업 기준 묶음을 보강해야 하면 source of truth 변경과 Task/Prompt 승인 게이트를 우회하지 않는다.
