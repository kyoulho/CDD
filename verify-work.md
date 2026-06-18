# Verify Work Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: 구현 결과가 기준 문서와 작업 기준서에 맞는지 검증할 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

## 핵심 용어

- 제품 기준 준비 상태: 무엇을 왜 만들 것인지에 대한 기획 준비도.
- 기술 설계 준비 상태: 제품 판단을 저장 구조, 상태, API, 코드 구조로 표현할 기준이 정해졌는지에 대한 설계 준비도.
- 구현 시작 가능 여부: 에이전트가 구현을 시작해도 되는지에 대한 실행 준비도.
- 이번 작업 기준 묶음: 이번 작업에서 따라야 할 승인된 기준 문서 묶음.
- 작업 기준서: 구현 전 작업 범위, 금지 범위, 검증 기준을 고정하는 작업 계약.

이 skill은 구현 후 결과를 문서, 정책, Task와 대조 검증한다.

Verification은 기본적으로 읽기와 판정 작업이다. 작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 verification result 파일을 생성하거나 수정하지 않고 분석 보고서만 작성한다. 검증 중 문제가 발견되어도 코드 수정, 테스트 수정, rollback, revision 실행으로 넘어가지 않는다.

테스트 통과만으로 완료 판단하지 않는다.

Verification result artifact는 `_artifact-metadata.md`의 metadata, `_artifact-templates.md`의 `Verification Result Metadata Template`, `_status-machine.md`의 status를 따른다. 사용자-facing 보고는 `_user-facing-language.md`를 따른다.

Verification result를 만들거나 수정하기 전에는 대상 프로젝트의 기존 문서 배치 구조를 먼저 확인한다. `docs/README.md`, 문서 index, document registry, 기존 검증 결과 목록, 기존 파일명과 누적 방식을 확인하고 `_artifact-templates.md`의 Document Placement Check를 작성한다.

기존 구조가 단일 검증 문서에 결과를 누적하는 방식이면 후속 검증도 같은 문서에 추가한다. 기존 구조가 task별 검증 결과 파일 분리 방식이면 후속 task도 같은 방식으로 분리한다. 기존 구조와 다른 파일 배치를 하려면 auto-stop하고 전체 문서 구조 변경안과 사용자 승인을 요구한다.

새 검증 결과 파일을 만들기 전에는 왜 기존 문서에 추가하지 않고 새 파일이 필요한지 보고한다.

검증 실패는 내부 status만으로 보고하지 않고, 무엇이 어긋났는지와 무엇을 먼저 고쳐야 하는지로 설명한다.

검증 실패 시 내부 코드나 진단표보다 "무엇이 어긋났는지"와 "무엇을 고쳐야 하는지"를 먼저 말한다. 상세 표는 사용자가 요청했을 때 제공한다.

## 입력

- 작업 기준서
- requiredDocuments
- documentCoverage
- rules
- source of truth
- 제품 기준 문서
- 기술 설계 기준 문서
- 구현 prompt
- check result
- 구현 diff 또는 변경 파일
- result/report
- 작업 기준 묶음
- 준비 상태 확인 결과

## 최소 guard checklist

Verification은 이 checklist를 실행 가능한 스크립트로 구현하지 않는다. guard는 자동 수정 도구가 아니라 위반 가능성을 감지하고 보고하는 제동 장치다. 실제 스크립트 구현은 별도 작업이다. 대상 프로젝트에 맞는 명령이나 수동 확인이 가능하면 check result 또는 verification matrix에 반영한다.

