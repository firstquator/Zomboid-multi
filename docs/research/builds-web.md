# 커뮤니티 추천 캐릭터 조합 조사 (B42, 2026-10-18 확인)

"캐릭터 만들기" 페이지에 넣을 커뮤니티 추천 조합(직업 + 특성)을 웹에서 모은 기록이다.

## 기준과 확인 방법

- 비용 기준: `web/src/data/character.json` (`build: 42.21.0`). 글마다 적힌 비용이 버전에 따라 다르므로, **모든 조합을 42.21 비용으로 다시 계산했다.**
  - 남은 포인트 = 직업 `cost` − 긍정 특성 비용 합 + 부정 특성 비용 절댓값 합. 0 이상이어야 캐릭터를 만들 수 있다.
  - 상호 배타 검사도 했다(`exclusive`). 아래 조합 중 배타 충돌이 있는 것은 없다. 참고로 자주 걸리는 배타: Athletic↔Smoker, Athletic↔Fit, Strong↔Stout, Fast Learner↔Crafty.
- 특성은 `글에 적힌 영문 이름` → `character.json id` 로 적는다. 이름이 정확히 맞지 않는 것은 맨 아래 "이름 매핑 메모"에 이유를 적었다.
- 직업이 주는 특성(Ax-pert → `axeman`, Burglar → `burglar`, Desensitized → `desensitized`)은 직업을 고르면 자동으로 붙으므로 긍정 특성 목록과 포인트 계산에서 뺐다.
- B42 자료만 넣었다. B41 시절 글은 "제외한 자료"에 따로 적었다.

### 조사 한계

- **Reddit 은 확인하지 못했다.** 이번 도구 환경에서 reddit.com 검색·열람이 막혀 있었다(검색 도구가 도메인 차단 오류를 냈고, 직접 요청은 403). 대신 Steam 토론 게시판과 한국 커뮤니티(나무위키, DC 갤러리) 글을 커뮤니티 의견으로 넣었다.
- Game Rant, TheGamer, Destructoid 같은 큰 매체의 "best build" 글은 B41 시절(2022) 글이거나 B42 정식 출시 전 글이었다. 큰 매체 중 B42 빌드를 실제로 적은 곳은 PC Gamer 하나였다.
- 공략 사이트 몇 곳은 자동 생성 글로 보인다(아래 신뢰도 메모 참고). 그래서 42.21 비용으로 다시 계산해서 포인트가 맞는지를 신뢰도 판단에 같이 썼다.

## 요약 표

"글 표기"는 글에 적힌 남은 포인트(없으면 –), "42.21 계산"은 이번에 다시 계산한 남은 포인트다. 음수면 그대로는 만들 수 없다.

| # | 출처 | 날짜 | 버전 | 조합 | 직업 | 긍정 | 부정 | 글 표기 | 42.21 계산 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | pzfans (Best Occupations & Traits) | 날짜 표기 없음 | 42.20.4 | Base Builder | `carpenter` | handy, fastlearner, organized, needslesssleep, dextrous | highthirst, weakstomach, slowreader, shortsighted, slowhealer, cowardly, sundaydriver, heartyappetite, pronetoillness, smoker | 0 | 0 |
| 2 | pzfans (Best Occupations & Traits) | 날짜 표기 없음 | 42.20.4 | Axe Warrior | `lumberjack` | strong, athletic, keenhearing | highthirst, weakstomach, slowreader, shortsighted, slowhealer, sundaydriver, heartyappetite, pronetoillness, needsmoresleep, clumsy, allthumbs, cowardly | 4 | 4 |
| 3 | pzfans (Best Occupations & Traits) | 날짜 표기 없음 | 42.20.4 | Veteran Gunner | `veteran` | stout, fit, keenhearing | highthirst, weakstomach, slowreader, shortsighted, slowhealer, sundaydriver, heartyappetite, pronetoillness, needsmoresleep, clumsy, allthumbs | 2 | 2 |
| 4 | pzfans (Best Beginner Builds) | 날짜 표기 없음 | 42.19 | Axeman | `lumberjack` | fit, stout, brave, outdoorsman | highthirst, smoker, slowreader, weakstomach, shortsighted, heartyappetite, slowhealer | 0 | 0 |
| 5 | PC Gamer | 2025-04-24 수정 | B42 | Brady, the punk lumberjack | `lumberjack` | outdoorsman, fit, strong | claustrophobic, pronetoillness, needsmoresleep, weakstomach, smoker, sundaydriver | – | 0 |
| 6 | PC Gamer | 2025-04-24 수정 | B42 | Maya, the sneaky burglar | `burglar` | dextrous, outdoorsman, inconspicuous | pronetoillness, weakstomach, weightgain, slowreader, smoker, highthirst, (overweight) | – | 1 |
| 7 | The Nerd Stash | 2026-08-05 | B42 Stable | Carpenter | `carpenter` | organized, crafty, whittler | pronetoillness, slowhealer, weakstomach, highthirst | – | 0 |
| 8 | The Nerd Stash | 2026-08-05 | B42 Stable | Burglar | `burglar` | inconspicuous, graceful, needslesssleep, dextrous, speeddemon | pronetoillness, slowhealer, weakstomach, slowreader, pacifist, heartyappetite | – | 0 |
| 9 | The Nerd Stash | 2026-08-05 | B42 Stable | Lumberjack | `lumberjack` | handy, stout, crafty | pronetoillness, slowhealer, weakstomach, heartyappetite, conspicuous | – | 0 |
| 10 | The Nerd Stash | 2026-08-05 | B42 Stable | Rancher | `rancher` | fishing, cook, whittler | pronetoillness, slowhealer, weakstomach | – | 0 |
| 11 | 나무위키 (Project Zomboid/공략) | 2026-10-16 수정 | 42빌드 | 뉴비 추천 | `constructionworker` | athletic, strong, fastlearner, organized, needslesssleep | thinskinned, conspicuous, heartyappetite, claustrophobic, pronetoillness, slowhealer, highthirst, weakstomach, slowreader, + shortsighted 또는 cowardly | – | 0 |
| 12 | Vaagame | 2026-09-22 | 42.20.4 | Balanced beginner | 미지정 | dextrous, outdoorsman, organized, brave | weakstomach, highthirst | – | 0 (커스텀 가정) |
| 13 | Steam 토론 "My B42 traits" (PauloMatix) | 2024-12-20 | 42.0 unstable | 커스텀 | `unemployed` | outdoorsman, gymnast, fit, keenhearing, strong | conspicuous, pronetoillness, pacifist, weakstomach, clumsy, weightgain, slowreader | 0 | 0 |
| 14 | Steam 가이드 (GigaGamer47) | 2025-12-21 수정 | B42 | Axe Sweep | `lumberjack` / `fireofficer` | strong 또는 stout, fit, keenhearing, dextrous, thickskinned | highthirst, smoker, slowreader, shortsighted | – | −19 ~ −23 |
| 15 | Steam 가이드 (Japheth, Burglar) | 2026-09-09 수정 | 42.13~42.20 | Battle Burglar | `burglar` | athletic 또는 fit, baseballplayer 또는 brawler, fastlearner, jogger, strong 또는 stout, needslesssleep | 이미지로만 제공 | 긍정 36점 | 확인 불가 |

