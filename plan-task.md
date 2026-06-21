# Plan Task Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: 제품/기술 기준 준비가 끝난 뒤 Plan과 작업 기준서를 작성할 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

## 핵심 용어

- 제품 기준 준비 상태: 무엇을 왜 만들 것인지에 대한 기획 준비도.
- 기술 설계 준비 상태: 제품 판단을 저장 구조, 상태, API, 코드 구조로 표현할 기준이 정해졌는지에 대한 설계 준비도.
- 구현 시작 가능 여부: 에이전트가 구현을 시작해도 되는지에 대한 실행 준비도.
- 이번 작업 기준 묶음: 이번 작업에서 따라야 할 승인된 기준 문서 묶음.
- 작업 기준서: 구현 전 작업 범위, 금지 범위, 검증 기준을 고정하는 작업 계약.
- 상호작용 방식 확인: 사용자 또는 운영자가 접하는 기능의 입력, 출력, 흐름, 실패와 피드백을 먼저 확인하는 절차.
- 프론트엔드 UX 확인: 웹/모바일 UI 작업에서 화면 상태, 정보 구조, 접근성, 반응형 동작, 시각 검증 기준을 먼저 확인하는 절차.
- 운영/품질 기준 확인: 성능, 보안, 권한, 조회, 재시도, 로그/감사, 운영 기준을 구현 전에 확인하는 절차.

이 skill은 문서 준비도가 `READY_FOR_PLANNING`이고 제품 기준 준비 상태와 기술 설계 준비 상태가 모두 `READY`일 때 Plan과 작업 기준서를 생성한다.

사용자 요청이 설명, 설계안, 문서 초안, 문서 수정, 구현 계획, 실제 코드 수정, 삭제/정리, 검증 중 무엇을 원하는지 애매하면 Plan/Task를 만들지 않는다. 애매하면 먼저 질문한다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 Plan 또는 작업 기준서 파일을 생성하거나 수정하지 않는다. 필요한 Plan/Task 변경 후보와 차단 사유만 보고한다.

문서 준비 전에는 Plan/Task를 만들지 않는다.

Project Context 준비 전에는 Plan/Task를 만들지 않는다. Plan/Task 생성 시 `_project-context.md`의 Project Context를 반드시 참고한다.

Planning Agent는 Plan/Task DRAFT를 만들 수 있지만, source of truth 변경 권한은 없다. Plan/Task를 APPROVED로 전환하기 전에는 사용자 review 또는 `_source-of-truth-manager.md`를 통한 source of truth 일관성 검토가 필요하다.

Plan과 작업 기준서 artifact는 가능한 한 `_artifact-metadata.md`의 metadata를 포함하고, status는 `_status-machine.md`를 따른다.

Plan과 작업 기준서를 만들거나 수정하기 전에는 대상 프로젝트의 기존 문서 배치 구조를 먼저 확인한다. `docs/README.md`, 문서 index, document registry, 기존 작업 산출물 목록, 기존 파일명과 누적 방식을 확인하고 `_artifact-templates.md`의 Document Placement Check를 작성한다.

기존 구조가 단일 작업 기준서에 task를 누적하는 방식이면 후속 phase/task도 같은 문서에 추가한다. 기존 구조가 task별 파일 분리 방식이면 후속 task도 같은 방식으로 분리한다. 기존 구조와 다른 파일 배치를 하려면 auto-stop하고 전체 문서 구조 변경안과 사용자 승인을 요구한다.

새 작업 기준서 파일을 만들기 전에는 왜 기존 문서에 추가하지 않고 새 파일이 필요한지 보고한다.

작업 기준서는 구현 전에 `_sot-packet.md`의 작업 기준 묶음으로 요약될 수 있어야 한다. 요약할 수 없거나 approved 기준 문서, allowedScope, forbiddenScope, requiredDecisions가 불명확하면 Plan/Task를 APPROVED로 만들지 말고 아직 필요한 결정을 질문한다.

작업 기준서 작성 전 `_readiness-gates.md`의 제품 기준 준비 상태와 기술 설계 준비 상태를 확인한다. 둘 중 하나라도 `NOT READY`이면 작업 기준서를 APPROVED로 만들지 말고 제품 또는 기술 설계 쪽 미확정 결정으로 돌아간다.

