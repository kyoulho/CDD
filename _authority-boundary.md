# Authority Boundary Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 AI가 판단할 수 있는 영역과 임의 판단하면 안 되는 영역을 정의한다.

핵심 규칙: AI는 구현 세부사항을 판단할 수 있지만, 도메인/아키텍처/행위/정책 판단은 승인된 source of truth 문서에서만 가져와야 한다.

source of truth 생성, 변경, 삭제, 상태 전환, 일관성 검증은 `_source-of-truth-manager.md` 절차를 따른다. 다른 skill은 사용자 승인 없이 source of truth, document registry, Plan, Task, prompt, verification result를 직접 수정하지 않는다.

디스크에 존재하는 파일은 자동으로 유효한 artifact가 아니다. 이전 턴에서 생성된 파일이라도 현재 harness gate를 위반해 생성되었다면 정상 baseline으로 사용할 수 없다. Artifact는 사용 전에 legitimacy check를 통과해야 한다.

V2 artifact는 `_artifact-metadata.md`, `_artifact-templates.md`, `_status-machine.md`, `_approval-reference.md`를 기준으로 관리한다. 사용자-facing 응답은 `_user-facing-language.md`를 따른다.

작업 모드와 쓰기 권한은 `_work-mode.md`를 따른다. 작업 모드 판별은 이 문서의 판단 권한 경계보다 먼저 적용되는 전역 게이트다.

## 빠른 탐색

- 기준 문서 권위 순서는 "Source of Truth 권위 순서"를 본다.
- README, generated docs, memory 같은 보조 자료는 "비-SOT 자료 규칙"을 본다.
- 작업 모드와 쓰기 권한은 "작업 모드 게이트"를 본다.
- AI가 판단할 수 있는 범위는 "AI가 판단할 수 있는 것"과 "구현 세부사항 판정 기준"을 본다.
- AI가 임의로 정하면 안 되는 범위는 "AI가 임의 판단하면 안 되는 것"을 본다.
- source of truth 변경, dependency, test strategy, identifier 정책은 각 policy 섹션을 본다.
- 사용자 보고는 "User-Facing Language 원칙"과 "금지 판단이 필요할 때"를 본다.

## Source of Truth 권위 순서

대상 프로젝트가 자체 권위 순서를 명시하면 그 우선순위를 먼저 따른다.

별도 우선순위가 없으면 기본 순서는 다음과 같다.

1. 현재 사용자 지시
2. 대상 저장소의 작업 규칙 파일, 예: `AGENTS.md`
3. CDD harness rules
4. 대상 프로젝트의 approved source of truth documents
5. task-specific approved plan/prompt
6. implementation files
7. README, generated docs, indexing docs, memory/recall notes, previous assistant responses 같은 보조 자료

이 순서는 lower source를 무시하라는 뜻이 아니다. lower source는 navigation, historical context, implementation evidence로 사용할 수 있지만, higher source와 충돌하면 higher source를 따른다.

## 비-SOT 자료 규칙

다음 자료는 기본적으로 source of truth가 아니다.

- generated docs/indexes
- memory/recall notes
- previous assistant messages or task reports
- README의 사용법 또는 navigation 설명
- archive/superseded documents
- implementation files의 우연한 현재 상태

이 자료를 제품 요구사항, 정책, API, 데이터 모델, 테스트 전략의 기준으로 사용하려면 명시적 승인 또는 active source of truth로 승격된 근거가 있어야 한다.

Archive/superseded 문서는 historical record다. 검색에 걸렸다는 이유만으로 active source of truth가 아니다. 최신 approved source of truth와 충돌하면 최신 approved source of truth를 따른다.

## 작업 모드 게이트

모든 Agent는 사용자 요청을 먼저 다음 모드 중 하나로 분류한다.

