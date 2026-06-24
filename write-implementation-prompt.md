# Write Implementation Prompt Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: 승인된 작업 기준서를 구현 지시서로 바꿀 때 사용한다.
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

이 skill은 승인된 작업 기준서를 구현 에이전트용 prompt로 변환한다.

V2에서는 implementation-prompt를 "구현 지시서"로 사용자-facing 표현한다. Prompt artifact는 `_artifact-metadata.md`의 metadata, `_artifact-templates.md`의 `Prompt Artifact Template`, `_status-machine.md`의 status, `_approval-reference.md`의 approval reference를 따른다.

구현 지시서를 만들거나 수정하기 전에는 `_source-of-truth-manager.md`의 문서 배치, 현재 작업 포인터, 기본 읽기 경로, active/history 분리 규칙을 따른다. 저장 전에는 `_artifact-templates.md`의 Document Placement Check를 작성하고, 새 파일이 필요하면 왜 기존 문서에 추가하지 않는지 보고한다.

구현 Agent가 완료된 task history, 과거 verification, completion, old prompt를 기본으로 읽어야만 현재 작업을 이해할 수 있다면 prompt를 만들지 말고 현재 작업 포인터 또는 active index/history 정리를 먼저 요구한다.

prompt 관련 차단 사유를 사용자에게 말할 때는 내부 용어를 나열하지 않고 "이 구현 지시서는 지금 기준으로 바로 사용할 수 없습니다"처럼 행동 중심으로 설명한다.

구현 지시서에는 Project Context 요약이 포함되어야 한다. 구현 Agent는 프로젝트가 테스트 베드인지, 실제 서비스인지, 데이터 정합성이나 추적 가능성이 중요한지, 어떤 단순화가 허용/금지되는지 알아야 한다.

구현 지시서는 코드 변경 지시에서 끝나면 안 된다. 구현 Agent가 작업 기준서의 범위, 금지 범위, `acceptanceCriteria`, `testRequirements`, `verificationCommands`를 기준으로 구현 결과를 대조하고, 검증과 완료 가능 여부까지 보고하도록 지시해야 한다. 구현만 끝났다는 보고는 CDD 완료가 아니다.

구현 지시서를 만들 수 없을 때는 Action-first, diagnostics-later를 따른다. prompt metadata나 approval reference 문제는 기본 응답에서 뒤로 미루고, 무엇을 먼저 선행해야 하는지로 안내한다.

구현 지시서는 `_sot-packet.md`의 작업 기준 묶음을 포함해야 한다. 작업 기준 묶음이 없거나 approvedSotDocuments, allowedScope, forbiddenScope, verificationCommands, userApprovalRequiredFor가 불명확하면 구현 지시서를 만들지 말고 아직 필요한 결정을 질문한다.

구현 지시서는 `_readiness-gates.md`의 준비 상태 확인 결과를 포함해야 한다. 제품 기준 준비 상태 또는 기술 설계 준비 상태가 `NOT READY`이면 구현 지시서를 만들지 말고 아직 필요한 결정을 질문한다.

구현 지시서가 DB table, column, migration, repository, API DTO 작업을 열려면 Storage Intent Check가 `DB_DESIGN_ALLOWED`여야 한다. API path나 request/response shape 작업을 열려면 Behavior Contract Check가 `API_DESIGN_ALLOWED`여야 한다. status enum이나 state transition 작업을 열려면 State Meaning Check가 `STATE_MODEL_ALLOWED`여야 한다.

구현 지시서가 사용자 또는 운영자가 접하는 기능을 열려면 상호작용 방식 확인 결론이 `상호작용 설계 가능`이어야 한다. 웹/모바일 UI 작업을 열려면 프론트엔드 UX 확인 결론이 `FRONTEND_UX_ALLOWED`여야 한다. 성능, 보안, 조회, 권한, 실패 처리, 재시도, 로그/감사 판단을 포함하면 운영/품질 기준 확인 결론이 `설계 가능`이어야 한다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 구현 지시서 파일을 생성하거나 수정하지 않는다. prompt draft 생성 후보를 제안할 수는 있지만 실제 prompt artifact 작성은 `PATCH_AUTHORIZED`, `APPLY_AUTHORIZED`, 또는 허용된 write-implementation-prompt 단계의 명시 승인 후에만 가능하다.

## 빠른 탐색

