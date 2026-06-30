# Document Readiness Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 사용자 Goal을 구현하기 전에 source of truth 문서가 충분한지 검증한다.

Readiness Agent는 `_readiness-gates.md`의 Product Readiness, Engineering Readiness, Implementation Readiness를 판정한다. 구현 작업은 세 gate가 모두 `READY`일 때만 가능하다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 readiness 결과를 분석 보고서로만 제공하고 문서, registry, Plan, Task, prompt, runs를 수정하지 않는다.

문서 준비도가 충분하면 후속 산출물이 참조할 수 있도록 `_artifact-templates.md`의 `Source Of Truth Snapshot Template` 형식으로 기준 문서 묶음을 기록한다.

Project Context는 도메인, 아키텍처, 테스트 전략보다 먼저 확인한다. `projectContext`가 없으면 `READY_FOR_PLANNING`을 선언하지 않는다.

문서 준비도가 충분하지 않으면 Plan/Task를 만들지 않는다. 부족한 문서나 정책은 `_missing-context.md`로 넘긴다.

Product Readiness 또는 Engineering Readiness가 `NOT READY`이면 Plan/Task를 만들지 않는다. Implementation Readiness가 `NOT READY`이면 구현, revision, completion으로 넘어가지 않는다.

이 skill은 `_source-of-truth-manager.md`의 하위 절차다. Readiness Agent는 source of truth를 직접 생성, 수정, 삭제, APPROVED 전환하지 않는다. 부족한 문서나 정책은 Source of Truth Manager의 Missing Context 흐름으로 넘긴다.

Readiness Agent는 사용자가 지정한 좁은 변경 scope를 그대로 source of truth 적용 가능 범위로 간주하지 않는다. 변경 후 known conflict가 남는다면 READY_FOR_PLANNING을 선언하지 않는다.

Readiness Agent는 디스크에 존재하는 docs, registry, Plan/Task, prompt, verification result를 자동으로 신뢰하지 않는다. 필요한 artifact가 legitimacy check를 통과하지 못하면 READY_FOR_PLANNING을 선언하지 않는다.

Readiness Agent는 문서 배치, 현재 작업 포인터, 기본 읽기 경로, active/history 분리, `cdd-audit` 실행 결과를 `_source-of-truth-manager.md`의 권위 규칙으로 확인한다. 그 확인에서 차단 항목이 있으면 `READY_FOR_PLANNING`을 선언하지 않는다.

## 빠른 탐색

- 판정에 필요한 입력은 "입력"을 본다.
- 제품, 기술 설계, 구현 시작 가능 여부는 "Readiness Gate 판정"을 본다.
- 결과 보고 구조는 "판정 출력 형식"을 본다.
- 부족한 결정을 나누는 기준은 "Missing Context 분리"를 본다.
- 문서 타입 후보와 수행 순서는 "문서 타입 후보", "수행 절차"를 본다.
- 사용자/운영자 상호작용, UI/UX, DB, API, status, 테스트, 운영 정책은 "필수 정책 점검 항목"을 본다.
- 결과 상태와 다음 이동은 "결과 상태", "다음 단계"를 본다.

## 입력

- 사용자 Goal
- Project Context 또는 Project Context 후보 답변
- 관련 문서 경로
- `document-registry.yml`이 있으면 registry 내용
- 기존 rules/source-of-truth 문서
- 기존 Plan/Task가 있으면 참고 정보
- SOT Packet이 있으면 승인된 기준 묶음

## Readiness Gate 판정

`_readiness-gates.md`의 기준으로 다음을 분리해서 판정한다.

### Product Readiness

Product Readiness는 "무엇을 왜 만들 것인가"에 대한 기획자 관점의 준비도다.

최소 확인 항목:

- 사용자 문제
- 대상 사용자
- 사용 시나리오
- 기능 범위
- 하지 않을 것
- 성공 기준
- 실패/예외 UX
- 이번 vertical slice의 제품 경계
- 사용자 또는 운영자가 접하는 기능의 상호작용 방식
- 입력과 출력
- 실패와 피드백
- 빈 상태
- 권한 없음 또는 실행 불가 상황
- 처리 중 또는 대기 중 피드백
- 사용자가 반드시 이해해야 하는 주요 문구와 결과
- 웹/모바일 UI인 경우 화면 상태, 정보 우선순위, 주요 행동, 반응형 기준, 접근성, 텍스트 overflow, 시각 검증 방법
- 웹/모바일 UI인 경우 분석 결과를 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저/스크린샷 검증 기준으로 고정한 UI 구현 계약
- Git 작업인 경우 포함할 변경, 제외할 변경, stage 방식, commit/push 대상, history rewrite 위험, recovery path를 고정한 버전관리 계약
- 버그리포트 작업인 경우 재현 절차, 실제/기대 결과, 환경, 영향도, 증거, 비밀정보 제거 기준을 고정한 버그리포트 계약

하나라도 작업 판단에 필요하지만 approved Product SOT에 없으면 `NOT READY`다.

사용자 또는 운영자가 접하는 기능인데 상호작용 방식, 입력, 출력, 실패, 빈 상태, 권한, 처리 중 피드백이 정해지지 않았으면 Product Readiness는 `NOT READY`다.

