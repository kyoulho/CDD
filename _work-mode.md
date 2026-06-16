# Work Mode Gate Skill

> Access: Internal chain module.
> 내부용 chain module이다. task entrypoint로 직접 호출하지 마라.
> 이 module만으로는 implementation, SOT changes, cleanup/delete, completion을 승인할 수 없다.

이 skill은 사용자 요청의 작업 모드를 먼저 판별하고, 해당 모드가 허용하는 행동 범위를 고정한다.

작업 모드 판별은 source of truth readiness, planning, prompt authoring, implementation, verification, revision, completion보다 먼저 수행한다.

요청이 어떤 작업인지 애매하면 먼저 질문한다. 애매한 요청을 임의로 해석하지 않는다. 애매한 요청을 구현 요청으로 승격하지 않는다. 애매한 요청을 파일 수정 승인으로 해석하지 않는다.

작업 성격을 하나로 확정할 수 없으면 가장 제한적인 방식으로 멈추고 사용자에게 자연어로 묻는다.

작업 성격이 명확하고 현재 모드가 파일 수정, 실행, 검증을 허용하면 사용자에게 다시 묻지 않고 허용 범위 안에서 다음 단계까지 진행한다. 단, 제품 판단이나 설계 판단이 비어 있거나 위험 변경이 있으면 자동 진행하지 않는다.

## 사용자 개입 필요 여부

작업 모드 판별 후에는 사용자 개입이 필요한지 함께 판정한다.

사용자 개입이 필요한 경우:

- 사용자가 선택해야 하는 제품 판단이 남아 있다.
- 사용자가 선택해야 하는 설계 판단이 남아 있다.
- 데이터 삭제, public API 제거, migration, dependency 대량 변경처럼 위험한 변경이 있다.
- 현재 요청이 실제 파일 수정을 허용하는지 불명확하다.
- 현재 문서 기준만으로 안전하게 다음 단계로 갈 수 없다.
- 사용자가 "아직 수정하지 마라", "분석만", "제안만"처럼 제한을 걸었다.

사용자 개입이 필요하면 멈추고 `_user-facing-language.md`의 "사용자 선택이 필요한 경우" 형식으로 선택지, 추천, 바로 답할 수 있는 문장을 제공한다.

사용자 개입 없이 진행 가능한 경우:

- 사용자의 요청이 명확하다.
- 현재 작업 모드가 필요한 파일 수정 또는 실행을 허용한다.
- 제품 기준과 설계 기준이 충분하다.
- 저장, 동작, 상태, 상호작용, 운영 기준이 충분하다.
- 작업 범위가 작고 명확하다.
- 금지된 작업에 닿지 않는다.
- 데이터 손실, public API 제거, migration 위험, dependency 대량 변경이 없다.
- 검증 방법이 명확하다.

이 경우 `_user-facing-language.md`의 "사용자 개입 없이 진행 가능한 경우" 형식으로 진행할 작업과 진행하지 않을 작업을 말한 뒤 실제로 다음 단계까지 수행한다. "진행합니다"라고 보고만 하고 멈추지 않는다.

## 작업 모드

### CLARIFICATION_NEEDED

사용자 요청이 설명, 설계안, 문서 초안, 문서 수정, 구현 계획, 실제 코드 수정, 삭제/정리, 검증 중 무엇을 원하는지 확정할 수 없는 상태다.

대표 표현:

- "정리해줘"
- "이거 진행해"
- "구조 잡아줘"
- "다음 단계로 가자"
- "고쳐줘"
- "문서 반영해"
- "설계해"
- "구현해도 될까?"

허용 행동:

- 현재 요청이 애매하다고 판단한다.
- 사용자가 원하는 단계가 무엇인지 자연어로 질문한다.
- 선택지를 제시한다.
- 기존 파일이나 기준 문서를 읽어도 되는지 명확하지 않으면 읽기 범위도 함께 확인한다.

금지 행동:

- 구현 시작
- 파일 생성, 수정, 삭제
- 문서 초안 저장
- source of truth 문서 수정
- Plan, Task, prompt, verification result 생성 또는 수정
- cleanup/delete 실행
- "좋아", "진행해", "다음", "반영해" 같은 표현만으로 권한 승격

사용자-facing 질문 예:

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

### ANALYSIS_ONLY

사용자가 분석, 원인 파악, 검토, 제안만 요청한 상태다.

대표 표현:

- "분석만 해줘"
- "수정하지 마"
- "원인만 봐줘"
- "검토만 해줘"
- "제안만 해줘"
- "이번 작업은 수정이 아니라 분석이다"
- "아직 파일을 수정하지 마라"

허용 행동:

- 파일 읽기
- 상태 확인
- 원인 분석
- 실패 패턴 분류
- 위험 분석
- 수정 대상 후보 제안
- 패치 계획 제안
- 사용자에게 다음 승인 문구 안내