- 처음에는 "최소 읽기 경로", "시작 조건", "금지 조건", "사용자 승인"만 먼저 본다.
- 구현 지시서 시작 가능 여부는 "시작 조건"과 "금지 조건"을 본다.
- 구현 지시서에 포함할 내용은 "구현 prompt에 포함할 내용"을 본다.
- 준비 상태 확인 예시는 "구현 prompt 준비 상태 확인 예시"를 본다.
- 구현 에이전트에게 줄 지시는 "구현 에이전트 지시"를 본다.
- 임의 결정 금지와 테스트 전략은 "구현 에이전트가 임의로 정하면 안 되는 항목", "테스트 전략 coverage 확인"을 본다.
- 기존 artifact 사용 가능 여부와 metadata는 "Artifact Legitimacy Check", "Prompt Metadata 예시"를 본다.
- 승인과 중단은 "미확정 결정 정지 규칙", "사용자 승인"을 본다.

## 최소 읽기 경로

구현 지시서 요청이면 먼저 `cdd-audit` 실행 경로 규칙에 따라 brief 결과와 승인된 작업 기준서만 읽는다. 사용자가 PATH를 설정했다고 가정하지 말고, PATH 명령이 없으면 CDD skill root의 `bin/cdd-audit` 절대 경로를 시도한다. 이 경로는 시작 조건과 금지 조건을 대체하지 않는다. 시작 조건이 충족되고 새 결정, 정책 충돌, 위험 변경이 없으면 구현 지시서를 내부 실행 기준으로 작성하고, 사용자가 실제 구현까지 요청한 경우 같은 요청 범위 안에서 이어간다.

작업 기준 묶음이 없거나 readiness, metadata, approval, artifact legitimacy가 불명확할 때만 `_sot-packet.md`, `_readiness-gates.md`, `_artifact-metadata.md`, `_artifact-templates.md`, `_approval-reference.md`, `_implementation-rules.md`, `_user-facing-language.md`를 연다.

## 시작 조건

다음이 모두 충족되어야 한다.

- 작업 기준서가 존재한다.
- Project Context가 존재한다.
- Task status가 APPROVED다.
- `documentCoverage.status`가 READY다.
- 모든 `dependsOn` Task가 COMPLETE 상태다.
- source of truth가 VALIDATED 상태다.
- known source of truth conflict가 없다.
- 아직 결정되지 않은 항목이 없다.
- 기존 prompt가 있다면 legitimacy check를 통과했다.
- 구현 지시서 저장 위치가 기존 문서 구조와 일치한다.
- 구현 지시서 저장 전 사용자 보고에 수정할 파일, 새로 만들 파일, 기존 문서 구조와 맞는지, 분리 후보, 유지 후보, 삭제/보존/비-SOT 분류 후보, README/index 갱신 필요 여부가 포함된다.
- `requiredDocuments`가 비어 있지 않거나, Task가 도메인/아키텍처/행위/정책 판단을 전혀 요구하지 않는 단순 기술 작업이다.
- 작업 기준서에서 작업 기준 묶음을 만들 수 있다.
- 작업 기준서에 제품 기준 준비 상태와 기술 설계 준비 상태가 `READY`로 기록되어 있다.
- 작업에 필요한 Storage Intent Check, Behavior Contract Check, State Meaning Check가 각각 허용 결론으로 기록되어 있다.
- 작업에 필요한 상호작용 방식 확인, 프론트엔드 UX 확인, 운영/품질 기준 확인이 허용 결론으로 기록되어 있다.
- 웹/모바일 UI 작업이면 requiredDocuments의 승인 문서 안에서 FRONTEND_UX_CRITERIA, USER_FLOW 또는 INTERACTION_SPEC, DESIGN_SYSTEM 또는 UI_PATTERN, FRONTEND_ARCHITECTURE 역할 coverage가 확인된다.
- 웹/모바일 UI 작업이면 분석 결과를 레이아웃, 정보 우선순위, 금지 패턴, 반응형, 브라우저/스크린샷 검증 기준으로 고정한 `uiImplementationContract`가 작업 기준서에 포함되어 있다.
- 사용자가 prompt 생성을 승인했거나, prompt 검토 단계로 진행하라고 지시했거나, 실제 구현/수정/정리 요청이 명확해서 구현 지시서 작성이 내부 실행 기준으로 필요한 상태다.
- prompt draft 생성 승인이 `PROMPT_DRAFT_APPROVAL`, 현재 workflow상 허용된 write-implementation-prompt 단계, 또는 명확한 실행 요청에 포함된 내부 지시서 작성 필요로 확인된다.

