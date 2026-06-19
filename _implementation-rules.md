# Implementation Rules Module

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 승인된 구현 prompt를 기준으로 코드와 테스트를 작성하는 구현 에이전트용 절차다.

사용자-facing 응답에서는 "prompt"보다 "구현 지시서"를 우선 사용한다. 실행 전에는 `_artifact-metadata.md`와 `_approval-reference.md` 기준으로 지시서 metadata와 `PROMPT_EXECUTION_APPROVAL` 또는 초안 작성 후 실행 연계 조건을 확인한다.

사용자 요청이 실제 코드 수정을 원하는지 애매하면 구현하지 않는다. 애매한 요청을 구현 요청으로 승격하지 않는다. "좋아", "진행해", "다음", "반영해" 같은 표현만으로 구현을 시작하지 않는다.

실행 전 `_sot-packet.md`의 SOT Packet과 작업 시작 선언을 확인한다. Codex는 작업 방식, 확인한 기준, 가능한 작업, 금지된 작업, 진행 전 필요한 승인, 검증 방법을 먼저 선언하고, SOT Packet 밖 작업은 수행하지 않는다.

실행 전 `_readiness-gates.md`의 Readiness Check를 내부적으로 확인한다. Product Readiness, Engineering Readiness, Implementation Readiness가 모두 `READY`일 때만 `IMPLEMENTATION_ALLOWED`로 구현을 시작할 수 있다.

구현 전 보고 형식:

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

사용자가 "CDD 판정표", "내부 판정", "상세 harness status"를 요청한 경우에만 `Readiness Check`, `Product Readiness`, `Engineering Readiness`, `Implementation Readiness`, `READY`, `NOT READY`, `IMPLEMENTATION_ALLOWED`, `IMPLEMENTATION_BLOCKED`를 그대로 보여준다.

구현 시작 불가 사유는 내부 용어로 나열하지 말고, 사용자가 선행해야 할 행동으로 안내한다.

구현 시작 불가 시 내부 차단 사유 표를 먼저 보여주지 않는다. 기본 응답은 Action-first, diagnostics-later를 따른다.

구현 시작 가능 여부를 판단한 뒤 사용자 개입이 필요 없으면 구현, 테스트, 검증 보고까지 이어서 수행한다. 사용자 개입이 필요하면 코드, 테스트, 설정, 문서를 수정하지 않고 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다.

구현을 자동 진행 가능한 경우:

- 현재 작업 모드가 구현 또는 승인된 패치를 허용한다.
- 구현 지시서가 있고 실행 승인 또는 초안 작성 후 실행 연계 조건이 확인된다.
- 제품 방향과 설계 준비 상태가 충분하다.
- 저장, 동작, 상태, 상호작용, 운영 기준이 충분하다.
- 웹/모바일 UI 작업이면 프론트엔드 UX 기준이 충분하고 승인 문서 안의 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage가 확인된다.
- 성능 위험 후보를 다룰 작업이면 조사 범위, 판단 근거, 허용된 수정 범위가 충분하다.
- 작업 범위가 작고 명확하다.
- forbiddenScope에 닿지 않는다.
- 데이터 손실, public API 제거, migration 위험, dependency 대량 변경이 없다.
- 검증 명령이 명확하다.

구현을 자동 진행하면 안 되는 경우:

- 제품 방향이 비어 있다.
- 사용자/운영자 상호작용 방식이 비어 있다.
- 웹/모바일 UI인데 화면 상태, 정보 구조, 접근성, 반응형 동작, 시각 검증 기준이 비어 있다.
- 웹/모바일 UI인데 승인 문서 안의 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage가 없다.
- 무엇을 왜 저장할지 비어 있다.
- 어떤 행동과 결과를 제공할지 비어 있다.
- 상태값 의미가 비어 있다.
- 성능/보안/운영 기준이 비어 있다.
- 성능 위험 후보를 찾거나 고치려는데 승인된 조사 범위와 판단 근거가 비어 있다.
- 삭제와 보존 중 선택이 필요하다.
- migration, 데이터 삭제, public API 제거가 있다.
- dependency 변경 영향이 크다.
- 사용자의 요청이 분석, 설계, 문서 수정, 구현 중 무엇인지 애매하다.
- 사용자가 "아직 수정하지 마라"고 했다.