- changed-file scope check: 변경 파일이 승인된 Task scope, 작업 기준 묶음의 allowedScope 또는 approvedScope 안에 있는지 확인한다.
- archive/superseded reference audit: archive/superseded 문서를 active source of truth처럼 참조했는지 확인한다.
- forbidden keyword audit: Task, 작업 기준 묶음의 forbiddenScope, approved source of truth가 금지한 용어, 기능, 접근이 되살아났는지 확인한다.
- generated/index docs modification guard: generated docs, indexing docs, memory/recall outputs가 승인 없이 수정되었는지 확인한다.
- document placement guard: 작업 기준서, 구현 지시서, 검증 결과, 완료 기록이 대상 프로젝트의 기존 문서 배치 구조를 따르는지 확인한다.
- migration change guard: migration, schema, seed, data repair 변경이 승인된 정책과 범위 안에 있는지 확인한다.
- interaction surface guard: 상호작용 방식 확인 없이 화면, CLI 명령, API surface, 배치 실행 방식, 저장 구조가 제안되거나 구현되었는지 확인한다.
- frontend UX guard: 프론트엔드 UX 확인 없이 route, page, component, layout, styling, motion, visual QA 기준이 제안되거나 구현되었는지 확인한다.
- frontend UX document coverage guard: 승인된 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 없이 웹/모바일 UI 기준이 제안되거나 구현되었는지 확인한다.
- premature structure proposal guard: Storage Intent Check, Behavior Contract Check, State Meaning Check 없이 table, column, API path, status enum이 제안되거나 구현되었는지 확인한다.
- operational quality guard: 운영/품질 기준 확인 없이 성능, 보안, 권한, 조회, 재시도, 로그/감사 정책이 제안되거나 구현되었는지 확인한다.
- performance scope guard: 구현 중 발견한 성능 위험 후보가 승인된 조사 범위 없이 코드 변경, acceptance criteria, completion 판단으로 승격되었는지 확인한다.
- SOT conflict check: 작업 기준 묶음, approved source of truth, 작업 기준서가 서로 충돌하는지 확인한다.
- completion report required-fields check: 완료 보고가 `complete-work.md`의 짧은 완료 보고 형식 또는 cleanup/delete 전용 완료 보고 형식을 충족하는지 확인한다.
- environment failure vs code failure classification: 실패가 환경 문제인지 코드 문제인지 분리해 보고한다.
- cleanup/delete verification: keep list가 보존되었는지, delete list가 근거대로 제거되었는지, stale route/API/UI/DB/test/doc reference가 남지 않았는지 확인한다.

## 준비 상태 재확인 예시

Verification 결과에는 다음 항목을 포함한다.

```text
준비 상태 다시 확인:
- 제품 기준 일치:
- 기술 설계 기준 일치:
- 구현 범위 준수:
- 금지 범위 위반:
- 보관/이전 문서를 현재 기준으로 사용:
- 구현 보류 상태에서 구현 발생:
```

테스트 통과만 확인하지 말고 제품 기준 문서 일치, 기술 설계 기준 문서 일치, allowedScope 밖 수정 여부, forbiddenScope 위반 여부, archive/superseded 문서를 active SOT처럼 사용했는지 여부, 준비 상태가 `NOT_READY`였는데 구현된 흔적이 있는지 확인한다.

## 역할

- 구현 결과를 작업 기준서, requiredDocuments, rules, source of truth, prompt, result와 대조한다.
- 구현 결과가 제품 기준 문서와 기술 설계 기준 문서 모두에 부합하는지 대조한다.
- 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부가 모두 `READY`였는지 확인한다.
- 사용자 또는 운영자가 접하는 기능이라면 상호작용 방식 확인이 허용 결론이었는지 확인한다.
- 웹/모바일 UI라면 프론트엔드 UX 확인이 허용 결론이었는지 확인한다.
- 웹/모바일 UI라면 requiredDocuments에 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 또는 동등한 승인 문서가 포함되어 있는지 확인한다.
- DB/API/status 구조가 포함된 경우 Storage Intent Check, Behavior Contract Check, State Meaning Check가 허용 결론이었는지 확인한다.
- 성능/보안/운영 판단이 포함된 경우 운영/품질 기준 확인이 허용 결론이었는지 확인한다.
- 성능 위험 후보가 구현 범위에 포함된 경우 조사 범위, 판단 근거, 허용된 수정 범위가 승인되어 있었는지 확인한다.
- verification matrix를 작성한다.
- source of truth와 충돌하는 구현을 찾는다.
- 문서에 없는 도메인/아키텍처/행위 판단이 코드에 들어갔는지 확인한다.
- 수정이 필요한지 판단한다.
- source of truth를 수정하지 않는다.
- source of truth 변경이 필요하면 finding으로 기록하고 `_source-of-truth-manager.md`로 라우팅한다.
- verification result metadata를 기록한다.
- verification result는 가능한 한 `_artifact-templates.md`의 `Verification Result Metadata Template` 형식으로 기록한다.
- verification result 저장 전 사용자 보고에 수정할 파일, 새로 만들 파일, 기존 문서 구조와 맞는지, README/index 갱신 필요 여부를 포함한다.
- 기존 문서 구조와 다른 파일 배치가 필요하면 검증 결과를 저장하지 말고 사용자 확인을 받는다.
- 검증 실패를 내부 하네스 용어만으로 보고하지 않고, 어떤 기준 문서와 작업 지시가 어긋났는지 설명한다.

## 검증 항목

verification matrix에는 최소한 다음 항목을 포함한다.

