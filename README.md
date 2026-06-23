# CDD

CDD는 AI 작업 에이전트가 성급하게 구현부터 시작하지 않도록 돕는 문서 기반 작업 하네스다.

프로젝트 작업 요청에 CDD 링크나 `$cdd`를 함께 넣으면, 에이전트는 먼저 기준 문서와 작업 조건을 확인한다. 기준이 충분하면 다음 단계까지 진행하고, 부족하면 무엇을 먼저 정해야 하는지 질문한다.

## 빠른 탐색

- 바로 쓰려면 "빠르게 쓰기"를 본다.
- `$cdd`가 어떤 문서로 시작하는지 보려면 "호출되면 어떻게 시작하나"를 본다.
- CDD가 구현 전에 막는 기준은 "CDD가 먼저 확인하는 것"을 본다.
- 어디서나 `cdd-audit`를 실행하려면 "`cdd-audit` 문서 점검"을 본다.
- 설치는 "설치", 변경 검증은 "검증"을 본다.

## 빠르게 쓰기

일반 구현 요청:

```text
$cdd
이 작업을 구현해줘.
```

먼저 판단만 받고 싶을 때:

```text
$cdd
현재 기준으로 바로 구현 가능한지 판단해줘.
아직 파일은 수정하지 마.
```

검증이나 완료 확인이 필요할 때:

```text
$cdd
검증 결과를 보고 완료 가능한지 확인해줘.
```

skill 이름은 `cdd`가 정식 이름이다. 실행 환경이 대소문자를 구분할 수 있으므로 `$cdd`처럼 소문자로 쓰는 편이 안전하다.

## 호출되면 어떻게 시작하나

`$cdd`를 호출하면 먼저 `SKILL.md`가 읽힌다. 그 다음 요청 성격에 따라 public entrypoint로 이동한다.

- 새 작업 또는 애매한 요청: `start-here.md`
- 작업 기준서 작성: `plan-task.md`
- 구현 지시서 작성: `write-implementation-prompt.md`
- 삭제, 폐기, 정리: `cleanup-delete.md`
- 결과 검증: `verify-work.md`
- 검증 실패 후 수정: `revise-work.md`
- 완료 보고: `complete-work.md`

사용자가 entrypoint를 직접 지정하지 않으면 보통 `start-here.md`에서 시작한다.

## CDD가 먼저 확인하는 것

CDD는 구현 전에 다음 기준이 충분한지 본다.

- 무엇을 왜 만들지
- 누가 어디서 어떻게 사용하는지
- 무엇을 입력하고 무엇을 결과로 받는지
- 실패, 빈 상태, 권한 없음, 처리 중 상태를 어떻게 알려줄지
- 웹/모바일 UI라면 화면 상태, 정보 우선순위, 디자인 시스템 또는 화면 패턴, 반응형, 접근성, 시각 검증 기준이 승인 문서 안의 역할로 명확한지
- 무엇을 왜 저장하고, 무엇은 저장하지 않을지
- 어떤 행동과 결과를 제공할지
- 상태값이 있다면 각 상태가 무엇을 뜻하는지
- 성능, 보안, 권한, 조회, 재시도, 로그/감사 기준이 있는지
- 작업 기준서, 구현 지시서, 검증 결과, 완료 기록이 기존 문서 구조에 맞게 저장되는지

이 기준이 비어 있으면 에이전트가 임의로 채우지 않고 사용자에게 선택을 요구해야 한다.

UI/UX 기준 문서는 특정 경로를 강제하지 않는다. 기본 후보로 `docs/ui-ux/*`, `docs/design-system/*` 같은 구조를 제안할 수 있지만, 프로젝트가 루트 `DESIGN.md` 같은 단일 기준 문서를 승인했다면 그 구조를 따른다. CDD가 확인하는 것은 파일 위치가 아니라 `FRONTEND_UX_CRITERIA`, `DESIGN_SYSTEM`, `UI_PATTERN`, `INTERACTION_SPEC` 같은 역할이 승인 문서 안에 명확히 기록되어 있는지다.

프론트엔드 구현 전에는 분석 결과를 화면 단위 UI 구현 계약으로 고정해야 한다. 예를 들어 "공간을 줄인다"는 문장은 그대로 구현 지시가 될 수 없고, 한 카드 유지, 정보 우선순위, 금지 패턴, 반응형 기준, 브라우저/스크린샷 검증 기준처럼 확인 가능한 계약으로 바뀌어야 한다. 계약이 없으면 CDD는 컴포넌트별 수정이나 visual QA 기준을 구현 지시서에 넣지 않는다.