웹/모바일 UI 작업인데 프론트엔드 UX 확인이 없거나 `FRONTEND_UX_BLOCKED`이면 Product Readiness는 `NOT READY`다.

웹/모바일 UI 작업인데 승인된 분석 결과가 화면 단위 `uiImplementationContract`로 고정되지 않았으면 Product Readiness는 `NOT READY`다.

### Engineering Readiness

Engineering Readiness는 "그 제품 판단을 어떤 아키텍처, 저장 구조, 상태, API, 운영/품질 기준, 코드 구조로 안전하게 표현할 것인가"에 대한 코드 설계자 관점의 준비도다.

기존 코드, DB, 프레임워크, 기술 스택이 있다는 사실만으로 Engineering Readiness를 `READY`로 판정하지 않는다. 제품 판단을 아키텍처, 저장 구조, 상태, API, 성능, 보안, 운영 기준으로 표현해도 되는 기준이 approved Engineering SOT에 있어야 한다.

최소 확인 항목:

- 도메인 모델
- 아키텍처 경계
- 데이터 흐름
- API 계약
- DB/저장 정책
- 상태 전이
- Storage Intent Check 결과
- Behavior Contract Check 결과
- State Meaning Check 결과
- 권한/보안 영향
- 운영/품질 기준
- 성능, 데이터 양, 조회 방식, 정렬/검색/페이지 처리, 응답 속도 기대치
- 성능 위험 조사 범위, 근거 기준, 허용된 수정 범위
- 민감 정보 노출, 실패 처리, 재시도, 멱등성, 로그/감사 필요 여부
- 외부 연동/의존성
- 테스트 전략
- 실패/예외 처리 정책
- migration/data compatibility 영향이 있는지 여부

하나라도 작업 판단에 필요하지만 approved Engineering SOT에 없으면 `NOT READY`다.

성능, 보안, 운영 기준이 필요한 작업인데 운영/품질 기준 확인이 없거나 `설계 보류`이면 Engineering Readiness는 `NOT READY`다.

구현 중 발견 가능한 성능 위험 후보를 다룰 작업인데 성능 위험 조사 범위, 판단 근거, 허용된 수정 범위가 승인 문서에 없으면 Engineering Readiness는 `NOT READY`다.

DB table, column, migration, repository, API DTO가 필요한 작업인데 Storage Intent Check가 없거나 `DB_DESIGN_BLOCKED`이면 Engineering Readiness는 `NOT READY`다.

API path, method, route, controller, request/response shape가 필요한 작업인데 Behavior Contract Check가 없거나 `API_DESIGN_BLOCKED`이면 Engineering Readiness는 `NOT READY`다.

status enum, status column, state transition이 필요한 작업인데 State Meaning Check가 없거나 `STATE_MODEL_BLOCKED`이면 Engineering Readiness는 `NOT READY`다.

### Implementation Readiness

Implementation Readiness는 "이제 에이전트가 구현해도 되는가"에 대한 실행 준비도다.

최소 확인 항목:

- Product Readiness = `READY`
- Engineering Readiness = `READY`
- approved SOT Packet 존재
- Task Contract 존재
- allowed scope / forbidden scope 명시
- verification commands 명시
- user approval gate 통과
- 필요한 선행 Task complete
- archive/superseded 문서를 active SOT로 사용하지 않음

Implementation Readiness가 `NOT READY`이면 구현 금지다.

## 판정 출력 형식

Readiness 결과는 구현 전 다음 형식으로 보고한다.

```text
Readiness Check
Product Readiness: READY / NOT READY
- 근거:
- 부족한 결정:
Interaction Design Check:
- 결론: 상호작용 설계 가능 / 상호작용 설계 보류 / 해당 없음
- 부족한 결정:
Frontend UX Check:
- 결론: FRONTEND_UX_ALLOWED / FRONTEND_UX_BLOCKED / 해당 없음
- 부족한 결정:
Engineering Readiness: READY / NOT READY
- 근거:
- 부족한 결정:
Operational Quality Check:
- 결론: 설계 가능 / 설계 보류 / 해당 없음
- 부족한 결정:
Implementation Readiness: READY / NOT READY
- 근거:
- 구현 가능 여부:
Conclusion:
- IMPLEMENTATION_ALLOWED / IMPLEMENTATION_BLOCKED
- 필요한 다음 행동:
```

`IMPLEMENTATION_ALLOWED`는 Product Readiness, Engineering Readiness, Implementation Readiness가 모두 `READY`일 때만 사용한다.

## Missing Context 분리

Readiness가 `NOT READY`이면 구현하지 말고 `_missing-context.md`로 돌아간다. 질문은 다음 범주로 분리한다.

- Product Missing Context
- Engineering Missing Context
- Implementation Missing Context

Product Missing Context 예: 이 기능의 사용자는 누구인가?

Engineering Missing Context 예: 이 상태는 DB에 저장되는가, 계산되는가?

Implementation Missing Context 예: 이번 Task에서 public API 변경이 허용되는가?

## 문서 타입 후보

필요한 문서 타입을 다음 후보에서 식별한다.

