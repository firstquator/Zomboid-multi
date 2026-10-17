# 유튜브 추천 캐릭터 조합 조사 (B42, 2026-10-18 확인)

"캐릭터 만들기" 페이지에 넣을 커뮤니티 추천 조합(직업 + 특성)을 유튜브 영상에서 모은 기록이다.

## 기준과 확인 방법

- 대상: Build 42 영상만 쓴다. 실제로 쓴 영상은 모두 **2026-08 이후**(42.20 stable 무렵부터 42.21까지)에 올라온 것이다. B41 영상과 B42 초기(2024-12~2025) 영상은 특성 비용이 지금과 달라 뺐다(맨 아래 "뺀 영상" 참고).
- 검색: `yt-dlp "ytsearch15:<검색어>"` 와 WebSearch 를 같이 썼다. 검색어는 `project zomboid build 42 best build`, `project zomboid b42 best traits`, `project zomboid build 42 beginner build`, `project zomboid build 42 best occupation`, `project zomboid 42.21 best build`, `project zomboid 42.20 build traits`, `좀보이드 42 특성 추천`, `좀보이드 b42 빌드`, `좀보이드 42빌드 직업 추천`, `좀보이드 42.21 특성` 등이다.
- 내용 확인: yt-dlp 로 **메타데이터(게시일·조회수·설명란·챕터)와 자동 자막만** 받았다. 영상 파일은 받지 않았다. 그래서 **화면에만 나오고 말로는 하지 않은 특성표는 확인하지 못했다.** 이런 영상은 "부분 확인"으로 표시했다.
- 검산: 모든 조합을 `web/src/data/character.json`(build 42.21.0)의 비용으로 다시 계산했다. 잔여 = 직업 cost + (부정 특성 점수 합) − (긍정 특성 비용 합). 0 이상이어야 게임을 시작할 수 있다. `exclusive`(함께 못 고르는 특성) 충돌도 같이 검사했고, 충돌은 하나도 없었다.
- 조회수는 2026-10-18 에 yt-dlp 로 읽은 값이다.
- 특성 표기: `영상에서 쓴 이름` → `character.json id`. 한국어 영상은 영상에서 부른 이름을 그대로 적었다.

## 요약

| # | 채널 | 영상 (게시일) | 버전 | 직업 | 긍정 | 부정 | 42.21 검산 | 확인 |
|---|---|---|---|---|---|---|---|---|
| 1 | Laughter | TOP 8 CHARACTER BUILDS In Build 42 (2026-08-11) | B42 Stable | policeofficer | target_shooter, hunter, stout, organized, speeddemon, inventive, dextrous, fastlearner, gymnast, lighteater | thinskinned, pronetoillness, slowhealer, weakstomach, conspicuous, slowreader, cowardly, claustrophobic, hemophobic, asthmatic, Out of Shape* | 0 | 자막 |
| 2 | FireSpark81 | Build 42 Negative Best Traits Guide (2026-08-08) | Build 42 | fitnessinstructor | strong, fit, fastlearner | weakstomach, slowreader, slowhealer, pronetoillness, conspicuous, pacifist, thinskinned | 0 | 자막+챕터 |
| 3 | OVERCHARGED EGG | The ULTIMATE NOOBS GUIDE To Project Zomboid Build 42, Day 1 (2026-08-07) | Build 42 | unemployed | athletic, strong, fastlearner, nightvision, organized, dextrous | clumsy, highthirst, slowreader, weakstomach, slowhealer, conspicuous, pronetoillness, thinskinned | 0 | 자막 |
| 4 | Duckie0012 | Project Zomboid Beginner's Guide, Build 42 Stable (2026-08-03) | B42 Stable | securityguard | dextrous, nightvision, keenhearing, needslesssleep | thinskinned, pronetoillness, conspicuous | 0 | 자막+챕터 |
| 5 | Orbanjo Gaming | Project Zomboid is Lying about XP, Build 42 Traits Explained (2026-08-25) | Build 42 | constructionworker | stout, fastlearner, organized, brave, gymnast, speeddemon | thinskinned, pacifist, conspicuous, slowhealer, weakstomach, slowreader, shortsighted, highthirst | 0 | 자막 |
| 6 | 던지기맨 좀비 | 좀보이드 42빌드 직업 특성 종결 (2026-08-08) | 42.20 | fitnessinstructor | speeddemon, dextrous, outdoorsman, needslesssleep, baseballplayer, organized, fastlearner, fit, keenhearing, strong | thinskinned, insomniac, hemophobic, claustrophobic, conspicuous, heartyappetite, pronetoillness, slowhealer, smoker, cowardly, highthirst, shortsighted, slowreader, weakstomach | +1 | 자막에서 재구성 |
| 7 | 단시니의 그저 그런 이야기 | 좀보이드 B42.20 샌드박스 및 특성 설정 (2026-08-16) | 42.20 | engineer | speeddemon, needslesssleep, organized, fastlearner, keenhearing, athletic, strong, dextrous | cowardly, highthirst, clumsy, weightloss, slowreader, weakstomach, thinskinned, slowhealer, conspicuous, heartyappetite, pronetoillness, pacifist, shortsighted, claustrophobic | 0 | 자막에서 재구성 |
| 8 | Pauly_dc (스페인어) | el MEJOR PERSONAJE de Project Zomboid (Build 42.21) (2026-10-02) | 42.21 | lumberjack | dextrous, needslesssleep, nightvision, gymnast, fastlearner, keenhearing, athletic | thinskinned, pacifist, pronetoillness, shortsighted, conspicuous, slowhealer, cowardly, weakstomach, slowreader, highthirst, clumsy | +1 | 설명란+자막 |
| 9 | Captain Capitalism | Project Zomboid Build 42.20 Best Negative Traits (2026-09-04) | 42.20 | lumberjack (또는 fireofficer) | athletic, strong (+ 나머지 자유) | shortsighted, highthirst, weakstomach, slowhealer, pronetoillness, heartyappetite, pacifist, thinskinned (선택: clumsy, conspicuous) | +10 남음 | 부분 확인 |
| 10 | 워킹녹스 : Walking Knox | 좀보이드 42 뉴비 공략 #1 (2026-08-27) | 42 | constructionworker | strong, athletic, keenhearing, brave | (화면에만 나와 확인 못 함) | – | 부분 확인 |

