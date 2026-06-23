# Readiness Gates

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

CDD 구현은 다음 세 확인 지점이 모두 `READY`일 때만 가능하다.

1. 제품 기준 준비 상태
2. 기술 설계 준비 상태
3. 구현 시작 가능 여부

하나라도 `NOT READY`이면 구현하지 말고 `_missing-context.md`로 돌아간다. 이 문서는 Markdown 규칙과 판정 형식만 정의한다. CLI, 스크립트, 자동 수정 도구를 구현하지 않는다.

## 제품 기준 준비 상태

제품 기준 준비 상태는 "무엇을 왜 만들 것인가"에 대한 기획자 관점의 준비도다. 내부명은 `Product Readiness`다.

최소 확인 항목:

- 사용자 문제
- 대상 사용자
- 사용 시나리오
- 기능 범위
- 하지 않을 것
- 성공 기준
- 실패/예외 UX
- 이번 vertical slice의 제품 경계
- 저장, API, 상태가 필요한 경우 그 제품 의미와 사용자가 다시 읽는 방식
- 사용자 또는 운영자가 접하는 기능인 경우 상호작용 방식
- 입력과 출력, 실패와 피드백, 빈 상태, 권한 없음, 처리 중 상태에서의 사용자/운영자 경험
- 사용자가 반드시 이해해야 하는 주요 문구와 결과
- 웹/모바일 UI인 경우 화면 상태, 정보 우선순위, 주요 행동, 반응형 기준, 접근성, 텍스트 overflow, 시각 검증 방법

`NOT READY` 예:

- 사용자가 왜 이 기능을 쓰는지 불명확하다.
- 기능 범위가 너무 넓거나 무한 확장된다.
- 하지 않을 것이 정의되지 않았다.
- 성공 기준이 테스트 가능하지 않다.
- 현재 작업이 제품 목표에 왜 필요한지 설명되지 않는다.
- 저장하려는 대상과 저장 이유가 제품 관점에서 설명되지 않았다.
- 사용자가 나중에 저장된 정보를 어떻게 다시 읽거나 활용하는지 설명되지 않았다.
- 사용자 또는 운영자가 어디서 기능을 발견하거나 실행하는지 설명되지 않았다.
- 입력, 출력, 실패, 빈 상태, 권한 없음, 처리 중 피드백이 정해지지 않았다.
- 웹/모바일 UI인데 화면 상태, 정보 구조, 반응형 동작, 접근성, 시각 검증 기준이 정해지지 않았다.
- 상호작용 방식이 비어 있는데 저장 구조, API, 화면, CLI 명령, 배치 실행 방식을 먼저 정해야 한다.

## 상호작용 방식 확인

사용자나 운영자가 직접 접하는 기능에서는 입력, 출력, 흐름, 오류, 빈 상태, 권한 없음, 처리 중 피드백, 주요 문구가 제품 판단이다.

이런 판단이 없으면 제품 기준 준비 상태를 `READY`로 표현하지 않는다. 인터페이스는 나중에 붙이는 부가 요소가 아니다. 사용자가 실제로 어떻게 쓰고, 실패 시 무엇을 알게 되는지가 정해지지 않았으면 먼저 질문한다.

상호작용 방식 확인:

```text
상호작용 방식 확인:
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
- 사용자가 반드시 이해해야 하는 문구나 결과는 무엇인가?
- 아직 정하지 못한 상호작용 결정:
- 결론: 상호작용 설계 가능 / 상호작용 설계 보류
```

플랫폼별 예시는 범용 예시로만 사용한다.

- 웹/모바일: 화면, 버튼, 폼, 목록, 빈 상태, 오류 메시지
- CLI: 명령어, 옵션, stdout/stderr, exit code, 실패 메시지
- API: request/response, validation error, permission failure, error code
- 배치/운영 도구: 실행 파라미터, dry-run, 실패 리포트, 재시도 기준, 운영자가 보는 summary/log

`상호작용 설계 보류`이면 화면, CLI 명령, API path, 배치 실행 방식, 저장 구조를 먼저 제안하지 않는다. Product Missing Context 질문으로 돌아간다.

## 프론트엔드 UX 확인

웹/모바일 UI 작업에서는 상호작용 방식 확인과 별도로 프론트엔드 UX 확인을 수행한다. 버튼이나 화면 이름만 정해졌다고 UI/UX 기준이 준비된 것은 아니다.

프론트엔드 UX 확인:

```text
프론트엔드 UX 확인:
- 대상 화면과 사용자 목표:
- 기존 디자인 시스템 또는 따라야 할 화면 패턴:
- 정보 우선순위와 주요 행동:
- UI 구현 계약으로 고정할 분석 결과:
- 레이아웃 계약:
- 정보 우선순위 계약:
- 금지 패턴:
- 기본/로딩/빈 상태/오류/권한 없음/성공 상태:
- 반응형 기준과 최소 지원 viewport:
- 접근성, keyboard/focus, label 기준:
- 텍스트 overflow, 긴 문구, CJK 표시 기준:
- 브라우저/스크린샷 검증 기준:
- 현재 사용자 화면 폭 우선 검증 여부:
- 아직 정하지 못한 UI/UX 결정:
- 결론: FRONTEND_UX_ALLOWED / FRONTEND_UX_BLOCKED / 해당 없음
```

`FRONTEND_UX_BLOCKED`이면 route, page, component, layout, styling, motion, visual QA acceptance criteria를 먼저 제안하지 않는다. Product Missing Context 또는 Engineering Missing Context 질문으로 돌아간다.

`FRONTEND_UX_ALLOWED`는 단순히 에이전트가 화면을 그릴 수 있다는 뜻이 아니다. 웹/모바일 UI 작업에서 화면 상태, 정보 구조, 접근성, 반응형 동작, 시각 검증 기준이 승인 문서 안에 역할로 기록되어 있어야 한다. 필요한 역할은 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE`다. 이 역할은 별도 파일에 있어도 되고, 프로젝트가 승인한 루트 `DESIGN.md` 같은 단일 기준 문서 안에 명확한 섹션이나 `owns`로 기록되어 있어도 된다.

분석 결과는 구현 계약이 아니다. "공간을 줄인다", "가독성을 높인다", "정보 우선순위를 바꾼다" 같은 분석 문장은 route/page/component/layout/styling 작업으로 넘기기 전에 레이아웃 계약, 정보 우선순위 계약, 금지 패턴, 반응형 기준, 브라우저/스크린샷 검증 기준으로 고정되어야 한다.

UI 구현 계약은 화면 단위 기준이다. 컴포넌트별 수정 목록만 있고 전체 화면에서 유지해야 할 높이, 밀도, 강조 수준, 숨김 금지, primary/secondary 정보 관계, 검증 viewport가 없으면 `FRONTEND_UX_BLOCKED`로 본다.

승인 문서 안에서 필요한 역할이 비어 있으면 `FRONTEND_UX_BLOCKED`로 보고한다. 이 경우 route, page, component, layout, styling, motion, visual QA 기준을 Task, 구현 지시서, acceptance criteria에 넣지 말고 Missing Context 질문으로 돌아간다.

## 기술 설계 준비 상태

기술 설계 준비 상태는 "그 제품 판단을 어떤 아키텍처, 저장 구조, 상태, API, 운영/품질 기준, 코드 구조로 안전하게 표현할 것인가"에 대한 코드 설계자 관점의 준비도다. 내부명은 `Engineering Readiness`다.

기술 설계 준비 상태는 기술 기반이 있거나 기존 코드가 있다는 뜻이 아니다. 제품 판단을 아키텍처, table, column, API path, status enum, 성능/보안/운영 기준으로 바꿔도 되는 기준이 문서상 정해졌다는 뜻이다.

최소 확인 항목:

- 도메인 모델
- 아키텍처 경계
- 데이터 흐름
- API 계약
- DB/저장 정책
- 상태 전이
- 저장 의미 확인 결과
- 동작 계약 확인 결과
- 상태 의미 확인 결과
- 권한/보안 영향
- 운영/품질 기준
- 데이터 양, 조회 방식, 정렬/검색/페이지 처리, 응답 속도 기대치
- 성능 위험을 찾거나 고칠 작업이라면 성능 위험 조사 범위, 근거 기준, 허용된 수정 범위
- 민감 정보 노출, 로그/감사, 재시도, 멱등성, 중복 실행 방지
- 외부 연동/의존성
- 테스트 전략
- 실패/예외 처리 정책
- migration/data compatibility 영향이 있는지 여부

`NOT READY` 예:

- 아키텍처 경계가 정의되지 않았다.
- DB/API/상태 흐름이 정의되지 않았다.
- 저장 의미가 정의되지 않았는데 table, column, migration, repository, API DTO를 정해야 한다.
- 동작 계약이 정의되지 않았는데 API path, method, controller, route, request/response shape를 정해야 한다.
- 상태 의미가 정의되지 않았는데 status enum, status column, state transition을 정해야 한다.
- 성능, 보안, 운영 기준이 비어 있는데 안전하거나 충분하다고 가정해야 한다.
- 데이터 양, 조회 방식, 정렬/검색/페이지 처리, 응답 속도 기대치가 필요한데 정의되지 않았다.
- 구현 중 보이는 성능 위험 후보를 승인된 작업 범위 없이 개선 대상으로 승격해야 한다.
- 권한 검증, 민감 정보 노출, 실패 처리, 로그/감사 필요 여부가 정의되지 않았다.
- 도메인 용어가 코드 모델로 매핑되지 않았다.
- 테스트 전략이 없다.
- 외부 연동 실패 정책이 없다.
- migration 영향이 있는데 별도 판단이 없다.
- 보안/권한 영향이 있는데 정의되지 않았다.

## 구조 제안 전 의미 확인

table, column, API path, status enum은 제품 판단의 결과다. 이것들이 제품 판단을 대신할 수 없다.

Codex는 다음 구조를 제안하기 전에 대응하는 확인을 먼저 수행한다.

- 화면, CLI 명령, 배치 실행 방식, 사용자/운영자 인터페이스 제안 전: 상호작용 방식 확인
- route, page, component, layout, styling, motion, visual QA 기준 제안 전: 프론트엔드 UX 확인
- UI 구현 계약 제안 전: 분석 결과를 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저/스크린샷 검증 기준으로 변환
- 웹/모바일 UI 구현 기준 제안 전: 승인 문서 안의 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할 coverage 확인
- DB table, column, migration, repository, API DTO 제안 전: Storage Intent Check
- API path, method, route, controller, request/response shape 제안 전: Behavior Contract Check
- status enum, status column, state transition 제안 전: State Meaning Check

Storage Intent Check:

```text
Storage Intent Check:
- 저장하려는 것:
- 저장하는 이유:
- 나중에 읽는 방식:
- 저장하지 않을 것:
- 구조화할 것:
- 자유 텍스트로 둘 것:
- 수정/삭제/보존 정책:
- 소유권/범위:
- 부족한 결정:
- 결론: DB_DESIGN_ALLOWED / DB_DESIGN_BLOCKED
```

`DB_DESIGN_ALLOWED`는 저장 의미와 저장 이유가 approved source of truth에 충분히 문서화되어 있을 때만 가능하다.

`DB_DESIGN_BLOCKED`이면 table, column, migration, repository, API DTO를 제안하지 않는다. 이 경우 Product Missing Context 또는 Engineering Missing Context 질문으로 돌아간다.

Behavior Contract Check:

```text
Behavior Contract Check:
- 사용자가 기대하는 동작:
- 호출자가 제공하는 입력:
- 성공 결과:
- 실패/예외 결과:
- 권한/범위:
- 멱등성/재시도:
- 외부에 노출할 표현:
- 부족한 결정:
- 결론: API_DESIGN_ALLOWED / API_DESIGN_BLOCKED
```

`API_DESIGN_BLOCKED`이면 API path, method, route, controller, request/response shape를 제안하지 않는다. 먼저 동작 계약을 Product Missing Context 또는 Engineering Missing Context로 질문한다.

State Meaning Check:

```text
State Meaning Check:
- 상태가 표현하는 의미:
- 상태를 바꾸는 사건:
- 각 상태에서 허용되는 행동:
- 종료/실패/취소 의미:
- 저장할지 계산할지:
- 외부에 노출할지:
- 부족한 결정:
- 결론: STATE_MODEL_ALLOWED / STATE_MODEL_BLOCKED
```

`STATE_MODEL_BLOCKED`이면 status enum, status column, state transition 이름을 제안하지 않는다. 먼저 상태 의미를 Product Missing Context 또는 Engineering Missing Context로 질문한다.

부분적으로 준비된 영역이 있어도 해당 check가 `*_BLOCKED`이면 구조 설계와 구현은 금지다. "부분 READY"라는 표현은 구현이나 DB 설계 제안 권한이 아니다.

## 운영/품질 기준 확인

성능, 보안, 운영 기준도 설계 판단이다. 단순히 코드 구조를 만들 수 있다고 설계가 준비된 것은 아니다.

작고 개인용인 기능은 가볍게 판단할 수 있지만, 판단 자체를 생략해도 된다는 뜻은 아니다. 기준이 비어 있으면 에이전트가 임의로 정하지 말고 사용자에게 선택지를 제시한다.

운영/품질 기준 확인:

```text
운영/품질 기준 확인:
- 예상 데이터 양은 어느 정도인가?
- 목록이나 조회가 있다면 정렬, 검색, 페이지 처리가 필요한가?
- 사용자가 기대하는 응답 속도는 어느 정도인가?
- 권한 검증은 어디에서 필요한가?
- 민감 정보나 외부 연동 정보가 노출될 위험이 있는가?
- 실패 시 사용자는 무엇을 알 수 있어야 하는가?
- 서버/클라이언트/작업 실행 환경 중 어디에서 검증해야 하는가?
- 재시도, 중복 실행 방지, 멱등성이 필요한가?
- 로그나 감사 기록이 필요한가?
- 성능 위험 후보를 찾는 작업이 승인된 범위인가, 아니면 구현 중 발견한 제안으로만 남겨야 하는가?
- 성능 위험 판단에 사용할 근거는 profiling, query plan, benchmark, production metric, 테스트 재현 중 무엇인가?
- 성능 개선으로 바꿔도 되는 범위는 local implementation, query shape, index/schema, caching, async/batch, dependency 중 어디까지인가?
- 아직 정하지 못한 운영/품질 결정:
- 결론: 설계 가능 / 설계 보류
```

`설계 보류`이면 안전하다고 가정하지 않는다. performance, security, operation, retry, logging, audit, pagination, search, sorting, permission, validation 정책을 임의로 정하지 않고 Engineering Missing Context 질문으로 돌아간다. 구현 중 성능 위험 후보가 보여도 승인된 범위와 근거 기준 없이 cache, pagination, indexing, async, batching, query 변경, dependency 추가를 수행하지 않는다.

## 구현 시작 가능 여부

구현 시작 가능 여부는 "이제 에이전트가 구현해도 되는가"에 대한 실행 준비도다. 내부명은 `Implementation Readiness`다.

최소 확인 항목:

- 제품 기준 준비 상태 = `READY`
- 기술 설계 준비 상태 = `READY`
- approved 작업 기준 묶음 존재
- 작업 기준서 존재
- allowed scope / forbidden scope 명시
- verification commands 명시
- user approval gate 통과
- 필요한 선행 Task complete
- archive/superseded 문서를 active SOT로 사용하지 않음
- 과거 task, completion, verification, prompt를 현재 기준으로 사용하지 않음
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference를 active 기준으로 사용하지 않음
- 현재 기준과 과거 기록 사이 충돌 없음
- 기본 읽기 경로의 큰 문서와 누적 문서에 대해 분리 후보/유지 후보 보고 완료
- 현재 작업 포인터로 현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서, 읽지 않을 과거 기록을 식별할 수 있음
- 기본 읽기 경로 계약으로 이번 작업에 필요한 최소 문서와 제외할 과거 기록/보조 자료가 분리됨

`NOT READY` 예:

- 제품 기준 또는 기술 설계 기준 중 하나라도 `NOT READY`다.
- 작업 기준 묶음이 없다.
- 작업 기준서가 없다.
- forbidden scope가 없다.
- 검증 명령이 없다.
- 사용자 승인이 없다.
- 아직 필요한 결정이 남아 있다.
- 과거 작업 기록이나 검증 기록을 현재 기준처럼 읽어야 구현할 수 있다.
- 현재 기준과 과거 task, completion, verification, prompt가 충돌한다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference 같은 보조 자료를 기준 문서처럼 사용해야 한다.
- 기본 읽기 경로의 큰 문서나 1000줄 이상 누적 문서가 있는데 분리 후보/유지 후보가 보고되지 않았다.
- 현재 작업 포인터가 없어 다음 task와 반드시 읽을 문서를 식별하려면 큰 누적 문서 전체를 읽어야 한다.
- 기본 읽기 경로 계약이 없어 완료된 task, 과거 verification, completion, old prompt가 현재 기준과 섞여 읽힌다.

## 판정 출력 형식

Codex는 구현 전에 다음 형식으로 보고한다.

```text
준비 상태 확인
제품 기준 준비: READY / NOT READY
- 근거:
- 부족한 결정:
상호작용 방식 확인:
- 결론: 상호작용 설계 가능 / 상호작용 설계 보류 / 해당 없음
- 부족한 결정:
프론트엔드 UX 확인:
- 결론: FRONTEND_UX_ALLOWED / FRONTEND_UX_BLOCKED / 해당 없음
- 부족한 결정:
기술 설계 준비: READY / NOT READY
- 근거:
- 부족한 결정:
운영/품질 기준 확인:
- 결론: 설계 가능 / 설계 보류 / 해당 없음
- 부족한 결정:
구현 시작 가능 여부: READY / NOT READY
- 근거:
- 구현 가능 여부:
문서 정합성:
- 현재 기준으로 읽을 문서:
- 과거 기록으로만 볼 문서:
- 보조 자료로만 볼 문서:
- 현재 기준과 과거 기록의 충돌:
현재 작업 포인터:
- 위치:
- 현재 gate:
- 다음 task:
- 반드시 읽을 문서:
- 읽지 않을 과거 기록:
문서 크기 / 읽기 비용:
- 기본 읽기 경로에서 큰 문서:
- 분리 후보:
- 유지 후보:
결론:
- 구현 가능 / 구현 보류
- 필요한 다음 행동:
```

내부 status인 `IMPLEMENTATION_ALLOWED`는 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부가 모두 `READY`일 때만 사용한다.

내부 status가 `IMPLEMENTATION_BLOCKED`이면 코드, 테스트, 설정, migration, dependency 변경을 수행하지 않는다.

## 미확정 결정 연결

준비 상태가 `NOT READY`이면 질문을 다음처럼 분리한다.

- 제품 관련 미확정 결정: 제품 목표, 사용자, 시나리오, 범위, 하지 않을 것, 성공 기준, 상호작용 방식, 입력/출력, 실패와 피드백, 빈 상태, 권한 없음, 처리 중 피드백, vertical slice 경계 질문.
- 기술 설계 관련 미확정 결정: 아키텍처, 도메인 모델, 데이터 흐름, API, 저장 정책, 상태 전이, 프론트엔드 UX 기준 문서, 디자인 시스템 또는 화면 패턴, 성능, 보안/권한, 운영/품질 기준, 외부 연동, 테스트 전략, 실패 처리, migration/data compatibility 질문.
- 구현 시작 관련 미확정 결정: 작업 기준 묶음, 작업 기준서, allowed/forbidden scope, verification command, user approval, 선행 Task 완료 여부, archive/superseded 참조 여부 질문.

예:

- 제품 관련 질문: 이 기능의 사용자는 누구인가?
- 기술 설계 관련 질문: 이 상태는 DB에 저장되는가, 계산되는가?
- 제품 관련 질문: 실패했을 때 사용자는 어떤 메시지나 결과를 받아야 하는가?
- 기술 설계 관련 질문: 목록이 많아졌을 때 정렬, 검색, 페이지 처리를 어떻게 할 것인가?
- 구현 시작 관련 질문: 이번 Task에서 public API 변경이 허용되는가?

## 금지되는 오해

- 제품 기준 준비 상태는 화면 기획서만 있다는 뜻이 아니다.
- 기술 설계 준비 상태는 코드가 이미 있다는 뜻이 아니다.
- README가 있다고 제품 기준 문서가 준비된 것이 아니다.
- 기존 구현이 있다고 기술 설계 기준 문서가 준비된 것이 아니다.
- 테스트가 통과한다고 구현 시작 가능 여부가 `READY`인 것은 아니다.
- 작업 기준서가 있다고 구현 가능한 것은 아니다.
- 작업 기준 묶음이 있어도 제품/기술 기준 중 하나가 부족하면 구현 금지다.
- 사용자의 "좋아"는 준비 상태 확인 통과나 구현 승인으로 자동 해석되지 않는다.
- 과거 completion, verification, task, prompt가 있다고 현재 기준이 준비된 것은 아니다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference는 탐색 보조 자료이지 구현 기준이 아니다.

## SOT 관계

제품 기준 문서와 기술 설계 기준 문서는 같은 파일에 함께 있을 수 있지만, 준비 상태 판정에서는 각각 필요한 결정을 별도로 확인한다.

제품 기준 문서만 있거나 기술 설계 기준 문서만 있으면 구현하지 않는다.

README, generated/index docs, memory/recall notes, previous reports, archive/superseded documents는 명시적으로 작업 기준 묶음에 포함되지 않으면 준비 상태 근거가 아니라 보조 자료다.

과거 task, completion, verification, old prompt는 그 시점의 사실 기록이며 현재 기준 문서가 아니다. active 기준 문서나 registry에서 승격 근거를 찾을 수 없으면 readiness 근거로 사용하지 않는다.

기본 읽기 경로의 문서가 400줄 또는 40KB를 넘으면 분리 후보로 보고한다. 1000줄 이상 누적 문서는 active index와 history 문서 분리 후보로 보고한다. 짧고 응집된 문서는 파일 수를 늘리지 않고 유지 후보로 보고한다. 문서 크기 문제만으로 구현을 막지는 않지만, 현재 기준과 과거 기록이 섞여 판단을 흐리거나 분리/유지 판단이 보고되지 않았으면 구현 시작 가능 여부를 `READY`로 보지 않는다.
