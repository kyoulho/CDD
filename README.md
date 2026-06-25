# CDD

CDD는 AI 작업 에이전트가 기준 없이 구현부터 시작하지 않도록 돕는 문서 기반 작업 하네스다.

프로젝트 작업 요청에 `$cdd`를 붙이면 에이전트는 먼저 기준 문서, 작업 범위, 승인 지점, 검증 방법을 확인한다. 기준이 충분하면 요청 범위 안에서 다음 단계까지 진행하고, 부족하면 무엇을 먼저 정해야 하는지 질문한다.

## 빠른 사용

구현 요청:

```text
$cdd
이 작업을 구현해줘.
```

판단만 받고 싶을 때:

```text
$cdd
현재 기준으로 바로 구현 가능한지 판단해줘.
아직 파일은 수정하지 마.
```

검증이나 완료 확인:

```text
$cdd
검증 결과를 보고 완료 가능한지 확인해줘.
```

skill 이름은 `cdd`다. 실행 환경이 대소문자를 구분할 수 있으므로 `$cdd`처럼 소문자로 쓰는 편이 안전하다.

## 어떻게 시작하나

`$cdd`가 호출되면 Codex는 먼저 `SKILL.md`를 읽고 요청 성격에 맞는 public entrypoint로 이동한다.

- 새 작업 또는 애매한 요청: `start-here.md`
- 작업 기준서 작성: `plan-task.md`
- 구현 지시서 작성: `write-implementation-prompt.md`
- 삭제, 폐기, 정리: `cleanup-delete.md`
- 결과 검증: `verify-work.md`
- 검증 실패 후 수정: `revise-work.md`
- 완료 보고: `complete-work.md`

`_`로 시작하는 파일은 내부 규칙이다. 사용자가 직접 부르기보다 public entrypoint 흐름 안에서 필요한 때만 읽는다.

## CDD가 막는 것

CDD는 다음 기준이 비어 있으면 구현, DB 설계, API 설계, 상태값 설계, 문서 적용, 삭제를 임의로 진행하지 않는다.

- 무엇을 왜 만들지
- 누가 어디서 어떻게 사용하는지
- 입력, 출력, 실패, 빈 상태, 권한 없음, 처리 중 피드백
- 무엇을 왜 저장하고 무엇은 저장하지 않을지
- 어떤 행동과 결과를 제공할지
- 상태값이 무엇을 의미하는지
- 성능, 보안, 권한, 조회, 재시도, 로그/감사 기준
- 작업 기준서, 구현 지시서, 검증 결과, 완료 기록의 저장 위치와 승인 상태

UI/UX 기준은 특정 파일 경로를 강제하지 않는다. `docs/ui-ux/*`, `docs/design-system/*`를 기본 후보로 제안할 수 있지만, 프로젝트가 루트 `DESIGN.md` 같은 단일 기준 문서를 승인했다면 그 구조를 따른다. CDD가 확인하는 것은 파일 위치가 아니라 `FRONTEND_UX_CRITERIA`, `DESIGN_SYSTEM`, `UI_PATTERN`, `INTERACTION_SPEC` 역할이 승인 문서 안에 명확한지다.

## 진행과 중단

다음 조건이 충분하면 CDD는 다시 묻지 않고 요청 범위 안에서 진행할 수 있다.

- 요청이 명확하다.
- 필요한 제품 판단과 설계 판단이 준비되어 있다.
- 작업 범위와 금지 범위가 분명하다.
- 검증 방법이 정해져 있다.
- 데이터 삭제, migration, public API 제거, 승인되지 않은 dependency 변경 같은 위험 변경이 없다.

다음 경우에는 먼저 멈추고 질문한다.