```text
PROJECT_CONTEXT
PROJECT_BRIEF
PRODUCT_REQUIREMENT
USER_SCENARIO
DOMAIN
BEHAVIOR
SYSTEM_ARCHITECTURE
API_CONTRACT
DATA_MODEL
FRONTEND_ARCHITECTURE
FRONTEND_UX_CRITERIA
DESIGN_SYSTEM
UI_PATTERN
USER_FLOW
INTERACTION_SPEC
IMPLEMENTATION_ARCHITECTURE
ARCHITECTURE_POLICY
MIGRATION_POLICY
JOB_SPEC
BROKER_INTEGRATION
EXTERNAL_REFERENCE
DECISION_LOG
TEST_STRATEGY
OPERATION
ERROR_POLICY
INTEGRATION_POLICY
BATCH_OPERATION_POLICY
INFRA_POLICY
DEPENDENCY_POLICY
```

## 수행 절차

1. Project Context가 있는지 확인한다.
2. Project Context가 없거나 프로젝트 성격이 불명확하면 Missing Context로 질문한다.
3. Project Context의 projectType, productionIntent, risk, allowedSimplifications, forbiddenSimplifications를 읽는다.
4. Goal을 구현 가능한 작업 영역으로 나눈다.
5. 각 작업 영역에 필요한 문서 타입을 식별한다.
6. Goal 또는 예상 Task가 사용자/운영자 interaction surface, DB, migration, repository, API, status/state, test, external integration, batch, infra, config를 포함하는지 확인한다.
7. 사용자 또는 운영자가 접하는 기능이면 상호작용 방식 확인을 수행한다.
8. 웹/모바일 UI 작업이면 프론트엔드 UX 확인을 수행한다.
9. DB table, column, migration, repository, API DTO가 필요하면 Storage Intent Check를 수행한다.
10. API path, method, route, controller, request/response shape가 필요하면 Behavior Contract Check를 수행한다.
11. status enum, status column, state transition이 필요하면 State Meaning Check를 수행한다.
12. 성능, 보안, 운영, 데이터 조회, 권한, 실패 처리, 로그/감사 판단이 필요하면 운영/품질 기준 확인을 수행한다.
13. 구현 중 발견 가능한 성능 위험 후보를 다룰 작업이면 성능 위험 조사 범위와 허용된 수정 범위를 확인한다.
14. Git 작업이 필요하면 버전관리 확인을 수행한다.
15. 버그리포트 작업이 필요하면 버그리포트 확인을 수행한다.
16. 관련 cross-cutting policy domain을 자동 식별한다.
17. `document-registry.yml`이 있으면 등록된 문서의 `type`, `status`, `owns`, `requiredFor`, `keywords`를 확인한다.
18. registry가 없으면 필요한 문서 타입을 추론하되, registry 부재를 readiness 결과에 기록한다.
19. 필요한 문서가 APPROVED 상태인지 확인한다.
20. DRAFT 또는 DEPRECATED 문서는 readiness 충족 근거로 사용하지 않는다.
21. 문서가 존재해도 구현 판단에 필요한 정책이 비어 있으면 부족하다고 판단한다.
22. 사용할 artifact가 있으면 생성 단계, 승인, dependency, documentCoverage, source of truth validation, superseded 여부를 확인한다.
23. legitimacy check를 통과하지 못한 artifact가 있으면 INVALID/QUARANTINED/SUPERSEDED 후보로 보고한다.
24. 현재 기준으로 읽을 문서, 과거 기록으로만 볼 문서, 보조 자료로만 볼 문서를 분류한다.
25. 현재 기준과 과거 기록 또는 보조 자료가 충돌하면 `READY_FOR_PLANNING`을 선언하지 않고 정합성 정리 질문으로 돌아간다.
26. 기본 읽기 경로의 문서 크기와 hot path 여부를 확인하고 분리 후보, 유지 후보, README/index 갱신 필요 여부를 기록한다.
27. 현재 작업 포인터와 기본 읽기 경로 계약이 있는지 확인한다. 없거나 불완전해 과거 기록까지 읽어야 하면 정합성 정리 질문으로 돌아간다.
28. source of truth 변경 요청이 있으면 영향받는 문서, Task Contract, prompt, verification result를 식별한다.
29. known conflict가 남는 partial source of truth update라면 Missing Context 또는 Source of Truth Change Request blocker로 보고한다.
30. Product Readiness와 Engineering Readiness를 판정한다.
31. Task Contract, SOT Packet, 승인 상태가 있으면 Implementation Readiness도 판정한다.
32. 부족한 항목이 있으면 Product/Engineering/Implementation Missing Context로 분리한 Missing Context Report를 만든다.
33. Product Readiness와 Engineering Readiness가 모두 `READY`이면 `READY_FOR_PLANNING`을 선언할 수 있다.

Readiness는 도메인/API 문서만 확인하면 안 된다. Goal 또는 Task가 DB, migration, repository, test, external integration, batch, infra, config를 포함하면 관련 cross-cutting policy를 반드시 점검한다.

## Cross-Cutting Policy 자동 식별

Readiness Agent는 Goal 표현, 예상 Task 유형, 필요한 파일 범위를 보고 다음 policy domain을 자동 식별한다.