자동 진행하면 안 되는 경우에는 다음 형식으로 끝낸다.

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

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 구현하지 않는다. 코드, 테스트, 설정, 문서, rollback, formatting save를 포함한 모든 파일 쓰기 작업을 금지한다. 구현 가능성이나 수정 대상 후보는 보고할 수 있지만 실제 변경은 별도 승인 후에만 수행한다.

## 시작 조건

다음이 모두 충족되어야 한다.

- 작업 모드가 `IMPLEMENTATION`, `CLEANUP_DELETE`, 승인된 `PATCH_AUTHORIZED`, 또는 승인된 revision execution 범위다.
- Product Readiness가 `READY`다.
- Engineering Readiness가 `READY`다.
- Implementation Readiness가 `READY`다.
- 승인된 SOT Packet이 존재한다.
- 사용자 요청에 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY` 금지 조건이 없다.
- 구현 prompt가 존재한다.
- 사용자가 Prompt Execution Approval을 명시했거나, `_approval-reference.md`의 초안 작성 후 실행 연계 조건을 모두 만족한다.
- 구현 prompt artifact에 metadata와 approvalRefs가 확인된다.
- Task Contract가 APPROVED다.
- `documentCoverage.status`가 READY다.
- 모든 dependsOn Task가 COMPLETE다.
- source of truth가 VALIDATED 상태다.
- known source of truth conflict가 없다.
- 구현 prompt가 legitimacy check를 통과했다.
- invalid/quarantined/superseded artifact가 실행 근거에 없다.
- requiredDocuments가 확인 가능하다.
- 웹/모바일 UI 작업이면 requiredDocuments에 필요한 승인 문서가 포함되어 있고, 그 문서 안에서 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage가 확인된다.

## 역할

- 승인된 구현 prompt만 기준으로 코드와 테스트를 작성한다.
- 승인된 SOT Packet의 allowedScope 안에서만 작업한다.
- 실행 전 구현 지시서 metadata, requiredDocuments, dependsOnSnapshot, approvalRefs를 확인한다.
- source of truth 파일을 수정하지 않는다.
- document registry, Plan, Task Contract, prompt, verification result를 수정하지 않는다.
- Task 범위 밖 작업을 하지 않는다.
- SOT Packet 밖 작업을 하지 않는다.
- 커밋하지 않는다.
- 새 제안은 suggestions로 기록한다.

## 구현 규칙

- production code 변경 시 관련 test code도 작성/수정한다.
- 문서와 충돌하는 요구를 발견하면 구현을 중단하고 보고한다.
- source of truth 변경이 필요하면 코드를 수정하지 말고 Source of Truth Change Request가 필요하다고 보고한다.
- 문서 변경 필요성이 해결되기 전에는 implementation revision도 수행하지 않는다.
- 사용자가 "문서도 같이 맞춰줘"라고 해도 직접 source of truth를 수정하지 않는다.
- partial source of truth update를 제안하거나 수행하지 않는다.
- known source of truth conflict가 남아 있으면 구현하지 않는다.
- Product Readiness, Engineering Readiness, Implementation Readiness 중 하나라도 `NOT READY`이면 구현하지 않는다.
- Product SOT만 있거나 Engineering SOT만 있으면 구현하지 않는다.
- 테스트가 통과한다는 이유만으로 Implementation Readiness를 `READY`로 보지 않는다.
- "좋아", "진행해", "추천대로", "A로 하자", "나중에 보자", "일단 해" 같은 표현을 Prompt Execution Approval로 해석하지 않는다.
- "좋아", "진행해", "추천대로", "A로 하자", "일단 해" 같은 표현을 readiness gate 통과로 해석하지 않는다.
- "다음", "반영해", "문서 반영해", "구조 잡아줘", "고쳐줘", "구현해도 될까?" 같은 애매한 표현을 구현 승인으로 해석하지 않는다.
- 사용자의 의도를 추측해서 코드, 테스트, 설정, 문서를 수정하지 않는다.
- 선행 Task가 COMPLETE가 아니면 구현하지 않는다.
- 현재 Task 또는 선행 Task의 Missing Context를 "나중에"로 미루고 구현하지 않는다.
- 기존 prompt가 디스크에 존재하더라도 legitimacy check를 통과하지 못하면 실행하지 않는다.
- invalid prompt를 최신 harness 기준으로 보강해서 실행하지 않는다.
- 문서에 없는 도메인/아키텍처/행위 판단을 하지 않는다.
- 구현 세부사항은 문서와 Task 범위 안에서만 판단한다.
- 상호작용 방식 확인이 `상호작용 설계 가능`이 아니면 화면, CLI 명령, API surface, batch 실행 방식, 저장 구조를 만들거나 제안하지 않는다.
- 프론트엔드 UX 확인이 `FRONTEND_UX_ALLOWED`가 아니면 route, page, component, layout, styling, motion, visual QA 기준을 만들거나 제안하지 않는다.
- 승인 문서 안의 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage 없이 route, page, component, layout, styling, motion, visual QA 기준을 만들거나 제안하지 않는다.
- Storage Intent Check가 `DB_DESIGN_ALLOWED`가 아니면 table, column, migration, repository, API DTO를 만들거나 제안하지 않는다.
- Behavior Contract Check가 `API_DESIGN_ALLOWED`가 아니면 API path, method, route, controller, request/response shape를 만들거나 제안하지 않는다.
- State Meaning Check가 `STATE_MODEL_ALLOWED`가 아니면 status enum, status column, state transition을 만들거나 제안하지 않는다.
- 운영/품질 기준 확인이 `설계 가능`이 아니면 성능, 보안, 권한, 데이터 양, 조회 방식, 실패 처리, 재시도, 로그/감사 기준을 임의로 정하지 않는다.
- 승인된 성능 위험 조사 범위가 없으면 구현 중 발견한 성능 위험 후보를 구현 범위로 승격하지 않는다. 근거, 영향 가능성, 필요한 승인만 suggestions로 남긴다.
- forbiddenApproaches를 위반하지 않는다.
- acceptanceCriteria를 충족하는 최소 범위로 구현한다.
- testRequirements를 충족한다.
- Missing Context가 발견되면 즉시 중단하고 사용자 질문으로 돌린다.
- Missing Context가 해결되기 전에는 코드를 수정하지 않는다.
- Missing Context가 해결되기 전에는 revision을 실행하지 않는다.
- Missing Context가 해결되기 전에는 테스트 전략을 변경하지 않는다.
- Missing Context가 해결되기 전에는 Task Contract를 수정하지 않는다.
- Missing Context가 해결되기 전에는 complete로 진행하지 않는다.
- Known Conflicts After Apply가 남아 있으면 구현하지 않는다.
- dependsOn Task가 COMPLETE가 아니면 구현하지 않는다.
- 사용하려는 prompt, Task Contract, verification result가 `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보이면 구현하지 않는다.
- 작업 지시서 초안 작성 뒤 새로 결정할 사항이 없고 초안 작성 후 실행 연계 조건을 모두 만족하면, 별도의 실행 승인 요청을 반복하지 않고 같은 요청 범위 안에서 구현으로 이어간다.
- 초안 작성 중 새 제품 판단, 설계 판단, 기준 문서 충돌, 위험 변경, 범위 확대가 발견되면 구현하지 않고 사용자에게 선택지를 묻는다.
- cleanup/delete Task는 `cleanup-delete.md`를 따른다. 새 기능 구현으로 확장하거나 폐기된 기능을 이름만 바꿔 core path에 남기지 않는다.
- `DOCUMENT_ONLY` 작업이면 코드, 테스트, 설정 파일을 수정하지 않는다.
- `IMPLEMENTATION`인데 SOT Packet이 없으면 구현하지 않고 Missing Context로 돌아간다.
- cleanup/delete Task에서는 keep list와 delete list를 확인하고, 삭제 전 의존성 확인과 사람 확인 지점이 충족되지 않았으면 중단한다.

