# Cleanup / Delete Playbook

> Access: Public entrypoint.
> 사용자 직접 호출 가능: 삭제, 폐기, legacy 제거, dead code 정리 작업을 다룰 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

이 playbook은 리팩토링이 아니라 폐기, 삭제, 정리 작업을 다룬다.

목표는 approved source of truth에서 더 이상 현재 제품 경계에 속하지 않는 legacy 기능을 근거 있게 제거하되, 삭제 전 의존성, 보존 방식, 데이터 손실, public API, 테스트, 문서 영향을 확인하게 하는 것이다.

이 playbook은 자동화 도구가 아니다. CLI, script, dependency를 추가하지 않는다.

## 빠른 탐색

- 처음에는 "최소 읽기 경로", "사용 시점", "금지되는 오해", "사람 확인 지점"만 먼저 본다.
- cleanup/delete로 분류할지 먼저 보려면 "사용 시점"과 "금지되는 오해"를 본다.
- 삭제 전 기준 확인은 "작업 전 확인"을 본다.
- 보존/비-SOT/삭제 분류는 "Keep List", "Stale 문서 분류", "Delete List"를 본다.
- 의존성과 삭제 방식은 "의존성 확인", "삭제 전략"을 본다.
- 사용자 승인이 필요한 지점은 "사람 확인 지점"을 본다.
- 검증과 완료 보고는 "검증 항목", "완료 보고 형식"을 본다.

## 최소 읽기 경로

cleanup/delete 요청이면 먼저 삭제인지 보존/비-SOT 표시인지 분류하고, `cdd-audit docs --root <project> --format brief --fail-on never`로 현재 기준과 제외할 과거 기록을 확인한다. 이 경로는 삭제 승인이나 보존 정책을 대체하지 않는다. 삭제 후보 목록, 보존 후보, 비-SOT 표시 후보와 추천을 브리핑하기 전에는 파일을 삭제하지 않는다.

실제 삭제, public API 제거, migration, 데이터 삭제, 되돌리기 어려운 변경이 포함될 때만 `_authority-boundary.md`, `_artifact-templates.md`, `_approval-reference.md`, `_implementation-rules.md`, `_user-facing-language.md`를 연다.

## 사용 시점

다음 경우에는 cleanup/delete 작업으로 분류한다.

- 제품 방향이 바뀌어 기존 기능을 제거한다.
- deprecated 기능을 실제 코드에서 삭제한다.
- archive branch/tag 또는 다른 보존 방식 이후 현재 브랜치를 축소한다.
- dead code, stale API, stale UI, stale DB artifact를 제거한다.
- superseded 문서나 이전 구현 흔적이 새 source of truth를 오염시킨다.
- stale 작업 기준서, 완료 기록, 검증 기록, old prompt가 현재 기준처럼 읽힐 위험이 있어 삭제/보존/비-SOT 분류가 필요하다.
- 리팩토링이 아니라 폐기가 목적이다.

## 금지되는 오해

- cleanup/delete는 리팩토링이 아니다.
- cleanup/delete는 새 기능 구현이 아니다.
- cleanup/delete는 기존 기능을 이름만 바꿔 살리는 작업이 아니다.
- cleanup/delete는 source of truth가 폐기한 기능을 "미래 확장성"이라는 이유로 core path에 남기는 작업이 아니다.
- cleanup/delete는 테스트를 쉽게 통과시키려고 검증을 약화하는 작업이 아니다.
- cleanup/delete는 stale 문서를 자동 삭제하는 작업이 아니다. 삭제, 보존, 비-SOT 분류 후보와 이유를 사용자에게 보여주고 승인받아야 한다.

기존 외부 계약과 행위 의미를 유지하면서 내부 구조만 바꾸면 리팩토링이다. 기능, API, 데이터, 문서, 테스트 범위, dependency를 제거하거나 비노출하는 판단이 들어가면 cleanup/delete로 다룬다.

## 작업 전 확인

삭제 전에 다음을 확인한다.

- 현재 사용자 지시
- 대상 저장소의 작업 규칙 파일
- CDD rules
- approved product boundary / source of truth documents
- archive branch/tag 또는 보존 방식이 있는지
- 현재 작업 브랜치
- worktree dirty 상태
- 삭제 대상이 Task scope 안에 있는지
- generated/index docs 수정 금지 여부
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference가 보조 자료로만 분류되었는지
- 과거 task/completion/verification/prompt가 current 기준으로 사용되고 있지 않은지
- migration/data loss 영향
- public API/UI 영향
- 테스트 영향