\* Out of Shape(체력 −2, 6점)는 `character.json` 에 없다. 아래 "데이터 메모" 참고.

- 1~8번은 영상이 말한 특성만으로 조합이 완성되고, 42.21 비용으로 계산해도 잔여가 0 또는 +1 이다. 영상 시점(42.20)과 42.21 사이에 이 조합들의 비용은 바뀌지 않은 것으로 보인다.
- 9~10번은 일부만 확인했다. 페이지에 넣는다면 "핵심 특성만" 형태로 쓰는 것이 맞다.
- Laughter 영상에는 조합이 8개 있다. 1번에는 총기 조합을 넣었고, 나머지 7개는 부록 A에 있다. 7개 모두 42.21 비용으로 잔여 0이다.

## 조합 상세

### 1. Laughter: 6 Aiming Policeman (총기 특화)

- 영상: TOP 8 CHARACTER BUILDS In Build 42 Project Zomboid
- URL: https://www.youtube.com/watch?v=ujrLpaM8HPI
- 게시: 2026-08-11 · 조회수 30,658 · 버전: "B42 Stable"(설명란)
- 직업: Police Officer → `policeofficer` (−4)
- 긍정: Target Shooter `target_shooter`, Hunter `hunter`, Stout `stout`, Organized `organized`, Speed Demon `speeddemon`, Inventive `inventive`, Dextrous `dextrous`, Fast Learner `fastlearner`, Gymnast `gymnast`, Light Eater `lighteater` (41점)
- 부정: 기본 6종(Thin-skinned `thinskinned`, Prone to Illness `pronetoillness`, Slow Healer `slowhealer`, Weak Stomach `weakstomach`, Conspicuous `conspicuous`, Slow Reader `slowreader`) + Cowardly `cowardly`, Claustrophobic `claustrophobic`, Fear of Blood `hemophobic`, Short of Breath `asthmatic`, Out of Shape(json 없음, 6점) (45점)
- 추천 이유: 경찰관의 조준 4에 Target Shooter와 Hunter를 더해 조준 6으로 시작하므로 패닉이 사격에 영향을 주지 않는다. 부정 특성은 거리를 두고 쏘는 플레이에는 거의 상관없는 것(겁쟁이, 밀실 공포증, 피 공포증, 천식, 체력 저하)으로 골랐다.
- 근거: 자막 09:04~10:30(챕터 "6 Aiming Policeman"). 영상이 말하는 "기본 6종 부정 + Dextrous + Fast Learner" 정의는 02:00~02:31.
- 검산: −4 + 45 − 41 = **0**