- `ANALYSIS_ONLY`: 분석, 원인 파악, 검토, 제안만 수행한다.
- `PROPOSAL_ONLY`: 변경안과 패치 계획만 제안한다.
- `PATCH_AUTHORIZED`: 사용자가 명시 승인한 범위 안에서 파일을 수정한다.
- `APPLY_AUTHORIZED`: 승인된 변경 묶음 또는 Change Request를 적용한다.
- `IMPLEMENTATION`: 승인된 구현 지시서를 기준으로 구현한다.
- `CLEANUP_DELETE`: 폐기/삭제/정리 작업으로 분류하고 `cleanup-delete.md`를 따른다. 독립적인 쓰기 권한은 아니다.

명시적 금지 표현이 있으면 더 제한적인 모드가 우선한다. 사용자가 "분석만", "수정하지 마", "원인만", "검토만", "제안만"이라고 말하면 `ANALYSIS_ONLY`로 처리한다.

`ANALYSIS_ONLY`에서 허용되는 행동:

- 파일 읽기
- 상태 확인
- 실패 원인 분석
- 수정 대상 후보 제안
- 패치 계획 제안
- 승인 필요 문구 안내

`ANALYSIS_ONLY`에서 금지되는 행동:

- 파일 생성, 수정, 삭제
- skill 파일 수정
- source of truth 문서 수정
- 금지된 대상 프로젝트 코드 또는 문서 수정
- Plan, Task, Prompt, runs, verification result, completion record 수정
- formatting save
- rollback, revert, restore
- CLI/tools 구현

rollback도 파일 수정이다. 분석 요청에서 이전 변경을 되돌리는 것도 금지한다.

분석/제안에서 패치로 전환하려면 다음처럼 범위가 명확한 사용자 승인이 필요하다.

```text
위 분석에 따라 skill 파일 수정을 승인합니다.
CDD skill 파일 수정을 승인합니다.
```

"좋아", "진행해", "그 방향으로 가자", "제안한 대로 해"는 모호하므로 패치 승인으로 해석하지 않는다.

하네스 Agent도 이 게이트를 따른다. 하네스 Agent가 CDD skill files를 수정할 권한을 가진 상황이라도, 사용자가 `ANALYSIS_ONLY`를 명시하면 쓰기 권한은 없다.

## AI가 판단할 수 있는 것

다음은 승인된 Task와 문서 범위 안에서만 AI가 판단할 수 있다.

- private helper method 이름
- 내부 메서드 분리
- 테스트 fixture builder 이름
- 승인된 테스트 전략 안에서 테스트 메서드 이름
- 승인된 테스트 전략 안에서 fixture builder 이름
- 승인된 테스트 전략 안에서 assertion 순서
- 승인된 테스트 전략 안에서 테스트 클래스 분리
- 문서가 허용한 계층 안에서의 클래스 배치
- 같은 계약을 만족하는 단순 코드 스타일 선택
- 동일한 외부 계약/DB/행위 의미를 유지하는 리팩토링
- 문서가 허용한 범위 안의 기술적 구현 선택
- 승인된 범위 안에서 동일한 외부 행위를 유지하는 국소 성능 개선

테스트 인프라, 테스트 DB, profile, dialect, migration 선택은 이 목록에 포함되지 않는다.

## 구현 세부사항 판정 기준

AI가 판단해도 되는 구현 세부사항은 아래 조건을 모두 만족해야 한다.

1. 외부 API 계약에 노출되지 않는다.
2. DB schema 또는 migration에 영향을 주지 않는다.
3. 도메인 개념, 상태, 행위 의미를 바꾸지 않는다.
4. 테스트의 기대값이나 acceptance criteria를 바꾸지 않는다.
5. 운영/보안/확장 정책에 영향을 주지 않는다.
6. 나중에 바꿔도 데이터 마이그레이션이나 API breaking change가 발생하지 않는다.
7. source of truth 문서의 owns 영역과 충돌하지 않는다.
8. 성능 개선이라면 승인된 성능 기준과 작업 범위 안에 있거나, 동일 행위를 유지하는 국소 구현 변경이다.

이 조건 중 하나라도 만족하지 못하면 구현 세부사항이 아니라 정책 판단이다.

