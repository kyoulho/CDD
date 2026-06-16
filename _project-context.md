# Project Context Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 프로젝트의 최상위 전제를 정의한다.

Project Context는 도메인 문서, 아키텍처 문서, 테스트 전략, Plan/Task보다 먼저 확인되어야 한다. 하네스는 프로젝트 성격이 확정되지 않았으면 바로 source of truth 문서, Plan, Task, 구현 지시서를 만들지 않는다.

목표는 운영 정책을 더 많이 요구하는 것이 아니라, 프로젝트 성격에 맞는 질문과 판단 강도를 정하는 것이다.

## Project Reality Over Harness Meta

Project Context는 프로젝트 자체의 목적, 사용자, 운영 전제, 도메인 위험, 기술 전제를 기록한다.

Project Context에는 하네스 검증 목적, 하네스 약점 발견 목적, skill validation 목적, prompt governance validation 목적을 기록하지 않는다.

하네스는 프로젝트를 운영, 검증, 평가에 사용할 수 있지만, 그 메타 목적은 project source of truth에 포함하지 않는다.

Do not contaminate project source of truth with harness evaluation purpose.

## 역할

Project Context는 다음을 확정한다.

- 프로젝트 목적
- 프로젝트 성격
- 사용자 유형
- 운영 전제
- 트래픽/성능 전제
- 데이터 정합성 중요도
- 보안/권한 요구
- 테스트 강도
- 배포/운영 고려 여부
- 실제 서비스, 연습용, 개인용, 내부용 등 프로젝트 자체의 성격
- AI가 단순화해도 되는 영역과 단순화하면 안 되는 영역

Project Context는 source of truth의 최상위 전제다. 도메인, 아키텍처, 테스트 전략, 운영 정책은 이 전제와 충돌하면 안 된다.

Project Context는 하네스 운영 목적을 소유하지 않는다. 하네스 평가 목적을 추적해야 한다면 project source of truth 밖의 별도 harness operation artifact를 사용한다.

Project Context는 `_readiness-gates.md`의 Product Readiness에 필요한 제품 경계, 사용자, 운영 전제를 제공한다. Project Context만으로 Product SOT가 완성되는 것은 아니지만, Product Readiness를 판정할 때 사용자 문제, 대상 사용자, 사용 시나리오, 하지 않을 것, 이번 vertical slice의 제품 경계가 Project Context와 충돌하지 않는지 확인한다.

## 프로젝트 성격 분류

복수 선택 가능하다.

```text
TEST_BED
PRACTICE_PROJECT
LOCAL_EXPERIMENT
PERSONAL_TOOL
INTERNAL_BACKOFFICE
INTERNAL_OPERATION_TOOL
PUBLIC_USER_SERVICE
HIGH_TRAFFIC_SERVICE
HIGH_CONSISTENCY_DOMAIN
REGULATED_OR_AUDIT_HEAVY_SYSTEM
PORTFOLIO_PROJECT
PRODUCTION_SERVICE
```

### TEST_BED와 PRACTICE_PROJECT 구분

`TEST_BED`:

- 특정 시스템, 도구, 하네스, 기술 가정의 검증을 목적으로 하는 내부 실험용 프로젝트
- 사용자가 명시적으로 "하네스 검증용 테스트 베드"라고 말한 경우에만 project type 후보로 둔다.

`PRACTICE_PROJECT`:

- 도메인 설계, 구현 연습, 학습, 기술 검증을 위한 프로젝트
- 실서비스 출시 목적은 아니며, 운영 인프라보다 학습, 설계 품질, 구현 품질이 중요하다.

사용자가 "연습용 프로젝트", "학습용", "복잡한 도메인을 설계하고 구현해보고 싶다"라고 말하면 user-facing 분류는 `PRACTICE_PROJECT`가 우선이다.

하네스 운영자가 뒤에서 이 프로젝트를 하네스 검증에 사용하더라도, 프로젝트 source of truth에는 `TEST_BED`로 우선 기록하지 않는다.

예:

```yaml
projectContext:
  project:
    id: high-consistency-practice
    projectType:
      - PRACTICE_PROJECT
      - LOCAL_EXPERIMENT
      - HIGH_CONSISTENCY_DOMAIN
    commercializationIntent: false
    primaryPurpose: "complex domain design and implementation practice"
```

## 필수 질문

프로젝트 시작 시 최소한 다음을 확인한다.

1. 이 프로젝트는 실제 서비스 출시용인가, 연습용인가?
2. 개인용인가, 내부 운영용인가, 외부 사용자용인가?
3. 상용화 의도가 있는가?
4. 트래픽/성능 요구는 낮음/중간/높음 중 무엇인가?
5. 데이터 정합성 중요도는 낮음/중간/높음/매우 높음 중 무엇인가?
6. 보안/권한 요구가 있는가?
7. 감사로그, 변경 이력, 추적 가능성이 필요한가?
8. 운영 배포까지 고려하는가?
9. 테스트는 어느 수준까지 필요한가?
10. AI가 단순화해도 되는 영역과 절대 단순화하면 안 되는 영역은 무엇인가?
11. 이번 vertical slice의 제품 경계는 어디까지인가?
12. 이 작업에서 명시적으로 하지 않을 것은 무엇인가?

