# Document Supplement Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 Missing Context에 대한 사용자 답변을 문서/정책 초안으로 변환한다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 문서/정책 초안 파일을 생성하거나 수정하지 않는다. 초안에 들어갈 내용과 필요한 승인 조건만 제안한다.

사용자 답변은 승인 전까지 source of truth가 아니다.

이 skill은 `_source-of-truth-manager.md`의 하위 절차다. 문서 초안 작성 권한은 Source of Truth Manager의 승인 모델을 따른다. 사용자 답변이나 명시 요청 없이 정책 DRAFT를 만들 수 없고, 별도 승인 없이 APPROVED 문서나 registry를 수정할 수 없다.

사용자 지정 scope는 APPLY 충분조건이 아니다. 문서 초안 또는 적용 묶음이 source of truth 정합성을 깨뜨리면 적용을 제안하지 않는다.

"A로 하자", "그 방향으로 가자", "좋아", "진행해", "추천대로", "알아서 반영해", "나중에 보자", "일단 해" 같은 표현은 Apply Approval로 해석하지 않는다. Direction Approval, Draft Approval, Apply Approval을 분리한다.

## 역할

- Missing Context 질문과 사용자 답변을 정리한다.
- 답변을 rules, domain document, behavior document, architecture note, decision log 후보로 변환한다.
- Project Context 답변을 `_project-context.md`의 Project Context Template 후보로 변환한다.
- 문서 초안이 어떤 판단을 소유하는지 명시한다.
- 사용자 승인 전까지 파일 저장 또는 source of truth 확정을 하지 않는다.
- 사용자가 변경 방향을 승인하면 target file list와 변경안을 제안한다.
- 사용자가 실제 적용을 명시적으로 승인하면 승인된 범위 안에서만 파일 저장 또는 변경을 수행한다.

## 출력 후보

```text
project-context.yml 또는 docs/project/context.md 초안
rules.yml 초안
docs/domain/*.md 초안
docs/behavior/*.md 초안
docs/user-flows/*.md 초안
docs/ui-ux/*.md 초안
docs/frontend/*.md 초안
docs/design-system/*.md 초안
docs/architecture/*.md 초안
docs/testing/*.md 초안
docs/operations/*.md 초안
docs/integration/*.md 초안
docs/decisions/*.md 초안
document-registry.yml 업데이트 초안
```

## 수행 절차

1. 사용자 답변을 Missing Context 항목과 매핑한다.
2. 각 답변이 어떤 판단 영역을 확정하는지 식별한다.
3. 적절한 문서 초안을 만든다.
4. 각 문서 초안에 `owns` 또는 동등한 "판단 소유 영역"을 명시한다.
5. document registry 업데이트 초안을 만든다.
6. 영향받는 source of truth 문서, Task Contract, prompt, verification result를 식별한다.
7. `Known Conflicts After Apply`를 작성한다.
8. Known Conflicts After Apply가 비어 있지 않으면 APPLY를 제안하지 않는다.
9. 사용자에게 변경 방향 승인을 요청한다.
10. 변경 방향 승인 후 target file list, 변경 목록, DRAFT diff/proposal을 보여준다.
11. 사용자가 Files Proposed for Apply 전체를 명시적으로 APPLY 승인한 뒤에만 source of truth 문서 저장 또는 변경을 수행한다.
12. 적용 후 문서 간 일관성, registry status, Plan/Task/prompt/verification result 영향을 검증한다.

## 문서 초안 생성 조건

문서 초안은 다음 중 하나가 있을 때만 생성할 수 있다.

1. 사용자가 Missing Context 질문에 답했다.
2. 사용자가 특정 정책 초안 생성을 명시적으로 요청했다.
3. 이미 APPROVED 문서의 내용을 재구성하는 경우다.

다음은 금지한다.

- Agent가 자기 추천안을 근거로 정책 DRAFT를 바로 생성하는 것
- Agent가 구현 편의를 위해 정책 문서를 사후 작성하는 것
- Agent가 코드 변경 후 그 코드에 맞춰 정책 문서를 만드는 것

사용자의 "알아서 해", "추천대로", "빨리 해", "그냥 맞춰줘", "문서도 같이 고쳐" 같은 표현은 APPROVED 반영 승인으로 해석하지 않는다. 모호하면 다시 질문한다.

## 문서 초안에 포함할 내용

- 문서 목적
- 이 문서가 소유하는 판단 영역
- Project Context라면 프로젝트 목적, projectType, 사용자, 운영 전제, risk, allowedSimplifications, forbiddenSimplifications
- 사용자 답변으로 확정된 정책
- 적용 범위
- 비범위
- 관련 문서
- 아직 미결인 질문

## 규칙

