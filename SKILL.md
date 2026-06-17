---
name: cdd
description: CDD 작업 하네스. 요청이 애매하거나 구현/인터페이스/DB/API/status 설계 전에 제품 기준, 상호작용 방식, 저장 의미, 동작 계약, 상태 의미, 운영/품질 기준, 작업 기준서, 검증 흐름을 확인해야 할 때 사용한다.
---
# CDD Skill

CDD는 승인된 기준 문서와 사용자 승인 지점이 준비된 작업만 구현으로 넘기게 하는 문서 기반 작업 하네스다. 이 디렉터리가 skill root이며, 보통 `start-here.md`에서 시작한다.

## 핵심 용어

- 제품 기준 준비 상태: 무엇을 왜 만들 것인지에 대한 기획 준비도.
- 기술 설계 준비 상태: 제품 판단을 저장 구조, 상태, API, 코드 구조로 표현할 기준이 정해졌는지에 대한 설계 준비도.
- 구현 시작 가능 여부: 에이전트가 구현을 시작해도 되는지에 대한 실행 준비도.
- 이번 작업 기준 묶음: 이번 작업에서 따라야 할 승인된 기준 문서 묶음.
- 작업 기준서: 구현 전 작업 범위, 금지 범위, 검증 기준을 고정하는 작업 계약.
- 상호작용 방식 확인: 사용자 또는 운영자가 접하는 기능의 입력, 출력, 흐름, 실패와 피드백을 먼저 확인하는 절차.
- 저장 의미 확인: table, column, migration, repository, API DTO를 말하기 전에 무엇을 왜 저장하는지 확인하는 절차.
- 운영/품질 기준 확인: 성능, 보안, 권한, 조회, 재시도, 로그/감사, 운영 기준을 구현 전에 확인하는 절차.

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

구현 전에는 제품 기준 준비 상태, 기술 설계 준비 상태, 구현 시작 가능 여부, 승인된 작업 기준 묶음, 사용자 승인 지점이 모두 준비되어야 한다. 내부 판정에서 하나라도 `NOT READY`이면 구현하지 말고 아직 필요한 결정을 먼저 묻는다.

요청이 설명, 설계안, 문서 초안, 문서 수정, 구현 계획, 실제 코드 수정, 삭제/정리, 검증 중 무엇을 원하는지 애매하면 먼저 질문한다. 애매한 요청을 임의로 해석하지 않고, 구현 요청이나 파일 수정 승인으로 승격하지 않는다.

사용자 또는 운영자가 접하는 기능은 상호작용 방식이 정해져야 한다. 입력, 출력, 실패, 빈 상태, 권한 없음, 처리 중 피드백이 비어 있으면 화면, CLI 명령, API surface, 배치 실행 방식, 저장 구조를 먼저 제안하지 않는다.

DB table, column, migration, repository, API DTO는 Storage Intent Check가 `DB_DESIGN_ALLOWED`일 때만 제안한다. API path와 request/response shape는 Behavior Contract Check가 `API_DESIGN_ALLOWED`일 때만 제안한다. status enum과 state transition은 State Meaning Check가 `STATE_MODEL_ALLOWED`일 때만 제안한다.

성능, 보안, 권한, 데이터 양, 조회 방식, 실패 처리, 재시도, 로그/감사 같은 운영/품질 기준이 비어 있으면 안전하다고 가정하지 않고 먼저 질문한다.

사용자에게 보여주는 기본 보고에서는 내부 판정 용어를 그대로 노출하지 않는다. `SOT`는 "확인한 기준 문서" 또는 "현재 기준", `Product Readiness`는 "제품 방향", `Engineering Readiness`는 "설계 준비 상태", `Implementation Readiness`는 "지금 바로 만들 수 있는지", `READY` / `NOT READY`는 "바로 진행 가능" / "아직 결정 필요"로 바꿔 말한다. `Storage Intent Check`, `Behavior Contract Check`, `State Meaning Check`도 각각 "무엇을 왜 저장할지", "사용자가 어떤 행동을 하고 어떤 결과를 받는지", "상태값이 무엇을 의미하는지"로 바꿔 말한다.

