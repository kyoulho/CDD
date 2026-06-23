# Start Here Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: CDD-controlled task를 시작, 계획, 지시서 작성, cleanup/delete, 검증, 수정, 완료할 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

이 파일은 CDD Skill Layer의 최초 진입점이다. 사용자가 이 파일을 링크하고 목표를 말하면, AI는 이 지시를 최상위 작업 절차로 따른다.

## 빠른 탐색

- CDD 전체 흐름을 처음 시작하면 "전체 지휘 흐름"을 본다.
- public/internal 접근은 "Public/Internal 접근 정책"과 "Routing Table"을 본다.
- 바로 적용할 금지/허용 규칙은 "즉시 적용할 규칙"을 본다.
- 기준 문서 권위와 변경 요청은 "Source of Truth 권위 순서", "Source of Truth 변경 라우팅"을 본다.
- 선행 작업, artifact 정합성, CLI 사용은 각 gate 섹션을 본다.
- 사용자 보고는 "User-Facing Language"와 "중단 조건"을 본다.

## 핵심 용어

- 제품 기준 준비 상태: 무엇을 왜 만들 것인지에 대한 기획 준비도.
- 기술 설계 준비 상태: 제품 판단을 저장 구조, 상태, API, 코드 구조로 표현할 기준이 정해졌는지에 대한 설계 준비도.
- 구현 시작 가능 여부: 에이전트가 구현을 시작해도 되는지에 대한 실행 준비도.
- 이번 작업 기준 묶음: 이번 작업에서 따라야 할 승인된 기준 문서 묶음.
- 작업 기준서: 구현 전 작업 범위, 금지 범위, 검증 기준을 고정하는 작업 계약.
- 상호작용 방식 확인: 사용자 또는 운영자가 접하는 기능의 입력, 출력, 흐름, 실패와 피드백을 먼저 확인하는 절차.
- 저장 의미 확인: table, column, migration, repository, API DTO를 말하기 전에 무엇을 왜 저장하는지 확인하는 절차.
- 운영/품질 기준 확인: 성능, 보안, 권한, 조회, 재시도, 로그/감사, 운영 기준을 구현 전에 확인하는 절차.

## 경로 규칙

- 이 디렉터리가 CDD skill root다.
- 첫 public entrypoint는 `start-here.md`다.
- 내부 chain 파일은 같은 디렉터리의 상대 파일명으로 참조한다.
- CDD 본체 경로와 대상 프로젝트의 제품/기술 기준 문서 경로를 섞지 않는다.

## Public/Internal 접근 정책

Public entrypoint만 task entrypoint가 될 수 있다. Internal module은 decision, rule, reference 역할만 하며 단독으로 `IMPLEMENTATION_ALLOWED`, `APPLY_AUTHORIZED`, `PATCH_AUTHORIZED`, `COMPLETE`를 만들 수 없다.

사용자가 internal module만 지정하면 Codex는 그 파일만 기준으로 작업을 실행하지 말고, 가장 가까운 public entrypoint를 선언한 뒤 그 흐름으로 라우팅한다.

CDD 본체 문서는 제품 기준 문서가 아니다. 실제 구현 기준은 대상 프로젝트의 제품 기준 문서, 기술 설계 기준 문서, 승인된 작업 기준 묶음이다.

## Routing Table

User intent:

- "start a task" -> `start-here.md`
- "plan this task" -> `plan-task.md`
- "write a Codex prompt" -> `write-implementation-prompt.md`
- "delete/cleanup/remove legacy" -> `cleanup-delete.md`
- "verify this result" -> `verify-work.md`
- "revise after verification" -> `revise-work.md`
- "complete/report" -> `complete-work.md`

Internal module direct mention:

- `_readiness-gates.md` 직접 호출 -> `start-here.md` 또는 `plan-task.md`로 라우팅한다.
- `_sot-packet.md` 직접 호출 -> `start-here.md` 또는 `plan-task.md`로 라우팅한다.
- `_implementation-rules.md` 직접 호출 -> `write-implementation-prompt.md` 또는 `start-here.md`로 라우팅한다.
- 그 밖의 `_*.md` 직접 호출 -> 가장 가까운 public entrypoint를 선언하고, 내부 모듈은 chain 안에서만 읽는다.

## 즉시 적용할 규칙

