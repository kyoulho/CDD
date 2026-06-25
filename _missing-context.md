# Missing Context Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 문서나 정책이 부족할 때 사용자에게 질문하는 방법을 정의한다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 Missing Context 질문과 필요한 결정 후보만 제시하고 파일을 수정하지 않는다. 사용자 답변을 받기 전이나 패치/적용 승인이 없을 때 문서 초안, Task, prompt, runs를 생성하지 않는다.

요청 자체가 애매한 것도 Missing Context다. 사용자가 설명, 설계안, 문서 초안, 문서 수정, 구현 계획, 실제 코드 수정, 삭제/정리, 검증 중 무엇을 원하는지 확정할 수 없으면 먼저 질문한다.

목표는 사용자가 긴 문서를 직접 쓰지 않아도, 짧은 답변으로 필요한 결정을 제공할 수 있게 만드는 것이다.

이 skill은 `_source-of-truth-manager.md`의 하위 절차다. Missing Context Agent는 질문을 만들고 사용자 답변을 기다릴 수 있지만, source of truth 문서, registry, Plan, Task, prompt, verification result를 수정하지 않는다.

## 빠른 탐색

- 이 module의 책임은 "역할"을 본다.
- 질문 생성 원칙은 "규칙"을 본다.
- 요청 자체가 애매한 경우는 "요청 의도 Missing Context"를 본다.
- 사용자에게 보여줄 구조는 "출력 형식"을 본다.
- 좋은 질문 기준과 추천 처리 방식은 "좋은 질문의 기준", "추천안 처리"를 본다.
- 테스트, 의존성, 프론트엔드 UX, 성능 범위 질문 예시는 각 Missing Context 예시를 본다.

## 역할

- 부족한 결정을 목록화한다.
- 애매한 사용자 요청의 의도를 확인한다.
- 왜 필요한지 설명한다.
- 사용자가 고를 수 있는 선택지를 제시한다.
- 추천안을 제시한다.
- 사용자가 짧게 답할 수 있게 만든다.
- 바로 답할 수 있는 문장을 제공한다.
- 사용자 답변 뒤 CDD가 무엇을 이어서 할지 알려준다.

## 규칙

- 질문은 구체적이어야 한다.
- 애매하면 먼저 질문한다.
- 사용자 요청을 임의로 해석하지 않는다.
- 애매한 요청을 구현 요청으로 승격하지 않는다.
- 애매한 요청을 파일 수정 승인으로 해석하지 않는다.
- 사용자가 긴 문서를 직접 쓰게 만들지 마라.
- 선택지와 추천안을 반드시 제공하라.
- 바로 답할 수 있는 문장을 반드시 제공하라.
- 질문 보고는 "다음에 할 일"로 끝내라.
- AI가 추천안을 자동 확정하지 마라.
- 사용자 답변은 승인 전까지 source of truth가 아니다.
- 질문은 현재 Goal과 Task 생성을 막는 실제 gap만 포함한다.
- Project Context가 없으면 도메인/아키텍처/테스트 전략 질문보다 먼저 프로젝트 성격과 운영 전제를 질문한다.
- 사용자에게 하네스 내부 목적을 묻지 않는다.
- 사용자가 이미 답한 프로젝트 목적, 출시 의도, 연습용 여부, 로컬 실행 여부를 Missing Context로 다시 묻지 않는다.
- Goal 또는 Task가 DB, migration, repository, test, external integration, batch, infra, config를 포함하면 cross-cutting policy gap을 우선 질문한다.
- testRequirements를 만들 수 있는데 TEST_STRATEGY가 없으면 구현 단계로 넘기지 말고 Missing Context로 질문한다.
- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library가 필요해 보이면 승인 여부를 질문한다.
- Missing Context가 해결되기 전에는 코드 수정, revision 실행, 테스트 전략 변경, Task Contract 수정, complete 진행을 하지 않는다.
- Missing Context 질문 전에는 정책 문서 DRAFT를 만들지 않는다.
- 사용자 답변 없이 source of truth DRAFT를 만들지 않는다.
- 사용자 답변이 있어도 DRAFT 저장 또는 적용은 Source of Truth Manager 승인 절차로 넘긴다.

## 요청 의도 Missing Context

다음 표현은 작업 성격이 애매할 수 있으므로 바로 구현하거나 파일을 수정하지 않는다.

- "정리해줘"
- "이거 진행해"
- "구조 잡아줘"
- "다음 단계로 가자"
- "고쳐줘"
- "문서 반영해"
- "설계해"
- "구현해도 될까?"

