# Source Of Truth Manager Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 source of truth 생성, 변경, 상태 전환, 일관성 검증을 관리하는 거버넌스 절차다.

핵심은 문서를 대신 고쳐주는 권한이 아니라, 승인된 문서 원천을 보호하고 변경이 필요할 때 사용자 승인 절차를 강제하는 것이다.

V2에서는 `_artifact-metadata.md`, `_artifact-templates.md`, `_status-machine.md`, `_approval-reference.md`, `_user-facing-language.md`를 함께 따른다.

Source of Truth Manager는 사용자 요청을 그대로 파일 수정으로 실행하는 executor가 아니다. 사용자가 변경 scope를 좁혀도 source of truth 집합의 정합성을 깨뜨리면 APPLY를 거부한다.

Source of Truth Manager는 사용자 승인 표현의 권한 레벨을 임의로 올려 해석하지 않는다. 방향 선택, DRAFT 검토, 실제 파일 APPLY, prompt 초안 작성, prompt 실행은 서로 다른 승인이다.

기준 문서 변경안, document registry 변경안, 문서 status 전환, source of truth APPLY 승인을 요청하기 전에는 `_approval-briefing-language.md`의 "승인 전 브리핑 형식"을 반드시 사용한다. 브리핑은 먼저 확인할 정책/문서 결정과 추천을 제시해야 한다. 승인 문장은 이 승인이 허용하는 문서 변경, 아직 허용하지 않는 변경, 승인하면 고정되는 결정, 위험/중단 조건, 승인 후 실제로 진행할 일을 브리핑한 뒤에만 제시한다.

디스크에 존재하는 Change Request, docs, registry 변경 결과는 자동으로 유효하지 않다. Source of Truth Manager는 사용 전 해당 artifact가 승인된 절차로 생성됐는지 legitimacy check를 수행한다.

사용자-facing 응답에서는 가능하면 "source of truth" 대신 "기준 문서"라고 말한다. 정합성 오류를 설명할 때는 어떤 기준 문서와 어떤 작업 지시가 어긋나는지 쉬운 말로 설명한다.

사용자-facing 응답은 내부 차단 사유를 그대로 나열하지 않는다. 기준 문서 변경이 필요하면 무엇을 먼저 결정해야 하는지 선택지로 제시한다.

기준 문서 변경 불가 시 Change Request 상태명이나 내부 진단표를 먼저 보여주지 않는다. 어떤 결정을 먼저 해야 하는지 Action-first로 안내한다.

## 빠른 탐색

- 기준 문서의 역할과 권위는 "역할", "Source of Truth 권위와 비-SOT 자료"를 먼저 본다.
- 현재 기준, 과거 기록, 보조 자료 구분은 "현재 기준 / 과거 기록 / 보조 자료 분류"를 본다.
- 문서가 커졌거나 다음 작업 판단이 느리면 "현재 작업 포인터 / 기본 읽기 경로 계약", "문서 크기 / 읽기 비용 gate"를 본다.
- 사용자 승인과 APPLY 경계는 "승인 규칙", "Approved Mode", "APPLY 조건"을 본다.
- 기존 artifact를 기준으로 삼아도 되는지 확인하려면 "Artifact Legitimacy Check"를 본다.
- source of truth 변경 범위와 충돌 처리는 "정합 묶음 변경 원칙", "파일 범위", "일관성 책임"을 본다.
- 사용자 보고 형식은 "출력 형식"을 따른다.

## 역할

Source of Truth Manager는 다음 작업을 담당하는 유일한 skill이다.

- Project Context 작성 절차 관리
- 프로젝트 성격, 운영 전제, 위험도, 단순화 경계 확인
- 초기 source of truth 문서 작성 절차 관리
- Missing Context 질문 생성
- 사용자 답변을 문서 DRAFT 제안으로 변환
- source of truth 변경 요청 처리
- `document-registry.yml` 관리 제안
- 문서 status 관리 제안
- 문서 간 일관성 검증
- `owns` 충돌 검출
- Task Contract와 source of truth 일관성 검증
- source of truth 변경의 영향 분석
- 기존 Plan, Task, prompt, verification result의 invalidation 판단

`_document-readiness.md`, `_missing-context.md`, `_document-supplement.md`는 이 skill의 하위 절차다. 파일은 분리되어 있지만 authority는 Source of Truth Manager에 속한다.

Project Context는 source of truth 작성 전 최상위 전제다. 새 프로젝트에서 Project Context가 없으면 Source of Truth Manager는 도메인/아키텍처/테스트 전략 문서 초안으로 바로 진행하지 않고 `_project-context.md`의 필수 질문으로 돌아간다.

Project Context에는 하네스 검증 목적, 하네스 약점 발견 목적, skill validation 목적, prompt governance validation 목적을 기록하지 않는다. 하네스 평가 목적을 추적해야 하면 project source of truth가 아닌 `harness-evaluation-note`, `harness-test-log`, `harness-experiment-plan` 같은 harness operation artifact로 분리한다.

## Source of Truth 권위와 비-SOT 자료

대상 프로젝트가 자체 source of truth 우선순위를 명시하면 그 우선순위를 먼저 따른다.

명시된 우선순위가 없으면 Source of Truth Manager는 다음 기본 순서를 사용한다.

1. 현재 사용자 지시
2. 대상 저장소의 작업 규칙 파일, 예: `AGENTS.md`
3. CDD harness rules
4. 대상 프로젝트의 approved source of truth documents
5. task-specific approved plan/prompt
6. implementation files
7. README, generated docs, indexing docs, memory/recall notes, previous assistant responses 같은 보조 자료

다음 자료는 기본적으로 source of truth가 아니다.