나머지 조합(같은 출처의 다른 조합, 포인트가 맞지 않는 조합)은 아래 출처별 상세에 모두 적었다.

## 출처별 상세

### 1. pzfans — Best Beginner Builds (Build 42.19)

- URL: https://pzfans.com/the-best-builds-for-beginners/
- 날짜: 페이지에 작성·수정 날짜 없음. 제목과 본문에 "Build 42.19" 로 적혀 있다.
- 신뢰도 메모: 팬 사이트. 적힌 비용이 42.21 값과 모두 같고, 글이 적은 남은 포인트가 이번 계산과 4개 모두 일치한다. "Athletic 과 Smoker 는 같이 못 고른다", "High Thirst 는 이제 2점" 처럼 B42 변경점을 짚는다.

| 조합 | 직업 | 긍정 | 부정 | 글 표기 / 42.21 계산 |
|---|---|---|---|---|
| Axeman | Lumberjack `lumberjack` (0) | Fit `fit`, Stout `stout`, Brave `brave`, Outdoorsy `outdoorsman` (18) | High Thirst `highthirst`, Smoker `smoker`, Slow Reader `slowreader`, Weak Stomach `weakstomach`, Short Sighted `shortsighted`, Hearty Appetite `heartyappetite`, Slow Healer `slowhealer` (18) | 0 / 0 |
| Ghost | Burglar `burglar` (−6) | Dextrous `dextrous`, Inconspicuous `inconspicuous`, Cat's Eyes `nightvision`, Graceful `graceful` (13) | High Thirst, Smoker, Slow Reader, Weak Stomach, Short Sighted, Slow Healer, Hearty Appetite, Disorganized `disorganized` (24) | 5 / 5 |
| Everyman | Custom Occupation `unemployed` (+8) | Fit, Stout, Fast Learner `fastlearner`, Dextrous, Wakeful `needslesssleep` (23) | High Thirst, Smoker, Slow Reader, Weak Stomach, Short Sighted, Slow Healer, Hearty Appetite (18) | 3 / 3 |
| Construction Worker builder-fighter | Construction Worker `constructionworker` (−2) | Fit, Stout, Handy `handy`, Outdoorsy `outdoorsman` (22) | Axeman 의 부정 7개 + Disorganized (24) | 0 / 0 |

- 추천 이유
  - Axeman: 도끼 레벨과 근력을 들고 시작하고, Fit 으로 지구력을 챙긴다. Athletic 대신 Fit 을 골라서 Smoker 를 고를 수 있다.
  - Ghost: 은신 기술과 차량 열쇠 없이 시동 걸기로 위험한 동네를 싸우지 않고 빠져나간다. Dextrous 로 줍기가 빠르고 Cat's Eyes 로 어두운 밤에 유리하다.
  - Everyman: 체력·근력 기본기에 Fast Learner 를 얹어 어떤 기술 방향이든 무난하다. Wakeful 은 긴 파밍 때 잠 부담을 줄인다.
  - Construction Worker: 초반 망치 계열과 물건관리가 좋고, Handy 가 목공·기지 작업을 돕는다.

### 2. pzfans — Best Occupations & Traits (Verified for Build 42.20.4)

- URL: https://pzfans.com/project-zomboid-the-best-occupations-and-traits/
- 날짜: 날짜 표기 없음. "Verified for Build 42.20.4" 로 적혀 있다.
- 신뢰도 메모: 1번과 같은 사이트. 6개 조합 모두 글의 남은 포인트가 42.21 계산과 일치한다.

| 조합 | 직업 | 긍정 | 부정 | 글 표기 / 42.21 계산 |
|---|---|---|---|---|
| Ghost Burglar | Burglar `burglar` (−6) | Inconspicuous `inconspicuous`, Graceful `graceful`, Cat's Eyes `nightvision`, Dextrous `dextrous` (13) | High Thirst `highthirst`, Weak Stomach `weakstomach`, Slow Reader `slowreader`, Short Sighted `shortsighted`, Slow Healer `slowhealer`, Cowardly `cowardly`, Sunday Driver `sundaydriver`, Smoker `smoker`, Reluctant Fighter `pacifist` (22) | 3 / 3 |
| Axe Warrior | Lumberjack `lumberjack` (0) | Strong `strong`, Athletic `athletic`, Keen Hearing `keenhearing` (26) | High Thirst, Weak Stomach, Slow Reader, Short Sighted, Slow Healer, Sunday Driver, Hearty Appetite `heartyappetite`, Prone to Illness `pronetoillness`, Sleepyhead `needsmoresleep`, Clumsy `clumsy`, All Thumbs `allthumbs`, Cowardly (30) | 4 / 4 |
| Base Builder | Carpenter `carpenter` (−2) | Handy `handy`, Fast Learner `fastlearner`, Organized `organized`, Wakeful `needslesssleep`, Dextrous (23) | High Thirst, Weak Stomach, Slow Reader, Short Sighted, Slow Healer, Cowardly, Sunday Driver, Hearty Appetite, Prone to Illness, Smoker (25) | 0 / 0 |
| Loot Runner | Burglar `burglar` (−6) | Organized, Dextrous, Cat's Eyes, Stout `stout` (15) | High Thirst, Weak Stomach, Slow Reader, Short Sighted, Slow Healer, Cowardly, Sunday Driver, Smoker, Hearty Appetite (21) | 0 / 0 |
| All-Rounder | Custom Occupation `unemployed` (+8) | Stout, Fit `fit`, Fast Learner, Keen Hearing, Wakeful, Dextrous, Outdoorsy `outdoorsman` (31) | High Thirst, Weak Stomach, Slow Reader, Short Sighted, Slow Healer, Cowardly, Sunday Driver, Hearty Appetite, Prone to Illness, Smoker, Conspicuous `conspicuous` (29) | 6 / 6 |
| Veteran Gunner (optional) | Veteran `veteran` (−8, Desensitized 자동) | Stout, Fit, Keen Hearing (18) | High Thirst, Weak Stomach, Slow Reader, Short Sighted, Slow Healer, Sunday Driver, Hearty Appetite, Prone to Illness, Sleepyhead, Clumsy, All Thumbs (28) | 2 / 2 |