### 2. FireSpark81: OP Meta Starter Build (피트니스 강사, 시작부터 체력·근력 10)

- 영상: You Info Is Outdated! Project Zomboid Build 42 Negative Best Traits Guide
- URL: https://www.youtube.com/watch?v=JTXhuGv1AU8
- 게시: 2026-08-08 · 조회수 182,769 · 버전: "Build 42"(게임 코드를 디컴파일해서 분석했다고 설명. 세부 버전은 말하지 않음)
- 직업: Fitness Trainer(= Fitness Instructor) → `fitnessinstructor` (−6, Nutritionist `nutritionist2` 자동 부여)
- 긍정: Strong `strong`, Fit `fit`, Fast Learner `fastlearner` (22점)
- 부정: Weak Stomach `weakstomach`, Slow Reader `slowreader`, Slow Healer `slowhealer`, Prone to Illness `pronetoillness`, Conspicuous `conspicuous`, Reluctant Fighter `pacifist`, Thin-skinned `thinskinned` (28점)
- 추천 이유: 체력 10, 근력 10, 달리기 2로 시작한다. 좀비의 첫 공격을 막아 내는 판정에 체력과 근력이 들어가서 처음부터 덜 맞는다고 설명한다. Reluctant Fighter(전투 XP −25%)를 Fast Learner(+30%)와 같이 고르면 전투 XP 배율은 0.975로 거의 그대로이고, Fast Learner를 사실상 1점에 사는 셈이라고 설명한다.
- 근거: 자막 12:06~13:40(챕터 "OP Meta Starter Build Setup").
- 검산: −6 + 28 − 22 = **0**

### 3. OVERCHARGED EGG: 커스텀 직업 초보 빌드

- 영상: The ULTIMATE NOOBS GUIDE To Project Zomboid Build 42 | Day 1
- URL: https://www.youtube.com/watch?v=ETUHLVlcf38
- 게시: 2026-08-07 · 조회수 312,254 · 버전: "Build 42"(아포칼립스, 신규 유저용 시리즈)
- 직업: Custom Occupation → `unemployed` (+8)
- 긍정: Athletic `athletic`, Strong `strong`, Fast Learner `fastlearner`, Cat's Eyes `nightvision`, Organized `organized`, Dextrous `dextrous` (35점)
- 부정: Clumsy `clumsy`, High Thirst `highthirst`, Slow Reader `slowreader`, Weak Stomach `weakstomach`, Slow Healer `slowhealer`, Conspicuous `conspicuous`, Prone to Illness `pronetoillness`, Thin-skinned `thinskinned` (27점)
- 추천 이유: 직업 보너스 대신 8점을 받고, 훈련하기 가장 귀찮은 체력과 근력을 특성으로 미리 올린다. B42는 밤이 매우 어두워 Cat's Eyes를 넣었다. Weak Stomach를 고르면 상한 음식을 절대 먹지 말라고 경고한다.
- 근거: 자막 04:10~07:40("35 points to spend" → "exactly zero points").
- 검산: +8 + 27 − 35 = **0**

### 4. Duckie0012: 경비원 저위험 초보 빌드

- 영상: Project Zomboid Beginner's Guide | Build 42 Stable
- URL: https://www.youtube.com/watch?v=19mLw7E-yTc
- 게시: 2026-08-03 · 조회수 82,447 · 버전: "Build 42 Stable"
- 직업: Security Guard → `securityguard` (−2, Night Owl `nightowl` 자동 부여)
- 긍정: Dextrous `dextrous`, Cat's Eyes `nightvision`, Keen Hearing `keenhearing`, Wakeful `needslesssleep` (14점)
- 부정: Thin-skinned `thinskinned`, Prone to Illness `pronetoillness`, Conspicuous `conspicuous` (16점)
- 추천 이유: Dextrous, Cat's Eyes, Keen Hearing은 매번 고르는 3종이고, 초보는 무기 스킬이 있는 직업을 고르라고 한다(경비원은 달리기 2, 짧은 둔기 1). 부정 특성은 포인트를 맞출 만큼만 골라 부담이 적다.
- 근거: 자막 02:53~06:20(챕터 "character creation" 02:53, "Security Guard is my preferred class so far" 04:42). "three points left over" 다음에 Wakeful을 넣는다.
- 검산: −2 + 16 − 14 = **0**