DB table, column, migration, repository, API DTO를 계획하려면 Storage Intent Check가 `DB_DESIGN_ALLOWED`여야 한다. API path나 request/response shape를 계획하려면 Behavior Contract Check가 `API_DESIGN_ALLOWED`여야 한다. status enum이나 state transition을 계획하려면 State Meaning Check가 `STATE_MODEL_ALLOWED`여야 한다.

사용자 또는 운영자가 접하는 기능을 계획하려면 상호작용 방식 확인 결론이 `상호작용 설계 가능`이어야 한다. 웹/모바일 UI 작업을 계획하려면 프론트엔드 UX 확인 결론이 `FRONTEND_UX_ALLOWED`여야 한다. 성능, 보안, 조회, 권한, 실패 처리, 재시도, 로그/감사 판단이 필요한 작업을 계획하려면 운영/품질 기준 확인 결론이 `설계 가능`이어야 한다.

사용자-facing 계획 보고에서는 내부 판정 용어를 그대로 제목으로 쓰지 않는다. `Product Readiness`는 "제품 방향", `Engineering Readiness`는 "설계 준비 상태", `Implementation Readiness`는 "지금 바로 만들 수 있는지", `Storage Intent Check`는 "무엇을 왜 저장할지", `Behavior Contract Check`는 "사용자가 어떤 행동을 하고 어떤 결과를 받는지", `State Meaning Check`는 "상태값이 무엇을 의미하는지"로 바꿔 말한다. 내부 enum은 작업 기준서 YAML과 에이전트 간 전달물에만 그대로 둔다.

## 시작 조건

다음이 모두 충족되어야 한다.

- `_document-readiness.md` 결과가 `READY_FOR_PLANNING`이다.
- 제품 기준 준비 상태가 `READY`다.
- 기술 설계 준비 상태가 `READY`다.
- Project Context가 존재하고 준비 상태 결과에 반영되어 있다.
- 필요한 source of truth 문서가 APPROVED 상태다.
- Goal을 Task로 분해할 때 AI가 문서 밖 정책 판단을 하지 않아도 된다.

## 역할

- Goal을 prompt 단위로 수행 가능한 Task로 나눈다.
- 각 Task에 requiredDocuments와 documentCoverage를 포함한다.
- 각 Task에 forbiddenApproaches와 testRequirements를 포함한다.
- Task 간 의존성을 명확히 한다.
- documentCoverage가 BLOCKED인 Task는 APPROVED로 만들지 않는다.
- Plan/Task가 source of truth 변경을 요구하면 직접 수정하지 말고 Source of Truth Change Request로 넘긴다.
- source of truth 변경 전후로 기존 Plan/Task가 무효화될 수 있음을 기록한다.
- source of truth 변경 후 기존 작업 기준서가 더 이상 정합하지 않으면 재생성 또는 수정이 필요하다고 보고한다.
- 변경된 source of truth와 불일치하는 작업 기준서를 warning으로 남긴 채 APPROVED로 만들지 않는다.
- 각 Task의 `dependsOn`을 명시하고, 후속 Task prompt 생성 확인 지점으로 사용되도록 기록한다.
- 각 Task가 Project Context의 projectType, productionIntent, risk, allowedSimplifications, forbiddenSimplifications와 충돌하지 않는지 확인한다.
- 각 Task에 제품 기준 준비 상태와 기술 설계 준비 상태 판정 근거를 반영한다.
- Plan/Task 저장 전 사용자 보고에 수정할 파일, 새로 만들 파일, 기존 문서 구조와 맞는지, README/index 갱신 필요 여부를 포함한다.
- README/index 갱신이 필요하면 같은 요청 범위 안에서 갱신 가능 여부를 확인한다. 구조 변경이 필요하면 저장하지 말고 사용자 승인을 받는다.

## 작업 기준서 필수 항목

```text
taskId
title
type
status
goal
workMode
requiredDocuments
documentCoverage
implementationConstraints
forbiddenApproaches
uiImplementationContract
acceptanceCriteria
testRequirements
humanGates
autoStopConditions
artifact metadata
projectContextRef
projectContextSummary
readinessCheck
allowedScope
forbiddenScope
verificationCommands
completionReportFormat
userApprovalRequiredFor
documentPlacementCheck
```

Task `type`에는 필요한 경우 `cleanup-delete`를 사용한다. cleanup/delete Task는 일반 refactor Task와 구분한다.