## 금지 조건

- 사용자 요청이 `ANALYSIS_ONLY`이면 prompt 파일을 생성하거나 수정하지 마라.
- 사용자 요청이 `PROPOSAL_ONLY`이면 prompt 변경안을 제안만 하고 저장하지 마라.
- 작업 기준서가 APPROVED가 아니면 프롬프트를 만들지 마라.
- documentCoverage가 READY가 아니면 프롬프트를 만들지 마라.
- 제품 기준 준비 상태 또는 기술 설계 준비 상태가 `NOT READY`이면 프롬프트를 만들지 마라.
- 상호작용 방식 확인이 없거나 `상호작용 설계 보류`이면 사용자/운영자 인터페이스, 화면, CLI 명령, API surface, 배치 실행 방식을 포함하는 프롬프트를 만들지 마라.
- 프론트엔드 UX 확인이 없거나 `FRONTEND_UX_BLOCKED`이면 route, page, component, layout, styling, motion, visual QA 기준을 포함하는 프롬프트를 만들지 마라.
- 승인 문서 안의 FRONTEND_UX_CRITERIA, USER_FLOW 또는 INTERACTION_SPEC, DESIGN_SYSTEM 또는 UI_PATTERN, FRONTEND_ARCHITECTURE 역할 coverage 없이 웹/모바일 UI의 route, page, component, layout, styling, motion, visual QA 기준을 포함하는 프롬프트를 만들지 마라.
- 웹/모바일 UI 작업인데 `uiImplementationContract`가 없으면 컴포넌트 수정, layout, styling, motion, visual QA 지시를 포함하는 프롬프트를 만들지 마라.
- 프로젝트가 루트 `DESIGN.md` 같은 단일 기준 문서를 승인했다면 파일 분리를 요구하지 않는다. 단, 그 문서 안에서 각 역할의 경계가 명확해야 한다.
- Storage Intent Check가 없거나 `DB_DESIGN_BLOCKED`이면 DB table, column, migration, repository, API DTO를 포함하는 프롬프트를 만들지 마라.
- Behavior Contract Check가 없거나 `API_DESIGN_BLOCKED`이면 API path, method, route, controller, request/response shape를 포함하는 프롬프트를 만들지 마라.
- State Meaning Check가 없거나 `STATE_MODEL_BLOCKED`이면 status enum, status column, state transition을 포함하는 프롬프트를 만들지 마라.
- 운영/품질 기준 확인이 없거나 `설계 보류`이면 performance, security, operation, sorting, search, pagination, permission, retry, logging, audit 정책을 포함하는 프롬프트를 만들지 마라. 성능 위험 후보 탐지 또는 개선을 열린 범위로 포함하는 프롬프트도 만들지 마라.
- requiredDocuments가 비어 있는데 도메인/아키텍처 작업이면 멈춰라.
- Task 없이 구현 prompt를 만들지 마라.
- 미확정 결정이 해결되지 않았으면 구현 prompt 또는 revision prompt를 만들지 마라.
- testRequirements 축소, DB integration test 대체, 테스트 이연을 prompt에서 임의로 지시하지 마라.
- source of truth 변경이 필요하면 prompt를 만들지 말고 Source of Truth Change Request로 넘겨라.
- source of truth 변경을 구현 prompt에 섞지 마라.
- partial source of truth update나 known conflict가 남은 source of truth 묶음을 근거로 prompt를 만들지 마라.
- 작업 기준서가 변경된 source of truth와 정합하지 않으면 prompt를 만들지 말고 planning으로 되돌려라.
- 선행 Task가 COMPLETE가 아니면 후속 Task prompt를 만들지 마라.
- 현재 Task 또는 선행 Task의 미확정 결정을 "나중에"로 미루고 prompt를 만들지 마라.
- 기존 prompt file이 존재한다는 이유만으로 정상 baseline으로 사용하지 마라.
- 기존 prompt가 legitimacy check를 통과하지 못하면 보강/수정하지 말고 멈춰라.
- invalid prompt를 최신 harness 기준으로 보강해서 계속 사용하지 마라.
- 기존 문서 구조와 다른 파일 배치를 하려면 prompt를 저장하지 말고 사용자 확인을 받아라.
- 현재 기준과 과거 산출물이 충돌하면 prompt를 저장하지 말고 정합성 정리 질문으로 돌아가라.