### 5. Orbanjo Gaming: 건축 인부 근접 빌드

- 영상: Project Zomboid is Lying about XP — Build 42 Traits Explained
- URL: https://www.youtube.com/watch?v=2PZNukP6bUY
- 게시: 2026-08-25 · 조회수 24,565 · 버전: "Build 42"(직업 25개 기준)
- 직업: Construction Worker → `constructionworker` (−2)
- 긍정: Stout `stout`, Fast Learner `fastlearner`, Organized `organized`, Brave `brave`, Gymnast `gymnast`, Speed Demon `speeddemon` (26점)
- 부정: Thin-skinned `thinskinned`, Reluctant Fighter `pacifist`, Conspicuous `conspicuous`, Slow Healer `slowhealer`, Weak Stomach `weakstomach`, Slow Reader `slowreader`, Short Sighted `shortsighted`, High Thirst `highthirst` (28점)
- 추천 이유: 건축 인부의 짧은/긴 둔기·물건관리 시작 레벨에 Stout로 근력 7을 더한 근접 빌드다. Reluctant Fighter는 Fast Learner로 상쇄하고, Gymnast로 조준 시 발걸음·조용한 발걸음에 4배 배율을 받는다. Prone to Illness를 더 넣으면 Speed Demon 대신 5점을 더 쓸 수 있다고 덧붙인다.
- 근거: 부정 특성별 선택은 자막 49:10~61:50, 최종 조합은 62:01~64:31("I have 26 points to spend" → Speed Demon으로 마감).
- 검산: −2 + 28 − 26 = **0**

### 6. 던지기맨 좀비: 근접은 피트니스 강사

- 영상: 좀보이드 42빌드 직업 특성 종결. 딱 '이 2개' 말고는 할 이유가 없습니다
- URL: https://www.youtube.com/watch?v=IkldfAON_do
- 게시: 2026-08-08 · 조회수 61,146 · 버전: "42.20 버전 기준"(설명란)
- 직업: 피트니스 강사 → `fitnessinstructor` (−6). 설명란 요약은 "근접 무기 = 피트니스 강사, 총기 = 경찰관"이다.
- 긍정: 속도광 `speeddemon`, 민첩한 `dextrous`, 등산애호가 `outdoorsman`, 잠이 없는 `needslesssleep`, 야구 선수 `baseballplayer`, 정리쟁이 `organized`, 현자 `fastlearner`, 건강함 `fit`, 예민한 청력 `keenhearing`, 튼튼함 → `strong`(json 이름: 강인함) (44점)
- 부정: 얇은 피부 `thinskinned`, 수면 장애 `insomniac`, 피 공포증 `hemophobic`, 밀실 공포증 `claustrophobic`, 넘치는 존재감 `conspicuous`, 대식가 `heartyappetite`, 질병에 취약함 `pronetoillness`, 느린 치유 `slowhealer`, 골초 `smoker`, 겁쟁이 `cowardly`, 높은 갈증 `highthirst`, 짧은 시야 `shortsighted`, 정독 `slowreader`, 소화불량 `weakstomach` (51점)
- 추천 이유: 피트니스 강사는 기본 체력이 8이라 육상 선수 대신 건강함만 찍어도 체력 10이 된다. 육상 선수는 골초와 함께 고를 수 없어서, 이렇게 하면 골초 3점까지 챙길 수 있다. 긴 둔기가 현재 가장 강한 근접 무기라 야구 선수를 넣고, 다른 무기를 쓸 거면 체조선수로 바꾼다. 튼튼함까지 찍으면 근력도 10이 된다.
- 근거: 영상 00:00~00:11 화면에 특성표가 나오지만 영상 파일을 받지 않아 보지 못했다. 위 목록은 **자막 01:27~02:52에서 하나씩 설명한 특성을 모은 것**이다. 42.21 비용으로 잔여가 +1이라 실제로 고를 수 있는 조합이다.
  - 업로더가 올린 영어 자막은 '수면 장애'를 Sleepyhead, '튼튼함'을 Stout로 옮겼다. 하지만 그렇게 하면 포인트가 −1이 되고, 근력도 10이 아니라 8이 된다. 그래서 한국어 내레이션대로 Restless Sleeper(`insomniac`)와 Strong(`strong`)으로 적었다.
  - 경찰관 조합은 화면에만 나와서 확인하지 못했다.