- 추천 이유
  - Ghost Burglar: 은신과 차량 시동으로 집 사이를 빠져나가고 여러 마리와 싸움을 피한다.
  - Axe Warrior: 높은 근력·체력으로 도끼 근접전과 청소를 한다. Athletic 을 골랐으므로 Smoker 는 못 넣는다.
  - Base Builder: 목공·물건관리·건설이 빠르고 Organized 로 자재를 더 많이 나른다.
  - Loot Runner: 빠른 옮기기, 더 큰 가방 용량, 밤 파밍과 차량 도주.
  - All-Rounder: 직업 기술 없이 유연한 솔로 시작. Athletic 대신 Fit 이라 Smoker 가능. 남는 6점은 Brawler 나 Organized 에 쓰라고 한다.
  - Veteran Gunner: 총기전 + 공황 억제. Desensitized 때문에 Cowardly, Brave, 광장·밀실 공포증, Fear of Blood 를 고를 수 없다.

### 3. PC Gamer — Project Zomboid traits guide

- URL: https://www.pcgamer.com/best-traits-project-zomboid/
- 작성자 Sarah Richter. 처음 게시 2022-02-11, **최종 수정 2025-04-24**(페이지 메타데이터 `dateModified`).
- 버전: 본문에 "Project Zomboid's build 42 has settled in, and all the fancy new features also came with a traits rework" 라고 적고 B42 기준으로 두 조합을 새로 썼다. 세부 패치 번호는 없다.
- 포인트 표기는 없다. 42.21 비용으로 계산하면 둘 다 0 이상이다.

| 조합 | 직업 | 긍정 | 부정 | 42.21 계산 |
|---|---|---|---|---|
| Brady, the punk lumberjack | Lumberjack `lumberjack` (Ax-Pert 자동) | Outdoorsy `outdoorsman`, Fit `fit`, Strong `strong` (18) | Claustrophobic `claustrophobic`, Prone to Illness `pronetoillness`, Sleepyhead `needsmoresleep`, Weak Stomach `weakstomach`, Smoker `smoker`, Sunday Driver `sundaydriver` (18) | 0 |
| Maya, the sneaky burglar | Burglar `burglar` (Burglar 자동) | Dextrous `dextrous`, Outdoorsy `outdoorsman`, Inconspicuous `inconspicuous` (8) | Prone to Illness, Weak Stomach, Slow Metabolism `weightgain`, Slow Reader `slowreader`, Smoker, High Thirst `highthirst`, High Weight `overweight` (15) | 1 |

- 추천 이유
  - Brady: Ax-pert 로 도끼가 빠르고 세다. 부정 특성으로 번 포인트로 Fit 과 Strong 을 둘 다 산다. Outdoorsy 로 감기와 숲 이동을 챙기고, 밀실 공포증은 넓은 방을 쓰면 버틸 만하다고 본다.
  - Maya: 차량 시동과 자물쇠 덜 부수기로 차를 털고 다닌다. Dextrous 로 빨리 챙기고 Inconspicuous 로 덜 들킨다. 차 안에서 담배를 구하기 쉬워 Smoker 를 감당한다.
- 메모: High Weight 는 character.json 에서 `professionOnly: true`, 비용 0 이다. 직접 고르는 특성이 아니라 체중 설정으로 붙는 상태여서 포인트 계산에 영향이 없다.

### 4. The Nerd Stash — Best Character Builds (Updated for Build 42 Stable)

- URL: https://thenerdstash.com/best-character-builds-in-project-zomboid/
- 작성자 Julio La Pine. 2026-08-05 게시·수정. "Build 42 Stable" 기준이라고 적혀 있다(세부 패치 번호 없음).
- 이 글은 Prone to Illness, Slow Healer, Weak Stomach 를 "거의 모든 조합에 넣는 기본 부정 특성"으로 쓴다.

| 조합 | 직업 | 긍정 | 부정 | 42.21 계산 |
|---|---|---|---|---|
| Carpenter | Carpenter `carpenter` (−2) | Organized `organized` (4), Crafty `crafty` (3), Whittler `whittler` (2) | Prone to Illness `pronetoillness` (4), Slow Healer `slowhealer` (3), Weak Stomach `weakstomach` (2), High Thirst `highthirst` (2) | 0 |
| Park Ranger | Park Ranger `parkranger` (−4) | Former Scout `formerscout` (6), Hiker `hiker` (5), Gardener `gardener` (2) | Prone to Illness (4), Slow Healer (3), Cowardly `cowardly` (2), Weak Stomach (2), Sunday Driver `sundaydriver` (1) | **−5 (부족)** |
| Burglar | Burglar `burglar` (−6) | Inconspicuous `inconspicuous` (4), Graceful `graceful` (4), Wakeful `needslesssleep` (3), Dextrous `dextrous` (2), Speed Demon `speeddemon` (1) | Prone to Illness (4), Slow Healer (3), Weak Stomach (2), Slow Reader `slowreader` (2), Reluctant Fighter `pacifist` (5), Hearty Appetite `heartyappetite` (4) | 0 |
| Lumberjack | Lumberjack `lumberjack` (0) | Handy `handy` (8), Stout `stout` (6), Crafty (3) | Prone to Illness (4), Slow Healer (3), Weak Stomach (2), Hearty Appetite (4), Conspicuous `conspicuous` (4) | 0 |
| Rancher | Rancher `rancher` (0) | Angler `fishing` (4), Keen Cook `cook` (3), Whittler (2) | Prone to Illness (4), Slow Healer (3), Weak Stomach (2) | 0 |

- 추천 이유
  - Carpenter: Organized 로 통나무·판자를 더 나르고, Crafty 로 제작 경험치, Whittler 로 조각을 올린다. 부정 특성은 관리가 쉽고 High Thirst 는 물가에 기지를 두면 된다.
  - Park Ranger: 숲에서 사는 플레이용. Former Scout(낚시·채집·응급처치), Hiker(채집·함정), Gardener(농사). Gardener 대신 Low Thirst 나 Light Eater 도 괜찮다고 한다. 42.21 비용으로는 5점이 모자라므로, 부정 특성을 더 넣거나 Gardener 를 빼고 Hiker 를 바꾸는 식의 조정이 필요하다.
  - Burglar: 들키지 않고 빠르게 털어 나오는 "smash-and-grab". Speed Demon 은 남은 1점을 쓰려고 넣었다.
  - Lumberjack: 기지를 짓고 보강하면서 근접전도 강한 조합. Handy 가 건물 내구도와 목공·조각·물건관리·석공을 올린다.
  - Rancher: 농장 중심. 가장 강한 조합은 아니라고 글이 직접 말한다.

### 5. Steam 가이드 — Project Zomboid (Build 42) Traits and Occupations Tier List (2025 UPDATED)