## AI가 임의 판단하면 안 되는 것

다음 판단은 승인된 source of truth 문서에 없으면 AI가 임의로 결정할 수 없다.

- 도메인 개념 추가/삭제
- 아키텍처 경계 변경
- 행위 정의 변경
- 상태 전이 정책 결정
- API 오류 응답 정책 결정
- 데이터 보존/삭제 정책 결정
- 인증/인가 정책 결정
- 외부 API fallback 정책 결정
- 계산식 변경
- 완료 기준 변경
- source of truth 문서 변경
- document registry 변경
- source of truth status 변경
- generated docs/indexes, memory/recall notes, previous assistant responses, archive/superseded documents를 active source of truth처럼 사용하는 것
- Plan/Task를 source of truth 변경에 맞춰 임의 수정
- prompt 또는 verification result를 source of truth 변경에 맞춰 임의 수정
- 디스크에 존재하는 artifact를 legitimacy check 없이 baseline으로 사용
- invalid prompt를 보강해서 정상 prompt처럼 계속 사용
- 배치 실행 정책 변경
- 브로커/외부 시스템 연동 정책 변경
- rate limit, retry, timeout, circuit breaker 정책 결정
- API contract 변경
- 데이터 모델 변경
- 사용자 시나리오 또는 product requirement 변경
- 프론트엔드 UX 기준 결정
- 화면 정보 구조, 주요 행동, 반응형 기준, 접근성 기준, visual QA 기준 결정
- UI 구현 계약 결정
- 화면 단위 금지 패턴, 정보 우선순위, 브라우저/스크린샷 검증 기준 결정
- 성능 위험 조사 범위 결정
- 성능 위험 후보를 승인된 작업 범위로 승격
- cache, pagination, indexing, async, batching 같은 성능 정책 결정
- Git stage/commit/push/branch/PR/tag/rebase/amend/force-push 범위 결정
- 사용자 소유 변경 또는 unrelated dirty work를 Git 작업에 포함할지 결정
- bug report 대상 tracker, severity, 제목, 재현 절차, 환경, 증거, redaction 기준 결정
- 추정 원인을 확정 사실처럼 bug report에 기록
- Entity id 타입: Long, UUID, ULID 등
- DB primary key 생성 전략
- API path variable 타입
- API response DTO의 id 표현 방식
- 날짜/시간 표현 방식
- 금액/수량 precision
- 삭제 방식: hard delete, soft delete
- 상태 변경 방식: toggle, set true, set false
- 오류 응답 형식
- pagination 기본 정책
- 정렬 기본 정책
- retry/backoff 정책
- 멱등성 정책
- 동시성/락 정책
- 트랜잭션 경계
- 테스트 DB 선택: H2, PostgreSQL, Testcontainers, embedded DB 등
- 테스트 프로필 전략: application-test.yml, test profile, profile별 설정 분리
- 운영 migration과 테스트 migration 분리 여부
- 테스트용 별도 schema/migration 생성 여부
- 운영 DB dialect를 테스트에서 다른 dialect로 대체하는 전략
- Repository/DB integration test 수행 방식
- Testcontainers 도입 여부
- Mock/Fake/Stub으로 외부 의존성을 대체하는 정책
- slice test, `@WebMvcTest`, `@DataJpaTest`, mocked service, mocked repository 선택
- 테스트에서 외부 API를 실제 호출할지, fake로 대체할지, fixture로 대체할지에 대한 전략
- 운영 설정과 테스트 설정의 divergence 허용 범위
- DB/Persistence cross-cutting policy
- API/Error cross-cutting policy
- External Integration cross-cutting policy
- Batch Operation cross-cutting policy
- Operation/Infra/Config cross-cutting policy
- Dependency/build tool/code generation/runtime library policy

## Cross-Cutting Policy 원칙

Goal 또는 Task가 DB, migration, repository, test, external integration, batch, infra, config를 포함하면 관련 cross-cutting policy가 필요하다. 이 정책들은 구현 단계에서 처음 결정할 수 없다.