- 검산: −6 + 51 − 44 = **+1**

### 7. 단시니: 기술자 풀셋 (파이프 폭탄)

- 영상: 좀보이드 B42.20 샌드박스 및 특성 설정
- URL: https://www.youtube.com/watch?v=4cDD7ZvfT6c
- 게시: 2026-08-16 · 조회수 1,229 · 버전: 42.20
- 직업: 기술자 → `engineer` (−4)
- 긍정: 속도광 `speeddemon`, 잠이 적음 `needslesssleep`, 정리쟁이 `organized`, 빠른 학습 `fastlearner`, 예민한 청력 `keenhearing`, 육상 선수 `athletic`, 튼튼함 → `strong`, 민첩함 `dextrous` (42점)
- 부정: 겁쟁이 `cowardly`, 높은 갈증 `highthirst`, 덤벙됨 `clumsy`, 빠른 대사 `weightloss`, 정독 `slowreader`, 소화불량 `weakstomach`, 얇은 피부 `thinskinned`, 느린 치유 `slowhealer`, 넘치는 존재감 `conspicuous`, 대식가 `heartyappetite`, 질병에 취약함 `pronetoillness`, 평화주의자 `pacifist`, 짧은 시야 `shortsighted`, 밀실 공포증 `claustrophobic` (46점)
- 추천 이유: 기술자는 처음부터 파이프 폭탄과 화염병을 만들 수 있다(레시피 잡지를 찾지 않아도 된다). 원래는 수면 장애를 쓰지만 초보에게는 관리가 어렵다며 짧은 시야와 밀실 공포증으로 바꿨다. 같은 영상에서 직업만 벌목꾼으로 바꾸면 4점이 남는데, 그때는 밀실 공포증을 빼라고 권한다. 피트니스 강사 변형(육상 선수 대신 건강함)도 보여 준다.
- 근거: 자막 03:32(직업), 04:28~06:15(긍정), 06:31~09:42(부정), 10:30~15:30(벌목꾼·소방관·피트니스 강사 변형). 특성표 화면은 보지 못했지만 내레이션만으로 계산한 잔여가 정확히 0이다.
- 검산: −4 + 46 − 42 = **0**

### 8. Pauly_dc (스페인어): 벌목꾼 장기 생존 빌드