- URL: https://steamcommunity.com/sharedfiles/filedetails/?id=3625646827
- 작성자 GigaGamer47 외 4명. 게시 2025-12-18, 수정 2025-12-21. 대상 "Build 42"(세부 패치 없음). 방문자 약 2.1만.
- **신뢰도 낮음.** 같은 주에 스페인어·독일어·프랑스어판이 올라왔고, 댓글에 "AI 로 쓴 글", "작성자 플레이 시간 20분" 같은 지적이 있다. 댓글 작성자 한 명이 "Car Before Day 3 를 Burglar 로 만들면 −18점"이라고 지적했고, 이번 계산도 같다. 조합마다 직업이 2~3개 적혀 있고 부정 특성이 모자라 **5개 조합 모두 42.21 비용으로 만들 수 없다.** 다만 멀티용 역할 분담(제작 담당, 의무병)을 따로 적은 유일한 글이라 참고용으로 남긴다.

| 조합 | 직업 | 긍정 | 부정 | 42.21 계산 |
|---|---|---|---|---|
| Solo "Axe Sweep" | Lumberjack `lumberjack` / Fire Officer `fireofficer` | Strong `strong` 또는 Stout `stout`, Fit `fit`, Keen Hearing `keenhearing`, Dextrous `dextrous`, Thick Skinned `thickskinned` | High Thirst `highthirst`, Smoker `smoker`, Slow Reader `slowreader`, Short Sighted `shortsighted` | −19(Stout) / −23(Strong) |
| Solo "Base Online by Week 1" | Carpenter `carpenter` / Construction Worker `constructionworker` | Handy `handy`, Organized `organized`, Fast Learner `fastlearner`, Dextrous, Wakeful `needslesssleep` | High Thirst, Smoker, Short Sighted, Slow Reader | −16 |
| Solo "Car Before Day 3" | Burglar `burglar` / Mechanic `mechanics` | Gymnast `gymnast`, Graceful `graceful`, Inconspicuous `inconspicuous`, Keen Hearing, Dextrous | High Thirst, Smoker, Slow Reader, Short Sighted | −18(Burglar) / −16(Mechanic) |
| Multiplayer "Crafter Core" | Blacksmith `smither` / Tailor `tailor` / Welder `metalworker` | Fast Learner, Organized, Dextrous, Outdoorsy `outdoorsman` | High Thirst, Slow Reader | −16 / −8 / −14 |
| Multiplayer "Medic That Doesn't Die" | Nurse `nurse` / Doctor `doctor` | Fast Learner, Dextrous, Resilient `resilient`, Keen Hearing | High Thirst, Slow Reader | −14 |

- 추천 이유
  - Axe Sweep: 도끼 기술 성장(공속·피해·치명타)과 지구력으로 울타리 틈에서 하나씩 정리한다.
  - Base Online by Week 1: 직업 경험치 배율과 Fast Learner 를 겹쳐 목공을 빨리 올린다.
  - Car Before Day 3: Burglar 는 시동 걸기, Mechanic 은 차를 오래 굴리기.
  - Crafter Core(멀티): 높은 시작 제작 기술로, 다른 사람이 파밍하는 동안 0부터 키우지 않는다.
  - Medic(멀티): Fear of Blood 는 남을 치료할 수 없게 막으므로 절대 넣지 말라고 한다.
- 이 가이드의 S 티어: 긍정 Athletic, Strong, Stout, Fast Learner, Keen Hearing, Dextrous, Organized, Thick Skinned, Handy / 부정 High Thirst, Slow Reader, Short Sighted, Smoker / 직업 Lumberjack, Fire Officer, Carpenter, Burglar, Blacksmith.

### 6. Steam 가이드 — Be The Best Burglar Build 42

- URL: https://steamcommunity.com/sharedfiles/filedetails/?id=3636688167
- 작성자 Japheth. 게시 2026-01-01, 수정 2026-09-09(Steam 은 올해 날짜에 연도를 생략한다). 본문에 42.13, 42.14, 42.17 기준 메모와 "Build 42.20 MP All Skills after 1 month" 기록이 있다.
- 조합별 부정 특성과 일부 조합은 이미지로만 올라와 있어 글자로 확인한 부분만 적는다. 제목의 점수(23~36 Points)는 긍정 특성 총량으로 보인다.

| 조합 | 직업 | 긍정(핵심) | 긍정(추가) | 부정 |
|---|---|---|---|---|
| Battle Burglar (36 Points) | Burglar `burglar` | Athletic `athletic` 또는 Fit `fit`, Baseball Player `baseballplayer` 또는 Brawler `brawler`, Fast Learner `fastlearner`, Runner `jogger`, Strong `strong` 또는 Stout `stout`, Wakeful `needslesssleep` | Brave `brave`, Dextrous `dextrous`, Gymnast `gymnast`, Target Shooter `target_shooter` | 이미지(확인 불가) |
| Burglar Ranger | Burglar `burglar` | Baseball Player, Fast Learner, Fit, Outdoorsy `outdoorsman`, Runner, Sewer `tailor`, Stout, Whittler `whittler` | Dextrous, Herbalist `herbalist`, Wakeful | 이미지(확인 불가) |

- 추천 이유
  - Battle Burglar: Burglar 의 Nimble 에 Runner 를 겹쳐 이동 속도를 최대로 올리고, 끌고 다니며(카이팅) 무리를 처리한다. 개조 야구방망이·쇠지렛대 추천.
  - Burglar Ranger: 채집·조각·재봉으로 자급자족하면서 전투·이동도 챙긴다. 포인트와 준비 시간이 많이 드는 것이 단점.
  - (Burglar Mechanic 은 작성자가 "B41 메타"라고 적어 뺐다.)
- 이 가이드가 "좋은 부정 특성"으로 꼽은 것: Clumsy `clumsy`, Conspicuous `conspicuous`, Hearty Appetite `heartyappetite`, High Thirst `highthirst`, Prone to Illness `pronetoillness`, Reluctant Fighter `pacifist`, Short Sighted `shortsighted`, Slow Healer `slowhealer`, Slow Reader `slowreader`, Thin-skinned `thinskinned`, Weak Stomach `weakstomach`. 피하라는 것: All Thumbs, Disorganized, Restless Sleeper, Short of Breath 등 에너지·전투·이동에 영향을 주는 특성.
- 멀티 관련 주장: Wakeful 옆에 "(Not available in MP)" 라고 적혀 있고, "MP 서버는 포인트와 특성 비용이 다를 수 있다"고 한다. 우리 서버 설정에서 확인이 필요하다(아래 "멀티 서버 메모").

### 7. Steam 토론 — "My B42 traits. Your opinion?"

- URL: https://steamcommunity.com/app/108600/discussions/0/595135824845164656/
- 원글 PauloMatix, 2024-12-20. B42 unstable 첫 공개(42.0) 직후 글이라 당시 비용은 지금과 조금 다르다(예: 글에는 Weak Stomach +3, Reluctant Fighter +4).