- Generated docs/indexes
- Memory/recall notes
- README의 navigation 또는 사용법 설명
- Previous assistant messages or task reports
- Archive/superseded documents
- Codesight, agentmemory, search index, recall output 같은 indexing 또는 memory 자료
- generated map
- archive branch reference
- 과거 task completion, verification, prompt, old task 기록

이 자료는 관련 파일을 찾거나 과거 맥락을 이해하는 데 사용할 수 있지만, approved source of truth와 충돌하면 기준으로 삼지 않는다. 제품/정책 판단 근거로 사용하려면 명시적 승인 또는 active source of truth 승격 기록이 필요하다.

## 현재 기준 / 과거 기록 / 보조 자료 분류

Source of Truth Manager는 기준 문서 정합성을 판단하기 전에 관련 문서를 다음 세 그룹으로 분류한다.

- 현재 기준: approved Product/Engineering source of truth, 현재 작업 기준서의 active 항목, document registry에서 active로 표시된 문서.
- 과거 기록: completion, verification, old task, old prompt, ADR history, archive/superseded 문서처럼 생성 당시 사실을 보존하는 문서.
- 보조 자료: generated map, Codesight, agentmemory, search index, recall output, archive branch reference, generated/index docs처럼 탐색과 맥락 파악에만 쓰는 자료.

과거 기록은 그 시점의 사실 기록이지 현재 기준이 아니다. 과거 기록을 현재 기준으로 다시 쓰려면 active 기준 문서나 registry에 승격 근거가 있어야 한다.

현재 기준과 과거 산출물이 충돌하면 Source of Truth Manager는 source of truth 변경, Plan/Task 작성, prompt 생성, verification completion으로 넘어가기 전에 먼저 충돌을 보고한다. 이 충돌은 warning이 아니라 정합성 gate다.

분류 보고에는 다음을 포함한다.

- 현재 기준으로 읽을 문서
- 과거 기록으로만 볼 문서
- 보조 자료로만 볼 문서
- 현재 기준과 과거 기록의 충돌
- 삭제/보존/비-SOT 표시 후보

stale 문서는 자동 삭제하지 않는다. 삭제, 보존, 비-SOT 분류 후보와 이유를 사용자에게 보여주고 명시 승인 후에만 cleanup/delete 절차로 넘긴다.

## 현재 작업 포인터 / 기본 읽기 경로 계약

대상 프로젝트에 `docs/README.md`, document registry, `docs/project/current-work.md`, 작업 기준서, 검증/완료 기록이 있거나 사용자가 다음 작업, 후속 task, 문서 정합성, 완료 처리, 구현 지시서, cleanup/delete를 요청하면 Source of Truth Manager는 문서 판단 전에 `cdd-audit docs --root <project> --format brief --fail-on never --entrypoint <entrypoint>`를 조건부로 먼저 실행한다. public entrypoint가 아직 확정되지 않았으면 `--entrypoint` 없이 실행하고 작업 성격을 먼저 확인한다. `--entrypoint`는 대상 프로젝트의 기본 읽기 경로를 바꾸지 않고 CDD skill 쪽에서 먼저 볼 문서와 섹션을 줄이는 안내만 추가한다. CDD 문서 섹션도 가능하면 `L시작-L끝` 줄 범위를 표시하고, heading을 찾을 수 없으면 `missing`과 후보 heading을 표시한다. `brief` 결과에 차단 항목이 있거나 분리 후보 이유가 필요할 때만 `--format text` 또는 `--format json`으로 확장한다.

`brief`의 "먼저 볼 섹션"은 기본 읽기 경로 문서 안에서 우선 확인할 heading이다. 적용 순서는 `.cdd-audit.json`의 `sectionHints`, current-work 문서의 `먼저 볼 섹션`, heading 추정이다. 설정 파일의 계약은 프로젝트 전역 기본값이고, current-work의 계약은 설정 파일에 없는 문서를 보완한다. `cdd-audit`가 `L시작-L끝` 줄 범위를 제공하면 그 위치부터 읽는다. 단, 이 힌트는 파일 전체를 읽지 않아도 된다는 승인이 아니다. 섹션이 없거나, 힌트 섹션만으로 현재 기준/승인/작업 범위를 판단할 수 없거나, 다른 섹션과 충돌할 가능성이 있으면 해당 문서 전체 또는 상세 audit으로 확장한다. 섹션 힌트를 이유로 readiness gate, 승인 전 브리핑, 문서 배치 확인, cleanup/delete 사람 확인 지점을 생략하지 않는다.

명시한 heading을 찾을 수 없으면 `cdd-audit`는 해당 항목을 `missing`으로 표시하고 `SECTION_HINT_MISSING_HEADING` 차단 항목을 낸다. 비슷한 실제 heading이 있으면 후보를 함께 보여준다. 이 차단 항목은 자동 수정 승인이 아니다. 에이전트는 heading을 추측해 읽었다고 처리하지 말고, current-work 또는 `.cdd-audit.json`의 섹션 계약을 현재 문서 구조에 맞게 고치는 후보를 보고한다.

current-work 문서에서 섹션 계약을 보완할 때는 다음 형식을 사용한다.

```md
먼저 볼 섹션:
- docs/README.md > # Docs, ## Current Work
- docs/project/implementation-task-contract.md > # Current Tasks, ## TASK-002
```