```text
acceptanceCriteria 충족 여부
제품 기준 문서 준수 여부
기술 설계 기준 문서 준수 여부
제품 기준 준비 상태 READY 여부
기술 설계 준비 상태 READY 여부
구현 시작 가능 여부 READY 여부
IMPLEMENTATION_BLOCKED 상태에서 구현이 진행되었는지 여부
forbiddenApproaches 위반 여부
requiredDocuments 준수 여부
documentCoverage READY 여부
testRequirements 충족 여부
Task 범위 초과 여부
문서에 없는 도메인/아키텍처/행위 판단 추가 여부
상호작용 방식 확인 없이 화면/CLI 명령/API surface/배치 실행 방식/저장 구조를 제안하거나 구현했는지 여부
프론트엔드 UX 확인 없이 route/page/component/layout/styling/motion/visual QA 기준을 제안하거나 구현했는지 여부
FRONTEND_UX_CRITERIA, USER_FLOW/INTERACTION_SPEC, DESIGN_SYSTEM/UI_PATTERN, FRONTEND_ARCHITECTURE 또는 동등한 승인 문서 없이 웹/모바일 UI 기준을 제안하거나 구현했는지 여부
Storage Intent Check 없이 table/column/migration/repository/API DTO를 제안하거나 구현했는지 여부
Behavior Contract Check 없이 API path/method/route/controller/request-response shape를 제안하거나 구현했는지 여부
State Meaning Check 없이 status enum/status column/state transition을 제안하거나 구현했는지 여부
운영/품질 기준 확인 없이 성능/보안/권한/조회/재시도/로그/감사 정책을 제안하거나 구현했는지 여부
성능 위험 후보를 승인된 조사 범위 없이 구현 범위로 승격했는지 여부
기존 코드나 기술 스택을 이유로 기술 설계 준비 상태를 READY로 본 흔적이 있는지 여부
source of truth 충돌 여부
source of truth, document registry, Plan, Task, prompt, verification result가 승인 없이 수정되었는지 여부
source of truth 문서 일부만 변경되어 다른 APPROVED 문서와 충돌하는지 여부
작업 기준서가 변경된 source of truth와 불일치하는지 여부
Known conflict가 남은 상태에서 implementation, revision, complete로 진행했는지 여부
영향 분석에서 발견한 충돌을 warning으로 낮추고 APPLY했는지 여부
Direction Approval을 Apply Approval로 오해했는지 여부
Source of Truth APPLY가 명시적 Apply Approval 없이 수행되었는지 여부
dependsOn 미완료 Task의 prompt가 생성되었는지 여부
선행 Task blocked/pending/revision 상태를 무시했는지 여부
미확정 결정을 "나중에"로 미루고 진행했는지 여부
기존 artifact를 legitimacy check 없이 정상 baseline으로 사용했는지 여부
이전 unauthorized change를 현재 baseline으로 받아들였는지 여부
prompt draft 확인 지점이 충족되지 않았는데 prompt를 생성/수정했는지 여부
invalid/quarantined/superseded artifact를 VALIDATED, implementation, completion 근거로 사용했는지 여부
archive/superseded 문서를 active source of truth처럼 사용했는지 여부
generated docs/indexes, memory/recall notes, previous assistant responses를 approved source of truth처럼 사용했는지 여부
cleanup/delete Task에서 keep list 항목을 삭제했는지 여부
cleanup/delete Task에서 delete list 항목을 이름만 바꿔 core path에 남겼는지 여부
cleanup/delete Task에서 stale route/API/UI/DB/test/doc reference가 남았는지 여부
승인된 TEST_STRATEGY 없이 mock/fake/stub/slice test를 선택했는지 여부
코드의 id 타입이 approved DATA_MODEL/API_CONTRACT 문서와 일치하는지 여부
DB primary key 생성 전략이 문서와 일치하는지 여부
API path variable/response id 타입이 문서와 일치하는지 여부
날짜/시간 포맷이 문서와 일치하는지 여부
error response code/message 형식이 문서와 일치하는지 여부
상태 변경 행위가 문서와 일치하는지 여부
삭제 행위가 문서와 일치하는지 여부
승인 문서에 없는 테스트 dependency가 추가되었는지 여부
H2, Testcontainers, embedded DB 등이 승인 없이 추가되었는지 여부
application-test.yml 또는 test profile이 승인 없이 추가되었는지 여부
db/migration-test/** 같은 테스트 전용 migration이 승인 없이 추가되었는지 여부
운영 migration과 테스트 migration이 분리되었는지 여부
테스트가 운영 DB dialect와 다른 dialect를 사용하도록 바뀌었는지 여부
승인되지 않은 mock/fake/stub 전략이 도입되었는지 여부
testRequirements를 만족시키기 위해 source of truth 밖 테스트 전략을 도입했는지 여부
승인 문서에 없는 production/test dependency가 추가되었는지 여부
승인 문서에 없는 Gradle plugin이 추가되었는지 여부
승인 문서에 없는 annotation processor가 추가되었는지 여부
승인 문서에 없는 code generation tool이 추가되었는지 여부
승인 문서에 없는 runtime-exposed library가 추가되었는지 여부
```