사용자-facing 질문은 내부 분류명을 그대로 나열하지 말고 쉬운 말로 묻는다.

```text
이 프로젝트는 실제 서비스로 만들 건가요, 아니면 설계와 구현을 연습하는 프로젝트인가요?
사용자는 내부 운영자인가요, 외부 고객인가요?
데이터 정합성이나 추적 가능성이 중요한 작업인가요?
운영 배포까지 고려하나요, 로컬 실험까지만 보면 되나요?
```

기본 사용자-facing 질문으로 금지한다.

```text
CDD 자체를 검증하는 테스트 베드인가요?
하네스 약점 발견이 목적인가요?
skill validation을 위한 프로젝트인가요?
prompt governance validation을 위한 프로젝트인가요?
```

사용자가 이미 답한 내용은 다시 묻지 않는다.

예:

```text
실제 서비스로 출시할 목적은 아니고, 복잡한 도메인을 설계하고 구현하는 연습용 프로젝트다.
```

이 경우 Project Context 초안은 다음처럼 추론한다.

```yaml
project:
  primaryPurpose: "complex domain design and implementation practice"
  commercializationIntent: false
  projectType:
    - PRACTICE_PROJECT
    - LOCAL_EXPERIMENT
```

첫 질문으로 "프로젝트 목적이 무엇인가요?"를 다시 묻지 않는다. 특히 "CDD 검증용인가요?"를 묻지 않는다.

## Project Context Template

```yaml
projectContext:
  artifact:
    id: PROJECT-CONTEXT-001
    type: project-context
    status: DRAFT
    schemaVersion: cdd.v2.1
    createdByRole: source-of-truth-manager
    createdAt: null

  project:
    id: null
    name: null
    description: null
    primaryPurpose: null
    projectType: []
    commercializationIntent: null

  users:
    primaryUsers: []
    secondaryUsers: []
    internalOnly: null
    publicFacing: null

  operation:
    deploymentTarget: null
    productionIntent: null
    expectedTraffic: null
    availabilityRequirement: null
    observabilityRequirement: null

  risk:
    dataConsistencyCriticality: null
    criticalDataInvolved: null
    securityRequirement: null
    auditRequirement: null
    complianceRequirement: null

  engineering:
    preferredStack: null
    testStrictness: null
    allowedSimplifications: []
    forbiddenSimplifications: []

  approval:
    approvalRefs: []
```

## Harness Evaluation Purpose 분리

Harness evaluation purpose must not be written into project-context source of truth.

하네스 평가 목적을 추적해야 한다면 project source of truth가 아닌 별도 harness operation artifact를 사용한다.

예:

```text
harness-evaluation-note
harness-test-log
harness-experiment-plan
```

These are not project source of truth documents. They are harness operation artifacts.

금지:

```yaml
harness:
  weaknessDiscoveryGoals:
    - "state transition policy detection"
```

사용자가 명시적으로 "이 프로젝트는 하네스 검증용 테스트 베드다"라고 말한 경우에도, Project Context에는 프로젝트의 제품/도메인 목적을 우선 기록한다. 하네스 평가 목적은 별도 `harness-evaluation-note` artifact로 제안한다.

## Project Context 추론 규칙

사용자 표현:

```text
실제 서비스로 출시할 목적은 아니다.
연습용 프로젝트다.
복잡한 도메인을 설계하고 구현해보고 싶다.
로컬에서 해보면 된다.
```

추론:

```yaml
commercializationIntent: false
productionIntent: false
projectType:
  - PRACTICE_PROJECT
  - LOCAL_EXPERIMENT
```

사용자 표현:

```text
정합성 중요 도메인, 상태 전이, 감사 추적, 중복 이벤트 처리
```

추론:

```yaml
projectType:
  - HIGH_CONSISTENCY_DOMAIN
dataConsistencyCriticality: VERY_HIGH
criticalDataInvolved: true
```

주의:

`PRACTICE_PROJECT`라고 해서 도메인 정합성을 약하게 보면 안 된다. `HIGH_CONSISTENCY_DOMAIN`이면 실서비스가 아니어도 상태 전이, 감사 추적, 중복 처리 같은 정합성 경계를 강하게 본다.

## Readiness 규칙

- `projectContext`가 없으면 `READY_FOR_PLANNING`을 선언하지 않는다.
- 프로젝트가 `TEST_BED`이면 상용 운영 요구를 과도하게 요구하지 않는다.
- `TEST_BED`는 사용자가 명시적으로 시스템, 도구, 기술 가정 검증을 말한 경우에만 적용한다.
- 프로젝트가 `PRACTICE_PROJECT`이면 운영 인프라보다 학습, 설계 품질, 구현 품질을 우선한다.
- 프로젝트가 `PRODUCTION_SERVICE` 또는 `HIGH_CONSISTENCY_DOMAIN`이면 데이터 정합성, 감사, 테스트 전략을 강화한다.
- 프로젝트가 `HIGH_TRAFFIC_SERVICE`이면 성능, 확장성, 비동기 처리, 캐시, 큐 정책이 Missing Context 후보가 된다.
- 프로젝트가 `INTERNAL_BACKOFFICE`이면 권한, 변경 이력, 검색/필터/엑셀 등 운영 UX가 Missing Context 후보가 된다.
- 프로젝트가 `PERSONAL_TOOL`이면 과도한 운영 인프라를 기본 요구하지 않는다.