## 작업 기준서 readinessCheck 예시

작업 기준서에는 다음 readinessCheck를 포함한다. YAML artifact에서는 `READY` / `NOT_READY`를 사용한다. 사용자-facing 보고에서는 이를 "바로 진행 가능" / "아직 결정 필요"로 바꿔 말하고, 내부 상태값을 기본 보고의 결론으로 쓰지 않는다.

```yaml
readinessCheck:
  productReadiness:
    status: READY
    evidence:
      - "승인된 제품 기준 문서가 사용자 문제, 대상 사용자, 사용 시나리오, 상호작용 방식, 입력, 출력, 실패와 피드백, 빈 상태, 권한 없음, 처리 중 피드백, 기능 범위, 하지 않을 것, 성공 기준, 이번 vertical slice 경계를 정의한다."
    missingDecisions: []
    interactionDesign: "상호작용 설계 가능"
    frontendUx: FRONTEND_UX_ALLOWED
  engineeringReadiness:
    status: READY
    evidence:
      - "승인된 기술 설계 기준 문서가 제품 판단을 아키텍처, 저장 구조, 상태, API, 성능, 보안, 운영/품질 기준, 코드 구조로 표현할 기준을 정의한다."
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
      - "Prompt execution approval is not recorded."
  conclusion: IMPLEMENTATION_BLOCKED
```

`conclusion: IMPLEMENTATION_ALLOWED`는 세 준비 상태가 모두 `READY`일 때만 가능하다. 하나라도 `NOT_READY`이면 `IMPLEMENTATION_BLOCKED`이며, 부족한 결정은 아직 필요한 결정으로 분리한다.

## 구조 제안 전 차단 규칙

Plan/Task는 미확정 결정을 채우기 위해 인터페이스, 화면, CLI 명령, 배치 실행 방식, table, column, API path, status enum을 먼저 제안하지 않는다. 구조 후보는 제품 판단과 설계 기준이 문서화된 뒤에만 쓴다.

- 상호작용 방식 확인이 없거나 `상호작용 설계 보류`이면 화면, CLI 명령, API surface, 배치 실행 방식, 저장 구조를 `acceptanceCriteria`, `implementationConstraints`, `allowedScope`, `testRequirements`에 넣지 않는다.
- 프론트엔드 UX 확인이 없거나 `FRONTEND_UX_BLOCKED`이면 route, page, component, layout, styling, motion, visual QA 기준을 `acceptanceCriteria`, `implementationConstraints`, `allowedScope`, `testRequirements`에 넣지 않는다.
- 웹/모바일 UI 작업인데 분석 결과를 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저/스크린샷 검증 기준으로 고정한 `uiImplementationContract`가 없으면 route, page, component, layout, styling, motion, visual QA 기준을 `acceptanceCriteria`, `implementationConstraints`, `allowedScope`, `testRequirements`에 넣지 않는다.
- Storage Intent Check가 없거나 `DB_DESIGN_BLOCKED`이면 table, column, migration, repository, API DTO를 `acceptanceCriteria`, `implementationConstraints`, `allowedScope`, `testRequirements`에 넣지 않는다.
- Behavior Contract Check가 없거나 `API_DESIGN_BLOCKED`이면 API path, method, route, controller, request/response shape를 넣지 않는다.
- State Meaning Check가 없거나 `STATE_MODEL_BLOCKED`이면 status enum, status column, state transition 이름을 넣지 않는다.
- 운영/품질 기준 확인이 없거나 `설계 보류`이면 performance, security, operation, sorting, search, pagination, permission, retry, logging, audit 정책을 넣지 않는다. 구현 중 발견 가능한 성능 위험 후보를 다루는 acceptance criteria도 넣지 않는다.
- 위 check가 BLOCKED이면 `documentCoverage.status: BLOCKED`로 두고 Product Missing Context 또는 Engineering Missing Context 질문을 만든다.
- `documentCoverage.status: PARTIAL`이어도 해당 구조 설계와 구현 prompt 생성은 금지다.
- 기존 DB, controller, enum, framework가 있다는 사실은 기술 설계 준비 상태 `READY`의 근거가 아니다.

## Task 작성 규칙