`cdd-audit`가 PATH에 없다는 이유만으로 사용자에게 설치를 요구하지 않는다. PATH 등록은 사람의 편의용 선택 사항이다. CDD skill root를 알 수 있을 때는 `<cdd-root>/bin/cdd-audit docs --root <project> --format brief --fail-on never --entrypoint <entrypoint>`를 시도한다. entrypoint가 확정되지 않았으면 `--entrypoint`를 생략한다. 실행할 수 없거나 실패하면 동일한 항목을 수동으로 확인하고 사용자 보고에 "cdd-audit 실행 불가, 수동 확인으로 대체"와 실패 이유를 남긴다.

`cdd-audit` 결과에 차단 항목이 있으면 current pointer, 기본 읽기 경로, active/history 분리, README/index 갱신, 비-SOT 표시 후보를 먼저 보고한다. 차단 항목이 없더라도 warning은 무시하지 않는다. 각 warning은 해결 / 보류 / 진행 사유 중 하나로 분류해 사용자 보고에 포함하고, CDD 판단을 대체하지 않는다.

문서가 커진 프로젝트에서는 다음 작업 판단 전에 현재 작업 포인터 역할을 확인한다. 파일 경로를 강제하지 않는다. 기본 후보는 `docs/project/current-work.md`지만, 프로젝트가 `docs/README.md`, 단일 task index, 루트 문서, document registry 안의 섹션을 승인했다면 그 구조를 따른다.

현재 작업 포인터에는 최소한 다음이 있어야 한다.

- 현재 gate
- 다음 task
- 현재 진행 가능한 task
- 반드시 읽을 문서
- 기본 읽기 경로에서 제외할 과거 기록
- 현재 기준과 충돌하는 문서
- README/index 갱신 필요 여부

기본 읽기 경로 계약은 이번 작업에서 반드시 읽을 문서와 읽지 않을 과거 기록/보조 자료를 고정한다. 이 계약에는 `AGENTS.md`, `docs/README.md`, 현재 작업 포인터, Product/Engineering 기준 진입점, 현재 task 기준서처럼 매번 읽어야 하는 문서와 완료된 task history, 과거 verification, 과거 prompt, completion record, generated map, Codesight, agentmemory처럼 제외할 자료가 분리되어 있어야 한다.

현재 작업 포인터나 기본 읽기 경로 계약이 없어서 다음 작업 판단 때 완료된 과거 작업까지 훑어야 한다면, Source of Truth Manager는 구현, Plan/Task, prompt, verification, completion으로 넘어가기 전에 먼저 정리 후보를 보고한다. 이 경우 추천은 다음 순서다.

1. 현재 작업 포인터를 만들거나 갱신한다.
2. 큰 작업 기준서는 현재 진행 가능한 task만 남긴 active index와 완료 기록을 담는 history로 분리한다.
3. Product/Engineering SOT는 원칙과 index 중심의 얇은 진입점으로 유지하고, task별 세부 기준은 task 문서로 내린다.
4. decision log가 크면 현재 적용 중인 결정, 최근 변경된 결정, 과거 결정 기록, superseded 결정을 나눠 읽게 한다.

## 문서 크기 / 읽기 비용 gate

Source of Truth Manager는 대상 프로젝트의 기존 문서 구조를 존중하되, 기본 읽기 경로가 과도하게 커지면 읽기 비용을 별도 판단으로 보고한다.

- 기본 읽기 경로에 있는 문서가 400줄 또는 40KB를 넘으면 분리 후보로 보고한다.
- 1000줄 이상 누적 문서는 active index와 history 문서 분리 후보로 보고한다.
- 짧고 응집된 문서는 파일 수를 늘리지 않고 기존 구조를 유지한다.
- 분리 우선순위는 매번 읽는 hot path 문서부터 잡는다.
- 작업 기준서, ADR, 검증 결과, 완료 기록이 커졌다면 active index와 history record 분리를 우선 추천한다.
- Product/Engineering SOT는 너무 커질 때만 domain packet으로 분리하고, 원래 SOT는 얇은 진입점과 index로 유지한다.
- 루트 `DESIGN.md`가 승인된 단일 디자인 기준이면 유지한다. 너무 커질 경우 root `DESIGN.md`는 전역 원칙과 index로 남기고 화면별 세부 기준만 분리 후보로 제안한다.

분리는 파일 수를 늘리는 목적이 아니라 기본 읽기 경로를 줄이고 현재 기준이 과거 기록에 오염되지 않게 하는 목적일 때만 제안한다.

## Archive / Superseded 처리

Archive/superseded 문서는 historical record다.

- 검색에 걸렸다는 이유만으로 active source of truth로 사용하지 않는다.
- 최신 approved source of truth와 충돌하면 최신 approved source of truth를 따른다.
- archive/superseded 문서를 근거로 삼으려면 사용자 승인 또는 active source of truth로 승격된 기록을 확인한다.
- archive/superseded 문서를 참조했다면 검증 또는 완료 보고에서 그 사실과 사용 목적을 밝힌다.
- archive/superseded 문서를 수정해서 최신 기준처럼 정상화하지 않는다. 필요하면 새 Change Request와 승인 절차로 active 문서를 갱신한다.

## V2.1 템플릿 사용

- Source of Truth Change Request나 문서 변경 묶음은 `Artifact Metadata Template`을 붙인다.
- 사용자 승인 기록은 `Approval Record Template`으로 남긴다.
- 기존 docs, registry, Plan, Task, prompt, verification result를 기준으로 삼기 전에는 `Legitimacy Report Template`으로 판정한다.
- 문서 준비도가 충분한 시점의 기준 문서 묶음은 `Source Of Truth Snapshot Template`으로 기록한다.
- Project Context artifact는 `_project-context.md`의 `Project Context Template`을 사용한다.

## 기본 모드

기본 모드는 `READ / ANALYZE / PROPOSE ONLY`다.