- 사용자 또는 운영자가 접하는 기능이면 USER_SCENARIO, BEHAVIOR, PRODUCT_REQUIREMENT 또는 동등한 제품 기준 문서에 상호작용 방식이 필요하다.
- 웹/모바일 UI이면 USER_SCENARIO, PRODUCT_REQUIREMENT, FRONTEND_UX_CRITERIA, USER_FLOW 또는 INTERACTION_SPEC, DESIGN_SYSTEM 또는 UI_PATTERN, FRONTEND_ARCHITECTURE 역할이 승인 문서 안에 필요하다.
- route, page, component, layout, styling, motion, visual QA가 있으면 승인 문서 안에 FRONTEND_UX_CRITERIA와 FRONTEND_ARCHITECTURE 역할이 필요하다.
- 웹/모바일 UI 구현이면 승인 문서 안의 FRONTEND_UX_CRITERIA 또는 동등한 역할에 UI 구현 계약이 필요하다.
- 디자인 시스템, 화면 패턴, 색상/타이포그래피/간격, component variant, motion 기준이 필요하면 승인 문서 안에 DESIGN_SYSTEM 또는 UI_PATTERN 역할이 필요하다.
- 역할은 별도 파일로 분리되어도 되고, 프로젝트가 승인한 루트 `DESIGN.md` 같은 단일 기준 문서 안에 명확한 섹션, metadata, `owns`로 기록되어도 된다. CDD는 `docs/design-system/*`나 `docs/ui-ux/*` 같은 경로를 강제하지 않는다.
- Repository/Flyway/DB migration이 있으면 TEST_STRATEGY와 MIGRATION_POLICY가 필요하다.
- DB schema, entity, repository가 있으면 DATA_MODEL, DB/Persistence policy, Storage Intent Check가 필요하다.
- API endpoint, DTO, controller가 있으면 API_CONTRACT, ERROR_POLICY, Behavior Contract Check가 필요하다.
- status enum, status column, state transition이 있으면 BEHAVIOR, DATA_MODEL 또는 DECISION_LOG, State Meaning Check가 필요하다.
- 성능, 조회, 권한, 보안, 실패 처리, 로그/감사, 운영 기준이 있으면 ARCHITECTURE_POLICY, OPERATION, ERROR_POLICY, TEST_STRATEGY 또는 동등한 승인 문서가 필요하다.
- 성능 위험 후보를 구현 범위로 다루려면 ARCHITECTURE_POLICY, OPERATION, TEST_STRATEGY 또는 작업 기준서에 조사 범위, 근거 기준, 허용된 수정 범위가 필요하다.
- 외부 API 연동이 있으면 INTEGRATION_POLICY가 필요하다.
- 배치가 있으면 BATCH_OPERATION_POLICY가 필요하다.
- profile, config, Docker/local runtime, env var가 있으면 INFRA_POLICY 또는 OPERATION 문서가 필요하다.
- 테스트 요구사항이 있으면 TEST_STRATEGY 문서가 필요하다.
- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library가 필요하면 DEPENDENCY_POLICY 또는 명시적 APPROVED 결정이 필요하다.

필요한 cross-cutting policy가 없으면 READY_FOR_PLANNING을 선언하지 않는다.

## Project Context 기반 조정

Readiness Agent는 Project Context를 기준으로 필요한 문서와 질문 강도를 조정한다.

- `PRACTICE_PROJECT`: 실서비스 운영 요구를 과도하게 요구하지 않는다. 대신 학습, 설계 품질, 구현 품질, 핵심 도메인 정책을 확인한다.
- `TEST_BED`: 사용자가 명시적으로 시스템/도구/기술 가정을 검증하는 테스트 베드라고 말한 경우에만 적용한다. 하네스 평가 목적은 Project Context가 아니라 별도 harness operation artifact로 분리한다.
- `LOCAL_EXPERIMENT` 또는 `PERSONAL_TOOL`: 복잡한 운영 인프라, 고가용성, 상용 관측성 정책을 기본 요구하지 않는다.
- `PRODUCTION_SERVICE`: 운영, 보안, 배포, 장애 대응, 관측성, 데이터 보존 정책을 Missing Context 후보로 본다.
- `HIGH_CONSISTENCY_DOMAIN`: 데이터 정합성, 기록 보존 정책, idempotency, auditability, duplicate event policy를 강하게 점검한다.
- `HIGH_TRAFFIC_SERVICE`: 성능, 확장성, 비동기 처리, 캐시, 큐, backpressure 정책을 Missing Context 후보로 본다.
- `INTERNAL_BACKOFFICE` 또는 `INTERNAL_OPERATION_TOOL`: 권한, 변경 이력, 검색/필터, 엑셀 export/import, 운영 UX를 Missing Context 후보로 본다.
- `PUBLIC_USER_SERVICE`: 외부 사용자 보안, validation, abuse 방지, 개인정보 노출 가능성을 Missing Context 후보로 본다.

## 판단 질문

Readiness Agent는 최소한 다음 질문에 답해야 한다.