- 모든 요청은 먼저 `_work-mode.md`를 읽고 작업 모드를 판별하라.
- 사용자 요청이 설명, 설계, 문서 수정, 구현, 삭제, 검증 중 무엇인지 애매하면 바로 작업하지 말고 먼저 질문한다.
- 애매하면 먼저 질문한다.
- 애매한 요청을 임의로 해석하지 않는다.
- 애매한 요청을 구현 요청으로 승격하지 않는다.
- 애매한 요청을 파일 수정 승인으로 해석하지 않는다.
- 애매한 요청을 삭제 승인으로 해석하지 않는다.
- "정리해줘", "이거 진행해", "구조 잡아줘", "다음 단계로 가자", "고쳐줘", "문서 반영해", "설계해", "구현해도 될까?"처럼 작업 성격을 하나로 확정할 수 없는 요청은 가장 제한적인 방식으로 멈추고 사용자에게 자연어로 묻는다.
- 작업 방식을 판별한 뒤 `_sot-packet.md`를 확인하고, 이번 작업 기준 묶음이 있는지 확인하라.
- `_readiness-gates.md`를 확인하고 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부를 판정하라.
- 작업 시작 전 `_sot-packet.md`의 형식으로 작업 방식, 이번 작업 기준, 가능한 작업, 금지된 작업, 진행 전 필요한 승인, 검증 방법을 선언하라.
- 작업 모드는 `CLARIFICATION_NEEDED`, `ANALYSIS_ONLY`, `PROPOSAL_ONLY`, `PATCH_AUTHORIZED`, `APPLY_AUTHORIZED`, `IMPLEMENTATION`, `DOCUMENT_ONLY`, `CLEANUP_DELETE` 중 하나로 분류한다.
- 사용자가 "분석만", "수정하지 마", "원인만", "검토만", "제안만"이라고 말하면 `ANALYSIS_ONLY`로 처리하고 파일을 생성, 수정, 삭제하지 마라.
- `ANALYSIS_ONLY`에서는 rollback도 파일 수정이므로 수행하지 마라.
- 수정 대상 파일을 제안하는 것은 허용되지만 실제 수정은 `PATCH_AUTHORIZED` 또는 `APPLY_AUTHORIZED` 전까지 금지다.
- 분석/제안에서 패치로 전환하려면 "위 분석에 따라 CDD skill 파일 수정을 승인합니다"처럼 범위가 분명한 명시 승인이 필요하다.
- "좋아", "진행해", "다음", "반영해" 같은 말만으로 구현, 문서 수정, 파일 수정, 삭제/정리를 시작하지 마라.
- 사용자 요청을 바로 구현하지 마라.
- 먼저 `_authority-boundary.md`를 읽고 판단 권한 경계를 확인하라.
- V2 표준인 `_artifact-metadata.md`, `_artifact-templates.md`, `_status-machine.md`, `_approval-reference.md`, `_user-facing-language.md`를 확인하라.
- 새 프로젝트를 시작하거나 프로젝트 성격이 불명확하면 `_project-context.md`를 읽고 Project Context를 먼저 확인하라.
- 새 프로젝트를 시작할 때는 사용자의 자연스러운 의도에서 Project Context를 먼저 추론하라.
- 사용자가 이미 "연습용", "실서비스 출시 목적 아님", "로컬에서 해보면 됨"이라고 말했으면 이를 Project Context 초안으로 받아들이고 같은 목적을 다시 묻지 마라.
- 사용자-facing 질문에서 "CDD test bed", "weakness discovery", "skill validation", "prompt governance validation"을 선택지로 노출하지 마라.
- 사용자가 이미 연습용 프로젝트라고 말했으면 `PRACTICE_PROJECT`로 보고 다음 제품/도메인 관련 미확정 결정으로 이동하라.
- Project Context가 없으면 source of truth 문서, Plan, Task, 구현 지시서를 만들지 마라.
- 문서 준비도 확인 없이 Plan/Task를 만들지 마라.
- 제품 기준 준비 상태와 기술 설계 준비 상태가 모두 `READY`가 아니면 Plan/Task를 만들지 마라.
- 사용자 또는 운영자가 접하는 기능인데 상호작용 방식이 정해지지 않았으면 화면, CLI 명령, API surface, 배치 실행 방식, 저장 구조를 제안하지 마라.
- 입력, 출력, 실패, 빈 상태, 권한 없음, 처리 중 피드백이 비어 있으면 제품 기준 준비 상태를 `READY`로 보지 마라.
- 웹/모바일 UI 작업인데 승인 문서 안에 `FRONTEND_UX_CRITERIA`, `USER_FLOW` 또는 `INTERACTION_SPEC`, `DESIGN_SYSTEM` 또는 `UI_PATTERN`, `FRONTEND_ARCHITECTURE` 역할이 명확히 기록되어 있지 않으면 화면 구조, route, page, component, layout, styling, motion, visual QA 기준을 먼저 제안하지 마라. 별도 파일 경로를 강제하지 말고, 프로젝트가 승인한 루트 `DESIGN.md` 같은 단일 기준 문서가 해당 역할을 소유하면 그 구조를 존중한다.
- 웹/모바일 UI 작업에서 분석 결과가 `uiImplementationContract`로 고정되어 있지 않으면 컴포넌트 수정으로 바로 들어가지 마라. 계약에는 레이아웃, 정보 우선순위, 금지 패턴, 반응형 기준, 브라우저/스크린샷 검증 기준이 있어야 한다.
- 저장 의미가 정해지지 않았으면 table, column, migration, repository, API DTO를 제안하지 마라.
- 동작 계약이 정해지지 않았으면 API path, method, route, request/response shape를 제안하지 마라.
- 상태 의미가 정해지지 않았으면 status enum, status column, state transition을 제안하지 마라.
- 성능, 보안, 운영/품질 기준이 비어 있으면 안전하다고 가정하지 말고 사용자에게 질문하라.
- Plan/Task 없이 구현 프롬프트를 만들지 마라.
- 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부 중 하나라도 `NOT READY`이면 구현하지 마라.
- 사용자 승인 없이 구현하지 마라.
- 구현 후 테스트만으로 완료하지 마라.
- 구현 결과를 문서, 정책, Task와 대조 검증하라.
- source of truth 변경 요청은 직접 적용하지 말고 `_source-of-truth-manager.md`로 라우팅하라.
- 사용자 승인 없이 source of truth, document registry, Plan, Task, prompt, verification result를 수정하지 마라.
- Source of Truth Manager는 사용자 요청을 그대로 파일 수정으로 실행하는 executor가 아니다.
- 사용자가 범위를 좁혀도 source of truth 정합성을 깨뜨리면 APPLY를 거부한다.
- "A로 하자", "그 방향으로 가자", "좋아", "진행해", "추천대로", "알아서 반영해", "나중에 보자", "일단 해" 같은 표현을 더 높은 권한 승인으로 해석하지 마라.
- 변경 방향 승인, DRAFT 승인, APPLY 승인, prompt draft 승인, prompt execution 승인을 분리하라.
- 사용자의 의도를 추측해서 파일을 수정하지 마라.
- 현재 Task 또는 선행 Task의 미확정 결정을 "나중에"로 미루고 후속 Task로 진행하지 마라.
- 현재 상태에 존재하는 artifact를 자동 신뢰하지 마라.
- 기존 artifact를 사용하기 전에 현재 harness 확인 지점을 통과해 생성됐는지 legitimacy check를 수행하라.
- 작업 기준서, 구현 지시서, 검증 결과, 완료 기록을 만들거나 수정하기 전에 대상 프로젝트의 기존 문서 배치 구조를 확인하라.
- 기존 문서 구조와 다른 파일 배치를 하려면 auto-stop하고 전체 문서 구조 변경안과 사용자 승인을 요구하라.
- source of truth 권위 순서를 확인하라. 대상 프로젝트가 별도 우선순위를 명시하지 않았다면 현재 사용자 지시, 대상 저장소의 작업 규칙 파일, CDD harness rules, approved source of truth documents, task-specific approved plan/prompt, implementation files, 보조 자료 순서로 본다.
- 저장소 전체 문서가 자동으로 기준 문서가 아니다. 이번 작업 기준 묶음에 포함된 approved SOT만 작업 기준으로 삼는다.
- README, generated docs, indexing docs, memory/recall notes, previous assistant responses, archive/superseded documents는 기본적으로 active source of truth가 아니다.
- 현재 기준, 과거 기록, 보조 자료를 먼저 분류하라. 과거 task/completion/verification/prompt는 그 시점의 사실 기록이며, active 기준으로 승격된 근거가 없으면 현재 기준이 아니다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference는 기본 읽기 경로에서 제외하고 보조 자료로만 취급하라.
- 대상 프로젝트에 문서 구조 판단이 필요한 흔적이 있으면 먼저 `cdd-audit docs --root <project> --format text --fail-on never`를 실행하라. 흔적에는 `docs/README.md`, document registry, `docs/project/current-work.md`, 작업 기준서, 검증/완료 기록, 후속 task/완료 처리/구현 지시서/cleanup-delete 요청이 포함된다.
- `cdd-audit`가 없거나 실패하면 같은 항목을 수동 확인으로 대체하고, 사용자에게 "cdd-audit 실행 불가, 수동 확인으로 대체"와 이유를 보고하라.
- `cdd-audit` 결과에 차단 항목이 있으면 구현, 작업 기준서, 구현 지시서, 검증, 완료로 넘어가지 말고 정리 후보와 추천을 먼저 보고하라.
- 기본 읽기 경로의 문서가 400줄 또는 40KB를 넘으면 분리 후보로 보고하라. 1000줄 이상 누적 문서는 active index와 history 문서 분리 후보로 보고하라.
- 문서가 커졌거나 다음 작업 판단에 과거 완료 기록까지 훑어야 한다면 현재 작업 포인터 역할을 확인하라. 파일명은 강제하지 않지만 기본 후보는 `docs/project/current-work.md`다. 현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서, 읽지 않을 과거 기록, 현재 기준과 충돌하는 문서, README/index 갱신 필요 여부가 짧게 있어야 한다.
- 기본 읽기 경로 계약을 확인하라. 이번 작업에서 반드시 읽을 문서와 기본 읽기 경로에서 제외할 과거 기록/보조 자료를 분리하지 못하면 구현, 작업 기준서, 구현 지시서, 검증, 완료로 넘어가기 전에 정합성 정리 질문으로 돌아가라.
- 현재 기준과 과거 산출물이 충돌하면 구현, 작업 기준서, 구현 지시서, 검증, 완료로 넘어가기 전에 먼저 정합성 정리 질문으로 돌아가라.
- 삭제, 폐기, dead code 제거, stale API/UI/DB artifact 제거 요청은 일반 리팩토링으로 보지 말고 `cleanup-delete.md`를 확인하라.
- `CLEANUP_DELETE`는 삭제 작업 분류와 playbook 선택이다. 파일 수정/삭제 권한은 별도의 patch/apply/implementation 승인과 cleanup/delete 사람 확인 지점을 통과해야 한다.
- 사용자-facing 응답은 `_user-facing-language.md`를 따르고, 내부 하네스 용어를 그대로 남발하지 마라.
- 사용자 요청을 라우팅할 때 최종 응답은 내부 차단 사유 목록이 아니라 사용자가 먼저 해야 할 행동 목록으로 번역한다.
- 기본 응답은 Action-first, diagnostics-later를 따른다.
- 라우팅 결과를 사용자에게 보여줄 때 내부 모드명이나 진단표보다 다음 행동을 우선 말한다.
- 기본 사용자 보고에서는 `Product Readiness`, `Engineering Readiness`, `Implementation Readiness`, `READY`, `NOT READY`, `Storage Intent Check`, `Behavior Contract Check`, `State Meaning Check`를 제목이나 결론으로 먼저 보여주지 않는다.
- 기본 사용자 보고에서는 `SOT`를 "확인한 기준 문서" 또는 "현재 기준"으로, `Vertical Slice`를 "첫 기능 범위"로, `DB/API/UI 결정`을 "저장 방식 / 동작 방식 / 화면 흐름"으로 바꿔 말한다.
- 기본 사용자 보고는 "확인한 기준", "현재 판단", "이유", "먼저 정할 것", "내 추천", "다음에 할 일", "내가 물어볼 것"을 우선 사용한다.
- 사용자가 "CDD 판정표", "내부 판정", "상세 harness status"를 명시적으로 요청했거나 에이전트 간 전달물을 작성할 때만 내부 용어와 enum을 노출한다.
- 모든 사용자-facing 응답은 마지막에 "다음에 할 일"을 포함한다.
- 사용자 선택이 필요한 경우에는 선택지, 제 추천, 바로 답할 수 있는 문장을 제공하고 멈춘다.
- 사용자 개입 없이 진행 가능한 경우에는 진행할 작업과 진행하지 않을 작업을 말한 뒤 요청 범위 안에서 다음 단계까지 수행한다.
- 완료한 경우에는 이번 작업이 완료되었다고 말하고 다음 후보와 추천을 남긴다.
- 단순히 "불가", "부족", "완료"로 끝내지 마라.
- 작업 중간마다 사용자 개입이 필요한지 먼저 판정하라.
- 사용자 개입이 필요한 판단: 제품 판단, 설계 판단, 삭제/보존 선택, 데이터 삭제, public API 제거, migration, 큰 dependency 변경, 실제 파일 수정 권한 불명확, 애매한 요청, 수정 금지 지시.
- 사용자 개입이 필요 없고 요청이 명확하며 기준, 범위, 검증 방법이 충분하면 다시 묻지 말고 문서 보강, 계획 작성, 구현 지시서 작성, 구현, 검증, 완료 보고 중 현재 요청이 허용한 다음 단계까지 진행하라.
- 검증 완료된 선행 작업 뒤에 사용자가 후속 작업을 명확히 요청했고 남은 일이 완료 기록 또는 문서 상태 정합성 정리뿐이면, 승인 문구를 다시 요구하지 말고 선행 작업을 complete 처리한 뒤 후속 작업으로 이어가라.
- 정책이나 설계가 비어 있으면 자동 진행하지 말고 사용자에게 선택을 요구하라.