기본 보고는 "확인한 기준", "현재 판단", "이유", "먼저 정할 것", "내 추천", "다음에 할 일", "내가 물어볼 것" 순서를 우선한다. 사용자가 "CDD 판정표", "내부 판정", "상세 harness status"를 요청했거나 구현 지시서, 작업 기준서, verification artifact, completion record 같은 에이전트 간 전달물을 작성할 때만 내부 용어와 enum을 노출한다.

모든 사용자-facing 응답은 "다음에 할 일"을 포함한다. 사용자 선택이 필요한 경우에는 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다. 사용자 개입 없이 진행 가능한 경우에는 현재 기준으로 안전하게 진행할 수 있는 범위와 진행하지 않을 범위를 말한 뒤 실제로 다음 단계까지 수행한다. 완료한 경우에는 이번 작업이 완료되었음을 말하고 다음 후보와 추천을 남긴다.

작업 기준서, 구현 지시서, 검증 결과, 완료 기록을 만들거나 수정하기 전에는 대상 프로젝트의 기존 문서 배치 구조를 먼저 확인한다. `docs/README.md`, 문서 index, document registry, 기존 작업 산출물 목록, 기존 파일명과 누적 방식을 우선 따른다. 단일 문서에 task를 누적하는 구조면 같은 문서에 추가하고, task별 파일 분리 구조면 같은 방식으로 분리한다. 기존 구조와 다른 파일 배치를 하려면 자동으로 멈추고 전체 문서 구조 변경안과 사용자 승인을 요구한다. 새 파일이 필요하면 저장 전에 왜 기존 문서에 추가하지 않는지 보고한다.

작업 중간마다 사용자 개입이 필요한지 판정한다. 제품 판단, 설계 판단, 삭제/보존 선택, migration, 데이터 삭제, public API 제거, 큰 dependency 변경, 애매한 요청, 수정 금지 지시가 있으면 멈추고 질문한다. 반대로 요청이 명확하고, 파일 수정이 허용되어 있고, 제품/설계/저장/동작/상태/상호작용/운영 기준과 검증 방법이 충분하며, 위험 변경과 금지 범위가 없으면 다시 묻지 말고 요청 범위 안에서 문서 보강, 구현, 검증, 보고까지 이어서 수행한다.

작업 지시서 초안 작성과 실행 승인을 기계적으로 연달아 요구하지 않는다. 사용자가 실제 구현, 문서 수정, cleanup/delete 실행, revision 실행까지 명확히 요청했고 작업 지시서 작성 중 새 미확정 결정, 정책 충돌, 위험 변경, 범위 확대가 없으면 작업 지시서를 내부 실행 기준으로 작성한 뒤 같은 요청 범위 안에서 바로 실행한다. 사용자가 "초안만", "먼저 보여줘", "검토 후 진행"을 요청했거나 새 결정이 필요하면 실행하지 않고 멈춘다.

선행 작업이 검증 완료 상태이고 후속 작업을 바로 요청한 경우, 남은 일이 완료 기록이나 문서 상태 정합성 정리뿐이면 별도 승인 문구를 요구하지 않는다. 검증 결과, 변경 범위, 사용자에게 이미 보고된 결과, 미확정 결정 없음이 확인되면 완료 기록 정합성 정리를 먼저 수행한 뒤 같은 요청 범위 안에서 후속 작업 지시서 작성 또는 다음 단계로 이어간다. 단, 검증 누락, 사용자에게 결과를 보고한 근거 부재, 정책 충돌, 위험 변경, 선행 작업 결과 불명확성이 있으면 멈추고 질문한다.

CDD 문서는 제품 기준 문서가 아니다. 실제 구현 기준은 대상 프로젝트의 제품 기준 문서, 기술 설계 기준 문서, 승인된 작업 기준 묶음이다.