문서는 무조건 나누지 않는다. CDD는 파일 수 증가를 피하면서 기본 읽기 경로를 줄이는 최소 분리 원칙을 따른다. 기본 읽기 경로 문서가 400줄 또는 40KB를 넘으면 분리 후보로 보고하고, 1000줄 이상 누적 문서는 active index와 history 문서 분리 후보로 본다. 짧고 응집된 문서는 유지한다.

과거 작업 기준서, 완료 기록, 검증 기록, 구현 지시서는 그 시점의 사실 기록이지 현재 기준 문서가 아니다. generated map, Codesight, agentmemory, search index, recall output, archive branch reference는 탐색 보조 자료이며 기본 읽기 경로와 현재 기준 묶음에서 제외한다.

문서가 커진 프로젝트에서는 현재 작업 포인터 역할이 필요하다. 파일명은 강제하지 않지만 기본 후보는 `docs/project/current-work.md`다. 이 역할은 현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서, 읽지 않을 과거 기록, 현재 기준과 충돌하는 문서, README/index 갱신 필요 여부를 짧게 가리켜야 한다.

CDD는 작업 시작 전에 기본 읽기 경로 계약을 확인해야 한다. 이 계약은 이번 작업에서 반드시 읽을 문서와 기본 읽기 경로에서 제외할 과거 기록/보조 자료를 나눈다. 완료된 task, 과거 검증 결과, 완료 기록, old prompt를 다시 훑어야만 다음 작업을 판단할 수 있다면 먼저 active index와 history 분리 또는 현재 작업 포인터 갱신을 제안해야 한다.

## `cdd-audit` 문서 점검

`bin/cdd-audit`는 CDD 문서 규칙을 보조하는 read-only CLI다. 파일을 만들거나 고치거나 삭제하지 않고, 현재 작업 포인터, 기본 읽기 경로, 큰 문서, active/history 혼재, 비-SOT 자료 혼입을 보고한다.

`cdd-audit`는 어느 프로젝트 디렉터리에서도 실행할 수 있어야 한다. 실행 파일은 symlink로 호출되어도 실제 CDD root를 찾아 `PYTHONPATH`를 잡고, 현재 위치가 프로젝트 하위 디렉터리이면 `docs/README.md`, `docs/project/current-work.md`, `document-registry.yml`, `AGENTS.md`, `.git` 같은 marker를 기준으로 project root를 자동 탐지한다.

실행 환경에는 Python 3.11 이상이 필요하다. `bin/cdd-audit`는 `python3.13`, `python3.12`, `python3.11`, `python3` 순서로 지원 버전을 찾고, 없으면 `uv run --python 3.12`를 시도한다. 둘 다 없으면 실행하지 않고 필요한 런타임을 알려준다.

문서 역할 판정은 프로젝트 설정과 문서 역할 선언을 우선한다. `.cdd-audit.json`의 `roleOverrides`, 문서 frontmatter의 `role`, `documentRole`, `type`이 있으면 본문 키워드보다 먼저 적용한다. `completion`, `verification`, `history`, `archive`, `superseded` 성격의 경로나 문서는 본문에 `next task` 같은 표현이 있어도 현재 작업 후보로 승격하지 않는다.

빠른 작업 판단이 필요하면 먼저 `--format brief`를 사용한다. `brief` 출력은 현재 작업 포인터, 먼저 읽을 문서, 읽지 않을 과거 기록/보조 자료, 차단/주의 개수만 보여준다. 차단 항목이나 분리 후보의 이유가 필요할 때만 text 또는 JSON 출력으로 확장한다.

큰 문서가 발견되면 단순히 "크다"라고만 보고하지 않는다. text와 JSON 출력 모두에서 분리 후보를 보여주며, 진입점에 남길 내용, packet 또는 history로 옮길 내용, README/index 갱신 필요 여부를 함께 보고한다.

직접 실행:

```sh
/path/to/cdd/bin/cdd-audit docs --root /path/to/project --format brief --fail-on never
```

PATH에 걸어두기:

```sh
mkdir -p ~/.local/bin
ln -s /path/to/cdd/bin/cdd-audit ~/.local/bin/cdd-audit
cdd-audit docs --root /path/to/project --format brief --fail-on never
```

프로젝트 하위 디렉터리에서 실행하면 `docs/README.md`, `docs/project/current-work.md`, `document-registry.yml`, `AGENTS.md`, `.git` 같은 marker를 기준으로 root를 자동 탐지한다.

symlink를 만든 뒤 어느 디렉터리에서든 실행:

```sh
cd /path/to/project/subdir
cdd-audit docs --format brief --fail-on never
```

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
  "roleOverrides": {
    "DESIGN.md": "current-criteria",
    "docs/archive/**": "history"
  },
  "ignore": ["node_modules/**", "dist/**"],
  "currentWorkPointer": "docs/project/current-work.md"
}
```

이 도구는 CDD 판단을 대체하지 않는다. 차단 항목이 나오면 CDD 절차에 따라 사용자에게 정리 후보와 선택지를 보고해야 한다.

CDD 저장소 자체는 `.cdd-audit.json`으로 `README.md`와 `SKILL.md`만 기본 읽기 경로로 둔다. `_*.md` 내부 모듈은 CDD harness reference이지 대상 프로젝트의 현재 기준 문서가 아니므로 self-audit에서 비-SOT 보조 자료로 분류한다.

## 진행하는 경우

다음 조건이 충분하면 CDD는 다시 묻지 않고 요청 범위 안에서 이어서 진행할 수 있다.

- 요청이 명확하다.
- 필요한 제품 판단과 설계 판단이 준비되어 있다.
- 작업 범위와 금지 범위가 분명하다.
- 검증 방법이 정해져 있다.
- 데이터 삭제, migration, public API 제거, 큰 dependency 변경 같은 위험 변경이 없다.

예를 들어 문서 보강 요청이면 문서 보강 후 검증까지 진행할 수 있고, 구현 요청이면 구현, 검증, 보고까지 이어갈 수 있다.

## 멈추는 경우

다음 경우에는 CDD가 먼저 멈추고 질문해야 한다.

- 요청이 설명, 설계, 문서 수정, 구현, 삭제, 검증 중 무엇인지 애매하다.
- 제품 방향이나 설계 기준이 비어 있다.
- 저장 의미, 동작 계약, 상태 의미, 상호작용 방식, 운영/품질 기준이 부족하다.
- 삭제와 보존 중 선택해야 한다.
- migration, 데이터 삭제, public API 제거, 큰 dependency 변경이 있다.
- 기존 문서 구조와 다른 파일 배치가 필요하다.
- 사용자가 "분석만", "수정하지 마", "초안만", "먼저 보여줘"처럼 제한했다.

멈출 때는 내부 상태명보다 자연어로 말한다.

```text
아직 구현하면 안 됩니다.
먼저 정해야 할 것이 있습니다.
```

## 문서 구조

사용자가 직접 호출할 수 있는 문서는 public entrypoint다.

- `start-here.md`
- `plan-task.md`
- `write-implementation-prompt.md`
- `cleanup-delete.md`
- `verify-work.md`
- `revise-work.md`
- `complete-work.md`

`_`로 시작하는 파일은 내부 규칙이다. 보통 사용자가 직접 부르지 않고, public entrypoint 흐름 안에서 에이전트가 읽는다.

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
PYTHONDONTWRITEBYTECODE=1 ./bin/cdd-audit docs --root . --format brief --fail-on never
PYTHONDONTWRITEBYTECODE=1 python3.12 tests/test_cdd_audit.py
```

`pytest`가 설치된 환경이면 다음 명령도 사용할 수 있다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3.12 -m pytest -q
```

skill-creator의 `quick_validate.py`는 실행 환경에 PyYAML이 있어야 한다. PyYAML이 없는 기본 macOS Python에서는 frontmatter를 `head -20 SKILL.md`와 `rg -n "^---$|^name: cdd$|^description:" SKILL.md`로 확인한다.

## 유지보수 메모

- skill 인식 기준은 `SKILL.md`에 둔다.
- 사용자가 직접 부르는 흐름은 public entrypoint에 둔다.
- 세부 판정 규칙은 `_*.md` 내부 module에 둔다.
- README는 링크로 들어온 사람이 빠르게 이해하는 안내서로 유지한다.