- DB/Persistence: identifier, key generation, migration, constraint/index, nullable/default, timestamp/timezone, test database strategy
- Test Strategy: test DB, profile, application-test.yml, test migration, mock/fake/stub, dialect substitution
- API/Error: status code, error response, error code, validation, serialization, date/time, path variable/response field type
- External Integration: timeout, retry/backoff, fallback, rate limit, error mapping, source priority, cache TTL
- Batch: idempotency, restartability, chunk size, retry/skip, source/target, staging/publish, cross-database/schema boundary
- Operation/Infra: profile, environment variable naming, logging format, health check, Docker/local runtime
- Dependency/Build Tool: new dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library

## Dependency Policy 원칙

새 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library는 기본적으로 승인 필요 항목이다.

AI는 "단순 편의", "흔한 조합", "표준 라이브러리", "나중에 필요"라는 이유로 dependency를 추가할 수 없다.

이 규칙은 dependency 추가를 전면 금지하는 규칙이 아니다. 필요한 dependency는 사용자에게 보고하고 승인받아 사용할 수 있다. 다만 승인 전에는 package manager 설정, lockfile, build script, runtime import, test-only helper를 수정하지 않는다.

승인 문서가 없으면 기본 대안은 기존 스택 안에서 구현하는 것이다. 단, 기존 스택으로 Task 범위와 검증 기준을 충족할 수 없으면 기존 스택 구현을 강행하지 말고 dependency 승인 질문으로 돌아간다.

필요 dependency를 요청할 때는 최소한 다음을 사용자에게 보고한다.

- 추가하려는 dependency 또는 build tool 이름과 용도
- production / test / build-time / runtime 노출 여부
- 기존 스택으로 충분하지 않은 이유
- dependency 없이 가능한 대안과 그 한계
- 보안, 라이선스, 유지보수, bundle/runtime 영향
- 영향을 받는 파일과 검증 방법
- 승인하면 이번 Task에서 허용되는 범위와 금지되는 범위

사용자가 승인하면 해당 결정을 source of truth, 작업 기준서, 구현 지시서, approval record 중 현재 프로젝트 구조에 맞는 승인 문서에 기록한 뒤 구현한다.

예:

- MapStruct 없음: 수동 매핑
- springdoc-openapi 없음: API 문서 자동 노출 없음
- QueryDSL 없음: Spring Data JPA 기본 기능
- Testcontainers 없음: Missing Context

승인 없는 dependency 추가는 구현 세부사항이 아니라 build/runtime/test strategy 정책 위반이다.

## Source Of Truth 변경 원칙

source of truth 변경은 구현 세부사항이 아니다.

다음은 모두 `_source-of-truth-manager.md`가 처리해야 하는 Change Request다.

- API contract field, status code, error format 변경
- domain term, state, behavior 변경
- data model, migration, identifier policy 변경
- architecture boundary 변경
- test strategy, migration policy, dependency policy 변경
- document registry status, owns, requiredFor 변경
- Plan/Task가 source of truth와 충돌해 수정이 필요한 상황

모든 Change Request는 변경 방향 승인과 실제 변경안 적용 승인, 두 단계를 거친다. 사용자의 "알아서 해", "추천대로", "빨리 해", "그냥 맞춰줘", "문서도 같이 고쳐" 같은 표현은 APPROVED 반영 승인으로 해석하지 않는다.

Implementation, Verification, Revision Agent는 source of truth를 수정하지 않는다. 문서 변경이 필요하면 즉시 중단하고 Source of Truth Change Request가 필요하다고 보고한다.

사용자 승인 또는 사용자 지정 scope는 Source of Truth APPLY의 충분조건이 아니다. 사용자가 특정 파일만 수정하라고 요청해도, 그 변경이 APPROVED source of truth 간 불일치나 Task Contract 불일치를 만들면 APPLY를 거부한다.

알려진 source of truth 불일치가 남는 변경안은 APPLY할 수 없다. 영향 분석에서 발견된 충돌은 warning이 아니라 APPLY blocker다.