## 전체 지휘 흐름

1. `_work-mode.md`를 읽고 사용자 요청의 작업 모드를 판별한다.
2. 작업 성격이 하나로 확정되지 않으면 파일을 수정하지 않고 사용자가 원하는 단계를 질문한다.
3. 사용자 개입이 필요한지 판정한다. 필요하면 선택지, 추천, 바로 답할 수 있는 문장을 제공하고 멈춘다.
4. 사용자 개입이 필요 없으면 현재 요청이 허용한 다음 단계까지 진행한다.
5. `_sot-packet.md`를 확인하고 이번 작업 기준 묶음의 존재 여부와 부족한 필드를 확인한다.
6. 현재 작업 포인터와 기본 읽기 경로 계약을 확인한다. 없거나 불완전해 과거 기록을 함께 훑어야 하면 먼저 정리 후보를 보고한다.
7. `_readiness-gates.md`를 확인하고 준비 상태 판정 형식을 준비한다.
8. 작업 시작 전 작업 방식, 이번 작업 기준, 가능한 작업, 금지된 작업, 진행 전 필요한 승인, 검증 방법을 선언한다.
9. `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 읽기, 분석, 제안만 수행하고 파일 수정 없이 다음 승인 문구를 포함해 보고한다.
10. `_authority-boundary.md`를 읽고 AI가 판단할 수 있는 영역과 금지된 판단 영역을 확인한다.
11. `_artifact-metadata.md`, `_artifact-templates.md`, `_status-machine.md`, `_approval-reference.md`, `_user-facing-language.md`를 확인한다.
12. 새 프로젝트이거나 프로젝트 성격이 불명확하면 `_project-context.md`로 Project Context를 확인한다.
13. 사용자 요청에서 실제 서비스 여부, 연습용 여부, 사용자 유형, 도메인 위험, 운영 전제를 추론할 수 있으면 Project Context 초안으로 받아들인다.
14. Project Context가 없으면 사용자에게 프로젝트 자체의 목적, 사용자, 운영 전제, 위험도, 단순화 경계를 질문한다. 하네스 내부 평가 목적은 묻지 않는다.
15. 사용자 요청을 Goal로 해석한다.
16. 현재 상태의 docs, registry, Plan/Task, prompt, verification result, completion record를 사용해야 하면 먼저 artifact legitimacy check를 수행한다.
17. legitimacy check를 통과하지 못한 artifact는 baseline으로 사용하지 않고 `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보로 보고한다.