| 직업 | 긍정 | 부정 | 글 표기 / 42.21 계산 |
|---|---|---|---|
| Unemployed (Custom Occupation) `unemployed` | Outdoorsy `outdoorsman`, Gymnast `gymnast`, Fit `fit`, Keen Hearing(글에는 "Kean Hearing") `keenhearing`, Strong `strong` | Conspicuous `conspicuous`, Prone to Illness `pronetoillness`, Reluctant Fighter `pacifist`, Weak Stomach `weakstomach`, Clumsy `clumsy`, Slow Metabolism `weightgain`, Slow Reader `slowreader` | 0 / 0 |

- 댓글 의견: Keen Hearing 대신 Wakeful·Dextrous·Cat's Eyes·Organized 를 권하는 사람, "B42 는 밤이 아주 어두워 Cat's Eyes 와 Wakeful 의 가치가 줄었다", "새 액체 시스템 덕에 High Thirst 부담이 줄었다", "근육 피로(muscle strain) 때문에 전투량이 제한되니 Gymnast 는 덜 필요하다"는 의견이 있었다.

### 8. Steam 토론 — "Share your B42 builds here!"

- URL: https://steamcommunity.com/app/108600/discussions/0/595136892797732014/
- 원글 2024-12-31(42.0 unstable 시기). 아래 조합들은 글에 포인트 표기가 없다.

| 작성자 | 직업 | 긍정 | 부정 | 42.21 계산 |
|---|---|---|---|---|
| PK_Ultra ("The Scout", apocalypse+ 샌드박스) | Custom `unemployed` | Cat's Eyes `nightvision`, Dextrous `dextrous`, Outdoorsy `outdoorsman`, Brave `brave`, Eagle Eyed `eagleeyed`, Graceful `graceful`, Inconspicuous `inconspicuous`, Fast Learner `fastlearner`, Fit `fit`, Keen Hearing `keenhearing`, Stout `stout` | Thin-skinned `thinskinned`, Fear of Blood `hemophobic`, Short of Breath `asthmatic`, Hearty Appetite `heartyappetite`, Prone to Illness `pronetoillness`, Reluctant Fighter `pacifist`, Slow Healer `slowhealer`, Weak Stomach `weakstomach`, Fast Metabolism `weightloss`, Slow Reader `slowreader`, High Thirst `highthirst` | 3 |
| FCino | Unemployed `unemployed` | Speedy demon `speeddemon`, fast learner, fast reader `fastreader`, dexterous `dextrous`, outdoorsy, ORGANIZED `organized`, STRONG (?) `strong` | High thirsty `highthirst`, thin skinned, weak stomach, slow healer, prone to illness | 0 (Strong 포함 시) |
| BananaRoch | Construction worker `constructionworker` | Cat's Eyes, Dextrous, Gardener `gardener`, Vehicle knowledge `mechanics`, Angler `fishing`, Brawler `brawler` | Sleepyhead `needsmoresleep`, Slow Reader, Clumsy `clumsy`, Weak stomach, Smoker `smoker`, High thirst, Slow Healer | −4 (42.0 당시 비용 기준 조합) |

- PK_Ultra 는 Slow Reader 대신 Smoker 를 넣어도 된다고 덧붙였다.

### 9. 나무위키 — Project Zomboid/공략

- URL: https://namu.wiki/w/Project%20Zomboid/%EA%B3%B5%EB%9E%B5
- 최근 수정 2026-10-16. 직업·긍정 특성 문단은 "42빌드에서는" 으로 시작한다. 부정 특성·포인트 맞추기 문단에는 빌드 표기가 따로 없다(앞 문단에 "42빌드는 전반적으로 부정 특성의 포인트 제공량이 낮아진 편" 이라는 언급이 있다).
- 한 개의 완성 조합으로 적혀 있지 않고 "추천 직업 + 모든 상황에서 좋은 긍정 + 페널티가 거의 없는 부정 + 포인트 맞추는 법" 으로 나뉘어 있어, 이를 이어 붙여 계산했다.

| 항목 | 내용 |
|---|---|
| 직업 | 뉴비용으로 건축 인부 `constructionworker` 와 피트니스 강사 `fitnessinstructor`. 초보에게는 짧은 둔기가 높은 건축 인부가 가장 낫다고 한다. 목수·DIY 전문가도 안정적. |
| 긍정 | 육상 선수 `athletic` (−10), 튼튼함 `strong` (−10), 현자 `fastlearner`, 정리쟁이 `organized`, 잠이 없는(Wakeful) `needslesssleep` |
| 부정 | 얇은 피부 `thinskinned` (+8), 넘치는 존재감 `conspicuous`, 대식가 `heartyappetite`, 밀실 공포증 `claustrophobic`, 질병에 취약함 `pronetoillness`, 느린 치유 `slowhealer`, 높은 갈증 `highthirst`, 소화불량 `weakstomach`, 정독 `slowreader` |
| 포인트 맞추기 | ① 수면장애 `insomniac`(+6)를 넣고 속도광 `speeddemon`(+1)과 "정비"(+3, 차량 지식 `mechanics` 로 봄)를 추가 ② 수면장애가 부담되면 짧은 시야 `shortsighted` 나 겁쟁이 `cowardly`(각 +2) |
| 피할 부정 | 천식환자, 평화주의자, 피 공포증, 청각장애 |

- 42.21 계산(건축 인부 −2 기준): 긍정 33, 부정 33 → −2. 방법 ②로 +2 → **0**, 방법 ①로 +6 −4 → **0**. 즉 문서의 포인트 맞추기는 건축 인부 기준으로 정확히 맞는다. 피트니스 강사(−6)로 하면 4점이 더 필요하다.
- 이유: 육상 선수·튼튼함은 체력·근력을 크게 올려 초반 난이도를 낮추고, 현자는 체력·근력 외 경험치를, 정리쟁이는 파밍 시간을 줄인다. 부정 특성은 대부분 실질 불이익이 작다고 본다(예: 질병은 좀비화가 어차피 치명적, 갈증은 물병 두 개로 해결).

### 10. Vaagame — Best Traits in Project Zomboid Build 42

- URL: https://vaagame.com/en-US/guides/project-zomboid-build-42-best-traits
- 게시 2026-09-22(메타데이터). 편집팀 명의. "Build 42.20.4" 로 비용을 확인했다고 적혀 있다. 긍정 특성 비용(Dextrous 2, Organized 4, Brave 4, Fast Learner 6, Athletic 10, Strong 10 …)이 42.21 과 같다.
- 직업을 정하지 않은 조합이 많다. 아래 계산은 직업 미지정 → 커스텀(+8)으로 가정했다.