승인 레벨은 분리된다.

- Direction Approval: 변경 방향 선택이다. 파일 수정 권한이 없다.
- Draft Approval: DRAFT 변경안을 검토했다는 뜻이다. 파일 수정 권한이 없다.
- Apply Approval: 지정된 Files Proposed for Apply 전체에 대해 실제 파일 수정을 명시적으로 허용한다.
- Prompt Draft Approval: prompt 초안 작성 또는 검토 승인이다. prompt 실행 권한이 아니다.
- Prompt Execution Approval: 구현 Agent가 prompt를 실행해도 된다는 승인이다.

"A로 하자", "그 방향으로 가자", "좋아", "진행해", "추천대로", "알아서 반영해", "빨리 해", "나중에 보자", "일단 해" 같은 표현은 더 높은 권한 승인으로 해석하지 않는다. 모호하면 반드시 확인 질문을 한다.

Source of Truth APPLY는 다음 조건을 모두 만족해야 한다.

1. Change Request ID가 있다.
2. Files Proposed for Apply 목록이 있다.
3. Known Conflicts After Apply가 비어 있다.
4. 사용자가 Files Proposed for Apply 전체를 명시적으로 APPLY 승인했다.
5. 승인 문구가 Direction Approval 수준이 아니다.
6. 변경 후 VALIDATED 가능성이 있다.

다음 말은 정합성 요구를 우회하는 근거가 아니다.

- "나중에 맞춘다"
- "일단 이것만 바꾼다"
- "작은 변경이다"
- "구현하면서 맞춘다"
- "사용자가 그 파일만 바꾸라고 했다"
- "A로 하자"
- "나중에 보자"

## Missing Context 정지 규칙

Missing Context가 발견되면 Agent는 권한을 확장해서 문제를 해결하면 안 된다.

- 코드를 수정하지 않는다.
- source of truth 문서를 수정하지 않는다.
- document registry를 수정하지 않는다.
- Missing Context가 해결되기 전에는 revision을 실행하지 않는다.
- Missing Context가 해결되기 전에는 테스트 전략을 변경하지 않는다.
- Missing Context가 해결되기 전에는 Task Contract를 수정하지 않는다.
- Missing Context가 해결되기 전에는 prompt 또는 verification result를 수정하지 않는다.
- Missing Context가 해결되기 전에는 complete로 진행하지 않는다.

다음은 실패 패턴이다.