- 각 Task는 prompt 단위로 수행 가능한 크기여야 한다.
- 애매한 요청을 구현 계획 요청으로 승격하지 마라.
- 애매한 요청을 작업 기준서 작성 승인으로 해석하지 마라.
- cleanup/delete Task는 `cleanup-delete.md`를 requiredDocuments 또는 implementationConstraints에 연결하고 keep list, delete list, humanGates, verification requirements를 포함한다.
- 문서에 없는 정책을 근거로 acceptance criteria를 만들지 마라.
- 구현 Task에 도메인/아키텍처 판단 변경을 섞지 마라.
- 새 판단이 필요하면 Task 생성이 아니라 아직 필요한 결정 질문으로 돌아가라.
- requiredDocuments에는 문서 id, path, reason을 포함한다.
- documentCoverage는 READY, PARTIAL, BLOCKED 중 하나로 기록한다.
- READY가 아닌 Task는 구현 prompt로 넘어갈 수 없다.
- DATA_MODEL, API_CONTRACT, BEHAVIOR 문서가 필요한 작업인데 requiredDocuments에 빠져 있으면 documentCoverage를 BLOCKED로 기록한다.
- 사용자 또는 운영자가 접하는 기능인데 상호작용 방식 확인이 `상호작용 설계 가능`이 아니면 Task를 APPROVED로 만들지 않는다.
- 웹/모바일 UI 작업인데 프론트엔드 UX 확인이 `FRONTEND_UX_ALLOWED`가 아니면 Task를 APPROVED로 만들지 않는다.
- 웹/모바일 UI 작업인데 승인 문서 안의 FRONTEND_UX_CRITERIA, USER_FLOW 또는 INTERACTION_SPEC, DESIGN_SYSTEM 또는 UI_PATTERN, FRONTEND_ARCHITECTURE 역할 coverage가 requiredDocuments에서 확인되지 않으면 documentCoverage를 BLOCKED로 기록한다.
- route/page/component/layout/styling/motion/visual QA 기준이 필요한 Task에는 승인 문서 안의 FRONTEND_UX_CRITERIA와 FRONTEND_ARCHITECTURE 역할 coverage가 필요하다.
- 웹/모바일 UI Task에는 화면 단위 `uiImplementationContract`를 포함한다. 이 계약은 레이아웃, 정보 우선순위, 금지 패턴, 반응형 기준, 브라우저/스크린샷 검증 기준을 포함해야 한다.
- 컴포넌트별 수정 목록만 있고 전체 화면의 빈 공간, 강조 수준, 숨김 금지, primary/secondary 정보 관계, 현재 사용자 viewport 검증 기준이 없으면 Task를 APPROVED로 만들지 않는다.
- 디자인 시스템, 화면 패턴, 색상/타이포그래피/간격, component variant, motion 기준이 필요한 Task에는 승인 문서 안의 DESIGN_SYSTEM 또는 UI_PATTERN 역할 coverage가 필요하다.
- CDD는 `docs/design-system/*`, `docs/ui-ux/*` 같은 파일 위치를 강제하지 않는다. 프로젝트가 루트 `DESIGN.md` 같은 단일 기준 문서를 승인했고 그 안에 역할 경계가 명확하면 해당 문서를 requiredDocuments로 사용할 수 있다.
- Storage Intent Check가 `DB_DESIGN_ALLOWED`가 아니면 DB table, column, migration, repository, API DTO 관련 Task를 APPROVED로 만들지 않는다.
- Behavior Contract Check가 `API_DESIGN_ALLOWED`가 아니면 API path, method, route, controller, request/response shape 관련 Task를 APPROVED로 만들지 않는다.
- State Meaning Check가 `STATE_MODEL_ALLOWED`가 아니면 status enum, status column, state transition 관련 Task를 APPROVED로 만들지 않는다.
- 운영/품질 기준 확인이 `설계 가능`이 아니면 성능, 보안, 권한, 조회, 실패 처리, 재시도, 로그/감사 관련 Task를 APPROVED로 만들지 않는다.
- 성능 위험 후보 탐지 또는 개선을 Task에 포함하려면 조사 범위, 판단 근거, 허용된 수정 범위, 금지 범위를 작업 기준서에 명시한다.
- id type, key generation, API-visible identifier 정책이 필요한데 누락되어 있으면 documentCoverage를 BLOCKED로 기록한다.
- DB/Repository/Flyway/Migration 관련 Task에는 TEST_STRATEGY 또는 DATA_MODEL/IMPLEMENTATION_ARCHITECTURE/MIGRATION_POLICY 문서가 필요하다.
- testRequirements에 DB integration test가 포함되어 있는데 테스트 DB 전략이 문서화되어 있지 않으면 Task를 APPROVED로 만들지 않는다.
- 테스트 전략이 문서에 없으면 documentCoverage.status를 BLOCKED로 둔다.
- Task에 testRequirements를 넣기 전에 해당 테스트 전략 문서가 있는지 확인한다.
- 각 Task는 작업 기준 묶음으로 압축 가능한 allowedScope, forbiddenScope, approvedArtifacts, verificationCommands, completionReportFormat을 포함하거나 참조한다.
- 제품 기준 문서만 있거나 기술 설계 기준 문서만 있으면 구현 Task를 만들지 않는다.
- Repository/Flyway testRequirements가 있는데 TEST_STRATEGY가 없으면 documentCoverage.status를 BLOCKED로 둔다.
- H2/Testcontainers/application-test.yml/test migration 정책이 없으면 Task를 APPROVED로 만들지 않는다.
- External integration Task에는 INTEGRATION_POLICY가 없으면 BLOCKED로 둔다.
- Batch Task에는 BATCH_OPERATION_POLICY가 없으면 BLOCKED로 둔다.
- Infra/config/profile Task에는 OPERATION 또는 INFRA_POLICY가 없으면 BLOCKED로 둔다.
- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library가 필요한 Task에는 DEPENDENCY_POLICY 또는 명시적 APPROVED 결정이 필요하다.
- dependency 승인 문서가 없으면 기본 대안은 기존 스택 안에서 구현하는 것이다.
- dependency 승인 없이 MapStruct, springdoc-openapi, QueryDSL, Testcontainers 같은 항목을 acceptanceCriteria나 implementationConstraints에 넣지 않는다.
- AI 판단 허용 영역과 금지 영역을 implementationConstraints와 forbiddenApproaches에 명확히 반영한다.
- 미확정 결정이 해결되기 전에는 작업 기준서를 수정하거나 APPROVED로 만들지 않는다.
- 작업 성격이 확정되기 전에는 작업 기준서를 수정하거나 APPROVED로 만들지 않는다.
- Source of Truth Manager 승인 없이 source of truth 변경을 반영해 작업 기준서를 수정하거나 APPROVED로 만들지 않는다.
- partial source of truth update 또는 known conflict가 남은 Change Request를 근거로 작업 기준서를 만들지 않는다.
- 현재 Task 또는 선행 Task의 미확정 결정을 "나중에"로 미루는 Plan을 만들지 않는다.
- 선행 Task가 COMPLETE가 아닌데 후속 Task prompt 생성을 허용하는 Plan을 만들지 않는다.
- testRequirements를 만족하지 못한다는 이유로 테스트 범위를 줄인 Task를 만들지 않는다.
- DB integration test를 unit/static test로 대체하거나 후속 Task로 이연하려면 사용자 승인과 작업 기준서 변경이 필요하다.
- cleanup/delete Task에서 삭제 대상이 keep list와 충돌하거나 archive 보존, DB drop/migration, public API 제거, dependency 대량 제거 판단이 필요하면 humanGates에 기록하고 APPROVED 전 사용자 확인을 요구한다.