- 영상: ✅el MEJOR PERSONAJE de Project Zomboid (Build 42.21)
- URL: https://www.youtube.com/watch?v=nAG9PhLwBXU
- 게시: 2026-10-02 · 조회수 11,270 · 버전: 42.21. 영어·한국어 영상 중 42.21을 명시한 완성 조합이 없어서 참고용으로 넣었다.
- 직업: Leñador(Lumberjack) → `lumberjack` (0, Ax-pert `axeman` 자동 부여)
- 긍정(자막): Hábil(Dextrous) `dextrous`, Insomne(Wakeful) `needslesssleep`, Ojos de gato(Cat's Eyes) `nightvision`, Gimnasta(Gymnast) `gymnast`, Aprendí rápido(Fast Learner) `fastlearner`, Oído Fino(Keen Hearing) `keenhearing`, Atlético(Athletic) `athletic` (35점)
- 부정(설명란 목록): Piel Fina(Thin-skinned) `thinskinned`, Pacifista(Reluctant Fighter) `pacifist`, Propenso a Enfermar(Prone to Illness) `pronetoillness`, Miope(Short Sighted) `shortsighted`, Visible(Conspicuous) `conspicuous`, Sanador Lento(Slow Healer) `slowhealer`, Cobarde(Cowardly) `cowardly`, Estómago Delicado(Weak Stomach) `weakstomach`, Lector Lento(Slow Reader) `slowreader`, Mucha Sed(High Thirst) `highthirst`, Torpe(Clumsy) `clumsy` (36점)
- 추천 이유: 벌목꾼은 근력 1, 도끼 2, 물건관리 1에 도끼 공격 속도 +25%(Ax-pert)와 숲 이동 속도 보너스가 있다. 평화주의자의 전투 XP 감소는 벌목꾼의 도끼 XP 배율과 Fast Learner로 메운다. 초보도 오래 살아남는 것을 목표로 했다.
- 근거: 설명란 "Rasgos de la Build" 목록(부정 11개), 자막 00:18(직업), 05:32~07:30(긍정).
- 검산: 0 + 36 − 35 = **+1**

### 9. Captain Capitalism: 42.20 부정 특성 + 벌목꾼 (부분 확인)

- 영상: Project Zomboid Build 42.20 Best Negative Traits
- URL: https://www.youtube.com/watch?v=21IEJmk6Qrk
- 게시: 2026-09-04 · 조회수 5,232 · 버전: 42.20
- 직업: Lumberjack `lumberjack`. Fire Officer `fireofficer`도 좋은 선택이라고 한다.
- 긍정: Athletic `athletic`, Strong `strong`. Reluctant Fighter와 짝으로 Fast Learner `fastlearner`를 암시한다("6점을 쓰면 모든 스킬 +30%").
- 부정: Short Sighted `shortsighted`, High Thirst `highthirst`, Weak Stomach `weakstomach`, Slow Healer `slowhealer`, Prone to Illness `pronetoillness`, Hearty Appetite `heartyappetite`, Reluctant Fighter `pacifist`, Thin-skinned `thinskinned`. 선택으로 Clumsy `clumsy`, Conspicuous `conspicuous`.
- 추천 이유: 벌목꾼 + Strong이면 근력 10에 도끼 +1과 빠른 도끼 공격이 붙는다. 소방관이면 체력 10, 근력 10이 된다. Prone to Illness는 Outdoorsy(2점)를 같이 고르면 사실상 공짜라고 한다.
- 근거: 자막 00:00~02:10(영상 전체가 2분 11초).
- 검산: 핵심만 고르면 +10(선택 부정까지 넣으면 +16)이 남는다. 나머지 특성은 영상이 정하지 않았다.

### 10. 워킹녹스: 건축 인부 뉴비 빌드 (부분 확인)

- 영상: 좀보이드 42 뉴비 공략 #1 - 직업과 특성부터 초반 할 일까지
- URL: https://www.youtube.com/watch?v=7m61Nw188Zo
- 게시: 2026-08-27 · 조회수 32,064 · 버전: 42(난이도 대유행, 로즈우드 시작)
- 직업: 건축인부 → `constructionworker` (−2)
- 긍정: 튼튼함 → `strong`, 육상 선수 `athletic`, 예민한 청력 `keenhearing`, 용감함 `brave` (30점)
- 부정: "부정적 특성은 이렇게 가면 된대"라고만 말하고 화면에만 보여 줘서 확인하지 못했다. 시작하려면 부정 특성이 최소 32점 필요하다.
- 추천 이유: 건축 인부는 1티어 무기인 긴 둔기와, 어디에나 널려 있는 짧은 둔기 포인트를 줘서 초보가 초반을 버티기 좋다.
- 근거: 자막 01:01~01:20.

## 부록 A: Laughter 영상의 나머지 7개 조합

URL https://www.youtube.com/watch?v=ujrLpaM8HPI · 영상이 말하는 "기본 6종 부정" = `thinskinned`, `pronetoillness`, `slowhealer`, `weakstomach`, `conspicuous`, `slowreader`. 01:21 에는 "inconspicuous"라고 잘못 말하지만 02:20 에 conspicuous로 정정한다. 7개 모두 42.21 비용으로 잔여가 0이다.

| 조합 (자막 시각) | 직업 | 긍정 | 부정 | 이유 요약 |
|---|---|---|---|---|
| Cozy Rancher (00:31) | `rancher` | strong, handy, hiker, formerscout, blacksmith, speeddemon, needslesssleep, nightvision, dextrous, fastlearner | Out of Shape*, hemophobic, pacifist, asthmatic, cowardly, clumsy, thinskinned, pronetoillness, slowhealer, weakstomach, conspicuous, slowreader, shortsighted | 싸우지 않는 목축·건설용이라 전투 관련 부정을 몰아넣는다. **멀티에서는 Slow Reader를 빼라**고 말한다(시간을 빨리 감을 수 없어서). |
| Vehicular Manslaughter (02:39) | `burglar` | strong, athletic, fastlearner, dextrous, speeddemon, hiker | 기본 6종, cowardly, pacifist, asthmatic, hemophobic | 시작부터 차를 직결할 수 있으니 차로 좀비 떼를 친다. 근접을 거의 안 해서 전투 관련 부정은 공짜다. |
| Construction Worker (04:14) | `constructionworker` | athletic, gymnast, fastlearner, dextrous | 기본 6종, highthirst | 가장 단순한 근접·파밍 빌드. 짧은 둔기·긴 둔기·물건관리 시작 레벨이 있다. |
| Extinction Firefighter (05:08) | `fireofficer` | dextrous, fastlearner, gymnast, athletic, brawler | 기본 6종, highthirst, claustrophobic | 익스팅션(모든 좀비가 달리는 설정)의 초반 근접용. 시작 도끼 2레벨이고, XP 배율이 Fast Learner 포함 약 7배다. |
| Long-term Survivor (06:17) | `smither` | dextrous, fastlearner, formerscout, gymnast, target_shooter, nightvision, needslesssleep, inventive, mechanics | 기본 6종, cowardly, claustrophobic, Out of Shape*, feeble | 장기 플레이용. 체력·근력은 운동으로 올릴 수 있으니 낮춰서 점수를 번다. 1년 넘게 할 거면 weak(Puny)·unfit으로 바꿔도 된다고 한다. 자막의 "farmer, scout"는 Former Scout를 잘못 받아 적은 것으로 봤다(이렇게 봐야 잔여가 0). |
| Burger Murderer (08:04) | `burgerflipper` | dextrous, fastlearner, gymnast, graceful, stout, fit | 기본 6종, claustrophobic | 단검(포위 공격)과 은신 위주라 익스팅션에서 유효하다. 직업 비용이 낮아 바꿔 넣을 여유가 많다. |
| Da Vinci Engineer (10:30) | `engineer` | speeddemon, dextrous, inventive, nightvision, mechanics, gymnast, hiker, fastlearner, formerscout, handy, hunter | 기본 6종, hemophobic, disorganized, pacifist, asthmatic, claustrophobic, smoker, cowardly | 거의 모든 스킬에 보너스를 받는 대신 근접이 약하다. 파이프 폭탄으로 마을을 정리한다. |

## 부록 B: 공통 패턴 (1~8번, 채널당 1개씩 8개 조합 기준)

- 부정 특성(8개 조합 중 몇 번 나왔는지): Thin-skinned 8, Conspicuous 8, Prone to Illness 7, Slow Healer 7, Weak Stomach 7, Slow Reader 7, High Thirst 5, Cowardly 4, Reluctant Fighter 4, Short Sighted 4, Claustrophobic 3, Clumsy 3.
  - 이유는 영상마다 거의 같다. 안 물리고 안 다치면 영향이 없고(얇은 피부·느린 치유·질병에 취약함), 상한 음식만 안 먹으면 되고(소화불량), 안경을 쓰면 되고(짧은 시야), 물통을 하나 더 들면 된다(높은 갈증).
- 긍정 특성: Fast Learner 7, Dextrous 6, Organized 5, Speed Demon 4, Strong 4, Keen Hearing 4, Wakeful 4, Gymnast 3, Athletic 3, Cat's Eyes 3.
- 자주 나온 짝:
  - Reluctant Fighter + Fast Learner(FireSpark81, Orbanjo, 단시니, Pauly_dc, Captain Capitalism): 전투 XP 감소를 Fast Learner가 메운다.
  - 피트니스 강사 + Strong + Fit(FireSpark81, 던지기맨): 시작부터 체력 10, 근력 10. 육상 선수는 골초와 함께 고를 수 없어서 Fit을 고르는 쪽이 점수가 남는다.
- 멀티 서버에 넣을 때 주의: Slow Reader는 "싱글에서는 시간을 빨리 감으면 된다"는 이유로 추천되는 경우가 많다(Laughter 01:21, OVERCHARGED EGG 04:40). 멀티에서는 시간을 빨리 감을 수 없다. Laughter는 멀티라면 Slow Reader를 빼라고 하고(01:30), Pauly_dc는 멀티 서버는 보통 독서 속도를 올려 두니 괜찮다고 한다(03:51~04:12). 우리 서버의 독서 속도 설정에 맞춰 안내 문구를 달아야 한다.

## 부록 C: 이름 대응과 데이터 메모

- **`character.json` 에 Out of Shape 가 없다.** B42.21 에도 있는 특성이다(체력 −2, 6점. Laughter 2026-08, ProjectTweak 2026-09-28 의 챕터 "Out of Shape" 26:00). `athletic`·`fit`·`unfit` 의 `exclusive` 에는 `"out of shape"` 문자열로 나오는데 traits 배열에는 항목이 없다. 같은 식으로 `"very underweight"` 도 exclusive 에만 나온다. 데이터를 뽑는 스크립트가 공백이 들어간 id 를 놓친 것으로 보인다.
- 한국어 유튜버 세 명(던지기맨 좀비, 단시니, 워킹녹스)이 Strong 을 **"튼튼함"** 이라고 부른다. `character.json` 의 이름은 "강인함"이다. 던지기맨·단시니 조합은 Strong(10점, 근력 +4)으로 계산해야 포인트와 "근력 10" 설명이 맞는다. 그래서 "튼튼함"을 `strong` 으로 적었다.
- 그 밖의 영상 표기와 json 이름 차이: 빠른 학습 ↔ 현자(`fastlearner`), 잠이 없는/잠이 적음 ↔ 잠이 적음(`needslesssleep`), 민첩한 ↔ 민첩함(`dextrous`), 빠른 대사 ↔ 빠른 신진대사(`weightloss`), 덤벙됨 ↔ 덤벙댐(`clumsy`), 수면 장애 ↔ 수면장애(`insomniac`).
- 단시니 영상은 평화주의자가 "원래 −6이었는데 5로 바뀌었다"고 말한다(08:50). 42.21 json 도 −5다.

## 뺀 영상 (이유)

| 영상 | 게시일 | 뺀 이유 |
|---|---|---|
| Swayed "The Most OVERPOWERED Build" (`_QRLANw8N9U`, 조회수 44.7만) | 2024-09-09 | B41 시기 영상 |
| (구)던지기맨 "한편으로 보는 좀보이드 추천 직업 특성 공략" (`9V3jJd4B8hE`) | 2024-02-25 | B41 |
| MrAtomicDuck "Surviving Your First Week In Build 42 - DAY ONE" (`YTf3qnqc0mM`) | 2024-12-22 | 42.0 unstable 직후. 그 뒤 특성 비용이 바뀌었다 |
| Punkyn "BUILD 42 BEGINNER TRAITS/BUILD GUIDE" (`kk83NdP_Zxg`), Fizxzy "The MOST OP BUILD -BUILD 42" (`ofbz3AtsGSQ`) | 2025-01-30, 2025-04-16 | B42 초기(42.13 이전) |
| 서논 "딸-각 30초 컷 가능! 좀보이드 특성 공략 가이드" (`9nKusJ1uxvM`) | 2025-08-03 | 42.13 이전이고, 특성표가 화면에만 나온다. "2~3년 전에 최적화한 조합"이라는 말로 보아 B41 에서 온 조합이다 |
| 서논 "좀보이드 42빌드 핵심 정리" (`7vWlRW5VmJ4`) | 2026-08-09 | 직업·특성 조합이 없다(전투·맵·제작 변경점 정리) |
| 던지기맨 좀비 "42빌드 뉴비 거점 공략" (`PDBqeYlizWE`) | 2026-08-20 | 커스텀 직업이고 특성은 화면에만 나온다. 6번과 같은 채널이다 |
| 묘토 "좀보이드 42빌드 신규 콘텐츠 전부 부수기" (`GJPyx9nYl-Y`, 조회수 22만) | 2026-09-07 | 피트니스 강사를 고른 이유만 말하고(도끼에 날카로움이 생겨 긴 둔기 메인이 낫다, 01:01), 특성은 화면에만 나온다. 6번과 방향이 같다는 참고 자료로만 쓴다 |
| nitaM "Stop Picking The Wrong Class (Build 42.21 Guide)" (`AGLglWhWI-s`) | 2026-10-05 | 직업 등급표만 있고 특성 조합이 없다 |
| MrAtomicDuck, ProjectTweak, itsbringr, Cambiel, Starz, CzechStag, Laughter(직업편) 의 직업·특성 티어표 | 2026-01~09 | 특성별 평가만 있고 완성된 조합이 없다 |