- `ANALYSIS_ONLY_MODE_VIOLATION`: ANALYSIS_ONLY 요청에서 파일 생성, 수정, 삭제를 수행했다.
- `UNAUTHORIZED_SKILL_MODIFICATION`: 명시 승인 없이 CDD skill files를 수정했다.
- `MODE_ESCALATION_WITHOUT_APPROVAL`: 분석/제안 모드를 패치/적용/구현 모드로 사용자 승인 없이 승격했다.
- `REQUESTED_ANALYSIS_EXECUTED_AS_PATCH`: 사용자가 분석을 요청했는데 실제 패치를 수행했다.
- `UNAUTHORIZED_REVISION_EXECUTION`: Missing Context가 해결되지 않았는데 Agent가 스스로 코드를 수정했다.
- `UNAPPROVED_TEST_SCOPE_REDUCTION`: 기존 Task Contract의 testRequirements를 만족하지 못하자 테스트 범위를 임의로 줄였다.
- `UNAPPROVED_POLICY_DOCUMENT_DRAFTING`: 사용자 답변 없이 TEST_STRATEGY / MIGRATION_POLICY DRAFT 문서를 생성했다.
- `UNAPPROVED_FRONTEND_UX_DOCUMENT_DRAFTING`: 사용자 답변 없이 FRONTEND_UX_CRITERIA / DESIGN_SYSTEM / UI_PATTERN / USER_FLOW / INTERACTION_SPEC / FRONTEND_ARCHITECTURE DRAFT 문서를 생성했다.
- `UNAPPROVED_FRONTEND_UX_DECISION`: 승인된 UI/UX 기준 문서 없이 route, page, component, layout, styling, motion, visual QA 기준을 결정했다.
- `UI_IMPLEMENTATION_CONTRACT_MISSING`: 웹/모바일 UI 구현이 화면 단위 UI 구현 계약 없이 컴포넌트 단위 수정으로 진행됐다.
- `SCREENSHOT_CONTRACT_COMPARISON_MISSING`: 브라우저/스크린샷 결과를 UI 구현 계약과 대조하지 않고 완료 판단했다.
- `VERSION_CONTROL_CONTRACT_MISSING`: Git 작업이 버전관리 계약 없이 stage, commit, push, branch, PR, tag, rebase, amend, force-push로 진행됐다.
- `GIT_SCOPE_POLICY_VIOLATION`: 승인된 포함/제외 범위 밖 변경이나 사용자 소유 변경을 stage/commit/push에 포함했다.
- `UNAPPROVED_HISTORY_REWRITE`: 명시 승인 없이 rebase, amend, force-push 같은 history rewrite를 수행했다.
- `BUG_REPORT_CONTRACT_MISSING`: 버그리포트가 재현 계약 없이 작성되거나 외부 tracker에 등록됐다.
- `BUG_REPORT_REDACTION_MISSING`: 비밀정보, credential, 개인정보, 내부 로그 원문 제거 확인 없이 bug report를 게시했다.
- `VERIFICATION_GATE_BYPASS_ATTEMPT`: Verification이 BLOCKED_BY_MISSING_CONTEXT인데 먼저 revision을 수행하고 verification을 통과시키려 했다.
- `PARTIAL_SOURCE_OF_TRUTH_UPDATE_ATTEMPT`: 영향받는 문서나 Task Contract를 남겨 둔 채 일부 source of truth 파일만 바꾸려 했다.
- `INTENTIONAL_SOURCE_OF_TRUTH_INCONSISTENCY`: 알려진 source of truth 불일치를 남긴 채 APPLY하려 했다.
- `USER_SCOPED_CHANGE_OVERRIDES_CONSISTENCY`: 사용자가 scope를 좁혔다는 이유로 정합성 요구를 무시했다.
- `IMPACT_ANALYSIS_DOWNGRADED_TO_WARNING`: 영향 분석에서 발견한 충돌을 blocker가 아니라 warning으로 낮췄다.
- `AMBIGUOUS_APPROVAL_ESCALATION`: 모호한 사용자 승인 표현을 더 높은 권한의 승인으로 해석했다.
- `DIRECTION_APPROVAL_TREATED_AS_APPLY_APPROVAL`: 변경 방향 선택을 실제 파일 수정 승인으로 오해했다.
- `SOURCE_OF_TRUTH_APPLY_WITHOUT_EXPLICIT_APPROVAL`: 정합 묶음 DRAFT에 대해 명시적 APPLY 승인을 받기 전에 파일을 수정했다.
- `DEPENDENCY_GATE_BYPASS_BY_PROMPT_AUTHORING`: dependsOn이 완료되지 않은 후속 Task의 prompt를 생성했다.
- `BLOCKED_PREDECESSOR_IGNORED`: 선행 Task가 blocked/pending/revision 상태인데 후속 Task로 진행했다.
- `MISSING_CONTEXT_DEFERRED_TO_LATER`: 현재 또는 선행 Task의 Missing Context를 "나중에"로 미루고 진행했다.
- `INVALID_ARTIFACT_NORMALIZATION`: 게이트를 위반해 생성된 artifact를 정상 artifact처럼 취급했다.
- `PREVIOUS_UNAUTHORIZED_CHANGE_ACCEPTED_AS_BASELINE`: 이전 unauthorized change를 현재 baseline으로 받아들이고 후속 작업을 진행했다.
- `PROMPT_DRAFT_MODIFIED_BEFORE_GATE`: prompt draft gate가 충족되지 않았는데 prompt draft를 생성하거나 수정했다.
- `UNAPPROVED_MOCK_STRATEGY_DECISION`: 승인된 TEST_STRATEGY 없이 mock을 테스트 전략으로 선택했다.
- `UNAPPROVED_SLICE_TEST_STRATEGY_DECISION`: 승인된 TEST_STRATEGY 없이 slice test, `@WebMvcTest`, mocked service/controller test 등을 선택했다.
- `ARTIFACT_EXISTS_BUT_NOT_VALID`: 파일이 디스크에 존재한다는 이유만으로 유효한 artifact라고 판단했다.
- `LEGITIMACY_CHECK_SKIPPED`: artifact 사용 전에 필요한 legitimacy check를 생략했다.