## Project Context 기반 Plan/Task 규칙

Plan/Task는 Project Context의 성격과 운영 전제를 반영해야 한다.

- `PRACTICE_PROJECT`: 구현 범위를 사용자의 도메인 설계·구현 연습 목표에 맞춘다. 상용 운영 인프라 Task를 기본 생성하지 않는다.
- `TEST_BED`: 사용자가 명시한 시스템/도구/기술 가정 검증 목표에 맞춘다. 하네스 평가 목적은 Plan/Task source of truth가 아니라 별도 harness operation artifact로 분리한다.
- `LOCAL_EXPERIMENT`: 복잡한 배포, 고가용성, 대규모 관측성 Task를 기본 생성하지 않는다.
- `PERSONAL_TOOL`: 개인 사용 범위에 맞춰 과도한 보안/운영 Task를 기본 생성하지 않는다.
- `PRODUCTION_SERVICE`: 운영, 보안, 배포, 장애 대응, 관측성 Task를 별도 고려한다.
- `HIGH_CONSISTENCY_DOMAIN`: 상태 전이, 기록 보존, idempotency, auditability, duplicate event handling Task를 분리한다.
- `HIGH_TRAFFIC_SERVICE`: 성능, 확장성, 비동기 처리, 캐시, 큐, backpressure 관련 Task를 분리하거나 아직 필요한 결정으로 질문한다.
- `INTERNAL_BACKOFFICE`: 권한, 변경 이력, 검색/필터, 엑셀 export/import, 운영자 UX를 별도 고려한다.