문서 저장이 필요한 경우, 다음을 먼저 수행한다.

- `_artifact-templates.md`의 Document Placement Check를 작성한다.
- `docs/README.md`, 문서 index, document registry, 기존 작업 산출물 목록, 기존 파일명과 누적 방식을 확인한다.
- 단일 문서 누적 구조면 같은 문서에 추가하고, task별 파일 분리 구조면 같은 방식으로 분리한다.
- 같은 문서에 추가하더라도 기본 읽기 경로가 400줄 또는 40KB를 넘거나 누적 문서가 1000줄 이상이면 분리 후보와 유지 후보를 보고한다.
- 작업 기준서, ADR, 검증 결과, 완료 기록은 커질 경우 active index와 history record 분리를 우선 검토한다.
- Product/Engineering 기준 문서는 너무 커질 때만 domain packet으로 분리하고, 원래 기준 문서는 얇은 진입점과 index로 유지한다.
- 루트 `DESIGN.md`가 승인된 단일 디자인 기준이면 유지하되, 너무 커질 경우 전역 원칙과 index만 남기고 화면별 세부 기준 분리를 제안한다.
- 기존 구조와 다른 파일 배치를 하려면 auto-stop하고 전체 문서 구조 변경안과 사용자 승인을 요청한다.
- 저장 전 사용자 보고에 수정할 파일, 새로 만들 파일, 기존 문서 구조와 맞는지, 현재 작업 포인터 갱신 필요 여부, 기본 읽기 경로 계약 변경 여부, 분리 후보, 유지 후보, 삭제/보존/비-SOT 분류 후보, README/index 갱신 필요 여부를 포함한다.

