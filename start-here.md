# Start Here Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: CDD-controlled task를 시작, 계획, 지시서 작성, cleanup/delete, 검증, 수정, 완료할 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

이 파일은 CDD Skill Layer의 최초 진입점이다. 사용자가 이 파일을 링크하고 목표를 말하면, AI는 이 지시를 최상위 작업 절차로 따른다.

## 빠른 탐색

- 처음 시작하면 "최소 읽기 경로"와 "Routing Table"만 먼저 본다.
- 요청이 애매하거나 권한이 불명확하면 "즉시 적용할 규칙"에서 중단 규칙만 확인한다.
- 작업 성격이 정해졌으면 해당 public entrypoint로 이동하고, 이 파일의 나머지 세부 규칙은 필요할 때만 본다.
- 기준 문서 권위와 변경 요청은 "Source of Truth 권위 순서", "Source of Truth 변경 라우팅"을 본다.
- 선행 작업, artifact 정합성, CLI 사용은 각 gate 섹션을 본다.
- 사용자 보고는 "User-Facing Language"와 "중단 조건"을 본다.

## 최소 읽기 경로

목표는 정확한 판단에 필요한 문서를 먼저 좁히는 것이다. 제품 기준, 설계 기준, 사용자 승인, 문서 정합성, readiness gate를 건너뛰기 위한 경로가 아니다.

처음부터 모든 internal module을 열지 않는다. 먼저 사용자 요청만으로 작업 성격을 다음 중 하나로 분류한다: 상태/다음 작업 조회, 설명/판단, 계획, 구현 지시서, 구현, cleanup/delete, 검증, 수정, 완료, 기준 문서 변경. 하나로 확정되지 않으면 파일을 수정하지 말고 자연어로 확인한다.

작업 성격이 확정되면 Routing Table의 public entrypoint 하나로 이동한다. 대상 프로젝트에 문서 구조가 있으면 `cdd-audit` 실행 경로 규칙에 따라 먼저 읽을 문서와 먼저 볼 섹션을 좁힌다. 사용자가 `cdd-audit`를 PATH에 등록했다고 가정하지 말고, PATH 명령이 없으면 CDD skill root 기준 `<cdd-root>/bin/cdd-audit docs --root <project> --format brief --fail-on never`를 시도한다. 먼저 볼 섹션은 `.cdd-audit.json`, current-work 문서, heading 추정 순서로 정해지는 문서 안의 진입점일 뿐이며, 줄 범위가 있으면 그 위치부터 확인한다. heading이 `missing`으로 표시되거나 기준/승인/gate 판단이 불충분하면 해당 문서 전체 또는 text/JSON audit으로 확장한다. `brief` 결과에 차단 항목이 있거나 분리 이유가 필요하면 반드시 text 또는 JSON으로 확장한다.

`_work-mode.md`, `_sot-packet.md`, `_readiness-gates.md`, `_authority-boundary.md`, `_artifact-*.md`, `_status-machine.md`, `_approval-reference.md`, `_user-facing-language.md`는 항상 먼저 읽는 파일이 아니다. 선택한 entrypoint가 요구하거나 판단이 막힌 경우에만 연다.

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

- 요청이 설명, 설계, 문서 수정, 구현, 삭제, 검증 중 무엇인지 애매하면 바로 작업하지 말고 자연어로 확인한다. 애매한 요청은 구현, 파일 수정, 삭제 승인으로 승격하지 않는다. 세부 분류는 `_work-mode.md`를 따른다.
- "다음 작업이 무엇인가?", "현재 상태 알려줘", "무엇이 남았어?"처럼 상태나 다음 후보만 묻는 요청은 조회로 답한다. 승인 브리핑이나 승인 문장을 요구하지 말고 `_user-facing-language.md`의 "조회형 질문 응답 형식"으로 현재 상태, 다음 후보, 진행 조건을 보고한다. 다음 후보가 구현 지시서 초안 작성처럼 사용자 승인이 필요한 산출물이라면 진행 후보 브리핑을 함께 제공한다.
- "다음 작업 진행하자", "다음 단계로 가자", "진행하자"처럼 실제 다음 단계 수행을 요청했고 현재 작업 포인터가 단일 다음 task를 가리키면 조회나 일반 선택지 목록으로 축소하지 않는다. 바로 실행할 수 없고 승인 문장이 필요하면 `_user-facing-language.md`의 "후속 작업 승인 요청 브리핑" 전체 형식을 사용한다.
- 파일 생성/수정/삭제는 사용자가 허용한 범위 안에서만 수행한다. "좋아", "진행해", "다음", "반영해" 같은 말만으로 더 높은 권한을 추정하지 않는다.
- 구현, 작업 기준서, 구현 지시서, 검증, 완료로 이어지는 요청이면 `_sot-packet.md`와 `_readiness-gates.md`가 요구하는 기준 준비 상태를 확인한다. 기준이 비어 있으면 table, API, status, UI, CLI, 배치 실행 방식, 저장 구조를 먼저 제안하지 않는다.
- 문서 구조, 현재 작업 포인터, 기본 읽기 경로, active/history 분리, `cdd-audit` 실행은 `_source-of-truth-manager.md`를 따른다. 대상 프로젝트에 문서 구조가 있으면 PATH 명령 또는 CDD skill root의 `bin/cdd-audit`로 최소 읽기 경로를 확인한다. `cdd-audit`를 실행할 수 없으면 같은 항목을 수동 확인으로 대체하고 실행 불가 이유를 보고한다.
- artifact 작성, 저장 위치, metadata, status, approval, 승인 전 브리핑은 `_artifact-templates.md`, `_artifact-metadata.md`, `_status-machine.md`, `_approval-reference.md`, `_user-facing-language.md`를 따른다.
- cleanup/delete는 일반 리팩토링이 아니다. 삭제/보존/비-SOT 표시 후보와 이유를 먼저 브리핑하고, 되돌리기 어려운 변경은 사람 확인 지점을 통과해야 한다.
- 사용자-facing 응답은 내부 차단 사유 목록이 아니라 사용자가 먼저 해야 할 행동 목록으로 번역한다. 모든 응답은 "다음에 할 일"을 포함한다.
- 사용자 개입이 필요 없고 요청이 명확하며 기준, 범위, 검증 방법이 충분하면 다시 묻지 말고 요청 범위 안에서 다음 단계까지 진행한다. 정책이나 설계가 비어 있으면 자동 진행하지 말고 선택지를 제시한다.