금지 행동:

- 파일 생성, 수정, 삭제
- skill 파일 수정
- source of truth 문서 수정
- 금지된 대상 프로젝트 코드 또는 문서 수정
- Plan, Task, Prompt, runs, verification result, completion record 수정
- formatting만 한다는 이유의 파일 저장
- rollback, revert, restore
- 자동 패치 적용
- CLI/tools 구현

rollback도 파일 수정이다. ANALYSIS_ONLY에서는 이전 unauthorized change를 되돌리는 것도 금지한다. 되돌리기가 필요하면 별도 `APPLY_AUTHORIZED` 또는 `PATCH_AUTHORIZED` 승인을 받아야 한다.

### PROPOSAL_ONLY

사용자가 변경 제안, 패치 방향, 설계안, diff 계획을 요청한 상태다.

허용 행동:

- 읽기
- 분석
- 변경안 작성
- 수정 파일 후보 제안
- 적용 전 사용자 승인 요청

금지 행동:

- 실제 파일 수정
- generated artifact 저장
- rollback
- 승인 없이 `apply_patch` 실행

### PATCH_AUTHORIZED

사용자가 특정 범위의 파일 수정을 명시적으로 승인한 상태다.

예:

- "위 분석에 따라 skill 파일 수정을 승인합니다"
- "CDD skill 파일 수정을 승인합니다"
- "분석한 대로 패치해줘"
- "위 제안을 CDD skill 파일에 반영해줘"

허용 행동:

- 승인된 범위 안의 파일 수정
- 승인된 범위 안의 새 파일 생성
- 수정 결과 검증
- 변경 요약 보고
- 사용자 개입이 필요 없는 후속 검증과 완료 보고까지 이어서 수행

금지 행동:

- 승인된 범위 밖 파일 수정
- source of truth 정합성 게이트 우회
- 대상 프로젝트 수정 금지 조건이 있는 경우 해당 파일 수정
- CLI/tools 구현 금지 조건이 있는 경우 tools 수정

### APPLY_AUTHORIZED

사용자가 이미 제시된 변경 묶음 또는 Change Request 적용을 명시 승인한 상태다.

APPLY_AUTHORIZED는 변경 방향 승인과 다르다. "A로 하자", "좋아", "진행해"는 APPLY 승인으로 해석하지 않는다.

허용 행동:

- 승인된 Files Proposed for Apply 전체를 적용
- 적용 후 정합성 확인
- 적용 결과 보고
- 사용자 개입이 필요 없는 후속 검증과 완료 보고까지 이어서 수행

금지 행동:

- 승인되지 않은 추가 파일 수정
- 일부 source of truth만 바꾸고 known conflict를 남기는 적용
- prompt execution 또는 implementation approval로 권한 승격

### IMPLEMENTATION

사용자가 승인된 구현 지시서를 기준으로 실제 구현을 요청한 상태다.

IMPLEMENTATION은 별도의 source of truth, Task Contract, prompt, approval gate를 통과해야 한다. 단순히 "구현해줘"라고 했다는 이유로 ANALYSIS_ONLY, PROPOSAL_ONLY, PATCH_AUTHORIZED를 무시하지 않는다.

### DOCUMENT_ONLY

사용자가 문서 작성이나 문서 수정만 요청한 상태다.

허용 행동:

- 승인된 문서 범위 안의 문서 생성 또는 수정
- 문서 변경에 필요한 읽기와 검색
- 문서 검증 명령 실행
- 사용자 개입이 필요 없는 후속 문서 검증과 보고까지 이어서 수행

금지 행동:

- 코드, 테스트, 설정 파일 수정
- dependency 추가
- CLI/tools 구현
- 문서 변경을 이유로 source of truth 승인 게이트 우회
- SOT Packet의 allowedScope 밖 문서 수정

### CLEANUP_DELETE

사용자가 폐기, 삭제, dead code 제거, stale API/UI/DB artifact 제거, deprecated 기능 제거를 요청한 상태다.

`CLEANUP_DELETE`는 일반 리팩토링이나 새 기능 구현이 아니다. 실행 전 `cleanup-delete.md`의 keep list, delete list, 의존성 확인, 사람 확인 지점을 Task에 반영해야 한다.

`CLEANUP_DELETE`는 삭제 작업 분류와 playbook 선택이지 독립적인 쓰기 권한이 아니다. 파일 수정/삭제는 승인된 `PATCH_AUTHORIZED`, `APPLY_AUTHORIZED`, 구현 prompt 실행 승인, 또는 승인된 revision execution 범위 안에서만 수행한다.

허용 행동:

- approved source of truth와 Task scope 안에서 legacy 기능 제거
- keep list와 delete list 작성
- 삭제 전 의존성 확인
- archive/superseded 참조 여부 확인
- 삭제 결과 검증과 완료 보고
- 사용자 개입이 필요 없는 cleanup/delete 검증과 보고까지 이어서 수행