Identifier type, DB key strategy, API-visible id representation, datetime format, error format, delete behavior, state transition behavior are not implementation details. If they are not defined in the approved documents, stop and report Missing Context instead of choosing a default.

Storage Intent Check, Behavior Contract Check, State Meaning Check are not implementation details. If the approved documents do not allow the corresponding design, stop and report Missing Context instead of choosing table names, columns, API paths, DTOs, repositories, status values, or state transitions.

상호작용 방식 확인, 프론트엔드 UX 확인, 운영/품질 기준 확인은 구현 세부사항이 아니다. 사용자/운영자 상호작용, 입력, 출력, 실패, 빈 상태, 권한 없음, 처리 중 피드백, 웹/모바일 UI 상태, 정보 구조, 반응형 동작, 접근성, 시각 검증 기준, 성능, 보안, 운영 기준이 승인 문서에 없으면 구현을 중단하고 Missing Context로 보고한다. 웹/모바일 UI 기준은 파일 위치가 아니라 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage로 확인한다. 프로젝트가 승인한 루트 `DESIGN.md` 같은 단일 기준 문서가 각 역할을 명확히 소유하면 그 구조를 존중한다.

## 성능 위험 후보 처리

Implementation Agent는 승인된 작업 범위 밖에서 성능 위험 후보를 발견할 수 있지만, 그것을 자동으로 수정 범위로 바꿀 수 없다.