| 조합 | 직업 | 긍정 | 부정 | 42.21 계산 |
|---|---|---|---|---|
| Balanced beginner | 미지정 | Dextrous `dextrous`, Outdoorsy `outdoorsman`, Organized `organized`, Brave `brave` | Weak Stomach `weakstomach`, High Thirst `highthirst` | 0 (커스텀 가정) |
| Melee-focused | Fire Officer `fireofficer` 또는 Lumberjack `lumberjack` | Strong `strong` 또는 Stout `stout`, Fit `fit` 또는 Athletic `athletic`, Dextrous | Weak Stomach, Prone to Illness `pronetoillness` | −8 ~ −16 (부정 특성 추가 필요) |
| Long-term builder | 미지정 | Organized, Fast Learner `fastlearner`, Outdoorsy | High Thirst, Slow Healer `slowhealer` | 1 (커스텀 가정) |

- 이유: Balanced 는 배우기 쉽고 부정 특성이 일상 관리로 해결된다. Melee 는 싸움과 몸 쓰는 플레이용. Long-term 은 부정 특성이 이동·인지에 직접 영향을 주지 않아 오래 짓고 파밍하는 캠페인에 맞는다.

### 11. DC 프로젝트 좀보이드 마이너 갤러리 — "42빌드 특성선택 이렇게도 하네..."

- URL: https://gall.dcinside.com/mgallery/board/view/?id=pzom&no=302533
- 2026-08-12. 해외 유튜버 영상을 요약한 글(영상 링크·제목은 글에 없음).
- 직업 Fitness Trainer `fitnessinstructor` + Fast Learner `fastlearner` + 부정 Slow Reader `slowreader`, Weak Stomach `weakstomach`, Conspicuous `conspicuous`, Slow Healer `slowhealer`, Prone to Illness `pronetoillness`, Thin Skinned `thinskinned`. "체력 10 과 근력 10 을 동시에 확보하는 메타 스타터 빌드"라고 한다.
- 42.21 계산: 적힌 특성만으로는 11점이 남는다. 피트니스 강사(체력 +3, 근력 +1)로 체력·근력 10 을 맞추려면 Athletic + Strong(20점)이 필요한데, 그러면 −9 가 된다. 원 영상에 부정 특성이 더 있었던 것으로 보이며 글만으로는 확인할 수 없다. **부분 정보로만 취급.**
- 부정 특성 이유(글 요약): Slow Reader 는 안경·편한 의자로 상쇄되는 사실상 공짜, Weak Stomach 는 상한 음식만 피하면 됨, Conspicuous 는 좀비 시각에만 영향, Slow Healer 는 부상 관리로 해결, Prone to Illness 는 체온·위생 관리로 예방, Thin Skinned 는 방어구로 줄임.

### 12. build42guide.wiki — Build 42 Traits (Recommended combos)

- URL: https://build42guide.wiki/character-tools/build-42-traits
- 2026-08-04 수정. 42.20.0 에서 비용 재확인이라고 적혀 있다. 긍정 특성 묶음만 있고 부정 특성·직업은 대부분 없다(부분 조합).

| 묶음 | 직업 | 긍정 |
|---|---|---|
| The forge base | Blacksmith `smither` | Blacksmith Knowledge `blacksmith`, Mason `mason`, Crafty `crafty` |
| The homesteader | 미지정 | Handy `handy`, Keen Cook `cook`, Organized `organized` |
| The wilderness start | 미지정 | Bushcrafter `wildernessknowledge`, Whittler `whittler`, Outdoorsy `outdoorsman` |
| The shooter | 미지정 | Target Shooter `target_shooter`, Keen Hearing `keenhearing`, Adrenaline Junkie `adrenalinejunkie` |
| Budget crafting dip | 미지정 | Inventive `inventive`, Artisan `artisan` |

- 메모: Blacksmith 직업은 이미 `blacksmith2`(단조 지식, 0점)를 자동으로 받는다. 같은 효과의 `blacksmith`(6점)를 또 사면 중복일 수 있으니, 페이지에 넣을 때는 이 묶음을 그대로 쓰지 않는 것이 좋다.

## 부분 조합 (완성 빌드가 아닌 참고 자료)

- Steam 가이드 "Occupation Tier List for Project Zomboid B42.13.1" (작성자 Gaius, 게시 2026-01-06): https://steamcommunity.com/sharedfiles/filedetails/?id=3640745623
  - S 티어 직업: Carpenter(큰 기술 보너스 + 남는 포인트, 제작법 다수), Lumberjack(도끼 +2, Ax-pert, 0점이라 부정 특성 불필요). A 티어: Fire Officer, Park Ranger, Police Officer, DIY Expert, Construction Worker.
  - 조합 제안: Burger Flipper `burgerflipper` + Handy `handy` / + Hunter `hunter` 또는 Blacksmith Knowledge `blacksmith`(Chef·Blacksmith 직업보다 낫다) / + Athletic `athletic`(Fitness Instructor 보다 낫다), Police Officer `policeofficer` + Brave `brave`(Veteran 보다 낫다), Veteran `veteran` + Conspicuous `conspicuous` + Weak Stomach `weakstomach` + High Thirst `highthirst`(42.21 계산 0점, −8 을 정확히 메운다), Carpenter `carpenter` + Vehicle Knowledge `mechanics`(Mechanic 보다 낫다).
- BisectHosting "Project Zomboid Best Negative Traits (Build 42)" (2026-07-31, 42.20 언급): https://www.bisecthosting.com/blog/project-zomboid-negative-traits-best-points-build-42
  - 부정 특성 추천 순위: Slow Reader, High Thirst, Short Sighted, Smoker, Conspicuous, Hard of Hearing, Slow Healer, Weak Stomach, Fast Metabolism, Prone to Illness. 적힌 포인트(2·2·2·3·4·4·3·2·2·4)가 42.21 과 같다.
- 한국 유튜브 "좀보이드 42빌드 직업 특성 종결. 딱 '이 2개' 말고는 할 이유가 없습니다": https://www.youtube.com/watch?v=IkldfAON_do
  - 검색 결과 요약상 "42.20 기준 근접 = 피트니스 강사, 총기 = 경찰관". 영상 본문·설명란은 확인하지 못했다.

## 신뢰도 낮음 (참고만)