- 요청이 설명, 설계, 문서 수정, 구현, 삭제, 검증 중 무엇인지 애매하다.
- 제품 방향, 상호작용 방식, 저장 의미, 동작 계약, 상태 의미, 운영/품질 기준이 부족하다.
- 삭제와 보존 중 선택해야 한다.
- migration, 데이터 삭제, public API 제거, 승인되지 않은 dependency 변경이 있다.
- 기존 문서 구조와 다른 파일 배치가 필요하다.
- 사용자가 "분석만", "수정하지 마", "초안만", "먼저 보여줘"처럼 제한했다.

멈출 때는 내부 상태명보다 자연어로 말해야 한다.

Dependency 변경은 무조건 금지하지 않는다. 기존 스택으로 정확히 구현하거나 검증할 수 없으면 에이전트는 필요한 dependency, 이유, 기존 대안의 한계, 영향 범위, 검증 방법을 보고한 뒤 사용자 승인을 받아야 한다. 승인 전에는 package manager 설정, lockfile, build script, runtime import를 변경하지 않는다.

```text
아직 구현하면 안 됩니다.
먼저 정해야 할 것이 있습니다.
```

## cdd-audit

`bin/cdd-audit`는 CDD 문서 규칙을 보조하는 read-only CLI다. 파일을 만들거나 고치거나 삭제하지 않고 다음을 보고한다.

- 현재 작업 포인터와 기본 읽기 경로
- 먼저 읽을 문서와 먼저 볼 섹션
- 큰 문서, active/history 혼재, 비-SOT 자료 혼입
- CDD skill root인 경우 `SKILL.md` frontmatter와 `agents/openai.yaml` 상태

사용자가 `cdd-audit`를 PATH에 직접 등록해야 CDD를 쓸 수 있는 것은 아니다. CDD를 skill로 호출한 에이전트는 skill root를 알고 있으므로 먼저 `cdd-audit` 명령을 시도하고, 없으면 `<cdd-root>/bin/cdd-audit` 절대 경로로 실행해야 한다. 둘 다 실행할 수 없을 때만 문서를 직접 읽어 수동 확인으로 대체하고, 보고에 실행하지 못한 이유를 남긴다.

반복 읽기를 줄이려면 먼저 `brief`를 사용한다.

```sh
/path/to/cdd/bin/cdd-audit docs --root /path/to/project --format brief --fail-on never --entrypoint plan-task
```

`--entrypoint`는 대상 프로젝트의 기준 문서를 바꾸지 않고, CDD skill 안에서 먼저 열 문서와 섹션을 좁히는 안내만 추가한다. 지원 값은 `start-here`, `plan-task`, `write-implementation-prompt`, `cleanup-delete`, `verify-work`, `revise-work`, `complete-work`다.

큰 CDD 문서는 가능한 한 섹션 단위로 먼저 읽는다. `cdd-audit`가 `L시작-L끝` 줄 범위를 보여주면 그 위치부터 확인하고, 판단이 막힐 때만 전체 문서로 확장한다. heading을 찾을 수 없으면 `missing`과 후보 heading을 함께 표시한다.

PATH에 걸어두기, 선택 사항:

```sh
mkdir -p ~/.local/bin
ln -s /path/to/cdd/bin/cdd-audit ~/.local/bin/cdd-audit
cdd-audit docs --root /path/to/project --format brief --fail-on never --entrypoint plan-task
```

이 설정은 사람이 터미널에서 짧게 실행하기 위한 편의 설정이다. CDD 에이전트는 PATH 설정을 사용자에게 요구하지 말고 skill root의 `bin/cdd-audit`를 fallback으로 사용한다.

프로젝트 하위 디렉터리에서 실행하면 `docs/README.md`, `docs/project/current-work.md`, `document-registry.yml`, `AGENTS.md`, `.git` 같은 marker를 기준으로 root를 자동 탐지한다.

상세 보고가 필요할 때:

```sh
cdd-audit docs --root /path/to/project --format text --fail-on never
```

JSON 출력:

```sh
cdd-audit docs --root /path/to/project --format json --fail-on never
```