성능 관련 Task는 "성능 이슈 가능성이 있는 부분을 에이전트가 찾아 고친다"처럼 열린 범위로 쓰지 않는다. 승인된 기준이 없으면 성능 위험 후보는 implementationConstraints가 아니라 suggestions 또는 후속 Missing Context로 남긴다.

`allowedSimplifications`는 Task 범위를 줄이는 자동 승인으로 해석하지 않는다. `forbiddenSimplifications`와 충돌하는 Task는 APPROVED로 만들지 않는다.

## Identifier Policy Coverage 예시

식별자 정책이 빠진 상태에서 Entity, DB migration, API endpoint, DTO, 테스트 fixture를 계획해야 한다면 Task를 APPROVED로 만들지 않는다.

```yaml
documentCoverage:
  status: BLOCKED
  missing:
    - area: identifier-policy
      reason: Entity id type and API-visible id representation are not defined.
      question: Should the entity id be Long, UUID, ULID, or another identifier type?
      recommendedDefault: Long for simple local CRUD API.
```

이 예시의 recommendedDefault는 제안일 뿐 승인된 정책이 아니다. 사용자가 승인하거나 source of truth 문서에 반영되기 전까지 acceptanceCriteria나 implementationConstraints에 넣지 않는다.

## Test DB Strategy Coverage 예시

Repository, Flyway, DB migration 테스트가 필요한데 테스트 DB/profile/migration 전략이 문서화되어 있지 않으면 Task를 APPROVED로 만들지 않는다.

```yaml
documentCoverage:
  status: BLOCKED
  missing:
    - area: test-db-strategy
      reason: Repository/Flyway tests require a documented test database strategy.
      question: Should tests use PostgreSQL/Testcontainers, a separate test PostgreSQL, H2, or defer DB integration tests?
      recommendedDefault: Defer DB integration tests or use PostgreSQL/Testcontainers only if explicitly approved.
```

이 recommendedDefault도 승인된 정책이 아니다. 사용자가 승인하거나 TEST_STRATEGY/source of truth 문서에 반영되기 전까지 Task를 APPROVED로 만들지 않는다.

## Cross-Cutting Policy Coverage 규칙

Task가 다음 영역을 포함하면 requiredDocuments에 해당 문서를 포함해야 한다.

- Frontend UI/UX: 승인 문서 안의 FRONTEND_UX_CRITERIA, FRONTEND_ARCHITECTURE, DESIGN_SYSTEM 또는 UI_PATTERN, USER_FLOW 또는 INTERACTION_SPEC 역할 coverage
- DB / Persistence: DATA_MODEL, MIGRATION_POLICY, TEST_STRATEGY
- API / Error: API_CONTRACT, ERROR_POLICY, BEHAVIOR
- External Integration: INTEGRATION_POLICY, EXTERNAL_REFERENCE
- Batch: BATCH_OPERATION_POLICY, JOB_SPEC
- Operation / Infra / Config: OPERATION 또는 INFRA_POLICY
- Dependency / Build Tool / Code Generation: DEPENDENCY_POLICY 또는 IMPLEMENTATION_ARCHITECTURE

필요 문서가 없으면 Task status를 APPROVED로 만들지 말고 `documentCoverage.status: BLOCKED`로 둔다.

## Dependency Coverage 예시

```yaml
documentCoverage:
  status: BLOCKED
  missing:
    - area: dependency-policy
      reason: A new dependency, plugin, annotation processor, code generation tool, or runtime-exposed library is required but not approved.
      question: Should this task approve the dependency, implement within the existing stack, or defer the dependency-requiring feature?
      recommendedDefault: Implement within the existing stack.
```

## 상태 규칙

- `APPROVED`: 문서 coverage가 READY이고 사용자가 Task를 승인했다.
- `DRAFT`: 아직 사용자 승인 전이거나 문서 coverage가 부족하다.
- `BLOCKED`는 Task status로 쓰지 말고 `documentCoverage.status`에 기록한다.