Prompt 생성은 단순 문서 작성이 아니라 후속 구현을 여는 확인 지점이다.

Prompt draft 생성 또는 수정도 확인 지점이 필요한 행동이다.

Prompt draft를 생성/수정하려면 다음이 모두 충족되어야 한다.

1. Task status APPROVED
2. `documentCoverage` READY
3. 모든 `dependsOn` Task COMPLETE
4. source of truth VALIDATED
5. Known Conflicts 없음
6. 미확정 결정 없음
7. 사용자 Prompt Draft 생성 승인, 현재 workflow에서 명확히 허용된 write-implementation-prompt 단계, 또는 명확한 실행 요청에 포함된 내부 지시서 작성 필요
8. 기존 prompt가 있다면 legitimacy check 통과

위 조건이 없으면 기존 prompt가 있더라도 보강/수정하지 말고 멈춘다.

Prompt draft approval은 `PROMPT_DRAFT_APPROVAL`이고, 실제 구현 시작 승인은 `PROMPT_EXECUTION_APPROVAL`이다. 초안 승인만으로 구현을 시작하지 않는다.

구현 지시서 초안, 수정, 실행 승인 요청 전에는 `_approval-briefing-language.md`의 "승인 전 브리핑 형식"을 반드시 사용한다. 브리핑은 먼저 확인할 정책/작업 결정과 추천을 제시해야 한다. 승인 문장은 이 승인이 허용하는 작성/실행 작업, 아직 허용하지 않는 작업, 승인하면 고정되는 결정, 위험/중단 조건, 승인 후 실제로 진행할 일을 브리핑한 뒤에만 제시한다. 브리핑 없이 구현 지시서 승인 문장만 출력하지 않는다.

선행 Task 완료 정합성 정리 뒤 후속 Task의 구현 지시서 초안 작성을 요청하는 경우에도 같은 규칙을 적용한다. "다음에 실제로 진행할 문장:" 아래에 `<TASK-ID> 구현 지시서 초안 작성을 승인합니다.`만 제시하지 말고, 이번 승인의 목적, 포함되는 것, 제외되는 것, 승인하면 고정되는 결정, 주의할 점, 승인 후 진행할 일을 먼저 브리핑한다. "승인하면 내가 진행할 일"만 나열하는 것도 금지한다. 단, 사용자가 다음 작업이나 현재 상태를 조회한 것뿐이면 구현 지시서 초안 작성 승인 요청으로 승격하지 않고 `_user-facing-language.md`의 "조회형 질문 응답 형식"으로 답한다. 이때도 다음 후보가 구현 지시서 초안 작성이면 목적, 포함 범위, 제외 범위, 주의할 점, 진행 후 가능해지는 것을 진행 후보 브리핑으로 설명한다.

다만 사용자가 이미 실제 구현, 문서 수정, cleanup/delete 실행, revision 실행까지 명확히 요청했고 구현 지시서 작성이 내부 실행 기준을 만드는 절차일 뿐이면, 구현 지시서 작성 뒤 새로 결정할 사항이 없는지 다시 판단한다. 새 제품 판단, 설계 판단, 위험 변경, 범위 확대, 기준 문서 충돌이 없으면 별도의 실행 승인 요청을 반복하지 않고 같은 요청 범위 안에서 `_implementation-rules.md`로 이어간다.

자동 실행 연계 조건:

- 사용자가 실제 실행까지 명확히 요청했다.
- 사용자가 "초안만", "계획만", "먼저 보여줘", "수정하지 마"라고 하지 않았다.
- 작업 지시서 작성 중 새 미확정 결정이 발견되지 않았다.
- 저장, 동작, 상태, 상호작용, 운영 기준이 충분하다.
- 웹/모바일 UI 작업이면 프론트엔드 UX 기준이 충분하다.
- 성능 위험 후보를 다룰 작업이면 조사 범위, 판단 근거, 허용된 수정 범위가 충분하다.
- allowedScope, forbiddenScope, verificationCommands가 명확하다.
- migration, 데이터 삭제, public API 제거, dependency 대량 변경, 되돌리기 어려운 cleanup/delete가 없다.
- 기존 artifact legitimacy가 확인됐다.

자동 실행 연계를 하면 안 되는 경우:

- 사용자가 초안 검토를 명시했다.
- 지시서 작성 중 미확정 결정, 정책 충돌, 기준 문서 변경 필요가 발견됐다.
- 실행하려면 사용자 요청 범위를 넓혀야 한다.
- 위험 변경 또는 사람 확인 지점이 있다.
- 선행 Task나 approval reference가 불명확하다.

자동 실행 연계가 가능한 경우 사용자-facing 보고는 다음처럼 끝낸다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
작업 지시서는 내부 실행 기준으로 작성하고, 새로 결정할 사항이 없으므로 같은 요청 범위 안에서 바로 실행합니다.

진행할 작업:
- 구현 지시서 작성
- 실행 가능 여부 확인
- 구현 또는 문서 수정
- 검증
- 결과 보고

진행하지 않을 작업:
- 기준 문서에 없는 정책 결정
- 요청 범위 밖 파일 수정
- 위험 변경
```

다음 상태의 선행 Task가 하나라도 있으면 후속 Task prompt 생성 금지다.

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

## 구현 prompt에 포함할 내용

- `_artifact-templates.md`의 `Prompt Artifact Template`
- artifact metadata
- approvalRefs
- status
- Task ID, title, type
- Goal
- projectContextRef
- projectContextSummary
- requiredDocuments 목록
- documentCoverage 상태
- 준비 상태 확인 결과
- Storage Intent Check, Behavior Contract Check, State Meaning Check 결과
- 상호작용 방식 확인 결과
- 운영/품질 기준 확인 결과
- implementationConstraints
- forbiddenApproaches
- uiImplementationContract
- acceptanceCriteria
- testRequirements
- 작업 기준서 기준 검증 지시
- `verificationCommands` 실행 또는 실행 불가 사유 보고 지시
- 완료 가능 여부 판단 지시
- source of truth 변경 금지
- source of truth 변경 필요 시 중단하고 `_source-of-truth-manager.md`로 라우팅하라는 지시
- known source of truth conflict가 발견되면 구현하지 말고 중단하라는 지시
- 선행 Task 미완료 또는 미확정 결정이 남은 상태에서는 구현하지 말고 중단하라는 지시
- 문서 밖 판단 금지
- 충돌 발견 시 중단/보고 규칙
- suggestions 분리 규칙
- 완료 보고 형식
- 작업 기준 묶음
- 제품 기준 문서와 기술 설계 기준 문서 모두에 대한 준수 지시
- 작업 시작 선언 형식: 작업 방식, 이번 작업 기준, 가능한 작업, 금지된 작업, 진행 전 필요한 승인, 검증 방법
- identifier type, DB key strategy, API-visible id representation, datetime format, error format, delete behavior, state transition behavior를 구현 세부사항으로 취급하지 말라는 지시
- 저장 의미, 동작 계약, 상태 의미가 없으면 table, column, API path, status enum을 만들지 말라는 지시
- 상호작용 방식이 없으면 화면, CLI 명령, API surface, 배치 실행 방식을 만들지 말라는 지시
- UI 구현 계약이 없으면 frontend route/page/component/layout/styling 작업을 하지 말라는 지시
- frontend 구현은 컴포넌트 단위 수정 목록보다 화면 단위 계약을 먼저 만족해야 한다는 지시
- 구현 후 브라우저/스크린샷을 UI 구현 계약과 대조하라는 지시
- 운영/품질 기준이 없으면 성능, 보안, 권한, 조회, 재시도, 로그/감사 정책을 임의로 정하지 말라는 지시
- H2, Testcontainers, test profiles, test-specific migrations, mock/fake/stub strategies, alternative database dialects를 승인 문서 없이 도입하지 말라는 지시
- 테스트를 통과시키기 위해 승인되지 않은 dependency, profile, test DB, test migration, mock/fake/stub 전략을 추가하지 말라는 지시
- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library를 승인 문서 없이 추가하지 말라는 지시
- 승인 문서가 없으면 기존 스택 안에서 구현하라는 지시

## 구현 prompt 준비 상태 확인 예시

구현 prompt에는 다음 블록을 포함한다.

```text
준비 상태 확인
제품 기준 준비: READY / NOT READY
- 근거:
- 부족한 결정:
상호작용 방식 확인:
- 결론: 상호작용 설계 가능 / 상호작용 설계 보류 / 해당 없음
- 부족한 결정:
기술 설계 준비: READY / NOT READY
- 근거:
- 부족한 결정:
운영/품질 기준 확인:
- 결론: 설계 가능 / 설계 보류 / 해당 없음
- 부족한 결정:
구현 시작 가능 여부: READY / NOT READY
- 근거:
- 부족한 결정:
결론:
- 구현 가능 / 구현 보류
- 필요한 다음 행동:
```

내부 결론이 `IMPLEMENTATION_BLOCKED`이면 코드, 테스트, 설정, migration, dependency 변경을 금지한다. 내부 결론이 `IMPLEMENTATION_ALLOWED`인 경우에만 작업 기준 묶음의 allowedScope 안에서 구현한다. 구현 prompt에는 작업 기준 묶음, allowedScope, forbiddenScope, verificationCommands를 함께 포함한다.

`projectContextSummary` 예:

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

## 구현 에이전트 지시

prompt에는 반드시 다음 의미가 들어가야 한다.

- 승인된 requiredDocuments 기준으로만 구현하라.
- 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부 중 하나라도 `NOT READY`이면 구현하지 말고 아직 필요한 결정으로 보고하라.
- 승인된 작업 기준 묶음 밖 작업을 하지 마라.
- IMPLEMENTATION인데 작업 기준 묶음이 없으면 구현하지 말고 아직 필요한 결정으로 보고하라.
- 문서에 없는 도메인/아키텍처/행위/정책 판단을 하지 마라.
- 구현 세부사항은 판단할 수 있지만 정책 판단은 할 수 없다.
- Identifier type, DB key strategy, API-visible id representation, datetime format, error format, delete behavior, state transition behavior are not implementation details. If they are not defined in the approved documents, stop and report 아직 필요한 결정 instead of choosing a default.
- 상호작용 방식 확인이 `상호작용 설계 가능`이 아니면 화면, CLI 명령, API surface, batch 실행 방식, 저장 구조를 만들거나 제안하지 마라.
- 웹/모바일 UI 작업에서 `uiImplementationContract`가 없으면 route, page, component, layout, styling, motion, visual QA 기준을 만들거나 제안하지 마라.
- `uiImplementationContract`의 금지 패턴을 구현 편의로 완화하지 마라.
- 검증은 DOM 존재 여부나 테스트 통과만으로 끝내지 말고, 브라우저/스크린샷 결과를 UI 구현 계약의 레이아웃, 정보 우선순위, 금지 패턴, 반응형 기준과 대조하라.
- Storage Intent Check가 `DB_DESIGN_ALLOWED`가 아니면 table, column, migration, repository, API DTO를 만들거나 제안하지 마라.
- Behavior Contract Check가 `API_DESIGN_ALLOWED`가 아니면 API path, method, route, controller, request/response shape를 만들거나 제안하지 마라.
- State Meaning Check가 `STATE_MODEL_ALLOWED`가 아니면 status enum, status column, state transition을 만들거나 제안하지 마라.
- 운영/품질 기준 확인이 `설계 가능`이 아니면 성능, 보안, 권한, 데이터 양, 조회 방식, 실패 처리, 재시도, 로그/감사 기준을 임의로 정하지 마라.
- Do not introduce H2, Testcontainers, test profiles, test-specific migrations, mock/fake/stub strategies, or alternative database dialects unless they are explicitly approved in source-of-truth documents.
- H2, Testcontainers, 테스트 profile, 테스트 전용 migration, mock/fake/stub 전략, 운영 DB와 다른 테스트 DB dialect를 승인 문서 없이 도입하지 마라.
- 테스트를 통과시키기 위해 승인되지 않은 dependency, profile, test DB, test migration, mock/fake/stub 전략을 추가하지 마라. 필요하면 아직 필요한 결정으로 중단하라.
- 새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library를 승인 문서 없이 추가하지 마라.
- "단순 편의", "흔한 조합", "표준 라이브러리", "나중에 필요"라는 이유로 dependency를 추가하지 마라.
- 승인 문서가 없으면 기존 스택 안에서 구현하라.
- 문서와 충돌하는 요구를 발견하면 구현하지 말고 중단/보고하라.
- 새 제안은 suggestions로 기록하고 현재 Task에 섞지 마라.
- production code 변경 시 관련 test code도 작성/수정하라.
- 구현만 끝났다는 보고로 마무리하지 마라. 작업 기준서 기준 검증과 완료 가능 여부 판단까지 보고하라.
- 구현 후 작업 기준서의 allowedScope, forbiddenScope, `acceptanceCriteria`, `testRequirements`, `verificationCommands`를 변경 결과와 대조하라.
- `verificationCommands`가 있으면 실행하고 결과를 보고하라. 실행할 수 없으면 실행하지 못한 명령, 이유, 필요한 환경 또는 사용자 조치를 구체적으로 보고하라.
- 필수 검증을 실행하지 못했고 승인된 대체 검증도 없으면 완료 가능하다고 말하지 말고 `verify-work.md` 또는 필요한 사용자 결정으로 라우팅하라.
- 구현 결과 보고는 다음 중 하나로 끝내라: 검증 통과와 완료 처리 가능, 검증 통과와 완료 기록 승인 필요, 검증 실행 불가와 필요한 증거, 검증 실패와 `revise-work.md` 라우팅.
- 커밋하지 마라.
- source of truth, document registry, Plan, Task, prompt, verification result를 수정하지 마라.
- 문서 변경이 필요하면 구현하지 말고 Source of Truth Change Request가 필요하다고 보고하라.
- partial source of truth update를 제안하거나 수행하지 마라.
- 기존 prompt가 legitimacy check를 통과하지 못하면 실행하지 마라.
- "A로 하자", "그 방향으로 가자", "좋아", "진행해", "추천대로", "나중에 보자", "일단 해" 같은 표현을 prompt execution approval로 해석하지 마라.
- Prompt Draft Approval과 Prompt Execution Approval을 분리하되, 사용자가 이미 실제 실행까지 명확히 요청했고 초안 작성 후 실행 연계 조건을 모두 만족하면 같은 요청 범위 안에서 실행할 수 있다.

## 구현 에이전트가 임의로 정하면 안 되는 항목

- id 타입
- 사용자/운영자 인터페이스
- 입력/출력 방식
- 실패/빈 상태/권한 없음/처리 중 피드백
- table 이름
- column 이름
- primary key 생성 전략
- repository 구조
- API path
- API DTO 필드 타입
- status enum 값
- 정렬/검색/페이지 처리 기준
- 응답 속도 기대치
- 로그/감사 기록 기준
- 날짜/시간 포맷
- 오류 code
- 상태 변경 방식
- 삭제 방식
- H2 또는 embedded DB 도입
- Testcontainers 도입
- application-test.yml 또는 test profile 도입
- 테스트 전용 migration 도입
- 운영 DB와 다른 테스트 dialect 사용
- mock/fake/stub 전략 선택
- dependency 추가
- Gradle plugin 추가
- annotation processor 추가
- code generation tool 추가
- runtime-exposed library 추가

## 테스트 전략 coverage 확인

Repository/Flyway/DB migration 관련 Task에서 TEST_STRATEGY 또는 동등한 승인 문서가 없으면 구현 prompt 생성을 중단하고 아직 필요한 결정으로 돌려야 한다.

External integration, batch, infra/config Task도 대응하는 INTEGRATION_POLICY, BATCH_OPERATION_POLICY, OPERATION/INFRA_POLICY 문서가 없으면 구현 prompt를 만들지 않는다.

Mock, fake, stub, slice test, `@WebMvcTest`, `@DataJpaTest`, mocked service, mocked repository는 모두 TEST_STRATEGY 판단이다. 승인된 TEST_STRATEGY 없이 AI가 임의로 선택할 수 없다.

Bad:

```text
TEST_STRATEGY가 없으니 @WebMvcTest + mock으로 POST API 테스트를 작성한다.
```

Correct:

```text
TEST_STRATEGY가 없으므로 API 테스트 전략을 아직 필요한 결정으로 질문한다.
```

## Artifact Legitimacy Check

Prompt file이 디스크에 존재해도 자동 사용하지 않는다.

사용 전 다음을 확인한다.

- prompt가 어떤 workflow 단계에서 생성되었는가?
- 생성 당시 Prompt Draft Approval 또는 허용된 write-implementation-prompt 단계였는가?
- 생성 당시 Task status가 APPROVED였는가?
- 생성 당시 `documentCoverage`가 READY였는가?
- 생성 당시 모든 `dependsOn` Task가 COMPLETE였는가?
- 생성 당시 source of truth가 VALIDATED였는가?
- 미확정 결정 또는 Policy Conflict가 unresolved 상태였는데 생성된 것은 아닌가?
- 이후 source of truth 변경, Task 변경, verification 결과로 superseded 되었는가?
- 현재 harness 기준으로도 prompt 생성 조건을 만족하는가?
- artifact metadata에 approvalRefs, sourceOfTruthVersion, dependsOnSnapshot, generatedFrom이 기록되어 있는가?

하나라도 확인할 수 없거나 위반이 있으면 정상 prompt baseline으로 사용하지 않는다. 해당 prompt는 `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보로 보고하고, gate를 통과한 뒤 새 prompt를 생성해야 한다.

