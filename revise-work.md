# Revise Work Skill

> Access: Public entrypoint.
> 사용자 직접 호출 가능: Verification findings를 기존 Task 범위 안의 수정 지시서로 바꿀 때 사용한다.
> Public entrypoint는 작업 흐름을 여는 문서이며, 단독으로 구현, 삭제, 기준 문서 변경, 완료 권한을 만들지는 않는다.

## 핵심 용어

- Verification findings: 검증에서 발견한 기준 불일치나 수정 필요 항목.
- Revision prompt: 기존 Task 범위 안에서만 실행할 수 있는 수정 지시서.
- 작업 기준서: 구현 전 작업 범위, 금지 범위, 검증 기준을 고정하는 작업 계약.

이 skill은 Verification findings를 바탕으로 수정 prompt를 만든다.

수정은 기존 Task 범위 안에서만 수행한다.

Revision prompt artifact는 `_artifact-metadata.md`, `_artifact-templates.md`의 `Prompt Artifact Template`, `_status-machine.md`, `_approval-reference.md`를 따른다. 사용자-facing 응답에서는 "수정 지시서"처럼 쉬운 표현을 우선 사용한다.

수정 불가 사유는 내부 status 목록이 아니라 먼저 해결해야 할 행동으로 안내한다.

기본 응답에서는 revision status, metadata, approvalRefs, legitimacy check 표를 먼저 보여주지 않는다. 상세 진단은 요청 시 제공한다.