- 이 목표를 Task로 쪼갤 수 있는가?
- 각 Task의 acceptance criteria를 만들 수 있는가?
- 테스트 요구사항을 만들 수 있는가?
- 도메인/아키텍처/행위 정책을 AI가 임의로 결정해야 하는 부분이 있는가?
- 필수 문서가 없거나 DRAFT 상태인가?
- 문서가 있어도 필요한 validation, error format, state transition, persistence, external integration 정책이 비어 있는가?
- 사용자 또는 운영자가 이 기능을 어디서 발견하거나 실행하는가?
- 사용자는 무엇을 입력하고 무엇을 출력으로 받는가?
- 실패, 빈 상태, 권한 없음, 처리 중 피드백이 정해져 있는가?
- 웹/모바일 UI라면 화면 상태, 정보 우선순위, 주요 행동, 반응형 기준, 접근성, 텍스트 overflow, 시각 검증 방법이 정해져 있는가?
- 웹/모바일 UI라면 이 기준이 승인 문서 안의 FRONTEND_UX_CRITERIA, FRONTEND_ARCHITECTURE, DESIGN_SYSTEM 또는 UI_PATTERN, USER_FLOW 또는 INTERACTION_SPEC 역할로 기록되어 있는가?
- 분석 결과가 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저/스크린샷 검증 기준으로 고정되어 있는가?
- 저장하려는 것, 저장 이유, 나중에 읽는 방식, 저장하지 않을 것이 정해져 있는가?
- 동작 계약 없이 API path나 request/response shape를 정하려는 것은 아닌가?
- 상태 의미 없이 status enum이나 상태 전이를 정하려는 것은 아닌가?
- 예상 데이터 양, 조회 방식, 정렬/검색/페이지 처리, 응답 속도 기대치가 정해져 있는가?
- 성능 위험 후보를 구현 중 발견했을 때 제안으로 남길지, 승인된 범위 안에서 수정할지 정해져 있는가?
- 성능 위험 판단 근거가 profiling, query plan, benchmark, production metric, 테스트 재현 중 무엇인지 정해져 있는가?
- Git 작업이면 포함할 변경, 제외할 변경, stage 방식, commit grouping, push 대상, history rewrite 위험, recovery path가 정해져 있는가?
- 버그리포트 작업이면 대상 tracker, 재현 절차, 실제/기대 결과, 환경, 영향도, 증거, 비밀정보 제거 기준이 정해져 있는가?
- 권한 검증, 민감 정보 노출, 재시도, 멱등성, 로그/감사 기준이 정해져 있는가?
- DB 통합 테스트를 어떤 방식으로 수행할 것인가?
- 테스트 DB는 운영 DB와 같은 제품/방언을 사용하는가?
- Testcontainers를 사용할 것인가?
- H2 같은 대체 DB를 사용할 것인가?
- 운영 migration과 테스트 migration을 동일하게 사용할 것인가?
- 테스트 전용 migration을 허용할 것인가?
- application-test.yml 또는 test profile 분리를 허용할 것인가?
- Repository 테스트는 통합 테스트로 할 것인가, 후속 Task로 미룰 것인가?
- 외부 의존성은 mock/fake/stub 중 무엇을 사용할 것인가?

## 필수 정책 점검 항목

Readiness 단계에서는 다음 정책이 필요한 작업인지 확인하고, 필요하다면 APPROVED 문서에 정의되어 있는지 검증한다.

### 사용자/운영자 상호작용 관련

- 사용자 또는 운영자가 접하는 기능인가?
- 이 기능을 사용하는 사람은 누구인가?
- 사용자는 어디서 이 기능을 발견하거나 실행하는가?
- 사용자는 무엇을 보고 시작하는가?
- 사용자는 무엇을 입력하는가?
- 사용자는 어떤 행동을 하는가?
- 성공하면 무엇을 보여주거나 반환하는가?
- 실패하면 무엇을 보여주거나 반환하는가?
- 데이터가 없을 때 무엇을 보여주거나 반환하는가?
- 권한이 없거나 접근할 수 없을 때 어떻게 반응하는가?
- 처리 중이거나 대기 중일 때 어떤 피드백을 주는가?
- 사용자가 반드시 이해해야 하는 문구나 결과가 정의되어 있는가?
- 상호작용 방식이 비어 있는데 저장 구조, API, 화면, CLI 명령, 배치 실행 방식을 먼저 만들고 있지 않은가?

### Frontend UI/UX 관련