## Prompt Metadata 예시

```yaml
artifact:
  id: PROMPT-TASK-002-001
  type: implementation-prompt
  status: DRAFT
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: write-implementation-prompt
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
    - APPROVAL-PROMPT-TASK-002-DRAFT
  generatedFrom:
    - tasks/TASK-002.yml
  knownConflicts: []
  supersedes: []
  supersededBy: null
```

사용자-facing 보고에서는 "prompt"보다 "구현 지시서"를 우선 사용한다.

차단 상황에서는 다음 형식을 우선 사용한다.

```text
확인한 기준:
- ...

현재 판단:
- 아직 결정 필요

이유:
- 지금은 구현 지시서를 만들 수 없습니다.

먼저 정할 것:
1. 선행 작업을 마무리할지, 작업 순서를 바꿀지 결정해 주세요.
2. 필요한 테스트 방식이나 기준 문서 결정을 정해 주세요.
3. 새 구현 지시서를 만들어도 되는지 승인해 주세요.

내 추천:
- 먼저 남은 결정을 정리한 뒤 구현 지시서를 새로 작성합니다.

다음에 할 일:
아직 직접 진행하면 안 됩니다. 먼저 아래 중 하나를 선택해야 합니다.

선택지:
1. 선행 작업을 먼저 마무리한다.
2. 작업 순서를 바꾸도록 기준 문서와 작업 기준서를 정리한다.
3. 구현 지시서 작성을 보류한다.

제 추천:
- 먼저 선행 작업과 테스트 방식을 정리한 뒤 구현 지시서를 새로 작성합니다.

바로 답할 수 있는 문장:
"추천안대로 선행 작업과 테스트 방식을 정리할 질문을 먼저 만들어라."
```