금지 행동:

- 폐기된 기능을 이름만 바꿔 core path에 남기기
- 새 기능 구현으로 확장
- 테스트를 통과시키기 위한 검증 약화
- existing migration 파일 수정
- 사용자 확인 없는 DB drop, public API 제거, 대량 삭제, dependency 대량 제거

## 모드 판별 우선순위

사용자 요청이 설명, 설계, 문서 수정, 구현, 삭제, 검증 중 무엇인지 애매하면 `CLARIFICATION_NEEDED`가 우선한다. 이 상태에서는 바로 작업하지 말고 먼저 질문한다.

명시적 금지 표현이 있으면 가장 제한적인 모드가 우선한다. cleanup/delete 요청과 분석 전용 요청이 함께 있으면 `ANALYSIS_ONLY`로 처리하고 delete list 후보만 보고한다.

예:

```text
원인 분석하고 필요한 패치 파일도 알려줘. 수정하지 마.
```

이 요청은 `ANALYSIS_ONLY`다. 수정 대상 파일을 제안할 수는 있지만 실제 수정은 금지한다.

예:

```text
위 분석에 따라 CDD skill 파일 수정을 승인합니다.
```

이 요청은 승인 문구와 범위가 있으므로 `PATCH_AUTHORIZED`다.

## 분석에서 패치로 전환하는 조건

ANALYSIS_ONLY 또는 PROPOSAL_ONLY에서 PATCH_AUTHORIZED로 전환하려면 사용자의 명시 승인이 필요하다.

허용 승인 예:

```text
위 분석에 따라 skill 파일 수정을 승인합니다.
CDD skill 파일 수정을 승인합니다.
분석한 대로 CDD skill files만 패치해줘.
위 제안을 CDD skill 파일에 반영해줘.
```

불충분한 표현:

```text
좋아.
진행해.
다음.
반영해.
그 방향으로 가자.
필요한 파일은 알아서 고쳐.
제안한 대로 해.
```

모호하면 패치하지 말고 어떤 파일 범위의 수정을 승인하는지 확인한다. 애매하면 먼저 질문한다.

## 하네스 에이전트에 대한 적용

하네스 skill을 수정하는 에이전트도 이 게이트를 따른다.

하네스 에이전트는 일반적으로 CDD skill files를 수정할 수 있는 역할일 수 있지만, 사용자가 ANALYSIS_ONLY를 명시하면 모든 쓰기 권한이 잠긴다.

사용자가 "skill layer를 분석하라", "하네스 실패를 검토하라", "수정하지 마라"라고 한 경우:

- skill 파일을 수정하지 않는다.
- README를 수정하지 않는다.
- rollback하지 않는다.
- "수정 대상 파일"은 보고서 안에서만 제안한다.

## 실패 패턴

- `AMBIGUOUS_REQUEST_ESCALATED`: 애매한 요청을 구현, 문서 수정, 삭제, 검증 실행으로 임의 승격했다.
- `ANALYSIS_ONLY_MODE_VIOLATION`: ANALYSIS_ONLY 요청에서 파일 생성, 수정, 삭제를 수행했다.
- `UNAUTHORIZED_SKILL_MODIFICATION`: 명시 승인 없이 CDD skill files를 수정했다.
- `MODE_ESCALATION_WITHOUT_APPROVAL`: 분석/제안 모드를 패치/적용/구현 모드로 사용자 승인 없이 승격했다.
- `REQUESTED_ANALYSIS_EXECUTED_AS_PATCH`: 사용자가 분석을 요청했는데 실제 패치를 수행했다.

## 사용자-facing 응답

요청 의도가 애매하면 내부 모드명을 먼저 말하지 않는다. 사용자에게 자연어로 묻는다.

Bad:

```text
Work Mode가 불명확합니다.
ANALYSIS_ONLY인지 IMPLEMENTATION인지 확인해 주세요.
```

Good:

```text
지금은 실제 수정을 시작하기 전에, 먼저 어느 단계까지 원하는지 확인해야 합니다.
현재 상태를 읽고 판단만 할까요, 문서 초안을 만들까요, 아니면 실제 파일 수정을 원하시나요?
```

ANALYSIS_ONLY 요청을 받으면 보고 마지막에 수정하지 않았음을 명시한다.

```text
이번 응답은 분석만 수행했습니다.
파일 수정, rollback, CLI/tools 구현은 하지 않았습니다.
필요하면 다음 단계에서 CDD skill 파일 수정을 명시적으로 승인해 주세요.
```

PATCH_AUTHORIZED 요청을 받으면 시작 전에 범위를 짧게 확인한다.

```text
이번 요청은 CDD skill files 범위의 PATCH_AUTHORIZED로 처리하겠습니다.
대상 프로젝트 파일과 tools/CLI는 수정하지 않겠습니다.
```