이 경우 사용자에게 자연어로 묻는다.

```text
지금 요청이 실제 파일 수정을 원하는 것인지, 먼저 설계/계획만 보려는 것인지 확인이 필요합니다.
어느 쪽으로 진행할까요?
1. 현재 상태를 읽고 판단만 한다
2. 문서 초안을 만든다
3. 문서를 실제로 수정한다
4. 구현 계획만 만든다
5. 코드를 실제로 수정한다
6. 삭제/정리 대상을 먼저 목록화한다
```

위 질문에 대한 답변은 작업 성격 선택일 뿐이다. 파일 수정 승인, source of truth 적용 승인, 구현 지시서 실행 승인, 삭제 승인을 자동으로 만들지 않는다.

## 출력 형식

```markdown
# Missing Context Report

## Status
BLOCKED_BY_MISSING_CONTEXT

## Missing Decisions

### 1. <decision topic>
- 필요한 이유:
- 관련 영역:
- 막고 있는 작업:
- 선택지:
  - A. <option>
  - B. <option>
  - C. <option>
- 추천: <recommended option>
- 질문: 어떤 정책으로 갈까요?

## Next Action
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

위 답변을 받으면 Source of Truth Manager의 document-supplement 하위 절차로 이동한다.
```

## 좋은 질문의 기준

좋은 질문:

- "삭제 정책은 hard delete인가 soft delete인가?"
- "title validation은 빈 값만 금지할까요, 길이 제한도 둘까요?"
- "API 오류 응답 형식은 기존 공통 포맷을 따르나요, 새 포맷이 필요한가요?"
- "Repository/Flyway 테스트는 PostgreSQL/Testcontainers, 별도 테스트 PostgreSQL, H2, 또는 이번 Task에서 DB 통합 테스트 제외 중 어떤 전략을 사용할까요?"
- "application-test.yml과 테스트 전용 migration을 허용하나요?"
- "외부 API 의존성은 실제 호출, fake, fixture, stub 중 무엇으로 대체하나요?"
- "이 Task에서 새 dependency를 승인하나요, 아니면 기존 스택 안에서 구현할까요?"
- "이 프로젝트는 실제 서비스 출시용인가요, 연습용인가요?"
- "데이터 정합성이나 추적 가능성이 중요한 작업인가요?"
- "이 화면의 주요 사용자 행동, 빈 상태, 오류 상태, 반응형 기준, 접근성 기준은 무엇인가요?"
- "분석 결과를 어떤 UI 구현 계약으로 고정할까요? 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저 검증 기준을 짧게 정해야 합니다."
- "성능 위험 후보는 이번 Task에서 조사/수정 범위인가요, 아니면 후속 제안으로만 남길까요?"

나쁜 질문:

- "요구사항을 더 자세히 써주세요."
- "아키텍처를 알려주세요."
- "어떻게 구현할까요?"

## 추천안 처리

추천안은 사용자의 결정을 돕기 위한 참고다. 추천안은 승인된 정책이 아니다.

사용자가 추천안을 선택하거나 명시적으로 승인해야 다음 단계로 갈 수 있다.

추천안을 제시할 때는 사용자가 그대로 보낼 수 있는 문장도 함께 제공한다.

예:

```text
바로 답할 수 있는 문장:
"추천안대로 문서 보강안을 만들고, 적용 전 다시 보여줘."
```

## 허용 행동

BLOCKED_BY_MISSING_CONTEXT 상태에서 허용되는 행동은 다음뿐이다.

- Missing Context 질문 작성
- 요청 의도 확인 질문 작성
- 선택지와 추천안 제시
- 사용자 답변 대기
- 사용자가 답변하면 `_source-of-truth-manager.md`의 `_document-supplement.md` 하위 절차로 이동

금지 행동:

- H2 제거, Testcontainers 추가 시도, 테스트 구조 변경 같은 코드 수정
- Repository DB 통합 테스트를 정적 테스트로 대체
- 테스트를 후속 Task로 임의 이연
- TEST_STRATEGY / MIGRATION_POLICY / FRONTEND_UX_CRITERIA / DESIGN_SYSTEM / UI_PATTERN / USER_FLOW / INTERACTION_SPEC / FRONTEND_ARCHITECTURE DRAFT 문서 임의 생성
- source of truth, document registry, Plan, Task, prompt, verification result 수정

## Test Strategy Missing Context 예시

## Project Context Missing Context 예시

Bad:

```text
CDD 자체를 검증하는 테스트 베드인가요?
하네스 약점 발견이 목적인가요?
skill validation 프로젝트인가요?
```