## Planning 규칙

Plan/Task 생성 시 반드시 `projectContext`를 참고한다.

- `TEST_BED`이면 사용자가 명시한 시스템, 도구, 기술 가정 검증 목표에 맞춘다.
- `PRACTICE_PROJECT`이면 사용자가 말한 도메인 설계·구현 연습 목표에 맞춘다.
- `PRODUCTION_SERVICE`이면 운영, 보안, 배포 관련 Task를 별도 고려한다.
- `HIGH_CONSISTENCY_DOMAIN`이면 상태 전이, idempotency, auditability 관련 Task를 분리한다.
- `LOCAL_EXPERIMENT`이면 복잡한 운영 인프라 Task를 기본 생성하지 않는다.

## Prompt Authoring 규칙

구현 지시서에는 `projectContextSummary`가 포함되어야 한다.

```yaml
projectContextSummary:
  projectType:
    - PRACTICE_PROJECT
    - LOCAL_EXPERIMENT
    - HIGH_CONSISTENCY_DOMAIN
  primaryPurpose: "complex domain design and implementation practice"
  productionIntent: false
  dataConsistencyCriticality: "VERY_HIGH"
  allowedSimplifications:
    - "No production external integration"
    - "No high traffic optimization"
  forbiddenSimplifications:
    - "No undocumented state transition"
    - "No silent consistency downgrade"
    - "No ignoring duplicated external events"
```

Implementation Agent는 `allowedSimplifications`를 구현 범위 축소 허용으로 오해하면 안 된다. `forbiddenSimplifications`는 Task 범위 안에서 반드시 지켜야 하는 정책 경계다.

## High Consistency Practice Project 예시

```yaml
projectContext:
  project:
    id: high-consistency-practice
    name: High Consistency Practice
    primaryPurpose: "complex domain design and implementation practice for a high-consistency workflow"
    projectType:
      - PRACTICE_PROJECT
      - LOCAL_EXPERIMENT
      - HIGH_CONSISTENCY_DOMAIN
    commercializationIntent: false

  users:
    primaryUsers:
      - "developer"
    internalOnly: true
    publicFacing: false

  operation:
    deploymentTarget: "local"
    productionIntent: false
    expectedTraffic: "LOW"
    availabilityRequirement: "LOW"
    observabilityRequirement: "LOW"

  risk:
    dataConsistencyCriticality: "VERY_HIGH"
    criticalDataInvolved: true
    securityRequirement: "LOW"
    auditRequirement: "MEDIUM"
    complianceRequirement: "NONE"

  engineering:
    testStrictness: "DOMAIN_STRICT_INFRA_LIGHT"
    allowedSimplifications:
      - "No production external integration"
      - "No production deployment"
      - "No high-traffic optimization"
      - "No authentication unless explicitly introduced"
    forbiddenSimplifications:
      - "No undocumented state transition"
      - "No silent consistency downgrade"
      - "No ignoring duplicate external events"
      - "No state transition invented by implementation agent"
```

이 예시는 실제 프로젝트 파일을 생성하라는 뜻이 아니다. 정합성이 중요한 연습용 프로젝트에서 제안할 수 있는 초기 Project Context 초안이다.

## High Consistency Practice Project 응답 예시

Bad:

```text
첫 번째 질문 — 이 프로젝트의 주된 목적은 무엇인가요?
A. CDD 자체를 검증하는 테스트 베드
B. 도메인 설계·구현 연습
C. 대외 공개용 산출물
D. 위 조합
```

Why bad:

```text
사용자가 이미 연습용 프로젝트라고 말했다. 하네스 내부 목적을 사용자-facing 질문으로 노출했다. 프로젝트 자체의 목적과 하네스 운영 목적을 섞었다.
```

Good:

```text
좋습니다. 이 프로젝트는 실서비스 출시용이 아니라 정합성이 중요한 도메인 흐름을 설계하고 구현해보는 연습용 프로젝트로 보겠습니다.
다만 데이터 정합성과 추적 가능성이 중요하므로 그 부분은 강하게 봐야 합니다. 운영 인프라나 고트래픽 처리는 과하게 보지 않고, 상태 전이·중복 처리·감사 추적 규칙을 먼저 정리하겠습니다.

먼저 아래 정책만 결정해 주세요.
1. 상태 전이는 어떤 단계로 나누나요?
2. 완료된 기록의 수정 또는 취소를 허용하나요?
3. 같은 외부 이벤트가 두 번 들어오면 어떻게 처리할까요?
4. 이벤트가 순서대로 들어오지 않으면 어떻게 처리할까요?
5. 감사 추적은 어느 수준까지 남겨야 하나요?
6. 데이터 정합성 검증은 어떤 테스트로 확인하나요?
```