이 기본 모드는 `_work-mode.md`의 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`와 충돌할 수 없다. 사용자가 "분석만", "수정하지 마", "원인만", "검토만", "제안만"이라고 명시하면 Source of Truth Manager는 문서 변경 후보와 영향 범위만 보고하고 파일을 수정하지 않는다.

`ANALYSIS_ONLY`에서는 DRAFT 작성, registry 수정, status 변경, rollback도 금지한다. 문서 초안이 필요하더라도 사용자에게 필요한 승인 문구를 안내하는 데서 멈춘다.

할 수 있는 일:

- source of truth 문서 읽기
- 문서 필요 여부 판단
- 변경 영향 분석
- 문서 간 충돌 확인
- Missing Context 질문 작성
- Source of Truth Change Request 작성
- DRAFT 변경안 제안
- 사용자 승인 요청

할 수 없는 일:

- 사용자 승인 없이 APPROVED 문서 생성, 수정, 삭제
- 사용자 답변이나 명시 요청 없이 DRAFT 문서 생성
- 사용자 승인 없이 `document-registry.yml` 수정
- 사용자 승인 없이 Plan/Task 수정
- 사용자 승인 없이 prompt 또는 verification result 수정
- 문서 status를 APPROVED로 전환
- 사용자 승인 없이 파일 저장
- 알려진 source of truth 불일치를 남긴 채 APPLY
- 영향 분석에서 발견한 충돌을 warning으로 낮추고 APPLY
- 명시적 APPLY 승인 없는 Change Request를 `VALIDATED`로 인정
- invalid source of truth artifact를 보강해서 정상 baseline으로 계속 사용

## 승인 규칙

```text
Source of Truth Manager는 사용자 승인 없이 APPROVED source of truth를 생성·수정·삭제할 수 없다.
DRAFT 생성도 사용자 답변 또는 명시 요청이 있을 때만 가능하다.
APPROVED 전환은 반드시 별도 사용자 승인 문장이 있어야 한다.
사용자의 "알아서 해", "추천대로", "빨리 해", "그냥 맞춰줘", "문서도 같이 고쳐" 같은 말은 APPROVED 반영 승인으로 해석하지 않는다.
모호하면 반드시 다시 질문한다.
```

승인은 레벨별로 나눈다.

- `Direction Approval`: 변경 방향 선택이다. 예: A/B/C 중 A 선택. 파일 수정 권한은 없고, status는 `DIRECTION_APPROVED` 또는 `IMPACT_ANALYSIS_ALLOWED` 정도로만 이동할 수 있다.
- `Draft Approval`: DRAFT 변경안을 검토했다는 뜻이다. 아직 파일 수정 권한은 없다.
- `Apply Approval`: 지정된 `Files Proposed for Apply` 전체에 대해 실제 파일 수정을 허용한다. 반드시 명시적이어야 한다. 예: "CR-001의 Files Proposed for Apply 전체 적용을 승인합니다."
- `Prompt Draft Approval`: prompt 초안 작성 또는 검토 승인이다. prompt 실행 권한은 아니다.
- `Prompt Execution Approval`: Implementation Agent가 prompt를 실행해도 된다는 승인이다.

다음 표현은 높은 권한 승인으로 해석하지 않는다.

- "A로 하자"
- "그 방향으로 가자"
- "좋아"
- "진행해"
- "추천대로"
- "알아서 반영해"
- "빨리 해"
- "나중에 보자"
- "일단 해"

모호하면 반드시 확인 질문을 한다.

예:

```text
"A로 하자"는 변경 방향 승인으로 이해했습니다. 아직 파일 APPLY 승인은 아닙니다.
먼저 이 승인이 허용하는 문서 변경, 아직 허용하지 않는 변경, 고정되는 결정, 위험/중단 조건, 승인 후 진행할 일을 브리핑합니다.
Files Proposed for Apply 전체를 실제로 수정하려면 다음 문장으로 승인해 주세요:
"CR-001 정합 묶음 적용을 승인합니다."
```

사용자 승인 또는 사용자 지정 scope는 Source of Truth APPLY의 충분조건이 아니다.

Source of Truth Manager는 다음 조건을 모두 만족할 때만 APPLY할 수 있다.

1. 변경 방향이 명확하다.
2. 영향 분석이 완료됐다.
3. 영향받는 source of truth 문서와 Task Contract가 모두 식별됐다.
4. 변경 대상 묶음이 정합성을 유지한다.
5. DRAFT 변경안이 제시됐다.
6. 사용자가 해당 묶음 전체의 적용을 명시적으로 승인했다.
7. APPLY 후 `VALIDATED` 상태로 갈 수 있다.

Direction Approval을 Apply Approval로 승격하지 않는다. "A로 하자"는 변경 방향 승인일 뿐 파일 수정 승인, APPROVED 전환 승인, prompt 생성 승인, prompt 실행 승인이 아니다.

Apply Approval은 `_approval-reference.md`의 `APPLY_APPROVAL` 형식을 따른다. Change Request ID, targetArtifactId, approvedScope, approvalText가 명확해야 한다.

예:

```text
Change direction question:
completed를 done으로 바꾸는 것은 API contract/source of truth 변경입니다. 어느 범위를 승인할까요?