18. 사용자 요청이 source of truth 생성/변경/삭제/상태 전환 요청인지 분류한다.
19. source of truth 변경 요청이면 `_source-of-truth-manager.md` 절차로 라우팅하고 직접 문서를 수정하지 않는다.
20. 관련 source of truth 문서를 찾는다.
21. 프로젝트에 `document-registry.yml`이 있으면 등록 문서의 type, status, owns, requiredFor를 확인한다.
22. registry가 없으면 Goal에 필요한 문서 타입을 임시로 추론하되, 추론을 source of truth로 확정하지 않는다.
23. archive/superseded/generated/index/memory/recall/previous-report 자료가 검색되면 보조 자료로만 취급하고 active source of truth 승격 근거를 확인한다.
24. `_source-of-truth-manager.md` 하위 절차로 `_document-readiness.md`를 사용해 제품 기준 준비 상태와 기술 설계 준비 상태를 판단한다.
25. 문서나 정책이 부족하면 `_source-of-truth-manager.md` 하위 절차로 `_missing-context.md`를 사용해 제품/기술/구현 관련 미확정 결정 질문을 만든다.
26. 사용자가 답하면 `_source-of-truth-manager.md` 하위 절차로 `_document-supplement.md`를 사용해 문서/정책 초안을 제안한다.
27. 사용자가 변경 방향과 실제 적용을 각각 명시적으로 승인하면 source of truth 문서와 document registry 업데이트를 승인된 범위 안에서만 수행한다.
28. 제품 기준 준비 상태와 기술 설계 준비 상태가 모두 `READY`일 때만 `plan-task.md` 절차로 Plan/Task를 만든다.
29. Task가 cleanup/delete 작업이면 `cleanup-delete.md`의 keep list, delete list, 의존성 확인, 사람 확인 지점을 Task와 prompt에 반영한다.
30. Task가 승인되고 `documentCoverage.status`가 READY일 때만 `write-implementation-prompt.md` 절차로 구현 prompt를 만든다.
31. 구현 prompt 작성 후 새 미확정 결정, 정책 충돌, 위험 변경, 범위 확대가 있는지 판단한다.
32. 사용자가 실제 구현까지 명확히 요청했고 초안 작성 후 실행 연계 조건을 모두 만족하면 별도 실행 승인 요청을 반복하지 않고 `_implementation-rules.md` 절차로 구현한다.
33. 사용자가 초안 검토를 요청했거나 실행 연계 조건을 만족하지 않으면 구현하지 말고 선택지, 추천, 바로 답할 수 있는 문장을 제공한다.
34. 구현 후 check를 수행한다.
35. `verify-work.md` 절차로 구현 결과를 제품 기준 문서, 기술 설계 기준 문서, 작업 기준서, requiredDocuments, rules, 기준 문서, prompt, result와 대조한다.
36. 문제가 있으면 `revise-work.md` 절차로 수정 prompt를 만들고 사용자 승인 후 수정 루프를 수행한다.
37. verification이 VERIFIED이고 사용자가 review를 승인한 뒤에만 `complete-work.md` 절차로 완료한다.
38. 단, 검증 완료된 선행 작업 뒤에 사용자가 후속 작업을 명확히 요청했고 후속 작업 전환 연계 조건을 모두 만족하면 완료 기록 정합성 정리를 먼저 수행한 뒤 후속 작업으로 이어간다.
39. 모든 사용자-facing 보고는 "다음에 할 일" 종료 형식으로 끝낸다.