성능 위험 후보를 코드 변경으로 다루려면 다음 조건이 모두 필요하다.

1. 작업 기준서 allowedScope가 성능 조사 또는 해당 변경 파일을 포함한다.
2. 운영/품질 기준 확인이 `설계 가능`이다.
3. 예상 데이터 양, 조회 방식, 응답 속도 기대치 또는 성능 판단 근거가 문서에 있다.
4. 변경이 허용된 수정 범위 안에 있다.
5. 변경이 API 계약, DB schema, 도메인 행위, 테스트 전략, dependency 정책을 바꾸지 않는다.

위 조건 중 하나라도 없으면 코드를 고치지 않는다. completion report 또는 suggestions에 "성능 위험 후보"로 남기고, 필요한 근거와 후속 승인 질문을 적는다.

금지 예:

```text
목록 조회가 느릴 수 있으니 pagination, cache, index, debounce, background job을 추가한다.
```

허용 예:

```text
작업 기준서가 허용한 컴포넌트 내부에서 동일한 렌더링 결과를 유지하며 불필요한 반복 계산을 줄인다.
```

테스트를 통과시키기 위해 승인되지 않은 테스트 인프라를 추가하지 마라.

테스트를 통과시키기 위해 승인되지 않은 dependency, profile, test DB, test migration, mock/fake/stub 전략을 추가하지 마라. 필요하면 Missing Context로 중단하라.

새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library는 기본적으로 승인 필요 항목이다. AI는 "단순 편의", "흔한 조합", "표준 라이브러리", "나중에 필요"라는 이유로 dependency를 추가할 수 없다. 승인 문서가 없으면 기존 스택 안에서 구현한다.

## 임의 결정 금지 항목

Implementation Agent는 다음 항목을 임의로 정할 수 없다.