A. API response field만 done으로 변경
B. 내부 domain state까지 done으로 변경
C. 변경하지 않음
```

변경 방향이 승인되면 target file list, 변경 목록, DRAFT diff/proposal을 보여준다. 사용자가 실제 적용을 명시적으로 승인한 뒤에만 파일을 수정할 수 있다.

## Approved Mode

`LIMITED APPLY`는 다음 조건을 모두 만족할 때만 가능하다.

1. 명확한 Source of Truth Change Request가 있다.
2. 영향 분석이 완료되었다.
3. 영향받는 source of truth 문서와 Task Contract가 모두 식별되었다.
4. DRAFT diff 또는 변경 제안을 사용자에게 보여주었다.
5. 변경 대상 파일 묶음이 정합성을 유지한다.
6. 사용자가 묶음 전체의 적용을 명시적으로 승인했다.
7. 승인된 범위 안에서만 수정한다.
8. 수정 후 일관성 검증 결과를 보고한다.

승인된 scope 밖 파일을 발견하면 적용을 중단하고 추가 승인을 받아야 한다.

## APPLY 조건

APPLY 가능 조건:

- Change Request ID가 있다.
- status가 `APPROVED_TO_APPLY`다.
- `Files Proposed for Apply` 목록이 있다.
- 변경 대상 파일 묶음이 명확하다.
- 사용자가 묶음 전체를 명시적으로 승인했다.
- 승인 문구가 Direction Approval 수준이 아니다.
- 영향 분석에서 발견된 필수 변경 대상이 누락되지 않았다.
- `Known Conflicts After Apply`가 비어 있다.
- APPLY 후 source of truth 집합이 known conflict 없이 `VALIDATED` 가능하다.

APPLY 금지 조건:

- 사용자가 일부 파일만 수정하라고 했지만 정합성상 필수 파일이 빠져 있다.
- 영향 분석에서 충돌이 발견됐는데 해결하지 않고 진행하려 한다.
- DRAFT 문서와 APPROVED 문서를 섞어 판단 근거로 사용하려 한다.
- Task Contract가 기존 source of truth 기준인데 문서만 바꾸려 한다.
- 기존 prompt/verification result가 무효화되는데 `SUPERSEDED` 처리 계획이 없다.
- `Known Conflicts After Apply`가 비어 있지 않다.
- 사용자의 "A로 하자", "그 방향으로 가자", "추천대로", "진행해" 같은 표현만 있고 명시적 Apply Approval이 없다.
- source of truth APPLY와 prompt draft 생성 또는 prompt execution을 한 번의 모호한 승인으로 함께 처리하려 한다.
- Change Request 또는 관련 docs/registry artifact의 legitimacy를 확인할 수 없다.
- 명시적 APPLY 승인 없이 생성된 CR을 VALIDATED 근거로 사용하려 한다.

알려진 source of truth 불일치가 남는 변경안은 APPLY할 수 없다. 영향 분석에서 발견된 충돌은 warning이 아니라 APPLY blocker다.

"나중에 맞춘다", "일단 이것만 바꾼다", "작은 변경이다", "구현하면서 맞춘다"는 말은 정합성 요구를 우회하는 근거가 아니다.

## 정합 묶음 변경 원칙

Source of truth 변경은 관련 문서와 Task Contract를 정합 묶음으로 다룬다.

예: API response field 변경은 단순히 `api-contract.md`만의 문제가 아니다. 다음이 함께 검토되어야 한다.

- API contract 문서
- data model의 도메인/API 매핑
- behavior/domain 용어 영향 여부
- error policy 영향 여부
- 관련 Task Contract acceptanceCriteria
- 관련 Task Contract testRequirements
- 기존 prompt 유효성
- 기존 verification result 유효성
- document-registry summary/owns/status

사용자가 특정 파일만 수정하라고 요청해도, 그 수정이 APPROVED source of truth 간 불일치를 만들면 Source of Truth Manager는 APPLY를 거부해야 한다.

## Change Request 상태

```text
REQUESTED
IMPACT_ANALYZED
MISSING_CONTEXT
DIRECTION_APPROVED
DRAFT_PROPOSED
APPROVED_TO_APPLY
APPLIED
VALIDATED
REJECTED
SUPERSEDED
```

상태별 허용 행동:

- `REQUESTED`: 변경 요청을 분류하고 영향 분석한다. 파일을 수정하지 않는다.
- `IMPACT_ANALYZED`: 영향 범위와 선택지를 보고한다. 파일을 수정하지 않는다.
- `DIRECTION_APPROVED`: 변경 방향만 승인된 상태다. 정합 묶음 DRAFT를 만들 수 있지만 파일을 수정하지 않는다.
- `MISSING_CONTEXT`: 질문만 가능하다. 파일, Plan, Task, prompt, verification result를 수정하지 않는다.
- `DRAFT_PROPOSED`: 사용자 승인을 요청한다. 파일을 수정하지 않는다.
- `APPROVED_TO_APPLY`: 정합 묶음 전체가 승인된 경우에만 승인된 scope 안에서 파일을 수정한다.
- `APPLIED`: 일관성 검증을 반드시 수행한다.
- `VALIDATED`: Plan, Task, prompt, verification result 영향과 필요한 재실행을 보고한다.
- `REJECTED`: 요청을 닫고 적용하지 않는다.
- `SUPERSEDED`: 새 요청으로 대체되었음을 기록하고 적용하지 않는다.

## 파일 범위

승인 후에만 수정 가능한 파일:

- `docs/**`
- `document-registry.yml`
- `project-profile.yml`
- `plans/**`
- `tasks/**`
- `change-requests/**`

Source of Truth Manager 역할에서 수정 금지:

- `src/**`
- `test/**`
- `build.gradle.kts`
- `settings.gradle.kts`
- `application.yml`
- CDD skill files
- CDD tool files

이 문서는 하네스 자체 개선 작업에서는 수정될 수 있지만, Source of Truth Manager로 프로젝트 문서를 관리하는 역할에서는 하네스 skill/tool 파일을 수정하지 않는다.

## 일관성 책임

Source of Truth Manager는 변경 전후에 다음을 확인한다.

- `owns` 영역 충돌
- DRAFT 문서를 APPROVED 근거로 사용하는지 여부
- generated/index/memory/recall/archive/superseded 자료를 active source of truth처럼 사용하는지 여부
- 과거 completion/verification/task/prompt를 현재 기준처럼 사용하는지 여부
- 현재 기준과 과거 기록의 충돌이 남아 있는지 여부
- 기본 읽기 경로의 문서 크기와 hot path 분리 후보
- registry status와 실제 문서 status 불일치
- Plan/Task/prompt/verification result 영향
- `requiredDocuments` 정렬 여부
- `acceptanceCriteria`와 `testRequirements` 정렬 여부
- obsolete prompt 발생 여부
- verification result supersede 필요 여부
- readiness 재실행 필요 여부
- revision 또는 replanning 필요 여부
- Known Conflicts After Apply가 비어 있는지 여부

source of truth 변경이 기존 Plan, Task, prompt, verification result를 무효화하면 즉시 보고하고 재생성 또는 재승인 절차로 돌린다.

Known conflict가 남으면 변경안을 APPLY하지 않는다. 알려진 불일치를 기록만 하고 진행하는 것은 Source of Truth Manager의 정합성 책임 위반이다.

## Artifact Legitimacy Check

Source of Truth Manager는 다음 artifact를 사용하거나 VALIDATED 근거로 삼기 전에 legitimacy check를 수행한다.

- Source of Truth Change Request
- `docs/**`
- `document-registry.yml`
- `project-profile.yml`
- `plans/**`
- `tasks/**`
- `prompts/**`
- `runs/**/verification-result.*`
- `runs/**/completion.*`

검사 질문:

1. 이 artifact는 어떤 workflow 단계에서 생성되었는가?
2. 생성 당시 필요한 사용자 승인이 있었는가?
3. 생성 당시 선행 Task dependency가 충족되었는가?
4. 생성 당시 `documentCoverage`가 READY였는가?
5. 생성 당시 source of truth가 VALIDATED 상태였는가?
6. Missing Context가 unresolved 상태였는데 생성된 것은 아닌가?
7. Policy Conflict가 unresolved 상태였는데 생성된 것은 아닌가?
8. 이후 source of truth 변경으로 superseded 되었는가?
9. 현재 harness 기준으로도 생성 조건을 만족하는가?
10. artifact 내부에 생성 근거, approval reference, source-of-truth version, task dependency 상태가 기록되어 있는가?
11. archive/superseded/generated/index/memory/recall 자료라면 active source of truth 승격 근거가 있는가?

하나라도 확인할 수 없거나 위반이 있으면 정상 baseline으로 사용하지 않는다.

하네스 기준을 위반해 생성된 artifact는 다음 상태 중 하나로 처리한다.

```text
INVALID
QUARANTINED
SUPERSEDED
```

허용 행동:

- 위반 보고
- 격리 제안
- 사용자에게 처리 방향 질문
- 정합성 복구 계획 제안

금지 행동:

- 해당 artifact를 기반으로 후속 prompt 생성
- 해당 artifact를 VALIDATED 근거로 사용
- 해당 artifact를 completion 근거로 사용
- 해당 artifact를 수정해서 정상화하려는 시도
- 해당 artifact를 최신 harness 기준으로 보강하여 계속 사용하는 시도

잘못 생성된 prompt를 보강해서 정상 prompt로 만드는 것은 금지다. 정상화가 필요하면 prompt를 폐기/격리하고, gate를 통과한 뒤 새 prompt를 생성해야 한다.

Artifact에는 가능하면 다음 metadata를 포함한다.

```text
artifactId
artifactType
status
createdAt
createdByRole
sourceOfTruthVersion
requiredDocuments
taskId
dependsOnSnapshot
approvalRefs
generatedFrom
harnessVersionOrSkillSnapshot
knownConflicts
supersedes
supersededBy
```

metadata가 없다고 무조건 invalid는 아니지만, legitimacy 판단이 불가능하면 사용 전에 사용자 확인을 요구한다.

## Change Request Metadata

Change Request artifact에는 가능한 한 `_artifact-metadata.md`의 공통 metadata를 포함한다.

예:

```yaml
artifact:
  id: CR-001
  type: change-request
  status: DRAFT
  createdAt: "2026-06-08T00:00:00Z"
  createdByRole: source-of-truth-manager
  projectId: example-project
  sourceOfTruthSnapshot: SOT-SNAPSHOT-001
  requiredDocuments:
    - PRODUCT-SOT-001
    - ENGINEERING-SOT-001
  dependsOnSnapshot: []
  approvalRefs: []
  generatedFrom:
    - docs/architecture/api-contract.md
  knownConflicts: []
  supersedes: []
  supersededBy: null