기본 응답에서는 metadata, approvalRefs, legitimacy check, dependsOn gate, `current gate`, `next gate`, `readiness gate`, `Product Readiness`, `Engineering Readiness`, `Implementation Readiness`, `READY`, `NOT READY`, `Storage Intent Check`, `Behavior Contract Check`, `State Meaning Check` 같은 내부 진단표를 먼저 보여주지 않는다. `현재 gate`나 `다음 gate`는 "현재 상태", "다음 단계", "다음에 필요한 승인"으로 바꿔 말한다. 사용자가 "자세히" 또는 "내부 판정도 보여줘"라고 요청하면 그때 상세 표를 제공한다.

사용자 개입 없이 진행 가능한 경우에는 다음 형식으로 말한 뒤 실제로 구현 지시서 작성과 검증까지 수행한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
현재 기준으로 안전하게 진행할 수 있으므로, 요청 범위 안에서 다음 작업까지 진행합니다.

진행할 작업:
- 구현 지시서 작성
- 기존 문서 구조에 맞는 저장 위치 확인
- 분리 후보, 유지 후보, 삭제/보존/비-SOT 분류 후보 확인
- README/index 갱신 필요 여부 확인
- 작업 기준 묶음과 문서 coverage 확인
- 구현 시작 가능 여부 보고

진행하지 않을 작업:
- 사용자 승인 없는 구현 실행
- 기준 문서에 없는 정책 결정
- 기존 문서 구조와 다른 파일 배치
```

## 미확정 결정 정지 규칙

아직 필요한 결정이 있으면 허용 행동은 사용자 질문으로 되돌리는 것뿐이다.

- 코드를 수정하지 않는다.
- source of truth 문서 또는 registry를 수정하지 않는다.
- revision을 실행하지 않는다.
- 테스트 전략을 변경하지 않는다.
- 작업 기준서를 수정하지 않는다.
- prompt 또는 verification result를 수정하지 않는다.
- complete로 진행하지 않는다.

현재 Task 또는 선행 Task의 미확정 결정은 "나중에"로 미룰 수 없다. 미확정 결정이 남아 있으면 후속 Task prompt 생성, 후속 Task implementation, complete, verification 통과 모두 금지다.

## 사용자 승인

구현 prompt를 만든 뒤 즉시 구현하지 않는다. 사용자가 prompt를 검토하고 승인해야 `_implementation-rules.md`로 넘어간다.