## Plan 작성 규칙

- Plan은 Goal에서 파생된 작업 순서를 나타낸다.
- Plan은 source of truth를 변경하는 구현 작업을 포함하지 않는다.
- source of truth 보강이 필요하면 별도 문서 보강 흐름으로 분리한다.
- source of truth 변경이 필요한 Plan/Task는 Change Request와 연결하고, 변경 승인 전에는 APPROVED로 만들지 않는다.
- source of truth 변경이 승인되면 기존 Plan/Task/prompt/verification result의 무효화 여부를 확인하고 필요한 재생성 또는 수정 범위를 보고한다.
- 후속 Task는 모든 dependsOn Task가 COMPLETE가 되기 전까지 write-implementation-prompt으로 넘어갈 수 없다고 명시한다.
- Plan completion criteria에는 테스트 통과와 verification 통과를 포함한다.

## Dependency Gate 규칙

다음 상태의 선행 Task가 하나라도 있으면 후속 Task prompt 생성과 implementation을 허용하지 않는다.

- DRAFT
- APPROVED but not started
- IN_PROGRESS
- PENDING_USER_APPROVAL
- BLOCKED_BY_MISSING_CONTEXT
- BLOCKED_BY_POLICY_CONFLICT
- NEEDS_SOURCE_OF_TRUTH_CHANGE
- NEEDS_REVISION
- VERIFIED but not reviewed/complete

예외는 사용자가 Plan/Task dependency 변경을 명시 승인하고 Source of Truth Manager가 변경된 Plan/Task 정합성을 VALIDATED한 경우뿐이다.

## 다음 단계

- Task가 APPROVED이고 documentCoverage가 READY이면 `write-implementation-prompt.md`로 이동한다.
- 부족한 문서/정책이 발견되면 `_missing-context.md`로 돌아간다.
- 사용자 개입 없이 진행 가능한 경우, Task 작성 후 검증하고 `write-implementation-prompt.md` 단계까지 이어서 진행할 수 있는지 판단한다.
- 사용자 선택이 필요한 경우, Plan/Task를 APPROVED로 만들지 않고 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다.

사용자-facing 보고에서는 내부 status만 말하지 않고, 다음 형식을 우선 사용한다.

```text
확인한 기준:
- ...

현재 판단:
- 바로 구현 가능 / 아직 결정 필요

이유:
- ...

먼저 정할 것:
1. ...
2. ...

내 추천:
- ...

다음에 할 일:
- ...

내가 물어볼 것:
1. ...
2. ...
```

사용자 선택이 필요한 경우에는 마지막을 다음처럼 끝낸다.

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

사용자 개입 없이 진행 가능한 경우에는 마지막을 다음처럼 끝내고 실제로 다음 단계까지 수행한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
현재 기준으로 안전하게 진행할 수 있으므로, 요청 범위 안에서 다음 작업까지 진행합니다.

진행할 작업:
- Plan/Task 작성
- 기존 문서 구조에 맞는 저장 위치 확인
- 문서 coverage 확인
- 가능한 경우 구현 지시서 작성 단계로 이동

진행하지 않을 작업:
- 기준 문서에 없는 정책 결정
- 승인되지 않은 구현 또는 삭제
- 기존 문서 구조와 다른 파일 배치
```

예를 들어 작업 지시를 만들 수 없으면 "작업 지시를 만들기 전에 기준 문서와 선행 작업 상태가 맞는지 확인해야 합니다"처럼 쉬운 표현을 먼저 사용하고, 내부 판정표는 사용자가 요청했을 때만 뒤에 붙인다.

## 미확정 결정 정지 규칙

Planning 중 미확정 결정이 발견되면 다음 행동만 허용된다.

- Task를 DRAFT 또는 BLOCKED coverage 상태로 둔다.
- 미확정 결정 질문을 만든다.
- 사용자 답변과 source of truth 승인 후 다시 planning한다.

금지:

- 작업 기준서 임의 수정
- source of truth 변경에 맞춘 Plan/Task 임의 수정
- testRequirements 축소
- 구현 prompt 생성
- 선행 Task incomplete 상태에서 후속 Task prompt 생성
- 미확정 결정을 "나중에"로 미루고 후속 Task 진행
- revision 실행
- complete 진행