- 웹/모바일 UI 작업인가?
- `USER_FLOW` 또는 `INTERACTION_SPEC`가 사용자 발견 경로, 시작 맥락, 입력, 행동, 성공/실패/빈 상태/권한 없음/처리 중 결과를 소유하는가?
- `FRONTEND_UX_CRITERIA`가 화면 상태, 정보 우선순위, primary action, 반응형, 접근성, text overflow, visual QA 기준을 소유하는가?
- `FRONTEND_UX_CRITERIA`가 UI 구현 계약을 소유하는가?
- `DESIGN_SYSTEM` 또는 `UI_PATTERN`이 색상, 타이포그래피, 간격, component pattern, motion 같은 시각 일관성 기준을 소유하는가?
- `FRONTEND_ARCHITECTURE`가 route/page/component/state/data loading/test boundary 같은 구현 구조만 소유하고, 제품 흐름이나 시각 정책을 대신 정하지 않는가?
- 위 역할이 별도 파일이 아니라 루트 `DESIGN.md` 같은 단일 승인 문서 안에 있다면, 각 역할의 경계가 명확한 섹션, metadata, `owns`로 구분되는가?
- 기존 디자인 시스템 또는 따라야 할 화면 패턴이 정의되어 있는가?
- 화면의 정보 우선순위와 primary action이 정의되어 있는가?
- 기본, 로딩, 빈 상태, 오류, 권한 없음, 성공 상태가 정의되어 있는가?
- 반응형 기준과 최소 지원 viewport가 정의되어 있는가?
- keyboard/focus, label, 접근성 기준이 정의되어 있는가?
- 긴 문구, 숫자, CJK, overflow 처리 기준이 정의되어 있는가?
- visual QA 방식이 정의되어 있는가?
- 브라우저/스크린샷 검증 기준이 UI 구현 계약에 연결되어 있는가?
- 프론트엔드 UX 확인이 없는데 route, page, component, layout, styling, motion, visual QA acceptance criteria를 먼저 만들고 있지 않은가?
- 승인 문서 안의 FRONTEND_UX_CRITERIA, DESIGN_SYSTEM 또는 UI_PATTERN, USER_FLOW 또는 INTERACTION_SPEC, FRONTEND_ARCHITECTURE 역할 coverage 없이 UI 구현 기준을 Task나 prompt에 넣고 있지 않은가?
- UI 구현 계약 없이 컴포넌트별 수정 목록만으로 Task나 prompt를 만들고 있지 않은가?

### DB / Persistence 관련

- Storage Intent Check가 `DB_DESIGN_ALLOWED`인가?
- 무엇을 저장하는지 정의되어 있는가?
- 왜 저장하는지 정의되어 있는가?
- 사용자가 나중에 어떻게 다시 읽거나 활용하는지 정의되어 있는가?
- 무엇은 저장하지 않을지 정의되어 있는가?
- 구조화할 것과 자유 텍스트로 둘 것이 구분되어 있는가?
- 수정/삭제/보존 정책이 정의되어 있는가?
- 소유권과 범위가 정의되어 있는가?
- 식별자 타입과 생성 전략이 정의되어 있는가?
- primary key generation strategy가 정의되어 있는가?
- migration strategy가 정의되어 있는가?
- constraint/index policy가 정의되어 있는가?
- nullable/default policy가 정의되어 있는가?
- timestamp/timezone policy가 정의되어 있는가?
- test database strategy가 정의되어 있는가?
- production migration과 test migration의 관계가 정의되어 있는가?

### Test Strategy 관련

- 테스트 DB 선택이 정의되어 있는가? PostgreSQL, Testcontainers, H2, 별도 테스트 DB, 또는 DB 통합 테스트 제외 중 무엇인가?
- test profile 사용 여부가 정의되어 있는가?
- application-test.yml 허용 여부가 정의되어 있는가?
- test-specific migration 허용 여부가 정의되어 있는가?
- mock/fake/stub 전략이 정의되어 있는가?
- 운영 DB dialect 대체 허용 여부가 정의되어 있는가?
- 테스트에서 외부 의존성을 어떻게 대체할지 정의되어 있는가?

### API 관련

- Behavior Contract Check가 `API_DESIGN_ALLOWED`인가?
- API path를 정하기 전에 사용자가 기대하는 동작과 성공/실패 결과가 정의되어 있는가?
- status code 정책이 정의되어 있는가?
- error response format이 정의되어 있는가?
- error code 정책이 정의되어 있는가?
- validation policy가 정의되어 있는가?
- serialization format이 정의되어 있는가?
- date/time format이 정의되어 있는가?
- path variable / response field type이 정의되어 있는가?

### State / Status 관련

- State Meaning Check가 `STATE_MODEL_ALLOWED`인가?
- 각 상태가 제품 관점에서 무엇을 의미하는지 정의되어 있는가?
- 어떤 사건이 상태를 바꾸는지 정의되어 있는가?
- 각 상태에서 허용되는 행동이 정의되어 있는가?
- 상태를 저장할지 계산할지 정의되어 있는가?
- 상태를 외부에 노출할지 정의되어 있는가?

### External Integration 관련

- timeout 정책이 정의되어 있는가?
- retry/backoff 정책이 정의되어 있는가?
- fallback 정책이 정의되어 있는가?
- rate limit 정책이 정의되어 있는가?
- error mapping 정책이 정의되어 있는가?
- source priority가 정의되어 있는가?
- cache TTL이 정의되어 있는가?

### Batch 관련

- idempotency가 정의되어 있는가?
- restartability가 정의되어 있는가?
- chunk size가 정의되어 있는가?
- retry/skip policy가 정의되어 있는가?
- source/target boundary가 정의되어 있는가?
- staging/publish boundary가 정의되어 있는가?
- cross-database/schema boundary가 정의되어 있는가?

### Operation/Infra 관련