exit code:

- `0`: 실행 성공, 차단 항목 없음
- `2`: 실행 성공, 차단 항목 있음
- `1`: 실행 실패

`--fail-on never`를 쓰면 차단 항목을 출력에 유지하면서 exit code만 `0`으로 둔다.

선택 설정 파일은 project root의 `.cdd-audit.json`, `cdd-audit.json`, `.cdd/audit.json` 중 하나를 쓴다.

```json
{
  "defaultReadPath": ["docs/README.md", "docs/project/current-work.md", "DESIGN.md"],
  "requiredReadDocuments": ["docs/README.md", "docs/project/current-work.md"],
  "excludedHistoricalRecords": ["docs/archive/**"],
  "excludedNonSotReferences": ["docs/generated-map.md"],
  "sectionHints": {
    "docs/README.md": ["# Docs", "## Current Work"]
  },
  "roleOverrides": {
    "DESIGN.md": "current-criteria",
    "docs/archive/**": "history"
  },
  "ignore": ["node_modules/**", "dist/**"],
  "currentWorkPointer": "docs/project/current-work.md"
}
```

`cdd-audit`는 CDD 판단을 대체하지 않는다. 차단 항목이 나오면 CDD 절차에 따라 사용자에게 정리 후보와 선택지를 보고한다.

주의 항목은 조용히 무시하지 않는다. `text` 보고의 "주의 항목 처리"에 따라 각 warning을 해결하거나, 이번 작업에서 보류해도 되는 이유를 보고하거나, 진행 사유를 사용자에게 설명한다. 먼저 볼 섹션 heading을 찾지 못한 경우처럼 읽기 경로 신뢰를 깨는 항목은 차단 항목으로 처리한다.

## 설치

이미 등록했다면 건너뛰어도 된다.

```sh
CDD_ROOT=/path/to/cdd
mkdir -p ~/.agents/skills
ln -s "$CDD_ROOT" ~/.agents/skills/cdd
```

정상 구조:

```text
~/.agents/skills/cdd/SKILL.md
```

등록 후에는 사용하는 에이전트 앱이나 세션을 다시 시작해야 새 skill이 잡힐 수 있다.

## 검증

CDD 변경 후에는 다음을 우선 실행한다.

```sh
git diff --check
./bin/cdd-verify
```

`bin/cdd-verify`는 `git diff --check`, CDD skill health를 포함한 `cdd-audit docs`, 전체 테스트를 같은 방식으로 실행한다. 내부적으로 Python 3.11 이상을 찾고, 없으면 `uv`를 사용하므로 사용자가 `python3.12` 같은 특정 명령을 직접 맞출 필요가 없다.

Codex skill 기본 형식은 `cdd-audit`의 skill health 검사로 확인한다. `skill-creator`의 `quick_validate.py`는 실행 환경에 `PyYAML`이 없으면 실패할 수 있으므로, CDD 자체 검증에서는 외부 패키지 설치를 요구하지 않는 `./bin/cdd-verify`를 우선 사용한다.

관련 기능을 바꿨다면 해당 테스트도 함께 실행한다.

```sh
./bin/cdd-test tests/test_cdd_audit_entrypoints.py
./bin/cdd-test tests/test_cdd_audit_skill_health.py
./bin/cdd-test tests/test_cdd_audit_section_hints.py
./bin/cdd-test tests/test_cdd_audit_section_suggestions.py
```

## 유지보수 메모

- `README.md`는 링크로 들어온 사람이 빠르게 이해하는 사람용 안내서로 유지한다.
- `SKILL.md`는 Codex가 skill을 호출하고 라우팅하기 위한 최소 에이전트 지침으로 유지한다.
- 세부 판정 규칙은 public entrypoint와 `_*.md` 내부 module에 둔다.
- CDD 자체 forward-testing이 필요할 때만 `references/forward-testing.md`를 사용한다.