## Source of Truth 권위 순서

대상 프로젝트가 자체 우선순위를 명시하면 그 우선순위를 먼저 따른다.

명시된 우선순위가 없으면 기본 순서는 다음과 같다.

1. 현재 사용자 지시
2. 대상 저장소의 작업 규칙 파일, 예: `AGENTS.md`
3. CDD harness rules
4. 대상 프로젝트의 approved source of truth documents
5. task-specific approved plan/prompt
6. implementation files
7. README, generated docs, indexing docs, memory/recall notes, previous assistant responses 같은 보조 자료

README는 navigation 역할을 할 수 있지만 제품 요구사항이나 정책의 source of truth로 자동 승격되지 않는다.

Generated docs/indexes, memory/recall notes, previous assistant messages or task reports는 명시적으로 approved source of truth로 승격되지 않은 한 보조 자료다.

Archive/superseded documents는 historical record다. 검색에 걸렸다는 이유만으로 active source of truth로 사용하지 않는다.

## 사람이 승인해야 하는 지점

다음 지점에서는 반드시 멈추고 사용자 승인을 받아야 한다.

- ANALYSIS_ONLY 또는 PROPOSAL_ONLY에서 파일 수정 단계로 전환하기 전
- 하네스 skill 파일을 수정하기 전
- 미확정 결정 답변을 source of truth 문서로 확정하기 전
- source of truth 변경 방향을 확정하기 전
- source of truth 변경안을 실제 파일에 적용하기 전
- 사용자 검토용 prompt 초안을 생성하기 전
- Plan/Task를 승인 상태로 전환하기 전
- 구현 prompt를 implementation에 전달하기 전. 단, 사용자가 실제 구현까지 명확히 요청했고 prompt 작성이 내부 실행 기준을 만드는 절차이며 초안 작성 후 실행 연계 조건을 모두 만족하면 같은 요청 범위 안에서 이어갈 수 있다.
- revision prompt를 실행하기 전
- 완료 전 IDE diff review 또는 동등한 review 승인 전. 단, 검증 완료된 선행 작업의 완료 기록 또는 문서 상태 정합성 정리만 남았고 후속 작업 전환 연계 조건을 모두 만족하면 같은 요청 범위 안에서 이어갈 수 있다.
- cleanup/delete에서 archive 보존 방식이 불명확하거나 대량 삭제, DB drop/migration, public API 제거, dependency 대량 제거, keep list 충돌, 폐기와 비노출 선택, 데이터 손실 가능성이 있는 경우