## 정책 위반 유형

Verification findings에는 필요 시 다음 유형을 사용한다.

```text
IDENTIFIER_POLICY_VIOLATION
DATA_MODEL_POLICY_VIOLATION
API_CONTRACT_POLICY_VIOLATION
BEHAVIOR_POLICY_VIOLATION
UNAPPROVED_POLICY_DECISION
INTERFACE_DESIGN_BEFORE_INTERACTION_DECISION
FRONTEND_UX_BEFORE_FRONTEND_UX_DECISION
FRONTEND_UX_DOCUMENT_COVERAGE_MISSING
DESIGN_SYSTEM_POLICY_VIOLATION
UNAPPROVED_FRONTEND_UX_DOCUMENT_DRAFTING
UNAPPROVED_FRONTEND_UX_DECISION
DB_DESIGN_BEFORE_STORAGE_INTENT
API_DESIGN_BEFORE_BEHAVIOR_CONTRACT
STATUS_MODEL_BEFORE_STATE_MEANING
OPERATIONAL_QUALITY_POLICY_MISSING
PERFORMANCE_SECURITY_OPERATION_ASSUMED_SAFE
PERFORMANCE_RISK_SCOPE_ESCALATED
TECH_STACK_TREATED_AS_ENGINEERING_READINESS
UNAPPROVED_TEST_STRATEGY_DECISION
TEST_DATABASE_POLICY_VIOLATION
TEST_MIGRATION_POLICY_VIOLATION
TEST_PROFILE_POLICY_VIOLATION
TEST_DIALECT_MISMATCH
UNAUTHORIZED_REVISION_EXECUTION
UNAPPROVED_TEST_SCOPE_REDUCTION
UNAPPROVED_POLICY_DOCUMENT_DRAFTING
VERIFICATION_GATE_BYPASS_ATTEMPT
UNAUTHORIZED_SOURCE_OF_TRUTH_CHANGE
NEEDS_SOURCE_OF_TRUTH_CHANGE
PARTIAL_SOURCE_OF_TRUTH_UPDATE_ATTEMPT
INTENTIONAL_SOURCE_OF_TRUTH_INCONSISTENCY
USER_SCOPED_CHANGE_OVERRIDES_CONSISTENCY
IMPACT_ANALYSIS_DOWNGRADED_TO_WARNING
AMBIGUOUS_APPROVAL_ESCALATION
DIRECTION_APPROVAL_TREATED_AS_APPLY_APPROVAL
SOURCE_OF_TRUTH_APPLY_WITHOUT_EXPLICIT_APPROVAL
DEPENDENCY_GATE_BYPASS_BY_PROMPT_AUTHORING
BLOCKED_PREDECESSOR_IGNORED
MISSING_CONTEXT_DEFERRED_TO_LATER
INVALID_ARTIFACT_NORMALIZATION
PREVIOUS_UNAUTHORIZED_CHANGE_ACCEPTED_AS_BASELINE
PROMPT_DRAFT_MODIFIED_BEFORE_GATE
UNAPPROVED_MOCK_STRATEGY_DECISION
UNAPPROVED_SLICE_TEST_STRATEGY_DECISION
ARTIFACT_EXISTS_BUT_NOT_VALID
LEGITIMACY_CHECK_SKIPPED
UNAPPROVED_DEPENDENCY_ADDITION
UNAPPROVED_BUILD_PLUGIN_ADDITION
UNAPPROVED_ANNOTATION_PROCESSOR_ADDITION
UNAPPROVED_CODE_GENERATION_TOOL
RUNTIME_EXPOSED_LIBRARY_POLICY_VIOLATION
NON_SOT_REFERENCE_USED_AS_AUTHORITY
ARCHIVE_OR_SUPERSEDED_USED_AS_ACTIVE_SOT
GENERATED_OR_INDEX_DOC_USED_AS_SOT
MEMORY_OR_RECALL_USED_AS_SOT
ENVIRONMENT_FAILURE_MISCLASSIFIED
CODE_FAILURE_MISCLASSIFIED
```