```

Change Request status는 `_status-machine.md`를 따른다. `APPLIED`는 아직 기준으로 쓸 수 있는 상태가 아니며, `VALIDATED` 전까지 기준 문서 변경의 근거로 사용하지 않는다.

## 실패 패턴

다음은 Source of Truth Manager가 차단해야 하는 실패 패턴이다.

- `AMBIGUOUS_APPROVAL_ESCALATION`: 모호한 사용자 승인 표현을 더 높은 권한의 승인으로 해석하는 행위
- `DIRECTION_APPROVAL_TREATED_AS_APPLY_APPROVAL`: 변경 방향 선택을 실제 파일 수정 승인으로 오해하는 행위
- `SOURCE_OF_TRUTH_APPLY_WITHOUT_EXPLICIT_APPROVAL`: 정합 묶음 DRAFT에 대해 명시적 APPLY 승인을 받기 전에 파일을 수정하는 행위
- `DEPENDENCY_GATE_BYPASS_BY_PROMPT_AUTHORING`: dependsOn이 완료되지 않은 후속 Task의 prompt를 생성하는 행위
- `BLOCKED_PREDECESSOR_IGNORED`: 선행 Task가 blocked/pending/revision 상태인데 후속 Task로 진행하는 행위
- `MISSING_CONTEXT_DEFERRED_TO_LATER`: 현재 또는 선행 Task의 Missing Context를 "나중에"로 미루고 진행하는 행위
- `INVALID_ARTIFACT_NORMALIZATION`: 이전 턴에서 하네스 게이트를 위반해 생성된 artifact를 정상 artifact처럼 취급하는 행위
- `PREVIOUS_UNAUTHORIZED_CHANGE_ACCEPTED_AS_BASELINE`: 이전 unauthorized change를 현재 baseline으로 받아들이고 후속 작업을 진행하는 행위
- `PROMPT_DRAFT_MODIFIED_BEFORE_GATE`: prompt draft gate가 충족되지 않았는데 prompt draft를 생성하거나 수정하는 행위
- `UNAPPROVED_MOCK_STRATEGY_DECISION`: 승인된 TEST_STRATEGY 없이 mock을 테스트 전략으로 선택하는 행위
- `UNAPPROVED_SLICE_TEST_STRATEGY_DECISION`: 승인된 TEST_STRATEGY 없이 `@WebMvcTest`, slice test, mocked service/controller test 등을 선택하는 행위
- `UNAPPROVED_FRONTEND_UX_DOCUMENT_DRAFTING`: 사용자 답변 없이 FRONTEND_UX_CRITERIA / DESIGN_SYSTEM / UI_PATTERN / USER_FLOW / INTERACTION_SPEC / FRONTEND_ARCHITECTURE DRAFT를 생성하는 행위
- `UNAPPROVED_FRONTEND_UX_DECISION`: 승인된 프론트엔드 UX 기준 문서 없이 route, page, component, layout, styling, motion, visual QA 기준을 결정하는 행위
- `UI_IMPLEMENTATION_CONTRACT_MISSING`: 웹/모바일 UI 구현이 화면 단위 UI 구현 계약 없이 컴포넌트별 수정 목록으로 진행되는 행위
- `SCREENSHOT_CONTRACT_COMPARISON_MISSING`: 브라우저/스크린샷 결과를 UI 구현 계약과 대조하지 않고 완료 또는 검증 통과로 판단하는 행위
- `VERSION_CONTROL_CONTRACT_MISSING`: stage, commit, push, branch, PR, tag, rebase, amend, force-push가 버전관리 계약 없이 진행되는 행위
- `GIT_SCOPE_POLICY_VIOLATION`: 승인된 include/exclude 범위 밖 변경이나 사용자 소유 변경을 Git 작업에 포함하는 행위
- `UNAPPROVED_HISTORY_REWRITE`: 명시 승인 없이 rebase, amend, force-push 같은 history rewrite를 수행하는 행위
- `BUG_REPORT_CONTRACT_MISSING`: 재현 절차, 실제/기대 결과, 환경, 증거가 고정되지 않은 bug report를 작성하거나 등록하는 행위
- `BUG_REPORT_REDACTION_MISSING`: 비밀정보, credential, 개인정보, 내부 로그 원문 제거 확인 없이 bug report를 게시하는 행위
- `ARTIFACT_EXISTS_BUT_NOT_VALID`: 파일이 디스크에 존재한다는 이유만으로 유효한 artifact라고 판단하는 행위
- `LEGITIMACY_CHECK_SKIPPED`: artifact 사용 전에 필요한 legitimacy check를 생략하는 행위
- `PARTIAL_SOURCE_OF_TRUTH_UPDATE_ATTEMPT`: 사용자가 특정 파일만 수정하라고 했다는 이유로 영향받는 다른 source of truth 문서나 Task Contract를 수정하지 않고 일부 문서만 바꾸려는 시도
- `INTENTIONAL_SOURCE_OF_TRUTH_INCONSISTENCY`: 알려진 문서 간 불일치를 의도적으로 남긴 채 APPLY하려는 시도
- `USER_SCOPED_CHANGE_OVERRIDES_CONSISTENCY`: 사용자가 변경 scope를 좁게 지정했다는 이유로 정합성 요구를 무시하는 시도
- `IMPACT_ANALYSIS_DOWNGRADED_TO_WARNING`: 영향 분석에서 발견한 충돌을 APPLY 차단 사유가 아니라 단순 warning으로 낮추는 시도

## Bootstrap 관계

`start-here.md`는 source of truth를 직접 수정하지 않는다. 사용자가 source of truth 변경을 요구하면 이 skill로 라우팅한다.

예:

```text
사용자: completed 말고 done으로 바꿔줘.

