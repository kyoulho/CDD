---
name: cdd
description: CDD 작업 하네스. 요청이 애매하거나 구현/프론트엔드 UI/UX/인터페이스/DB/API/status/성능 설계 전에 제품 기준, 상호작용 방식, 사용자 경험 기준, 저장 의미, 동작 계약, 상태 의미, 운영/품질 기준, 작업 기준서, 검증 흐름을 확인해야 할 때 사용한다.
---
# CDD Skill

CDD는 승인된 기준 문서와 사용자 승인 지점이 준비된 작업만 구현으로 넘기게 하는 문서 기반 작업 하네스다. 이 디렉터리가 skill root이며, 보통 `start-here.md`에서 시작한다.

## 빠른 탐색

- 처음 호출되면 "Routing"으로 public entrypoint를 고른다.
- 사용자가 직접 읽을 문서는 "Public Entry Points"만 노출한다.
- `_*.md`는 "Internal Modules"의 접근 정책을 따른다.
- CDD 핵심 용어가 필요하면 "핵심 용어"를 먼저 본다.

## 읽기 경로 최적화

목표는 정확한 판단을 유지하면서 반복 읽기 비용을 줄이는 것이다. 이 규칙은 제품 기준, 설계 기준, 사용자 승인, 문서 정합성, readiness gate를 생략하거나 약화하는 규칙이 아니다.

처음부터 모든 public entrypoint와 internal module을 읽지 않는다. 사용자 요청에 맞는 public entrypoint 하나를 고르고, 대상 프로젝트에 문서 구조가 있으면 `cdd-audit docs --root <project> --format brief --fail-on never --entrypoint <entrypoint>`로 정확한 판단에 먼저 필요한 프로젝트 문서와 CDD 문서 섹션을 좁힌다. entrypoint가 아직 애매하면 `--entrypoint` 없이 실행하고, `_work-mode.md` 기준으로 작업 성격을 먼저 확인한다. `brief`에서 차단 항목이 있거나 상세 분리 이유가 필요할 때는 반드시 `--format text` 또는 `--format json`으로 확장한다.

선택한 entrypoint와 `brief`가 가리킨 문서의 "먼저 볼 섹션"을 우선 확인한다. 섹션 힌트(section hint)는 문서 전체 판단을 대체하지 않는다. `.cdd-audit.json`의 `sectionHints`, current-work 문서의 `먼저 볼 섹션`, heading 추정 순서로 적용한다. `cdd-audit`가 줄 범위를 제공하면 해당 위치부터 읽되, 명시된 heading이 `missing`이거나 `SECTION_HINT_MISSING_HEADING` warning이 있으면 섹션 계약을 갱신해야 한다. 후보 heading이 함께 표시되면 현재 문서 구조에 맞게 고칠 후보로 보고한다. 힌트가 없거나, 힌트 섹션만으로 기준/승인/gate를 판단할 수 없거나, 섹션끼리 충돌하면 해당 문서 전체 또는 상세 audit으로 확장한다. `_*.md` internal module은 해당 entrypoint가 요구하거나 판단이 막힌 경우에만 연다. 과거 task, completion, verification, old prompt, generated map, Codesight, agentmemory는 current pointer가 명시적으로 요구하지 않는 한 기본 읽기에서 제외한다.

## 핵심 용어

- 제품 기준 준비 상태: 무엇을 왜 만들 것인지에 대한 기획 준비도.
- 기술 설계 준비 상태: 제품 판단을 저장 구조, 상태, API, 코드 구조로 표현할 기준이 정해졌는지에 대한 설계 준비도.
- 구현 시작 가능 여부: 에이전트가 구현을 시작해도 되는지에 대한 실행 준비도.
- 이번 작업 기준 묶음: 이번 작업에서 따라야 할 승인된 기준 문서 묶음.
- 작업 기준서: 구현 전 작업 범위, 금지 범위, 검증 기준을 고정하는 작업 계약.
- 상호작용 방식 확인: 사용자 또는 운영자가 접하는 기능의 입력, 출력, 흐름, 실패와 피드백을 먼저 확인하는 절차.
- 프론트엔드 UX 확인: 웹/모바일 UI 작업에서 화면 상태, 정보 구조, 접근성, 반응형 동작, 시각 검증 기준을 먼저 확인하는 절차.
- 저장 의미 확인: table, column, migration, repository, API DTO를 말하기 전에 무엇을 왜 저장하는지 확인하는 절차.
- 운영/품질 기준 확인: 성능, 보안, 권한, 조회, 재시도, 로그/감사, 운영 기준을 구현 전에 확인하는 절차.
- 현재 작업 포인터: 다음 판단에 필요한 현재 gate, 다음 task, 반드시 읽을 문서, 읽지 않을 과거 기록을 짧게 가리키는 승인된 문서 또는 섹션.
- 기본 읽기 경로 계약: 이번 작업에서 반드시 읽을 문서와 기본 읽기 경로에서 제외할 과거 기록/보조 자료를 고정하는 계약.
- 섹션 힌트(section hint): 반드시 읽을 문서 안에서 먼저 확인할 heading 목록과 가능하면 줄 범위. 정확한 판단을 돕는 안내일 뿐, readiness gate나 문서 전체 확인을 대체하지 않는다.