## 환경 실패와 코드 실패 구분

Verification은 실패를 환경 실패와 코드 실패로 분리해서 보고한다.

환경 실패 예:

- Docker/Testcontainers unavailable
- `node_modules` missing
- lockfile/package mismatch
- local port occupied
- external service unavailable
- missing credential

코드 실패 예:

- compile error
- typecheck error
- unit test assertion failure
- migration SQL error
- contract test mismatch
- lint/format failure
- runtime exception caused by changed code

규칙:

- 환경 실패를 코드 성공으로 포장하지 않는다.
- 코드 실패를 환경 문제로 뭉개지 않는다.
- 실패 원인, 재현 명령, 필요한 후속 조치를 보고한다.
- 원인을 확정할 수 없으면 unknown으로 표시하고 추가 확인이 필요한 증거를 적는다.

## Identifier/API/Data Model 검증

다음을 반드시 확인한다.

- 상호작용 방식 확인이 `상호작용 설계 가능`이기 전에 화면, CLI 명령, API surface, 배치 실행 방식, 저장 구조가 제안되거나 구현되지 않았는가?
- Storage Intent Check가 `DB_DESIGN_ALLOWED`이기 전에 table, column, migration, repository, API DTO가 제안되거나 구현되지 않았는가?
- Behavior Contract Check가 `API_DESIGN_ALLOWED`이기 전에 API path, method, route, controller, request/response shape가 제안되거나 구현되지 않았는가?
- State Meaning Check가 `STATE_MODEL_ALLOWED`이기 전에 status enum, status column, state transition이 제안되거나 구현되지 않았는가?
- 코드의 id 타입이 approved DATA_MODEL/API_CONTRACT 문서와 일치하는가?
- DB primary key 생성 전략이 문서와 일치하는가?
- API path variable/response id 타입이 문서와 일치하는가?
- 날짜/시간 포맷이 문서와 일치하는가?
- error response code/message 형식이 문서와 일치하는가?
- 상태 변경 행위가 문서와 일치하는가?
- 삭제 행위가 문서와 일치하는가?
- 구현 코드가 문서에 없는 정책을 새로 도입하지 않았는가?

## Interaction / Operational Quality 검증

다음을 반드시 확인한다.

- 사용자 또는 운영자가 접하는 기능의 입력, 출력, 실패, 빈 상태, 권한 없음, 처리 중 피드백이 approved Product SOT와 일치하는가?
- 상호작용 방식이 비어 있는데 인터페이스, 화면, CLI 명령, API surface, 배치 실행 방식이 구현되지 않았는가?
- 웹/모바일 UI의 화면 상태, 정보 구조, 주요 행동, 반응형 기준, 접근성, text overflow, visual QA 기준이 approved Product/Frontend SOT와 일치하는가?
- 웹/모바일 UI 작업의 requiredDocuments에 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 또는 동등한 승인 문서가 포함되어 있는가?
- 프론트엔드 UX 확인이 비어 있는데 route, page, component, layout, styling, motion, visual QA 기준이 구현되지 않았는가?
- 운영/품질 기준 확인이 `설계 가능`이기 전에 성능, 보안, 권한, 데이터 양, 조회, 정렬, 검색, 페이지 처리, 재시도, 로그/감사 정책이 제안되거나 구현되지 않았는가?
- 성능 위험 후보가 승인된 조사 범위, 판단 근거, 허용된 수정 범위 없이 코드 변경으로 승격되지 않았는가?
- 에이전트가 빈 정책을 채워 자신의 구현을 정당화하지 않았는가?

## Test Strategy 검증

다음을 반드시 확인한다.