- 사용자 답변에 없는 정책을 임의 추가하지 마라.
- 모호하면 다시 질문하라.
- 문서 초안에는 "이 문서가 어떤 판단을 소유하는지"를 명시하라.
- DRAFT 초안을 APPROVED source of truth처럼 사용하지 마라.
- document registry에 등록하더라도 사용자 승인 전 status는 DRAFT로 취급한다.
- APPROVED 전환은 별도 사용자 승인 문장이 있을 때만 수행한다.
- 승인된 target file list 밖 파일을 수정하지 마라.
- 테스트 전략 답변은 TEST_STRATEGY 문서 초안으로 분리하고, DATA_MODEL/MIGRATION_POLICY/IMPLEMENTATION_ARCHITECTURE와의 관계를 명시한다.
- H2, Testcontainers, test profile, test-specific migration, mock/fake/stub 같은 선택은 사용자 답변에 있더라도 승인 전까지 implementation 근거로 사용하지 않는다.
- Missing Context가 해결되기 전에는 코드 수정, revision 실행, 테스트 전략 변경, Task Contract 수정, complete 진행을 하지 않는다.
- 사용자 답변 없이 TEST_STRATEGY / MIGRATION_POLICY DRAFT를 생성하지 않는다.
- 사용자 답변 없이 FRONTEND_UX_CRITERIA / DESIGN_SYSTEM / UI_PATTERN / USER_FLOW / INTERACTION_SPEC / FRONTEND_ARCHITECTURE DRAFT를 생성하지 않는다.
- source of truth 변경이 Plan, Task, prompt, verification result를 무효화하면 적용 후 반드시 invalidation을 보고한다.
- 사용자가 특정 파일만 수정하라고 해도 정합성상 필수 파일이 빠지면 APPLY를 제안하지 않는다.
- 영향 분석에서 발견한 충돌을 warning으로 낮추지 않는다.
- `Known Conflicts After Apply`가 비어 있지 않으면 APPLY 금지다.
- Direction Approval을 Apply Approval로 승격하지 마라.
- Prompt Draft Approval을 Prompt Execution Approval로 승격하지 마라.

## Cross-Cutting Policy 초안 규칙

사용자 답변이 cross-cutting policy를 확정한다면 적절한 문서 초안으로 변환한다.

- Project Context 답변: `_project-context.md`의 Project Context Template 기반 초안
- 사용자 흐름/상호작용 답변: USER_FLOW 또는 INTERACTION_SPEC 초안
- Frontend UI/UX 답변: FRONTEND_UX_CRITERIA 초안
- Design system/visual pattern 답변: DESIGN_SYSTEM 또는 UI_PATTERN 초안
- Frontend architecture 답변: FRONTEND_ARCHITECTURE 초안
- DB/Persistence 답변: DATA_MODEL 또는 MIGRATION_POLICY 초안
- Test Strategy 답변: TEST_STRATEGY 초안
- API/Error 답변: API_CONTRACT 또는 ERROR_POLICY 초안
- External Integration 답변: INTEGRATION_POLICY 초안
- Batch 답변: BATCH_OPERATION_POLICY 초안
- Operation/Infra 답변: OPERATION 또는 INFRA_POLICY 초안
- Dependency/build tool 답변: DEPENDENCY_POLICY 또는 IMPLEMENTATION_ARCHITECTURE 초안

각 초안에는 다음을 포함한다.

- 이 문서가 소유하는 판단 영역
- 허용되는 방식
- 금지되는 방식
- testRequirements 또는 implementationConstraints에 반영할 항목
- 아직 미결인 항목

Frontend UI/UX 초안에는 다음을 포함한다.

- 대상 화면과 사용자 목표
- 사용자 흐름과 주요 행동
- 정보 우선순위와 primary action
- 기본, 로딩, 빈 상태, 오류, 권한 없음, 성공 상태
- 반응형 기준과 최소 지원 viewport
- keyboard/focus, label, 접근성 기준
- 텍스트 overflow, 긴 문구, 숫자, CJK 표시 기준
- 디자인 시스템 또는 따라야 할 화면 패턴
- 허용되는 styling, layout, motion 범위
- visual QA 방식과 acceptance criteria
- route/page/component/layout/styling/testRequirements에 반영할 항목
- 아직 미결인 UI/UX 결정

Project Context 초안에는 하네스 검증 목적, 하네스 약점 발견 목적, skill validation 목적, prompt governance validation 목적을 넣지 않는다. 사용자가 별도로 하네스 평가 기록을 원하면 `harness-evaluation-note`, `harness-test-log`, `harness-experiment-plan` 같은 project source of truth 밖 artifact를 제안한다.

Dependency 초안에는 다음을 포함한다.

- 승인된 dependency/plugin/annotation processor/code generation tool 이름
- 도입 목적
- 허용 범위
- runtime 노출 여부
- 금지되는 대체 dependency
- 기존 스택 안에서 구현하지 않는 이유

## 다음 단계

- 사용자가 변경 방향을 승인하면 실제 적용 대상 파일과 변경안을 제안한다.
- 사용자가 실제 적용을 명시적으로 승인하면 source of truth 파일과 document registry 업데이트를 승인된 범위 안에서만 반영한다.
- 적용 후 known conflict가 남는다면 적용하지 않고 Source of Truth Change Request를 다시 작성한다.
- 문서 준비도가 충족되면 `plan-task.md`로 이동한다.
- 여전히 부족하면 `_missing-context.md`로 돌아간다.