## Public Entry Points

사용자가 직접 호출할 수 있는 public entrypoint는 다음 파일뿐이다.

- `start-here.md`
- `plan-task.md`
- `write-implementation-prompt.md`
- `cleanup-delete.md`
- `verify-work.md`
- `revise-work.md`
- `complete-work.md`

## Internal Modules

`_`로 시작하는 internal module은 public entrypoint 흐름 안에서만 읽는다.

- `_work-mode.md`
- `_authority-boundary.md`
- `_project-context.md`
- `_source-of-truth-manager.md`
- `_document-readiness.md`
- `_missing-context.md`
- `_document-supplement.md`
- `_readiness-gates.md`
- `_sot-packet.md`
- `_implementation-rules.md`
- `_artifact-metadata.md`
- `_artifact-templates.md`
- `_status-machine.md`
- `_approval-reference.md`
- `_user-facing-language.md`

Internal module을 task entrypoint로 직접 실행하지 마라. Internal module은 단독으로 implementation, cleanup/delete, SOT changes, completion을 승인할 수 없으며 `IMPLEMENTATION_ALLOWED`, `APPLY_AUTHORIZED`, `PATCH_AUTHORIZED`, `COMPLETE`를 만들 수 없다. 사용자가 internal module을 직접 지정하면 `start-here.md` 또는 가장 가까운 public entrypoint로 라우팅한다.

## Routing

- 새 작업 시작 -> `start-here.md`
- Plan/Task 작성 -> `plan-task.md`
- 구현 지시서 작성 -> `write-implementation-prompt.md`
- 삭제/폐기/정리 -> `cleanup-delete.md`
- 결과 검증 -> `verify-work.md`
- 검증 실패 후 수정 -> `revise-work.md`
- 완료 보고 -> `complete-work.md`

## Core Gates

구현 전에는 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부, 승인된 작업 기준 묶음, 사용자 승인 지점이 모두 준비되어야 한다. 내부 판정에서 하나라도 `NOT READY`이면 구현하지 말고 아직 필요한 결정을 먼저 묻는다. 세부 판정은 `_readiness-gates.md`와 각 public entrypoint의 시작 조건을 따른다.

요청이 애매하면 `_work-mode.md`의 작업 성격 판단 규칙을 적용하고, 구현 요청이나 파일 수정 승인으로 승격하지 않는다. 사용자 또는 운영자가 접하는 기능의 상호작용, UI/UX, 저장 의미, 동작 계약, 상태 의미, 운영/품질 기준은 `_readiness-gates.md`의 gate를 따른다.

문서 배치, 현재 작업 포인터, 기본 읽기 경로 계약, active/history 분리, `cdd-audit` 실행 기준은 `_source-of-truth-manager.md`에 둔다. artifact metadata와 저장 전 보고 형식은 `_artifact-templates.md`를 따른다.

사용자-facing 보고는 `_user-facing-language.md`를 따른다. 기본 응답에서는 내부 판정 용어를 먼저 노출하지 않고, "지금 가능한가 / 왜 멈춰야 하는가 / 무엇을 먼저 정해야 하는가 / 다음에 할 일"을 자연어로 말한다.

자동 진행과 승인 연계는 `_approval-reference.md` 및 선택한 public entrypoint의 "최소 읽기 경로"를 따른다. 새 미확정 결정, 정책 충돌, 위험 변경, 범위 확대가 있으면 멈추고 사용자에게 선택지를 제시한다.

CDD 문서는 제품 기준 문서가 아니다. 실제 구현 기준은 대상 프로젝트의 제품 기준 문서, 기술 설계 기준 문서, 승인된 작업 기준 묶음이다.