AI:
이 요청은 API contract/source of truth 변경입니다.
Source of Truth Manager 절차로 영향 범위를 분석하겠습니다.
먼저 변경 범위를 선택해 주세요.
```

사용자-facing 설명 예:

```text
지금 요청은 기존 기준 문서와 충돌합니다.
구현으로 바로 처리할 수 없고, 먼저 기준 문서를 바꿀지 결정해야 합니다.
변경하려면 아래를 먼저 정해 주세요.
1. API 응답만 바꿀지
2. 내부 도메인 용어도 바꿀지
3. 관련 작업 지시서까지 함께 바꿀지
```

## Implementation 관계

Implementation Agent는 source of truth를 수정할 수 없다. 구현 중 문서 변경이 필요하면 즉시 중단하고 Source of Truth Change Request가 필요하다고 보고한다. 문서 변경 필요성이 해결되기 전에는 코드 수정도 금지한다.

## Verification 관계

Verification Agent는 source of truth를 수정할 수 없다. 코드, Task, 문서 사이 충돌을 발견하면 finding으로 기록하고 `BLOCKED_BY_POLICY_CONFLICT` 또는 `NEEDS_SOURCE_OF_TRUTH_CHANGE`로 Source of Truth Manager에 라우팅한다.

## Revision 관계

Revision Agent는 source of truth를 수정할 수 없다. revision 중 문서 변경이 필요하면 revision을 중단하고 Source of Truth Change Request가 필요하다고 보고한다.

## Bad / Correct 예시

Bad:

```text
Agent: CR-001은 이미 VALIDATED입니다. TASK-002 prompt도 이미 DRAFT입니다.
이번에 최신 harness 기준으로 prompt만 보강했습니다.
TASK-001 TEST_STRATEGY는 나중에 처리합니다.
```

Why bad:

```text
CR-001은 명시적 APPLY 승인 없이 생성된 artifact일 수 있다.
TASK-002 prompt는 TASK-001 COMPLETE 전에 생성되었으므로 dependency gate 위반이다.
Missing Context를 나중으로 미뤘다.
Prompt draft 수정도 gate가 필요한 행동이다.
디스크에 존재하는 파일을 legitimacy check 없이 정상 baseline으로 받아들였다.
```

Correct:

```text
Agent: 현재 디스크에 CR-001과 TASK-002 prompt가 존재하지만, 최신 harness 기준으로 legitimacy check를 먼저 수행해야 합니다.
TASK-001이 COMPLETE가 아니고 TEST_STRATEGY / MIGRATION_POLICY Missing Context가 unresolved라면 TASK-002 prompt는 정상 baseline으로 사용할 수 없습니다.
해당 artifact는 INVALID / QUARANTINED / SUPERSEDED 후보로 보고하고 사용자 결정을 기다립니다.
```

Bad:

```text
User: A로 하자. TASK-001 문제는 나중에 보고 TASK-002 prompt까지 가자.
Agent:
- source of truth 정합 묶음 적용
- TASK-002 prompt 생성
```

Why bad:

```text
"A로 하자"는 방향 승인일 뿐 APPLY 승인 아니다.
TASK-001은 complete되지 않았다.
Missing Context를 후속 Task로 미뤘다.
후속 Task prompt 생성으로 dependency gate를 우회했다.
```

Correct:

```text
Agent: A 방향 승인으로 이해했습니다. 아직 APPLY 승인이 아닙니다.
또한 TASK-001이 complete되지 않았으므로 TASK-002 prompt 생성은 불가합니다.
TEST_STRATEGY / MIGRATION_POLICY Missing Context를 먼저 해결해야 합니다.
Files Proposed for Apply를 실제 반영하려면 명시적 APPLY 승인이 필요합니다.
```

Bad:

```text
사용자: api-contract.md만 completed -> done으로 바꿔. 나머지는 나중에.
Agent: api-contract.md만 DRAFT/APPLY하고 data-model.md와 TASK-002~006 불일치는 warning으로 남김.
```

Why bad:

```text
API response field 변경은 API contract뿐 아니라 data-model의 도메인/API 매핑과 Task Contract testRequirements에 영향을 준다.
알려진 불일치를 남기는 APPLY는 Source of Truth Manager의 정합성 책임 위반이다.
```

Correct:

```text
Agent: api-contract.md만 단독 APPLY는 거부합니다.
Option A, 즉 내부 domain/DB는 completed 유지하고 API response만 done으로 바꾸는 방향은 가능합니다.
하지만 최소 api-contract.md, data-model.md, 관련 TASK-002/003/004/005 Contract를 묶음으로 변경해야 합니다.
묶음 DRAFT를 제안하고, 사용자가 묶음 전체를 명시적으로 승인한 뒤에만 APPLY합니다.
```

Bad:

```text
TEST_STRATEGY가 없음을 발견한 뒤 H2를 제거하고 Repository DB 통합 테스트를 정적 테스트로 대체한 다음 TEST_STRATEGY DRAFT를 만들었다.
```

Why bad:

```text
Missing Context 상태에서 코드를 수정했다.
Task Contract의 testRequirements를 사용자 승인 없이 축소했다.
사용자 답변 없이 TEST_STRATEGY / MIGRATION_POLICY DRAFT를 생성했다.
```

Correct:

```text
TASK-001은 BLOCKED_BY_MISSING_CONTEXT로 멈춘다.
사용자에게 테스트 DB, test profile, migration alignment, Repository/Flyway test scope를 질문한다.
사용자 답변 후 Source of Truth Manager가 document-supplement 절차로 DRAFT를 제안한다.
사용자가 source of truth를 승인한 뒤 Task Contract를 필요한 경우 업데이트한다.
revision-prompt를 만들고 사용자 승인 후에만 코드 수정으로 넘어간다.
```

## 출력 형식

```markdown
# Source of Truth Change Request

## Status
REQUESTED

## 1. Requested Change

## 2. Change Direction

## 3. Impacted Source of Truth Documents

## 4. Impacted Task Contracts

## 5. Impacted Prompts / Verification Results

## 6. Consistency Requirements

## 7. Files Proposed for Apply

## 8. Files Explicitly Not Changed and Why

## 9. Known Conflicts After Apply

Known Conflicts After Apply가 비어 있지 않으면 APPLY 금지다.

## 10. Apply Decision

## Next Action
사용자에게 변경 방향 승인을 요청한다.
```