## Source of Truth 변경 라우팅

start-here.md는 source of truth를 직접 수정하지 않는다.

사용자가 문서 원천에 해당하는 변경을 요청하면 다음처럼 응답하고 `_source-of-truth-manager.md`로 전환한다.

```text
사용자: completed 말고 done으로 바꿔줘.

AI:
이 요청은 API contract/source of truth 변경입니다.
Source of Truth Manager 절차로 영향 범위를 분석하겠습니다.
먼저 변경 범위를 선택해 주세요.
```

사용자의 "알아서 해", "추천대로", "빨리 해", "그냥 맞춰줘", "문서도 같이 고쳐" 같은 표현은 source of truth 적용 승인으로 해석하지 않는다. 모호하면 다시 질문한다.

사용자가 "api-contract.md만 바꾸고 나머지는 나중에 맞추자"처럼 scope를 좁혀도, 그 변경이 APPROVED 기준 문서나 작업 기준서와 known conflict를 만들면 APPLY를 거부한다.

"A로 하자"는 Direction Approval로만 해석한다. 파일 APPLY, source of truth APPROVED 전환, prompt draft 생성, prompt execution 승인이 아니다.

예:

```text
"A로 하자"는 변경 방향 승인으로 이해했습니다. 아직 파일 APPLY 승인은 아닙니다.
Files Proposed for Apply 전체를 실제로 수정하려면 다음 문장으로 승인해 주세요:
"CR-001 정합 묶음 적용을 승인합니다."
```

## Task Dependency Gate

후속 Task prompt 생성은 권한 있는 행동이다. prompt 생성은 단순 문서 작성이 아니라 후속 구현을 여는 확인 지점이다.

Task prompt는 다음 조건을 모두 만족할 때만 생성한다.

- Task status가 APPROVED다.
- `documentCoverage.status`가 READY다.
- 모든 `dependsOn` Task가 COMPLETE 상태다.
- source of truth가 VALIDATED 상태다.
- known conflict가 없다.
- prompt 생성 승인 또는 현재 workflow에서 허용된 write-implementation-prompt 단계다.

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

## Artifact Legitimacy Check

디스크에 존재하는 파일은 자동으로 유효한 artifact가 아니다. 이전 턴에서 생성된 파일이라도 현재 harness 확인 지점을 위반해 생성되었다면 정상 baseline으로 사용할 수 없다.

사용 전 검사 대상:

- Source of Truth Change Request
- `docs/**`
- `document-registry.yml`
- Plan/작업 기준서
- prompt files
- verification result
- completion record

검사 질문:

1. 이 artifact는 어떤 workflow 단계에서 생성되었는가?
2. 생성 당시 필요한 사용자 승인이 있었는가?
3. 생성 당시 선행 Task dependency가 충족되었는가?
4. 생성 당시 `documentCoverage`가 READY였는가?
5. 생성 당시 source of truth가 VALIDATED 상태였는가?
6. 미확정 결정이 남아 있는데 생성된 것은 아닌가?
7. Policy Conflict가 unresolved 상태였는데 생성된 것은 아닌가?
8. 이후 source of truth 변경으로 superseded 되었는가?
9. 현재 harness 기준으로도 생성 조건을 만족하는가?
10. artifact 내부에 생성 근거, approval reference, source-of-truth version, task dependency 상태가 기록되어 있는가?