- 운영/품질 기준 확인 결론이 `설계 가능`인가?
- 예상 데이터 양이 정의되어 있는가?
- 목록이나 조회가 있다면 정렬, 검색, 페이지 처리가 필요한지 정의되어 있는가?
- 사용자가 기대하는 응답 속도가 정의되어 있는가?
- 성능 위험 조사 범위와 허용된 수정 범위가 정의되어 있는가?
- 성능 위험 후보를 증거 없이 구현 범위로 승격하지 않도록 금지 범위가 정의되어 있는가?
- 권한 검증 위치와 방식이 정의되어 있는가?
- 민감 정보나 외부 연동 정보 노출 위험이 검토되어 있는가?
- 실패 시 사용자가 알아야 하는 정보가 정의되어 있는가?
- 서버/클라이언트/작업 실행 환경 중 어디에서 검증해야 하는지 정의되어 있는가?
- 재시도, 중복 실행 방지, 멱등성이 필요한지 정의되어 있는가?
- 로그나 감사 기록 필요 여부가 정의되어 있는가?
- profile strategy가 정의되어 있는가?
- environment variable naming이 정의되어 있는가?
- logging format이 정의되어 있는가?
- health check가 정의되어 있는가?
- Docker/local runtime policy가 정의되어 있는가?

### Dependency / Build Tool 관련

- 새 dependency 추가가 승인되어 있는가?
- Gradle plugin 추가가 승인되어 있는가?
- annotation processor 추가가 승인되어 있는가?
- code generation tool 도입이 승인되어 있는가?
- runtime-exposed library 도입이 승인되어 있는가?
- 승인 문서가 없을 때 기존 스택 안에서 구현하는 대안이 가능한가?
- dependency를 추가하지 않는 기본 대안이 Task 범위와 testRequirements를 충족하는가?
- dependency가 필요하지만 승인 문서가 없으면 사용자에게 목적, 범위, 대안, 영향, 검증 방법을 보고하고 승인 여부를 묻는가?
- 기존 스택만으로 Task 범위와 검증 기준을 충족할 수 없는데도 "dependency 금지"를 이유로 부정확한 구현을 강행하지 않는가?

Identifier type, key generation, API-visible id representation은 구현 세부사항이 아니라 문서화되어야 할 정책이다. 이 정책은 DATA_MODEL, API_CONTRACT, ARCHITECTURE_POLICY 또는 DECISION_LOG 문서에 의해 승인되어야 한다.

Storage Intent Check, Behavior Contract Check, State Meaning Check는 구현 세부사항이 아니라 문서화되어야 할 정책 판단이다. 이 check가 `*_BLOCKED`이면 table, column, migration, repository, API DTO, API path, status enum을 제안하지 말고 Missing Context로 돌아간다.

상호작용 방식 확인과 운영/품질 기준 확인도 구현 세부사항이 아니라 문서화되어야 할 제품/설계 판단이다. 이 결정이 비어 있으면 화면, CLI 명령, batch 실행 방식, API surface, 저장 구조, 성능/보안/운영 정책을 임의로 정하지 말고 Missing Context로 돌아간다.

테스트 DB, 테스트 profile, test migration, Testcontainers, H2, mock/fake/stub 정책이 문서화되어 있지 않으면 Implementation Agent가 임의로 선택하면 안 된다.

Do not classify test database choice, test profile strategy, test-specific migrations, Testcontainers, H2, mock/fake/stub strategy, or database dialect substitution as implementation details. They require approved source-of-truth decisions.

테스트 DB 선택, 테스트 profile 전략, 테스트 전용 migration, Testcontainers, H2, mock/fake/stub 전략, DB dialect 대체는 구현 세부사항으로 분류하지 마라. 승인된 source of truth 결정이 필요한 정책이다.

새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library는 구현 세부사항으로 분류하지 마라. 승인된 source of truth 결정 또는 현재 작업의 명시적 approval record가 필요한 정책이다. 승인 문서가 없으면 기존 스택 안에서 구현하는 것이 기본 대안이다. 단, 기존 스택으로 Task 범위와 testRequirements를 충족할 수 없으면 dependency 승인 질문으로 돌아간다.

## 결과 상태

### READY_FOR_PLANNING

다음이 모두 만족될 때만 선언한다.

- Project Context가 존재하고 프로젝트 성격, 운영 전제, risk, 단순화 경계가 충분히 정의되어 있다.
- Product Readiness가 `READY`다.
- Engineering Readiness가 `READY`다.
- 필요한 문서가 APPROVED 상태다.
- 문서가 Goal 수행에 필요한 도메인/아키텍처/행위/정책 판단을 커버한다.
- acceptance criteria와 testRequirements를 문서 근거로 만들 수 있다.
- AI가 문서 밖 판단을 하지 않아도 Plan/Task를 생성할 수 있다.
- source of truth 문서와 Task Contract 사이 known conflict가 없다.
- 현재 기준과 과거 completion/verification/task/prompt 사이 known conflict가 없다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference를 active 기준으로 사용하지 않았다.
- 기본 읽기 경로의 문서 크기와 분리 후보가 보고되었다.
- 현재 작업 포인터와 기본 읽기 경로 계약으로 이번 작업에 필요한 최소 읽기 문서를 식별할 수 있다.
- Git 작업이면 버전관리 계약이 준비되었다.
- 버그리포트 작업이면 버그리포트 계약이 준비되었다.
- 필요한 artifact가 legitimacy check를 통과했다.

### BLOCKED_BY_MISSING_CONTEXT

다음 중 하나라도 있으면 선언한다.