작업 모드가 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY`이면 수정 지시서 생성, 코드 수정, 테스트 수정, rollback을 하지 않는다. 필요한 revision 후보와 승인 조건만 보고한다.

수정 지시서를 만들기 전에는 현재 기준, 과거 검증 기록, 기존 prompt, 작업 기준서를 분리해서 확인한다. 검증 결과와 기존 prompt는 그 시점의 사실 기록이며 현재 기준 문서가 아니다. 현재 기준과 과거 산출물이 충돌하면 revision prompt를 만들지 말고 Source of Truth 정합성 정리로 돌린다.

기본 읽기 경로의 revision, prompt, verification 기록이 400줄 또는 40KB를 넘으면 분리 후보로 보고한다. 1000줄 이상 누적 문서는 active index와 history 문서 분리 후보로 보고한다. 짧고 응집된 문서는 파일 수를 늘리지 않고 기존 구조를 유지한다.

## 시작 조건

Revision은 다음 조건을 모두 만족해야만 가능하다.

1. 작업 모드가 revision 실행을 허용하는 `PATCH_AUTHORIZED`, `APPLY_AUTHORIZED`, 또는 승인된 revision execution 상태다.
2. 사용자 요청에 `ANALYSIS_ONLY` 또는 `PROPOSAL_ONLY` 금지 조건이 없다.
3. Verification Result가 존재한다.
4. status가 NEEDS_REVISION이다.
5. status가 BLOCKED_BY_MISSING_CONTEXT, BLOCKED_BY_POLICY_CONFLICT, NEEDS_SOURCE_OF_TRUTH_CHANGE, BLOCKED_BY_PREDECESSOR이면 revision 금지다.
6. 필요한 source of truth 문서가 APPROVED 상태다.
7. revision-prompt가 생성되어 있다.
8. 사용자가 revision-prompt 실행을 승인했다.
9. findings가 구체적으로 작성되어 있다.
10. 수정이 기존 Task 범위 안에서 가능하다.
11. revision 근거가 되는 prompt와 verification result가 legitimacy check를 통과했다.

## 역할

- Verification findings를 수정 가능한 작업 목록으로 변환한다.
- 기존 작업 기준서와 requiredDocuments를 다시 포함한다.
- 수정 prompt를 만든다.
- 사용자가 수정 prompt를 승인하면 implementation으로 보낸다.
- 수정 완료 후 check와 verification을 다시 수행한다.

## 규칙

- 수정 프롬프트도 사용자 승인 후 실행한다.
- source of truth를 수정하지 않는다.
- document registry, Plan, 작업 기준서, prompt, verification result를 수정하지 않는다.
- 완료 후 check와 verification을 다시 수행한다.
- 기존 Task 범위를 넓히지 않는다.
- 새 정책/도메인 판단이 필요하면 수정 prompt가 아니라 미확정 결정 질문으로 보낸다.
- source of truth 변경이 필요하면 revision prompt를 만들지 말고 Source of Truth Change Request로 넘긴다.
- source of truth 변경이 필요한 동안에는 코드 수정도 금지한다.
- partial source of truth update나 known conflict가 남은 상태에서는 revision prompt를 만들지 않는다.
- 사용자 scope를 따르기 위해 source of truth 정합성을 깨뜨리는 revision을 만들지 않는다.
- 선행 Task가 COMPLETE가 아니면 후속 Task revision prompt를 만들지 않는다.
- 현재 Task 또는 선행 Task의 미확정 결정을 "나중에"로 미루고 revision하지 않는다.
- Direction Approval을 Apply Approval로 해석해 source of truth 변경 revision을 만들지 않는다.
- invalid prompt나 invalid verification result를 기반으로 revision하지 않는다.
- 기존 invalid prompt를 보강해서 revision prompt로 사용하지 않는다.
- 미확정 결정이 해결되기 전에는 revision prompt를 만들거나 실행하지 않는다.
- 현재 기준과 과거 verification, prompt, task, completion 기록이 충돌하면 revision prompt를 만들지 않는다.
- generated map, Codesight, agentmemory, search index, recall output, archive branch reference를 revision 기준으로 사용하지 않는다.
- 구현 결과가 승인되지 않은 테스트 전략을 도입했고 verification status가 NEEDS_REVISION이며 승인된 대체 전략이 이미 존재한다면, revision prompt는 그 전략으로 되돌리도록 지시한다.
- 구현 결과가 승인되지 않은 dependency, Gradle plugin, annotation processor, code generation tool, runtime-exposed library를 도입했고 기존 승인 스택 안에서 수정 가능하다면, revision prompt는 그 변경을 제거하도록 지시한다.
- 승인된 대체 전략이 없거나 사용자 정책 결정이 필요하면 revision prompt가 아니라 미확정 결정 질문 또는 Source of Truth Change Request로 되돌린다.
- 새로운 테스트 전략이 필요하다고 판단되면 revision prompt가 아니라 미확정 결정 질문으로 되돌린다.
- 새로운 dependency/build tool/code generation 정책이 필요하면 revision prompt가 아니라 미확정 결정 질문으로 되돌린다.
- H2를 Testcontainers로 바꾸는 식의 대체 전략도 source of truth 승인 없이는 금지한다.

## 수정 prompt에 포함할 내용

- artifact metadata
- status
- approvalRefs
- 기존 Task ID
- verification status와 finding 목록
- 수정해야 할 항목
- 수정하지 말아야 할 항목
- requiredDocuments
- forbiddenApproaches
- testRequirements
- source of truth 변경 금지
- 완료 후 check/verification 재실행 지시
- 승인되지 않은 테스트 dependency/profile/migration/dialect/mock/fake/stub 제거 지시
- 승인되지 않은 production dependency/plugin/annotation processor/code generation/runtime-exposed library 제거 지시
- testRequirements 축소 금지
- DB integration test를 unit/static test로 대체 금지
- Repository save/find 테스트 제거 금지
- Flyway 실제 적용 테스트를 SQL 정적 검증으로 대체 금지

Revision prompt draft approval과 execution approval은 분리한다. 수정 지시서 초안 검토만으로 수정 실행을 시작하지 않는다.

## 승인되지 않은 테스트 전략 finding 예시

```text
Finding: H2 and test-specific migration were introduced without approved TEST_STRATEGY.