- Vortex Gaming "Guide to the Best Character Builds for Project Zomboid Build 42" (2025-09-24): https://vortexgaming.io/en/postdetail/550607
  - 영상 내용을 자동 요약한 글이다. "Insomniac"를 긍정 특성으로, "Kitchen Apprentice" 를 직업으로 적는 등 이름이 게임과 다르다. 모든 조합에 Insomniac(→ Wakeful `needslesssleep` 으로 추정) + Athletic, 부정 Slow Reader, Weak Stomach, Slow Healer, Prone to Illness, Conspicuous, Thin-Skinned 를 깔고 직업별로 더한다.
  - Construction Worker: Handy, Cat's Eyes, Gymnast (+ Speed Demon, Amateur Mechanic → `mechanics`, Keen Hearing 또는 Fast Learner) / 부정 Short Sighted, Cowardly, Overweight(→ `overweight`, 직접 선택 불가).
  - Carpenter: Handy, Cat's Eyes, Gymnast, Baseball Player / 부정 Cowardly, Short Sighted, Overweight. 고급형은 Brave + Carver(→ `whittler`), 부정 Feeble(→ `feeble`).
  - Lumberjack/Firefighter: Cat's Eyes, Strong, Handy, Brave / 부정 Short Sighted, Overweight.
  - Kitchen Apprentice(→ `burgerflipper` 로 추정: 짧은 칼날 +1 이 있는 저가 요리 직업): Handy, Gymnast, Keen Hearing / 부정 Cowardly, Overweight.
  - 포인트 표기 없음. Overweight 를 직접 고르는 전제라 42.21 에서는 그대로 만들 수 없다.

## 제외한 자료 (B41 또는 버전 불명확)

| 자료 | 이유 |
|---|---|
| Game Rant "Project Zomboid: The Best Build" (2022-02-24): https://gamerant.com/project-zomboid-best-build/ | B41 글. Smoker +4, "Lightfooted/Nimble/Sneaking" 를 특성처럼 적는 등 B41 기준. |
| Game Rant "The Best Traits, Ranked" (2022-01-24): https://gamerant.com/project-zomboid-best-positive-negative-traits-ranked/ | B41 글. B42 에서 빠진 Lucky 를 추천. |
| Game Rant "7 Best Occupations, Ranked" (2026-08-04 수정): https://gamerant.com/project-zomboid-best-occupations/ | 버전 표기 없음, 특성 조합 없음. 직업 순위만(Carpenter > Burglar > Lumberjack > Veteran > Electrician > Farmer > Mechanic). |
| Destructoid "Best Occupations, ranked" (2024-11-30): https://www.destructoid.com/best-occupations-in-project-zomboid-ranked/ | B42 출시 전 글. 직업 비용도 B41 값(Carpenter +2 등). |
| XGamingServer "Best Traits & Occupations Guide" (2026-06-11): https://xgamingserver.com/blog/project-zomboid-traits-occupations-guide/ | 글 스스로 "포인트는 B41 값"이라고 밝힘(High Thirst −6, Slow Healer −6 등). 조합: Veteran + Keen Hearing/Fast Learner/Iron Gut/Outdoorsman/Cat's Eyes, Fire Officer + Strong(Stout)/Fit, Burglar + Organized/Dextrous/Keen Hearing — **B41 비용 기준**. |
| projectzomboid.wiki "Traits Tier List" (수정일 표기 충돌): https://projectzomboid.wiki/builds/traits-tier-list/ | Smoker −4, High Thirst −6 같은 B41 값과 존재하지 않는 "Fortitude" 특성을 적음. |
| game-rack.com, guides-factory.com, build42guide.wiki 티어 리스트 | 완성 조합 없음(팁·티어만). build42guide.wiki 티어 리스트는 Organized 를 6점으로 적어 42.21(4점)과 다름. |

## 멀티 서버 메모

- 수면 관련 특성: Japheth 가이드는 Wakeful 을 "MP 에서 불가"라고 적었다. 다른 글도 "멀티에서는 서버 설정으로 수면을 끌 수 있다"고 한다. 우리 서버 샌드박스에서 수면을 끄면 Wakeful(3점)·Sleepyhead·Restless Sleeper 는 의미가 없거나 선택이 막힐 수 있으니, 페이지에 넣기 전에 서버 설정을 확인해야 한다. Wakeful 이 들어간 조합: pzfans Everyman·Base Builder·All-Rounder, The Nerd Stash Burglar, 나무위키, Japheth Battle Burglar.
- 멀티 역할 분담: GigaGamer47 가이드만 "제작 담당(Blacksmith/Tailor/Welder + Fast Learner, Organized, Dextrous, Outdoorsy)"과 "의무병(Nurse/Doctor + Fast Learner, Dextrous, Resilient, Keen Hearing)"을 따로 적었다. 포인트가 맞지 않으니 부정 특성을 더 붙여야 한다.
- 의무병 역할이라면 Fear of Blood `hemophobic` 는 피한다(남을 치료할 수 없음 — GigaGamer47, Japheth 둘 다 언급).

## 이름 매핑 메모

글의 이름과 character.json 의 `nameEn` 이 정확히 같지 않은 것들이다.

| 글의 이름 | 매핑한 id (character.json 이름) | 이유 |
|---|---|---|
| Outdoorsy, Outdoorsman | `outdoorsman` (Outdoorsy) | id 는 outdoorsman, 표시 이름은 Outdoorsy. 같은 특성. |
| Cat's Eyes, Cats Eyes, Night Vision | `nightvision` (Cat's Eyes) | 같은 특성. |
| Wakeful, 잠이 없는 | `needslesssleep` (Wakeful, 잠이 적음) | 같은 특성. |
| Reluctant Fighter, Pacifist, 평화주의자 | `pacifist` (Reluctant Fighter) | id 가 옛 이름. |
| Runner | `jogger` (Runner) | id 가 옛 이름. |
| Sewer | `tailor` (Sewer, 재단술) — 특성 | 직업 Tailor(`tailor`, 재봉사)와 id 가 같지만 이 경우는 특성. |
| Angler | `fishing` (Angler) — 특성 | 직업 Fishing Guide(`fisherman`)와 다름. |
| Bushcrafter | `wildernessknowledge` (Bushcrafter) | id 가 옛 이름. |
| Keen Cook | `cook` (3점) | `cook2` 는 요리 직업이 자동으로 받는 0점짜리. |
| Blacksmith Knowledge | `blacksmith` (6점) | `blacksmith2` 는 Blacksmith 직업이 자동으로 받는 0점짜리. |
| Vehicle Knowledge, Amateur Mechanic, 나무위키 "정비(+3)" | `mechanics` (Vehicle Knowledge, 3점) | Amateur Mechanic 은 B41 이름. 나무위키 "정비"는 이름이 다르지만 3점짜리 정비 관련 특성은 차량 지식뿐이라 이것으로 봤다. |
| Speed Demon, "Speedy demon" | `speeddemon` | 오타. |
| Restless Sleeper, 수면장애 | `insomniac` (Restless Sleeper) | id 가 옛 이름. |
| Slow Metabolism / Fast Metabolism | `weightgain` / `weightloss` | id 가 효과 이름. |
| Sleepyhead | `needsmoresleep` | 같은 특성. |
| Fear of Blood / Short of Breath | `hemophobic` / `asthmatic` | 같은 특성. |
| High Weight, Overweight | `overweight` (High Weight) | `professionOnly: true`, 0점. 직접 고르는 특성이 아니다. |
| 튼튼함 (나무위키) | `strong` (Strong, 강인함) | 나무위키 표기 "튼튼함(−10)"은 비용 10·근력 대폭 상승 설명이 Strong 과 같다. character.json 한국어 이름은 "강인함"(건장함 = Stout 6점과 혼동 주의). |
| Kean Hearing | `keenhearing` | 오타. |
| Fire Officer | `fireofficer` (Firefighter) | 같은 직업. |
| Fitness Trainer | `fitnessinstructor` (Fitness Instructor) | 같은 직업. |
| Unemployed, Custom Occupation | `unemployed` (Custom Occupation, +8) | 같은 직업. |
| Insomniac (Vortex, 긍정으로 적음) | `needslesssleep` 로 추정 | 긍정 특성 중 피로를 줄이는 것은 Wakeful 뿐. Vortex 자료는 신뢰도 낮음. |
| Carver (Vortex) | `whittler` 로 추정 | 조각(Carving) 특성은 Whittler. |
| Kitchen Apprentice (Vortex) | `burgerflipper` 로 추정 | 그런 직업은 없다. 설명(짧은 칼날, 요리)과 가장 가까운 저가 직업이 Burger Flipper(요리 2, 물건관리 1, 짧은 칼날 1). Chef(`chef`, −2)일 수도 있다. |
| Ax-pert, Burglar(특성), Desensitized | `axeman`, `burglar`, `desensitized` | 직업이 자동으로 주는 특성. 포인트 계산에서 뺐다. |