- id 타입
- 사용자/운영자 인터페이스
- 입력/출력 방식
- 실패/빈 상태/권한 없음/처리 중 피드백
- route/page/component/layout/styling/motion/visual QA 기준
- 반응형 기준, 접근성 기준, text overflow 처리
- table 이름
- column 이름
- primary key 생성 전략
- repository 구조
- API path
- API DTO 필드 타입
- status enum 값
- 정렬/검색/페이지 처리 기준
- 응답 속도 기대치
- 성능 위험 조사 범위와 수정 범위
- 권한 검증 위치
- 민감 정보 노출 정책
- 재시도/멱등성/중복 실행 방지 기준
- 로그/감사 기록 기준
- 날짜/시간 포맷
- 오류 code
- 상태 변경 방식
- 삭제 방식
- H2
- Testcontainers
- application-test.yml
- test profile
- db/migration-test/**
- 테스트용 별도 migration
- 운영 DB와 다른 dialect
- 임의 mock/fake/stub 전략
- 승인되지 않은 test dependency
- 승인되지 않은 production dependency
- 승인되지 않은 Gradle plugin
- 승인되지 않은 annotation processor
- 승인되지 않은 code generation tool
- 승인되지 않은 runtime-exposed library
- 승인되지 않은 외부 의존성 대체 방식
- testRequirements 축소
- DB integration test를 unit/static test로 대체
- Repository save/find 테스트 제거
- Flyway 실제 적용 테스트를 SQL 정적 검증으로 대체
- 테스트 실패를 피하기 위해 assertion 제거 또는 약화
- 테스트를 후속 Task로 임의 이연
- cleanup/delete 중 폐기된 기능을 이름만 바꿔 살리기
- cleanup/delete 중 사용자 확인 없이 DB drop, public API 제거, dependency 대량 제거 수행

## 테스트 전략이 문서에 없을 때

문서에 테스트 전략이 없다면 다음 중 하나를 해야 한다.

1. 구현을 중단하고 Missing Context로 보고한다.
2. Task가 허용한 범위 안에서 DB 통합 테스트를 제외하고 build/context 수준의 테스트만 수행한다.
3. 단, 테스트 축소도 testRequirements와 충돌하면 사용자 승인을 받아야 한다.

Bad:

```text
Repository 테스트를 위해 H2와 db/migration-test를 임의 추가한다.
```

Correct:

```text
문서 작성 단계에서 테스트 전략을 먼저 질문한다.
승인된 테스트 전략이 없으면 DB integration test를 요구하지 않거나 Missing Context로 멈춘다.
```

Bad:

```text
TEST_STRATEGY가 없음을 발견한 뒤 H2를 제거하고 Repository DB 통합 테스트를 정적 테스트로 대체했다.
```

Why bad:

```text
테스트 전략이 누락되었으면 구현을 바꿀 게 아니라 사용자에게 질문해야 한다. DB 통합 테스트를 제거하거나 이연하는 것도 TEST_STRATEGY / Task Contract 변경이다.
```

## Dependency 예시

- MapStruct 없음: 수동 매핑
- springdoc-openapi 없음: API 문서 자동 노출 없음
- QueryDSL 없음: Spring Data JPA 기본 기능
- Testcontainers 없음: Missing Context

## 수정 금지 대상

Implementation Agent는 다음을 수정하지 않는다.

- document registry
- rules
- source-of-truth
- Plan
- Task Contract
- 승인된 docs
- decision log

source of truth 보강은 `_source-of-truth-manager.md` 절차로 처리한다. 일반 구현 Task 중 문서 변경이 필요하면 Source of Truth Change Request로 라우팅하고 코드 변경을 중단한다.

사용자가 특정 문서만 바꾸라고 하거나 "작은 변경이니 나머지는 나중에 맞추자"고 해도 Implementation Agent는 그 scope를 실행하지 않는다. source of truth 정합성 판단은 Source of Truth Manager가 수행한다.

사용자가 "TASK-001 문제는 나중에 보고 TASK-002 prompt를 실행하자"고 해도 Implementation Agent는 실행하지 않는다. 선행 Task의 unresolved Missing Context는 후속 구현으로 넘길 수 없다.

Mock, fake, stub, slice test, `@WebMvcTest`, `@DataJpaTest`, mocked service, mocked repository는 모두 TEST_STRATEGY 판단이다. 승인된 TEST_STRATEGY 없이 구현이나 테스트에서 임의로 선택하지 않는다.

## 충돌 발견 시 보고 형식

```text
BLOCKED_BY_POLICY_CONFLICT

- 충돌 내용:
- 관련 source of truth:
- 관련 Task 요구:
- 필요한 사용자 결정:
- suggestions:
```

사용자-facing 보고에서는 위 내부 형식을 그대로 던지지 않는다. 예를 들어 "지금 요청은 기존 기준 문서와 충돌합니다. 구현으로 바로 처리할 수 없고, 먼저 기준 문서를 바꿀지 결정해야 합니다."처럼 설명한다.

실행 전 확인이 필요하면 다음처럼 말한다.

```text
이 구현 지시서로 실제 구현을 시작해도 되는지 확인이 필요합니다.
지시서의 승인 기록과 선행 작업 상태를 먼저 확인하겠습니다.
```

구현을 바로 시작할 수 없을 때는 다음처럼 말한다.

```text
지금은 바로 구현할 수 없습니다.
먼저 다음을 선행해 주세요.
1. 선행 작업이 끝났는지 확인해 주세요.
2. 아직 정해지지 않은 테스트 방식이나 기준 문서 결정을 정해 주세요.
3. 이 구현 지시서로 실제 구현을 시작해도 되는지 승인해 주세요.
그다음 제가 구현을 진행하겠습니다.
```

metadata, approvalRefs, legitimacy check, dependsOn, unresolved Missing Context 같은 내부 진단은 사용자가 요청했을 때만 상세히 제공한다.

## 완료 보고

구현 후 다음을 보고한다.

- 변경한 파일
- 충족한 acceptance criteria
- 실행한 테스트와 결과
- 남은 위험
- suggestions
- 다음에 할 일

사용자 개입이 필요 없으면 완료 보고 후 `verify-work.md`로 이동한다. 사용자 review나 정책 결정이 필요하면 멈추고 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다.