## 전체 지휘 흐름

1. 사용자 요청만으로 작업 성격을 먼저 분류한다. 상태/다음 작업 조회라면 `_work-mode.md`의 `STATUS_INQUIRY`로 처리하고 파일 수정, artifact 생성, 승인 요청을 시작하지 않는다. 모호하거나 권한 해석이 필요하면 `_work-mode.md`를 읽고 작업 모드를 판별한다.
2. 작업 성격이 하나로 확정되지 않으면 파일을 수정하지 않고 사용자가 원하는 단계를 질문한다.
3. 사용자 개입이 필요한지 판정한다. 필요하면 선택지, 추천, 바로 답할 수 있는 문장을 제공하고 멈춘다.
4. 사용자 개입이 필요 없으면 현재 요청이 허용한 다음 단계까지 진행한다.
5. 구현, 작업 기준서, 구현 지시서, 검증, 완료로 이어지는 요청이면 `_sot-packet.md`를 확인하고 이번 작업 기준 묶음의 존재 여부와 부족한 필드를 확인한다.
6. 현재 작업 포인터와 기본 읽기 경로 계약을 확인한다. 없거나 불완전해 과거 기록을 함께 훑어야 하면 먼저 정리 후보를 보고한다.
7. 제품/설계/구현 가능 여부가 불명확하거나 작업 기준서/구현 지시서를 만들 때만 `_readiness-gates.md`를 확인하고 준비 상태 판정 형식을 준비한다.
8. 작업 시작 전 작업 방식, 이번 작업 기준, 가능한 작업, 금지된 작업, 진행 전 필요한 승인, 검증 방법을 선언한다.
9. `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 읽기, 분석, 제안만 수행하고 파일 수정 없이 다음 승인 문구를 포함해 보고한다.
10. 권한 경계, 문서 수정, 삭제, 승인, 완료 판단이 걸릴 때만 `_authority-boundary.md`를 읽고 AI가 판단할 수 있는 영역과 금지된 판단 영역을 확인한다.
11. artifact를 만들거나 승인 문장을 제시할 때만 `_artifact-metadata.md`, `_artifact-templates.md`, `_status-machine.md`, `_approval-reference.md`, `_user-facing-language.md`를 확인한다.
12. 새 프로젝트이거나 프로젝트 성격이 불명확할 때만 `_project-context.md`로 Project Context를 확인한다.
13. 사용자 요청에서 실제 서비스 여부, 연습용 여부, 사용자 유형, 도메인 위험, 운영 전제를 추론할 수 있으면 Project Context 초안으로 받아들인다.
14. Project Context가 없으면 사용자에게 프로젝트 자체의 목적, 사용자, 운영 전제, 위험도, 단순화 경계를 질문한다. 하네스 내부 평가 목적은 묻지 않는다.
15. 사용자 요청을 Goal로 해석한다.
16. 현재 상태의 docs, registry, Plan/Task, prompt, verification result, completion record를 사용해야 하면 먼저 artifact legitimacy check를 수행한다.
17. legitimacy check를 통과하지 못한 artifact는 baseline으로 사용하지 않고 `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보로 보고한다.

문서 저장이 필요한 경우, 다음을 먼저 수행한다.

- `_source-of-truth-manager.md`의 문서 배치와 읽기 비용 규칙을 확인한다.
- `_artifact-templates.md`의 Document Placement Check를 작성한다.
- 저장 전 사용자 보고에 수정할 파일, 새로 만들 파일, 기존 문서 구조와 맞는지, current pointer/read path/README/index 갱신 필요 여부를 포함한다.

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