하나라도 확인할 수 없거나 위반이 있으면 정상 baseline으로 사용하지 않는다. 위반 artifact는 `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보로 보고하고 사용자에게 처리 방향을 질문한다.

## CLI 사용

CLI는 필수가 아니라 보조 도구다. 필요한 경우 AI 에이전트가 다음 작업에 CLI를 사용할 수 있다.

- 준비 상태 확인 prompt 생성
- supplement prompt 생성
- planning prompt 생성
- implementation prompt 생성
- check 실행과 result 기록
- verification prompt 생성
- revision prompt 생성
- completion 기록

사용자가 CLI 명령을 직접 외워서 실행할 필요는 없다.

## User-Facing Language

사용자-facing 응답에서는 내부 하네스 용어를 그대로 남발하지 않는다.

기본 응답은 Action-first, diagnostics-later다. 내부 진단표, harness status, metadata, approvalRefs, dependsOn, legitimacy check 같은 용어는 사용자가 요청했을 때만 상세히 제공한다.

권장 표현:

- `SOT`나 `source of truth` 대신 "확인한 기준 문서" 또는 "현재 기준"
- `Product Readiness` 대신 "제품 방향"
- `Engineering Readiness` 대신 "설계 준비 상태"
- `Implementation Readiness` 대신 "지금 바로 만들 수 있는지"
- `READY` / `NOT READY` 대신 "바로 진행 가능" / "아직 결정 필요"
- `Vertical Slice` 대신 "첫 기능 범위"
- `DB/API/UI 결정` 대신 "저장 방식 / 동작 방식 / 화면 흐름"
- `Storage Intent Check` 대신 "무엇을 왜 저장할지"
- `Behavior Contract Check` 대신 "사용자가 어떤 행동을 하고 어떤 결과를 받는지"
- `State Meaning Check` 대신 "상태값이 무엇을 의미하는지"
- `implementation-prompt` 대신 "구현 지시서"
- `dependsOn gate` 같은 내부 표현 대신 "선행 작업이 아직 끝나지 않았습니다"
- `APPLY_APPROVAL` 대신 "문서 묶음을 실제로 바꿔도 되는지 확인"
- `QUARANTINED` 대신 "잠시 보류"
- `SUPERSEDED` 대신 "이전 기준이라 더 이상 사용하면 안 됨"

보고는 가능한 한 다음 순서를 따른다.

1. 확인한 기준
2. 현재 판단: 바로 구현 가능 / 아직 결정 필요
3. 이유
4. 먼저 정할 것
5. 내 추천
6. 다음에 할 일
7. 내가 물어볼 것

사용자가 명시적으로 "CDD 판정표"나 "내부 판정"을 요청하지 않았다면 `Product Readiness`, `Engineering Readiness`, `Implementation Readiness`, `READY`, `NOT READY`, `Storage Intent Check`, `Behavior Contract Check`, `State Meaning Check`를 기본 보고의 제목이나 결론으로 쓰지 않는다.

사용자가 "그냥 해줘", "빠르게 가자", "기존 파일로 해도 되잖아"라고 할 때는 다음 패턴을 우선 사용한다.

```text
지금은 바로 진행할 수 없습니다.
먼저 다음을 선행해 주세요.
1. ...
2. ...
3. ...
그다음 제가 ...를 진행하겠습니다.
```

내부 판정은 사용자가 "왜?", "자세히", "내부 판정도 보여줘"라고 요청했을 때만 상세히 보여준다.

요청 자체가 애매할 때는 다음 패턴을 우선 사용한다.

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

기본 응답에서 피할 형태:

```text
| 항목 | 현재 | harness |
|------|------|---------|
| approvalRefs | 없음 | 필수 |
| legitimacy check | 미통과 | ... |
| dependsOn | 미 COMPLETE | ... |
```

## 중단 조건

다음 상황이면 진행하지 말고 보고하라.

- 필요한 source of truth 문서가 없거나 DRAFT/DEPRECATED 상태다.
- 문서가 있지만 필요한 정책이 비어 있다.
- 사용자 요청이 승인 문서와 충돌한다.
- Task 없이 구현을 요구한다.
- Task의 `documentCoverage.status`가 READY가 아니다.
- source of truth 변경이 구현 범위에 섞였다.
- source of truth 변경 승인 없이 문서, registry, Plan, Task, prompt, verification result를 수정해야 한다.
- 사용자 요청이 애매한데 구현, 문서 수정, 파일 수정, 삭제/정리로 진행해야 한다.
- 사용자가 지정한 변경 scope가 source of truth 정합성을 깨뜨린다.
- known conflict가 남은 상태에서 Plan/Task, 구현, revision, complete로 진행해야 한다.
- 선행 Task가 COMPLETE가 아닌데 후속 Task prompt를 생성해야 한다.
- 현재 또는 선행 Task의 미확정 결정을 "나중에"로 미루고 후속 Task로 진행해야 한다.
- 기존 artifact가 legitimacy check를 통과하지 못했는데 baseline으로 사용해야 한다.
- invalid prompt를 보강해서 정상 prompt처럼 계속 사용해야 한다.
- 승인된 TEST_STRATEGY 없이 mock, fake, stub, slice test, `@WebMvcTest`, `@DataJpaTest`, mocked service, mocked repository를 선택해야 한다.