Good:

```text
이 프로젝트는 실제 서비스 출시용인가요, 연습용인가요?
운영 배포까지 고려하나요, 로컬 실행만 보면 되나요?
데이터 정합성이나 추적 가능성이 중요한 작업인가요?
완료된 기록의 수정 또는 취소를 허용하나요?
감사 추적은 어느 수준까지 남겨야 하나요?
```

```markdown
### 1. Project character
- 필요한 이유: 프로젝트 성격을 알아야 운영, 보안, 테스트, 데이터 정합성 질문의 강도를 맞출 수 있다.
- 관련 영역: PROJECT_CONTEXT
- 막고 있는 작업: source of truth 문서 작성, Plan/Task 생성, 구현 지시서 생성
- 선택지:
  - A. 도메인 설계·구현 연습용 프로젝트
  - B. 로컬 실험 또는 개인용 도구
  - C. 내부 운영/백오피스 도구
  - D. 외부 사용자 대상 실제 서비스
- 추천: 사용자가 연습용이라고 이미 말했다면 A로 보고 다음 도메인 정책 질문으로 넘어간다.
- 질문: 이 프로젝트는 실제 서비스 출시용인가요, 연습용인가요?

### 2. Risk and simplification boundary
- 필요한 이유: AI가 과도한 운영 정책을 요구하거나, 반대로 중요한 정합성 정책을 단순화하지 않게 해야 한다.
- 관련 영역: PROJECT_CONTEXT / TEST_STRATEGY / OPERATION
- 막고 있는 작업: readiness, planning
- 선택지:
  - A. 데이터 정합성 낮음, 운영 요구 낮음
  - B. 데이터 정합성 중간, 운영 요구 중간
  - C. 데이터 정합성 높음, 운영 요구 낮음
  - D. 데이터 정합성 매우 높음, 감사/추적 필요
- 추천: 완료 기록, 재고, 정산, 권한 변경처럼 정합성이나 추적 가능성이 중요하면 C 또는 D.
- 질문: 데이터 정합성, 감사/추적, 보안/권한 요구는 어느 정도인가요? AI가 단순화해도 되는 영역과 절대 단순화하면 안 되는 영역도 알려주세요.
```

사용자가 이미 "실제 서비스로 출시할 목적은 아니고, 복잡한 도메인을 설계하고 구현하는 연습용 프로젝트"라고 말했다면 위 질문을 반복하지 않는다. 다음 질문은 아직 답하지 않은 product/domain decision으로 이동한다.

## Test Strategy Missing Context 예시

```markdown
### 1. Test database strategy
- 필요한 이유: TASK-001 includes Repository/Flyway tests. Implementation Agent cannot choose H2, PostgreSQL, Testcontainers, or test migration strategy without approved source of truth.
- 관련 영역: TEST_STRATEGY / DATA_MODEL / MIGRATION_POLICY / IMPLEMENTATION_ARCHITECTURE
- 막고 있는 작업: Repository/Flyway testRequirements and implementation prompt generation
- 선택지:
  - A. Use PostgreSQL/Testcontainers
  - B. Use separate local PostgreSQL test DB
  - C. Defer DB integration tests and only run build/context tests for TASK-001
  - D. Use H2 with explicit approval and documented dialect divergence
- 추천: C for lightweight first harness validation, or A if DB fidelity is required.
- 질문: 이번 Task의 테스트 DB 전략은 무엇으로 승인할까요?
```

## Dependency Missing Context 예시

```markdown
### 1. Dependency approval
- 필요한 이유: Task가 새 library/build tool/code generation tool 없이는 구현 방향이 달라질 수 있다.
- 관련 영역: DEPENDENCY_POLICY / IMPLEMENTATION_ARCHITECTURE / TEST_STRATEGY
- 막고 있는 작업: dependency 추가 여부에 따라 implementationConstraints와 forbiddenApproaches가 달라진다.
- 보고할 내용: dependency 이름과 용도, production/test/build/runtime 노출 여부, 기존 스택 대안과 한계, 영향 파일, 보안/라이선스/유지보수/bundle 영향, 검증 방법
- 선택지:
  - A. 새 dependency를 승인하고 목적/범위를 문서화한다.
  - B. 새 dependency 없이 기존 스택 안에서 구현한다.
  - C. dependency가 필요한 기능을 후속 Task로 이연한다.
- 추천: 기존 스택으로 Task 범위와 검증 기준을 만족할 수 있으면 B. 그렇지 않으면 A를 승인하거나 C로 이연한다.
- 질문: 새 dependency를 승인할까요, 아니면 기존 스택 안에서 구현할까요?
```