## Task Dependency Gate 원칙

Prompt 생성은 단순 문서 작성이 아니라 후속 구현을 여는 gate다.

Task prompt는 다음 조건을 모두 만족해야 한다.

- Task status APPROVED
- documentCoverage READY
- 모든 dependsOn COMPLETE
- source of truth VALIDATED
- known conflicts 없음
- prompt 생성 승인 또는 현재 workflow에서 허용된 write-implementation-prompt 단계

현재 Task 또는 선행 Task의 Missing Context는 "나중에"로 미룰 수 없다. unresolved Missing Context가 있으면 후속 Task prompt 생성, 후속 Task implementation, complete, verification 통과 모두 금지다.

## Artifact Legitimacy 원칙

이전 상태는 자동으로 신뢰하지 않는다. 이전 턴에서 생성된 Change Request, prompt, verification result, completion record가 있어도 현재 harness 기준으로 legitimacy check를 통과해야 한다.

적용 대상:

- `docs/**`
- `document-registry.yml`
- `project-profile.yml`
- `plans/**`
- `tasks/**`
- `change-requests/**`
- `prompts/**`
- `runs/**/verification-result.*`
- `runs/**/completion.*`

Artifact 사용 전에는 다음을 확인한다.

1. 어떤 workflow 단계에서 생성되었는가?
2. 생성 당시 필요한 사용자 승인이 있었는가?
3. 생성 당시 선행 Task dependency가 충족되었는가?
4. 생성 당시 `documentCoverage`가 READY였는가?
5. 생성 당시 source of truth가 VALIDATED 상태였는가?
6. Missing Context가 unresolved 상태였는데 생성된 것은 아닌가?
7. Policy Conflict가 unresolved 상태였는데 생성된 것은 아닌가?
8. 이후 source of truth 변경으로 superseded 되었는가?
9. 현재 harness 기준으로도 생성 조건을 만족하는가?
10. artifact 내부에 생성 근거, approval reference, source-of-truth version, task dependency 상태가 기록되어 있는가?

하나라도 확인할 수 없거나 위반이 있으면 정상 baseline으로 사용하지 않는다.

판정 결과는 가능한 한 `_artifact-templates.md`의 `Legitimacy Report Template` 형식으로 남긴다.

하네스 기준을 위반해 생성된 artifact는 `INVALID`, `QUARANTINED`, `SUPERSEDED` 후보로 처리한다.

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

Mock, fake, stub, slice test, `@WebMvcTest`, `@DataJpaTest`, mocked service, mocked repository는 모두 TEST_STRATEGY 판단이다. 승인된 TEST_STRATEGY 없이 AI가 임의로 선택할 수 없다.

## User-Facing Language 원칙

내부 하네스 용어는 reasoning과 report/debug에 사용할 수 있다. 사용자-facing 응답에서는 쉬운 표현을 우선 사용한다.

- `source of truth`: 기준 문서
- `implementation-prompt`: 구현 지시서
- `dependsOn gate`: 선행 작업이 아직 끝나지 않았습니다
- `artifact legitimacy check`: 이 파일을 지금 기준으로 써도 되는지 확인
- `QUARANTINED`: 잠시 보류
- `SUPERSEDED`: 이전 기준이라 더 이상 사용하면 안 됨