Allowed revision when status is NEEDS_REVISION and approved source of truth already defines the target strategy:
Remove H2, remove application-test.yml, remove db/migration-test/**, and adjust tests to the approved strategy.

Not allowed:
Replace H2 with Testcontainers unless Testcontainers is approved in source of truth.
If TEST_STRATEGY is missing, do not remove H2 or change tests yet. Stop with BLOCKED_BY_MISSING_CONTEXT and ask the user.
```

## Verification 상태별 허용 행동

- VERIFIED: revision을 만들지 않는다. user review approval 요청과 complete만 가능하다.
- NEEDS_REVISION: revision-prompt 생성 가능. 사용자 승인 후 revision 가능하다.
- BLOCKED_BY_MISSING_CONTEXT: 미확정 결정 질문만 가능. 코드 수정, revision, complete 금지.
- BLOCKED_BY_POLICY_CONFLICT: 충돌 보고만 가능. 사용자 정책 결정 또는 source of truth 수정 승인 전 코드 수정, revision 금지.
- NEEDS_SOURCE_OF_TRUTH_CHANGE: Source of Truth Change Request만 가능. 사용자 승인 전 코드 수정, revision, complete, 문서 직접 수정 금지.
- BLOCKED_BY_PREDECESSOR: 선행 Task 완료 전 후속 Task revision, implementation, complete 금지.

## 중단 조건

다음이면 revision prompt를 만들지 않는다.

- finding을 해결하려면 새 도메인 정책이 필요하다.
- finding을 해결하려면 architecture boundary 변경이 필요하다.
- source of truth와 Task 요구가 충돌한다.
- Task 범위 밖 기능 추가가 필요하다.
- finding을 해결하려면 새로운 테스트 DB/profile/migration/mock/fake/stub 정책이 필요하다.
- finding을 해결하려면 새로운 dependency/plugin/annotation processor/code generation/runtime library 정책이 필요하다.
- verification status가 BLOCKED_BY_MISSING_CONTEXT 또는 BLOCKED_BY_POLICY_CONFLICT다.
- verification status가 NEEDS_SOURCE_OF_TRUTH_CHANGE다.
- verification status가 BLOCKED_BY_PREDECESSOR다.
- verification status가 BLOCKED_BY_INVALID_ARTIFACT다.
- Known Conflicts After Apply가 비어 있지 않다.
- 작업 기준서가 변경된 source of truth와 불일치한다.
- dependsOn Task가 COMPLETE가 아니다.
- 미확정 결정을 "나중에"로 미루고 있다.
- revision 근거 artifact가 legitimacy check를 통과하지 못했다.
- 현재 기준과 과거 verification, prompt, task, completion 기록 사이 충돌이 남아 있다.
- revision-prompt 실행에 대한 사용자 승인이 없다.

이 경우 `_missing-context.md` 또는 `_source-of-truth-manager.md`로 이동한다.

사용자-facing 보고에서는 내부 status만 말하지 않고, "이 문제는 현재 작업 범위 안에서 고칠 수 없습니다. 먼저 기준 문서나 선행 작업 상태를 정리해야 합니다."처럼 설명한다.

수정 지시서를 만들 수 없을 때는 다음 형식을 우선 사용한다.

```text
지금은 수정 지시서를 만들 수 없습니다.
먼저 다음을 선행해 주세요.
1. 기준 문서와 작업 지시가 서로 맞는지 정리해 주세요.
2. 선행 작업이 끝났는지 확인해 주세요.
3. 수정 지시서를 만들어도 되는지 승인해 주세요.

다음에 할 일:
아직 직접 진행하면 안 됩니다. 먼저 아래 중 하나를 선택해야 합니다.

선택지:
1. 기준 문서와 작업 지시의 충돌을 먼저 정리한다.
2. 선행 작업을 먼저 완료한다.
3. 수정 지시서 작성을 보류한다.

제 추천:
- 기준 문서 충돌과 선행 작업 상태를 먼저 정리한 뒤 수정 지시서를 작성합니다.

바로 답할 수 있는 문장:
"추천안대로 충돌과 선행 작업 상태를 정리할 질문부터 만들어라."
```

수정 지시서를 만들 수 있고 사용자 개입이 필요 없으면 다음 형식으로 말한 뒤 실제로 수정 지시서 작성과 검증 준비까지 수행한다.

```text
다음에 할 일:
사용자 선택이 필요한 부분은 없습니다.
현재 기준으로 안전하게 진행할 수 있으므로, 요청 범위 안에서 다음 작업까지 진행합니다.

진행할 작업:
- 수정 지시서 작성
- 수정 범위와 금지 범위 확인
- 검증 방법 정리

진행하지 않을 작업:
- 승인되지 않은 코드 수정
- 기준 문서에 없는 정책 결정
```