- Project Context가 없다.
- Product Readiness가 `NOT READY`다.
- Engineering Readiness가 `NOT READY`다.
- Implementation Readiness가 구현 단계에서 `NOT READY`다.
- 프로젝트 목적, 성격, 사용자, 운영 전제, 데이터 정합성 중요도, 보안/권한 요구, 테스트 강도, 단순화 경계가 불명확하다.
- 필수 문서가 없다.
- 필수 문서가 DRAFT 또는 DEPRECATED 상태다.
- 필요한 정책이 문서에 없다.
- 사용자 또는 운영자가 접하는 기능인데 상호작용 방식, 입력, 출력, 실패, 빈 상태, 권한, 처리 중 피드백이 없다.
- 상호작용 방식이 비어 있는데 저장 구조, API, 화면, CLI 명령, 배치 실행 방식을 정해야 한다.
- 웹/모바일 UI 작업인데 승인 문서 안의 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage가 없다.
- 웹/모바일 UI 작업인데 화면 상태, 정보 구조, 접근성, 반응형 동작, visual QA 기준을 문서 근거 없이 정해야 한다.
- 웹/모바일 UI 작업인데 UI 구현 계약 없이 분석 방향을 바로 구현으로 넘겨야 한다.
- 운영/품질 기준이 없는데 성능, 보안, 권한, 조회, 재시도, 로그/감사, 실패 처리 판단이 필요하다.
- Storage Intent Check가 없거나 `DB_DESIGN_BLOCKED`인데 DB table, column, migration, repository, API DTO가 필요하다.
- Behavior Contract Check가 없거나 `API_DESIGN_BLOCKED`인데 API path, method, route, controller, request/response shape가 필요하다.
- State Meaning Check가 없거나 `STATE_MODEL_BLOCKED`인데 status enum, status column, state transition이 필요하다.
- identifier type, key generation, API-visible id representation이 필요한데 문서에 없다.
- DB/Repository/Flyway/Migration 테스트 전략이 필요한데 TEST_STRATEGY, DATA_MODEL, MIGRATION_POLICY, IMPLEMENTATION_ARCHITECTURE 문서에 없다.
- 필요한 cross-cutting policy domain이 식별되었지만 APPROVED source of truth 문서가 없다.
- Repository/Flyway testRequirements를 만들 수 있지만 테스트 DB/profile/migration 전략이 없다.
- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library가 필요하지만 승인 문서가 없다.
- 사용자 Goal이 기존 source of truth와 충돌한다.
- 사용자 지정 scope가 source of truth 정합성을 깨뜨린다.
- partial source of truth update 후 known conflict가 남는다.
- 필요한 artifact가 디스크에 존재하지만 생성 근거나 현재 gate 충족 여부를 확인할 수 없다.
- artifact가 invalid/quarantined/superseded 후보이다.
- Task 분해를 하려면 AI가 금지된 판단을 해야 한다.

## Missing Context 예시

```text
Missing Decision: Test database strategy is not defined.

Reason:
TASK-001 includes Repository/Flyway tests. Implementation Agent cannot choose H2, PostgreSQL, Testcontainers, or test migration strategy without approved source of truth.

Options:
A. Use PostgreSQL/Testcontainers
B. Use separate local PostgreSQL test DB
C. Defer DB integration tests and only run build/context tests for TASK-001
D. Use H2 with explicit approval and documented dialect divergence

Recommended:
C for lightweight first harness validation, or A if DB fidelity is required.
```

```text
Missing Decision: Dependency addition is not approved.

Reason:
The task appears to require a new library or build tool change. Implementation Agent cannot add a dependency, plugin, annotation processor, or code generation tool without an approved decision. If the dependency is necessary, report the purpose, scope, alternatives, impact, and verification plan before asking for approval.

Options:
A. Approve the named dependency and document its purpose/scope/impact
B. Implement within the existing stack
C. Defer the feature that requires the dependency

Recommended:
B only if the existing stack can satisfy the task and verification requirements. A if the dependency is required by product, architecture, or test strategy.
```

## 다음 단계

- `READY_FOR_PLANNING`: `plan-task.md`로 이동한다.
- `BLOCKED_BY_MISSING_CONTEXT`: `_missing-context.md`로 이동한다.

## Missing Context 정지 규칙

Readiness가 Missing Context를 발견하면 그 시점의 허용 행동은 Missing Context Report 작성과 사용자 질문뿐이다.

- 코드를 수정하지 않는다.
- source of truth 문서를 수정하지 않는다.
- document registry를 수정하지 않는다.
- revision을 실행하지 않는다.
- 테스트 전략을 변경하지 않는다.
- Task Contract를 수정하지 않는다.
- prompt 또는 verification result를 수정하지 않는다.
- complete로 진행하지 않는다.
- TEST_STRATEGY / MIGRATION_POLICY / FRONTEND_UX_CRITERIA / DESIGN_SYSTEM / UI_PATTERN / USER_FLOW / INTERACTION_SPEC / FRONTEND_ARCHITECTURE 같은 정책 문서 DRAFT를 사용자 답변 없이 생성하지 않는다.

정상 흐름:

```text
Readiness detects Missing Context
→ stop
→ ask user
→ user decides policy
→ Source of Truth Manager uses document-supplement to propose DRAFT based on user answer
→ user approves source of truth
→ planning/task update if needed
```