위 항목 중 하나라도 확인할 수 없으면 삭제하지 말고 아직 필요한 결정 질문 또는 사용자 확인으로 돌아간다.

## Keep List

삭제 전에 keep list를 작성한다.

Keep list는 새 제품 경계와 현재 approved source of truth에 필요한 자산이다.

예시 범주:

- reusable infrastructure
- authentication setup
- external data adapter
- generic formatting utilities
- generic test/build setup
- approved product boundary docs
- harness/workflow docs
- reusable CI/local infra

실제 keep list는 대상 프로젝트의 approved source of truth로 결정한다. 이 문서의 예시는 기본 보존 목록이 아니다.

## Stale 문서 분류

stale 문서나 오래된 작업 산출물은 먼저 다음 중 하나로 분류한다.

- 삭제 후보: 현재 기준과 충돌하고 보존 가치가 없으며 삭제해도 추적 가능성과 감사 기록을 해치지 않는 문서.
- 보존 후보: historical record로 가치가 있어 남겨야 하지만 현재 기준으로 읽히면 안 되는 문서.
- 비-SOT 표시 후보: 탐색 보조나 archive reference로 남길 수 있지만 기본 읽기 경로와 현재 기준 묶음에서 제외해야 하는 문서.

분류 보고에는 각 후보의 이유, 현재 기준과의 충돌 여부, README/index 갱신 필요 여부, `_user-facing-language.md`의 "승인 전 브리핑 형식", 사용자 승인 문장을 포함한다. 브리핑은 먼저 확인할 삭제/보존 결정과 추천을 제시해야 한다. 승인 문장은 이 승인이 허용하는 삭제/보존/비-SOT 표시 작업, 아직 허용하지 않는 작업, 되돌리기 어려운 위험, 승인 후 실제로 진행할 정리를 브리핑한 뒤에만 제시한다.

stale 문서를 보존하거나 비-SOT로 표시하면 현재 작업 포인터와 기본 읽기 경로 계약에서도 제외 목록이 갱신되어야 하는지 확인한다. 삭제하지 않더라도 기본 읽기 경로에서 빠지지 않으면 다음 작업 판단을 계속 오염시킬 수 있다.

사용자 승인 전에는 stale 문서를 삭제, 이동, archive 처리, 비-SOT 표시 처리하지 않는다.

## Delete List

삭제 전에 delete list를 작성한다.

Delete list는 제거할 대상과 제거 근거를 함께 기록한다.

분류:

- domain packages
- API endpoints / DTOs
- UI screens/components
- database tables/columns/migration cleanup candidates
- tests/fixtures/mocks
- documents that should be moved to archive/superseded
- dependencies
- generated artifacts

각 항목에는 다음을 붙인다.

- 제거 근거가 되는 approved source of truth 또는 사용자 지시
- keep list와 충돌하지 않는 이유
- public API, data, test, document 영향
- 삭제 대신 비노출 또는 archive가 필요한지 여부

## 의존성 확인

삭제 전에 다음 참조를 확인한다.

- direct imports
- indirect imports
- routes/navigation
- API contract references
- tests/fixtures/mocks
- DB entity/repository/native query references
- generated code references
- build config references
- documentation references
- task/prompt/verification references

참조가 남아 있으면 삭제하지 않거나, 참조 제거가 Task scope에 포함되어 있는지 확인한다.

## 삭제 전략

- 대상 기능이 approved source of truth에서 제거되었으면 core path에서 제거한다.
- 삭제가 너무 크면 먼저 entrypoint/routing/API exposure를 끊고, 남은 dead code를 별도 cleanup 후보로 보고한다.
- existing migration 파일은 수정하지 않는다.
- DB cleanup이 필요하면 새 migration 또는 별도 migration Task로 분리한다.
- 데이터 손실 위험이 있으면 사용자 확인 없이는 drop하지 않는다.
- public API 제거는 영향 범위를 보고한다.
- UI 제거는 navigation, route, test까지 같이 정리한다.
- dependency 제거는 사용처가 0인지 확인한 뒤 진행한다.
- generated/index docs는 대상 프로젝트 규칙이 허용하지 않으면 수정하지 않는다.