- 승인 문서에 없는 테스트 dependency가 추가되었는가?
- H2, Testcontainers, embedded DB 등이 승인 없이 추가되었는가?
- application-test.yml 또는 test profile이 승인 없이 추가되었는가?
- db/migration-test/** 같은 테스트 전용 migration이 승인 없이 추가되었는가?
- 운영 migration과 테스트 migration이 분리되었는가?
- 테스트가 운영 DB dialect와 다른 dialect를 사용하도록 바뀌었는가?
- 승인되지 않은 mock/fake/stub 전략이 도입되었는가?
- testRequirements를 만족시키기 위해 source of truth 밖 테스트 전략을 도입했는가?
- 승인 문서에 없는 production/test dependency가 추가되었는가?
- 승인 문서에 없는 Gradle plugin이 추가되었는가?
- 승인 문서에 없는 annotation processor가 추가되었는가?
- 승인 문서에 없는 code generation tool이 추가되었는가?
- 승인 문서에 없는 runtime-exposed library가 추가되었는가?
- testRequirements를 축소했는가?
- DB integration test를 unit/static test로 대체했는가?
- Repository save/find 테스트를 제거했는가?
- Flyway 실제 적용 테스트를 SQL 정적 검증으로 대체했는가?
- 테스트 실패를 피하기 위해 assertion을 제거하거나 약화했는가?
- 테스트를 후속 Task로 임의 이연했는가?
- 미확정 결정이 해결되기 전에 코드 수정, revision 실행, 정책 문서 DRAFT 생성이 있었는가?
- source of truth 문서 일부만 변경되어 다른 APPROVED 문서와 충돌하는가?
- 작업 기준서가 변경된 source of truth와 불일치하는가?
- Known conflict가 남은 상태에서 complete 또는 implementation 진행이 있었는가?
- Known Conflicts After Apply가 비어 있지 않은데 APPLY했는가?
- 영향 분석에서 발견한 충돌을 warning으로 낮췄는가?
- "A로 하자" 같은 Direction Approval을 파일 APPLY 승인으로 해석했는가?
- 명시적 Apply Approval 없이 Files Proposed for Apply를 수정했는가?
- Prompt Draft Approval을 Prompt Execution Approval로 해석했는가?
- dependsOn이 COMPLETE가 아닌 후속 Task prompt를 생성했는가?
- 선행 Task가 BLOCKED_BY_MISSING_CONTEXT, BLOCKED_BY_POLICY_CONFLICT, PENDING_USER_APPROVAL, NEEDS_REVISION, NEEDS_SOURCE_OF_TRUTH_CHANGE 상태인데 후속 Task로 진행했는가?
- 미확정 결정을 "나중에"로 미루고 prompt, implementation, revision, complete로 진행했는가?
- artifact가 디스크에 존재한다는 이유만으로 정상 baseline으로 사용했는가?
- Change Request, prompt, verification result, completion record에 대해 legitimacy check를 수행했는가?
- invalid/quarantined/superseded artifact를 수정해서 정상화하려 했는가?
- archive/superseded 문서를 active source of truth처럼 사용했는가?
- generated docs/indexes, memory/recall notes, previous assistant responses를 approved source of truth처럼 사용했는가?
- 명시적 APPLY 승인 없는 CR을 VALIDATED로 인정했는가?
- TASK dependency 확인 지점 위반으로 생성된 prompt를 정상 DRAFT로 인정했는가?
- 승인된 TEST_STRATEGY 없이 mock, fake, stub, `@WebMvcTest`, `@DataJpaTest`, slice test, mocked service/repository를 선택했는가?

## 결과 상태

```text
VERIFIED
NEEDS_REVISION
BLOCKED_BY_MISSING_CONTEXT
BLOCKED_BY_POLICY_CONFLICT
NEEDS_SOURCE_OF_TRUTH_CHANGE
BLOCKED_BY_PREDECESSOR
BLOCKED_BY_INVALID_ARTIFACT
```

## Verification Result Metadata 예시

```yaml
artifact:
  id: VERIFY-TASK-002-001
  type: verification-result
  status: DRAFT
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: verify-work
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
    - APPROVAL-PROMPT-TASK-002-EXECUTE
  generatedFrom:
    - prompts/TASK-002.md
    - tasks/TASK-002.yml
  knownConflicts: []
  supersedes: []
  supersededBy: null
```

### VERIFIED

다음이 모두 만족될 때만 사용한다.

- acceptanceCriteria 충족
- forbiddenApproaches 위반 없음
- requiredDocuments 준수
- documentCoverage READY
- testRequirements 충족
- Task 범위 초과 없음
- 문서 밖 도메인/아키텍처/행위 판단 없음
- source of truth 충돌 없음
- Known Conflicts After Apply 비어 있음
- 모든 dependsOn Task COMPLETE
- 미확정 결정 없음
- 사용자/운영자 상호작용 방식이 approved Product SOT와 일치
- 웹/모바일 UI라면 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 또는 동등한 승인 문서와 일치
- 운영/품질 기준이 approved Engineering SOT와 일치
- source of truth APPLY와 prompt execution이 각각 명시적으로 승인됨
- 사용한 artifact가 legitimacy check 통과
- invalid/quarantined/superseded artifact가 없음
- archive/superseded 문서를 active source of truth 근거로 사용하지 않음
- generated/index/memory/recall/previous-report 자료를 approved source of truth로 오인하지 않음
- identifier, key generation, API-visible id representation이 승인 문서와 일치
- table, column, migration, repository, API DTO가 Storage Intent Check 허용 결론 뒤에만 등장함
- API path, request/response shape가 Behavior Contract Check 허용 결론 뒤에만 등장함
- status enum, status column, state transition이 State Meaning Check 허용 결론 뒤에만 등장함
- 승인되지 않은 테스트 DB/profile/migration/dialect/mock/fake/stub 전략이 없음
- 승인되지 않은 dependency, plugin, annotation processor, code generation tool, runtime-exposed library 추가 없음

### NEEDS_REVISION

Task 범위 안에서 수정 가능한 문제가 있으면 사용한다.

예:

- acceptance criteria 일부 미충족
- 테스트 누락
- 구현 누락
- forbiddenApproaches 위반이지만 문서 정책 결정 없이 수정 가능

NEEDS_REVISION은 승인된 source of truth 안에서 수정 가능한 구현 문제에만 사용한다. 미확정 결정이 필요하면 NEEDS_REVISION이 아니다.

### BLOCKED_BY_MISSING_CONTEXT

필요한 정책 문서나 사용자 결정이 없어 검증을 완료할 수 없으면 사용한다.

허용 행동:

- 미확정 결정 질문만 가능
- 코드 수정 금지
- revision 금지
- complete 금지

### BLOCKED_BY_POLICY_CONFLICT

새 정책/도메인 판단이 필요하거나 source of truth와 충돌해 사용자의 결정이 필요하면 사용한다.

허용 행동:

- 충돌 보고만 가능
- 사용자의 정책 결정 또는 source of truth 수정 승인 필요
- 코드 수정 금지
- revision 금지
- complete 금지

### NEEDS_SOURCE_OF_TRUTH_CHANGE

구현 또는 Task 요구를 유지하려면 source of truth 변경이 필요한 경우 사용한다.

허용 행동:

- Source of Truth Change Request 작성
- 영향 분석 보고
- 변경 방향 질문
- 코드 수정 금지
- revision 금지
- complete 금지
- source of truth 직접 수정 금지

다음 경우에도 사용한다.

- 일부 source of truth 문서만 변경되어 다른 APPROVED 문서와 충돌한다.
- 작업 기준서가 변경된 source of truth와 불일치한다.
- Known Conflicts After Apply가 남아 있다.
- 사용자 scope를 따르려면 source of truth 정합성을 깨야 한다.
- Direction Approval만 있고 Apply Approval이 없다.
- known conflict나 invalidated predecessor 때문에 후속 Task prompt 생성이 불가능하다.

`NEEDS_SOURCE_OF_TRUTH_CHANGE`는 Verification Agent가 문서를 고치라는 의미가 아니다. `_source-of-truth-manager.md` 절차로 넘기라는 의미다.

### BLOCKED_BY_PREDECESSOR

선행 Task가 완료되지 않아 후속 Task 검증이나 prompt 생성이 불가능하면 사용한다.

허용 행동:

- 선행 Task 상태 보고
- 미확정 결정 질문 또는 필요한 확인 지점 안내
- 후속 Task prompt 생성 금지
- 후속 Task implementation 금지
- complete 금지

### BLOCKED_BY_INVALID_ARTIFACT

기존 artifact가 legitimacy check를 통과하지 못하거나 생성 근거를 확인할 수 없으면 사용한다.

허용 행동:

- 위반 보고
- `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보 표시
- 사용자에게 처리 방향 질문
- 정합성 복구 계획 제안

금지 행동:

- 해당 artifact를 기반으로 후속 prompt 생성
- 해당 artifact를 VALIDATED 근거로 사용
- 해당 artifact를 completion 근거로 사용
- 해당 artifact를 수정해서 정상화
- 해당 artifact를 최신 harness 기준으로 보강하여 계속 사용

## 다음 단계

- VERIFIED: `complete-work.md`로 이동 가능. 단, 사용자 review approval이 필요하다.
- NEEDS_REVISION: revision-prompt 생성 가능. 사용자 승인 후 revision 가능.
- BLOCKED_BY_MISSING_CONTEXT: 미확정 결정 질문만 가능. 코드 수정, revision, complete 금지.
- BLOCKED_BY_POLICY_CONFLICT: 충돌 보고만 가능. 사용자 정책 결정 또는 source of truth 수정 승인 전 코드 수정, revision 금지.
- NEEDS_SOURCE_OF_TRUTH_CHANGE: Source of Truth Change Request만 가능. 사용자 승인 전 코드 수정, revision, complete, 문서 직접 수정 금지.
- BLOCKED_BY_PREDECESSOR: 선행 Task 완료 전 후속 Task prompt, implementation, revision, complete 금지.
- BLOCKED_BY_INVALID_ARTIFACT: artifact 격리/폐기/복구 방향 결정 전 prompt, implementation, revision, complete 금지.
- 사용자 개입 없이 진행 가능한 경우에는 검증 명령을 실행하고 결과와 다음 후보까지 보고한다.
- 사용자 선택이 필요한 경우에는 수정하지 않고 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다.

## User-Facing Reporting

사용자에게는 내부 status만 단독으로 보고하지 않는다.

사용자-facing 검증 보고는 다음을 우선한다.

```text
확인한 기준:
- ...

현재 판단:
- 바로 완료 가능 / 아직 결정 필요 / 수정 필요

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

검증 보고에서 `Product Readiness`, `Engineering Readiness`, `Implementation Readiness`, `READY`, `NOT READY`, `Storage Intent Check`, `Behavior Contract Check`, `State Meaning Check`를 기본 제목이나 결론으로 쓰지 않는다. 내부 상태값은 verification artifact나 사용자가 요청한 상세 판정표에만 그대로 둔다.

검증 보고에는 실패가 환경 실패인지 코드 실패인지, 실행한 재현 명령이 무엇인지, 필요한 후속 조치가 무엇인지 포함한다. archive/superseded 문서를 참조했다면 active source of truth가 아니라 historical context로 참조했는지 밝힌다.

검증이 통과했지만 사용자 review approval이 필요하면 다음처럼 끝낸다.

```text
다음에 할 일:
아직 직접 완료 처리하면 안 됩니다. 먼저 변경 결과를 리뷰해야 합니다.

선택지:
1. 변경 결과를 승인하고 완료 보고로 이동한다.
2. 수정할 점을 알려주고 revision으로 이동한다.
3. 기준 문서를 먼저 바꿀지 검토한다.

제 추천:
- 변경 범위와 검증 결과가 기준과 맞으면 완료 보고로 이동합니다.

바로 답할 수 있는 문장:
"검증 결과를 승인한다. 완료 보고로 진행해라."
```

검증 요청만으로 충분하고 추가 사용자 결정이 없으면 다음처럼 끝내고 가능한 다음 확인까지 수행한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
현재 기준으로 안전하게 진행할 수 있으므로, 요청 범위 안에서 다음 작업까지 진행합니다.

진행할 작업:
- 검증 명령 실행
- 기준 문서와 작업 범위 대조
- 기존 문서 구조에 맞는 검증 결과 저장 위치 확인
- 결과와 다음 후보 보고

진행하지 않을 작업:
- 코드 수정
- 기준 문서 변경
- 기존 문서 구조와 다른 파일 배치
```

완료한 검증 보고는 다음처럼 끝낸다.

```text
다음에 할 일:
이번 검증은 완료되었습니다.

다음 후보:
1. 완료 보고로 이동
2. 발견된 문제를 수정하기 위한 revision 준비
3. 기준 문서 충돌 여부 정리

제 추천:
- 검증이 통과했다면 완료 보고로 이동합니다.
```

기본 응답에서는 다음 같은 내부 진단표를 먼저 보여주지 않는다.

```text
| 항목 | 현재 | harness |
|------|------|---------|
| metadata / approvalRefs | 없음 | 시작 조건 필수 |
| legitimacy check | 미통과 | 생성 시 gate 위반 |
| dependsOn | 미 COMPLETE | implementation 금지 |
```

Bad:

```text
BLOCKED_BY_POLICY_CONFLICT.
```

Good:

```text
지금 요청은 기존 기준 문서와 충돌합니다. 구현으로 바로 처리할 수 없고, 먼저 기준 문서를 바꿀지 결정해야 합니다.
```

Bad:

```text
TASK-002 prompt legitimacy check failed due to unresolved predecessor gate.
```

Good:

```text
TASK-002 구현 지시서 파일은 있지만, 선행 작업인 TASK-001이 아직 끝나지 않아 지금 기준으로는 사용할 수 없습니다. 먼저 TASK-001의 남은 결정을 정리해야 합니다.
```

Good:

```text
검증을 통과하지 못했습니다.
기준 문서와 구현 지시서가 서로 맞지 않는 부분이 있습니다.
먼저 다음을 정리해 주세요.
1. 기준 문서를 바꿀지, 구현을 기준 문서에 맞출지
2. 선행 작업을 먼저 끝낼지, 작업 순서를 바꿀지
3. 새 구현 지시서를 만들지
그다음 다시 검증할 수 있는 상태로 정리하겠습니다.
```