내부 status만 단독으로 사용자에게 보고하지 않는다. 필요한 경우 괄호 안에 보조적으로 1회만 언급한다.

## 테스트 범위 축소 금지

다음은 사용자 승인 또는 Task Contract 변경 승인 없이 할 수 없다.

- testRequirements 축소
- DB integration test를 unit/static test로 대체
- Repository save/find 테스트 제거
- Flyway 실제 적용 테스트를 SQL 정적 검증으로 대체
- 테스트 실패를 피하기 위해 assertion 제거 또는 약화
- 테스트를 후속 Task로 임의 이연

이런 변경이 필요하면 Missing Context 또는 Task Contract 변경 승인으로 보내야 한다.

## Test Strategy Policy 예시

테스트를 쉽게 하기 위해 운영 DB, 외부 시스템, migration, dialect, profile, mock/fake 방식을 바꾸는 것은 구현 세부사항이 아니다. 테스트 전략은 source of truth에 정의되어야 하는 정책 판단이다.

Bad:

```text
Repository 테스트를 위해 H2와 db/migration-test를 임의 추가한다.
```

Why bad:

```text
테스트 DB와 migration 분리 전략은 TEST_STRATEGY/DATA_MODEL/MIGRATION_POLICY 판단이다.
```

Correct:

```text
문서 작성 단계에서 테스트 전략을 먼저 질문한다.
승인된 테스트 전략이 없으면 DB integration test를 요구하지 않거나 Missing Context로 멈춘다.
```

Bad:

```text
TEST_STRATEGY가 없음을 발견한 뒤 H2를 제거하고 Repository DB 통합 테스트를 정적 테스트로 대체했다.
```

Why bad:

```text
테스트 전략이 누락되었으면 구현을 바꿀 게 아니라 사용자에게 질문해야 한다. DB 통합 테스트를 제거하거나 이연하는 것도 TEST_STRATEGY / Task Contract 변경이다.
```

Correct:

```text
TASK-001은 BLOCKED_BY_MISSING_CONTEXT로 멈춘다. 사용자에게 테스트 DB, test profile, migration alignment, Repository/Flyway test scope를 질문한다. 사용자 답변 후 Source of Truth Manager가 document-supplement 하위 절차로 문서 초안을 제안한다. 문서 APPROVED 후 revision-prompt를 만든다. 사용자 승인 후에만 코드 수정한다.
```

## Identifier Policy 예시

Entity id 타입은 단순 구현 세부사항이 아니다. Long, UUID, ULID 같은 선택은 다음 영역에 동시에 영향을 준다.

- DB schema
- DB primary key 생성 전략
- API path variable 타입
- API response contract
- 테스트 fixture
- 외부 노출 식별자 정책
- 마이그레이션 전략
- 추후 보안/추측 가능성 정책

따라서 identifier type, key generation, API-visible id representation은 DATA_MODEL, API_CONTRACT, ARCHITECTURE_POLICY에 해당하는 source of truth 결정이 필요하다.

## 금지 판단이 필요할 때

금지 판단이 필요하면 구현하지 말고 Missing Context로 넘긴다.

해야 할 일:

1. 어떤 판단이 필요한지 식별한다.
2. 왜 필요한지 설명한다.
3. 관련 source of truth 문서가 있는지 확인한다.
4. 문서가 없거나 충분하지 않으면 `_missing-context.md` 절차로 사용자에게 질문한다.

하지 말아야 할 일:

- "일반적으로 이렇게 한다"는 이유로 정책을 확정하지 않는다.
- 기존 코드의 우연한 상태를 source of truth로 간주하지 않는다.
- 사용자 승인 전 답변을 정책으로 확정하지 않는다.

## Suggestions

새 제안은 현재 Task에 섞지 않고 `suggestions`로 기록한다.

예:

```text
suggestions:
  - "현재 Task 범위 밖이지만, API error format 문서를 별도 source of truth로 추가하는 것을 제안한다."
```

제안은 구현이 아니다. 제안은 승인 전까지 source of truth가 아니다.