## Frontend UX Missing Context 예시

```markdown
### 1. Frontend UX criteria
- 필요한 이유: 웹/모바일 UI는 버튼과 화면 이름만으로 구현 기준이 충분하지 않다. 화면 상태, 정보 우선순위, 반응형, 접근성, visual QA 기준이 있어야 구현과 검증이 가능하다.
- 추가 이유: 분석 결과를 구현 계약으로 고정하지 않으면 구현 에이전트가 컴포넌트 단위로 해석해 전체 화면 의도를 놓친다.
- 관련 영역: PRODUCT_REQUIREMENT / USER_SCENARIO / FRONTEND_UX_CRITERIA / USER_FLOW / INTERACTION_SPEC / DESIGN_SYSTEM / UI_PATTERN / FRONTEND_ARCHITECTURE
- 막고 있는 작업: route/page/component/layout/styling/visual QA가 포함된 Task와 구현 지시서 생성
- 선택지:
  - A. 기존 디자인 시스템과 화면 패턴을 따르고, 기본/로딩/빈 상태/오류/권한 없음 상태를 모두 정의한다.
  - B. 최소 UI만 만들되 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 접근성, overflow, 브라우저/스크린샷 검증 기준은 명시한다.
  - C. 이번 Task에서는 UI 구현을 제외하고 API/도메인 작업만 진행한다.
- 추천: B. 디자인 세부안을 크게 늘리지 않으면서도 구현 에이전트가 임의로 화면을 만들지 않게 막는다.
- 질문: 이번 UI의 주요 행동, 화면 상태, 반응형/접근성/visual QA 기준은 어느 수준으로 승인할까요?

위 답변을 받으면 `_document-supplement.md`는 필요한 범위에 따라 FRONTEND_UX_CRITERIA, USER_FLOW 또는 INTERACTION_SPEC, DESIGN_SYSTEM 또는 UI_PATTERN, FRONTEND_ARCHITECTURE 초안을 제안한다. 답변 전이나 APPLY 승인 전에는 route, page, component, layout, styling, motion, visual QA 기준 또는 `uiImplementationContract`를 Task나 구현 지시서에 넣지 않는다.

사용자 답변이 일부만 채워졌다면 채워진 문서 초안만 제안한다. 예를 들어 사용자 흐름만 답했고 화면 상태나 디자인 시스템 기준이 비어 있으면 `USER_FLOW` 또는 `INTERACTION_SPEC` 초안만 제안하고, `FRONTEND_UX_CRITERIA`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE`는 계속 질문으로 남긴다.

UI 구현 계약은 짧아도 된다. 예:

```text
UI 구현 계약:
- 레이아웃: 현재 자산 요약은 한 카드 안의 compact analysis panel이다.
- 정보 우선순위: 종목명/자산명이 primary이고 코드는 secondary다.
- 금지 패턴: KPI를 3개 카드로 쪼개지 않고, 태그를 "외 n개"로 숨기지 않고, 표 숫자를 전부 bold 처리하지 않는다.
- 반응형: 현재 사용자 화면 폭을 먼저 만족하고 이후 desktop/mobile을 확인한다.
- 브라우저 검증: 스크린샷에서 빈 공간, 볼드 과다, 정보 우선순위, 숨김 처리를 계약과 대조한다.
```
```

## Performance Risk Scope Missing Context 예시

```markdown
### 1. Performance risk scope
- 필요한 이유: 구현 에이전트가 "느릴 수 있음"을 이유로 pagination, cache, index, async, dependency를 임의로 추가하면 성능 정책과 아키텍처 판단을 대신하게 된다.
- 관련 영역: OPERATION / ARCHITECTURE_POLICY / TEST_STRATEGY
- 막고 있는 작업: 성능 위험 후보 탐지 또는 성능 개선을 포함한 Task와 구현 지시서 생성
- 선택지:
  - A. 이번 Task에서 성능 위험 후보는 발견해도 suggestions로만 남긴다.
  - B. profiling, benchmark, query plan, 테스트 재현 같은 근거가 있는 후보만 같은 allowedScope 안에서 수정한다.
  - C. 별도 성능 조사 Task를 만들고 데이터 양, 응답 속도, 허용 변경 범위를 먼저 승인한다.
- 추천: A. 기준이 아직 없다면 구현 범위를 넓히지 않고 후속 판단으로 남기는 것이 안전하다.
- 질문: 성능 위험 후보는 이번 Task에서 어디까지 다룰까요?
```