## 자주 겹치는 특성

완성 조합을 낸 11개 출처(pzfans, PC Gamer, The Nerd Stash, Steam 가이드 2개, Steam 토론 2개, Vaagame, 나무위키, DC 갤러리, build42guide.wiki)와 그 안의 38개 조합에서 셌다. "출처 수"는 그 특성을 한 번이라도 넣은 출처 개수, "조합 수"는 넣은 조합 개수다. "A 또는 B" 로 적힌 것은 양쪽 모두 한 번씩 셌다. pzfans 두 글은 한 출처로 셌다. Vortex(신뢰도 낮음)와 제외한 B41 자료는 세지 않았다.

### 긍정 특성 (상위)

| 순위 | 특성 | id | 42.21 비용 | 출처 수 (/11) | 조합 수 (/38) |
|---|---|---|---|---|---|
| 1 | Outdoorsy (등산 애호가) | `outdoorsman` | 2 | 8 | 13 |
| 2 | Strong (강인함) | `strong` | 10 | 8 | 8 |
| 3 | Fast Learner (현자) | `fastlearner` | 6 | 7 | 13 |
| 4 | Fit (건강함) | `fit` | 6 | 7 | 12 |
| 5 | Organized (정리쟁이) | `organized` | 4 | 7 | 10 |
| 6 | Dextrous (민첩함) | `dextrous` | 2 | 6 | **18** (조합 수 1위) |
| 7 | Stout (건장함) | `stout` | 6 | 6 | 12 |
| 8 | Keen Hearing (예민한 청력) | `keenhearing` | 6 | 5 | 9 |
| 9 | Wakeful (잠이 적음) | `needslesssleep` | 3 | 5 | 7 |
| 10 | Inconspicuous (부족한 존재감) | `inconspicuous` | 4 | 5 | 6 |
| 11 | Handy (능숙함) | `handy` | 8 | 4 | 5 |
| 12 | Graceful (우아함) | `graceful` | 4 | 4 | 5 |
| 13 | Athletic (육상 선수) | `athletic` | 10 | 4 | 4 |
| 14 | Whittler (조각가) | `whittler` | 2 | 3 | 4 |
| 15 | Brave (용감함) | `brave` | 4 | 3 | 3 |

- 근력 쪽은 Strong(8곳)과 Stout(6곳)로 나뉘고, 체력 쪽은 Fit(7곳)이 Athletic(4곳)보다 많다. Athletic 은 Smoker 와 같이 못 고르고 10점이라, Fit + Smoker 로 가는 조합이 많았다.
- Cat's Eyes 는 2곳(5개 조합)에서만 나왔다. Steam 토론에서 "B42 는 밤과 실내가 아주 어두워 가치가 줄었다"는 의견이 여러 번 나왔다.

### 부정 특성 (상위)

| 순위 | 특성 | id | 42.21 비용 | 출처 수 (/11) | 조합 수 (/38) |
|---|---|---|---|---|---|
| 1 | Weak Stomach (소화불량) | `weakstomach` | −2 | 9 | **26** |
| 2 | Slow Reader (정독) | `slowreader` | −2 | 9 | 23 |
| 3 | Prone to Illness (질병에 취약함) | `pronetoillness` | −4 | 9 | 18 |
| 4 | High Thirst (높은 갈증) | `highthirst` | −2 | 8 | 24 |
| 5 | Slow Healer (느린 치유) | `slowhealer` | −3 | 7 | 22 |
| 6 | Conspicuous (넘치는 존재감) | `conspicuous` | −4 | 6 | 6 |
| 7 | Hearty Appetite (대식가) | `heartyappetite` | −4 | 5 | 14 |
| 8 | Reluctant Fighter (평화주의자) | `pacifist` | −5 | 5 | 5 |
| 9 | Short Sighted (짧은 시야) | `shortsighted` | −2 | 4 | 15 |
| 10 | Smoker (골초) | `smoker` | −3 | 4 | 14 |
| 11 | Clumsy (덤벙댐) | `clumsy` | −2 | 4 | 5 |
| 12 | Thin-skinned (얇은 피부) | `thinskinned` | −8 | 4 | 5 |
| 13 | Sunday Driver (초보 운전) | `sundaydriver` | −1 | 3 | 8 |
| 14 | Cowardly (겁쟁이) | `cowardly` | −2 | 3 | 7 |
| 15 | Sleepyhead (잠꾸러기) | `needsmoresleep` | −4 | 3 | 4 |

- 거의 모든 출처가 공통으로 쓰는 "기본 부정 묶음"은 Weak Stomach + Slow Reader + Prone to Illness + High Thirst + Slow Healer (합 13점)다.
- 피하라고 적힌 것: Short of Breath(나무위키, Japheth), Fear of Blood(나무위키, GigaGamer47 — 의무병일 때), Reluctant Fighter·Deaf(나무위키), All Thumbs·Disorganized·Restless Sleeper(Japheth). 다만 pzfans 는 All Thumbs·Disorganized 를, 나무위키는 Restless Sleeper 를 포인트 맞추기용으로 쓰는 등 출처끼리 의견이 갈린다.