삭제와 비노출이 모두 가능하면 사용자에게 선택지를 제시한다. 삭제가 되돌리기 어렵거나 데이터 손실 가능성이 있으면 멈추고 확인한다.

## 사람 확인 지점

다음 상황에서는 사용자 확인이 필요하다.

- archive 보존 방식이 불명확하다.
- 대량 삭제 전이다.
- DB drop/migration 전이다.
- public API 제거 전이다.
- dependency 대량 제거 전이다.
- source of truth 해석이 애매하다.
- 삭제 대상이 keep list와 충돌한다.
- 폐기와 비노출 중 선택이 필요하다.
- 삭제 후 되돌리기 어렵거나 데이터 손실 가능성이 있다.

"정리해줘", "안 쓰는 것 지워줘", "나중에 필요하면 다시 만들자" 같은 표현은 위 확인 지점을 자동 통과시키지 않는다.

## 자동 진행과 중단

자동 진행 가능한 경우:

- cleanup/delete 요청이 명확하다.
- 파일 수정 또는 삭제 범위가 현재 요청에서 허용되어 있다.
- keep list와 delete list가 approved source of truth 또는 명시 사용자 지시로 충분히 구분된다.
- 삭제 대상이 작업 범위 안에 있다.
- 삭제 대상이 keep list와 충돌하지 않는다.
- migration, 데이터 손실, public API 제거, dependency 대량 제거가 없다.
- 검증 방법이 명확하다.

이 경우에는 다시 묻지 않고 해당 범위 안에서 정리 후 검증과 보고까지 수행한다.

자동 진행하면 안 되는 경우:

- 삭제와 보존 중 선택이 필요하다.
- archive 보존 방식이 불명확하다.
- DB drop, migration, 데이터 삭제가 있다.
- public API 제거가 있다.
- dependency 대량 제거가 있다.
- 삭제 대상이 keep list와 충돌한다.
- source of truth 해석이 애매하다.
- 삭제 후 되돌리기 어렵다.
- 사용자가 분석만 요청했거나 아직 수정하지 말라고 했다.

이 경우에는 삭제하지 않고 선택지, 제 추천, 바로 답할 수 있는 문장을 제공한다.

## 검증 항목

cleanup/delete 작업 후 다음을 확인한다.

- changed-file scope check
- forbidden/superseded reference audit
- generated/index docs modification guard
- compile/typecheck
- unit/integration tests
- build
- migration validation if applicable
- `git diff --check`
- completion report required fields

환경 실패와 코드 실패는 `verify-work.md` 기준으로 분리한다.

## 완료 보고 형식

cleanup/delete 완료 보고에는 다음을 포함한다.

- 읽은 source of truth
- 현재 작업 브랜치
- archive 보존 여부
- keep list
- delete list
- 삭제한 파일/패키지/API/UI/DB 후보
- 삭제하지 않은 항목과 이유
- 수정한 tests/fixtures/docs
- dependency 변경 여부
- 실행한 검증 명령과 결과
- 환경 실패/코드 실패 구분
- 남은 legacy 후보
- 다음 cleanup 후보

사용자-facing 완료 보고는 마지막에 다음 중 하나를 포함한다.

```text
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
```

또는:

```text
다음에 할 일:
이번 cleanup/delete 작업은 완료되었습니다.

다음 후보:
1. ...
2. ...
3. ...

제 추천:
- ...
```

## 다른 CDD 단계와의 연결

- `_work-mode.md`: cleanup/delete는 일반 implementation/refactor와 다른 작업 유형이다. 분석 전용 요청에서는 delete list를 제안만 하고 파일을 수정하지 않는다.
- `plan-task.md`: cleanup/delete Task는 별도 type으로 작성하고 keep list, delete list, human gates, verification requirements를 포함한다.
- `_implementation-rules.md`: cleanup/delete 실행 중 새 기능을 구현하거나 폐기된 기능을 이름만 바꿔 살리지 않는다.
- `verify-work.md`: cleanup/delete 결과는 scope, stale reference, generated/index docs, migration/data loss, forbidden/superseded reference를 검증한다.
- `complete-work.md`: cleanup/delete 완료 보고는 keep/delete list와 archive 보존 여부를 포함한다.
