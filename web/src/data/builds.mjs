// 캐릭터 만들기 페이지의 추천 조합과 특성 평가.
//
// id 는 web/src/data/character.json(게임 파일에서 추출)의 id 다. 포인트가 모자라거나
// 함께 못 고르는 특성이 섞이면 테스트(tests/character.test.mjs)가 막는다.
// 평가는 우리 서버 설정(독서 0.1, 잠 설정 꺼짐, 스킬 보존 일지)을 반영한다.

export const builds = [
  {
    id: "melee",
    title: "근접 생존형",
    tag: "처음이라면",
    profession: "fireofficer",
    good: ["thickskinned", "keenhearing", "dextrous"],
    bad: ["slowreader", "heartyappetite", "highthirst", "sundaydriver", "smoker", "pronetoillness"],
    why: [
      "소방관은 포인트를 쓰지 않으면서 달리기·근력·체력·도끼가 함께 오른다",
      "두꺼운 피부로 물리거나 긁힐 위험을 줄이고, 예민한 청력으로 다가오는 좀비를 먼저 알아챈다",
      "부정 특성은 생활에 조금 불편한 것만 골라 포인트를 맞췄다",
    ],
  },
  {
    id: "builder",
    title: "건축·생산 담당",
    tag: "기지 만들기",
    profession: "carpenter",
    good: ["fastlearner", "organized", "dextrous"],
    bad: ["slowreader", "heartyappetite", "highthirst", "sundaydriver", "smoker", "weakstomach"],
    why: [
      "목수는 목공예 +4 로 시작해 벽·바리케이드·가구를 바로 만들 수 있다",
      "현자로 경험치를 더 받고, 스킬 보존 일지에 기록해 두면 죽어도 이어 간다",
      "정리쟁이는 상자와 가방에 더 많이 담겨 재료 관리가 편하다",
    ],
  },
  {
    id: "support",
    title: "의료·요리 담당",
    tag: "팀 지원",
    profession: "doctor",
    good: ["cook", "organized", "dextrous", "irongut"],
    bad: ["slowreader", "highthirst", "sundaydriver", "smoker", "heartyappetite"],
    why: [
      "의사는 의료 +6 이라 상처 치료와 봉합을 처음부터 잘한다. 멀티에서는 동료 치료가 큰 역할이다",
      "열정적인 요리사로 요리 레시피를 알고 시작하고, 강철 위장으로 음식 탈이 줄어든다",
      "1점이 남는다. 남아도 그대로 시작할 수 있다",
    ],
  },
  {
    id: "driver",
    title: "차량·정비 담당",
    tag: "이동과 수리",
    profession: "mechanics",
    good: ["keenhearing", "dextrous", "speeddemon"],
    bad: ["slowreader", "heartyappetite", "highthirst", "smoker", "weakstomach"],
    why: [
      "자동차 정비공은 차량정비 +4 와 차량 지식으로 차를 고치고 부품을 다룬다",
      "운전을 맡으므로 초보 운전 대신 속도광을 넣었다",
      "차로 멀리 다니므로 예민한 청력으로 주변 위험을 먼저 알아챈다",
    ],
  },
];

// tag: good(추천) / ok(상황에 따라) / bad(피하기) / server(우리 서버에선 효과 없음) / off(우리 서버에선 고를 수 없음)
export const verdicts = {
  // 긍정
  thickskinned: { tag: "good", note: "물리거나 긁힐 위험이 줄어 죽을 확률 자체가 내려간다" },
  keenhearing: { tag: "good", note: "뒤나 옆에서 다가오는 좀비 소리를 먼저 듣는다" },
  dextrous: { tag: "good", note: "2점으로 물건 옮기기가 빨라지는 가성비 특성" },
  organized: { tag: "good", note: "가방·상자 용량이 늘어 루팅과 정리가 편하다" },
  fastlearner: { tag: "good", note: "경험치가 늘어난다. 스킬 보존 일지로 기록하면 죽어도 남는다" },
  strong: { tag: "ok", note: "근력 +4. 효과는 크지만 10점이라 초반 예산에 부담이 크다" },
  athletic: { tag: "ok", note: "체력 +4. 효과는 크지만 10점이고 골초와 함께 못 고른다" },
  outdoorsman: { tag: "ok", note: "2점으로 비·추위 영향을 덜 받는다" },
  irongut: { tag: "ok", note: "상한 음식으로 탈 날 확률이 줄어든다" },
  lowthirst: { tag: "ok", note: "물을 덜 마셔도 된다. 단수 이후에 편하다" },
  inconspicuous: { tag: "ok", note: "좀비 눈에 덜 띈다" },
  eagleeyed: { tag: "ok", note: "시야가 넓어지고 빨리 확보된다" },
  cook: { tag: "ok", note: "요리 담당이라면 좋다" },
  mechanics: { tag: "ok", note: "차량 담당이라면 좋다. 자동차 정비공은 이미 가지고 시작한다" },
  fastreader: { tag: "server", note: "우리 서버는 책을 거의 바로 읽어서 효과가 거의 없다" },
  needslesssleep: { tag: "off", note: "우리 서버는 잠 설정이 꺼져 있어 고를 수 없다" },
  // 부정
  slowreader: { tag: "good", note: "우리 서버는 독서가 거의 바로 끝나 사실상 공짜 2점이다" },
  sundaydriver: { tag: "good", note: "운전만 느려진다. 운전을 맡지 않으면 부담이 적다" },
  highthirst: { tag: "good", note: "물을 조금 더 자주 마시면 된다" },
  heartyappetite: { tag: "ok", note: "초반에는 음식이 많아 부담이 적다. 나중엔 식량 관리가 필요하다" },
  smoker: { tag: "ok", note: "담배는 흔하다. 피우면 스트레스가 내려간다. 육상 선수와 함께 못 고른다" },
  pronetoillness: { tag: "ok", note: "감기 같은 병에 잘 걸린다. 좀비 감염은 어차피 치료할 수 없다" },
  weakstomach: { tag: "ok", note: "상한 음식만 피하면 된다" },
  pacifist: { tag: "ok", note: "전투 경험치만 줄어든다. 전투를 덜 맡는 사람에게 맞다" },
  cowardly: { tag: "ok", note: "공황에 쉽게 빠진다. 전투를 맡는다면 피한다" },
  allthumbs: { tag: "ok", note: "물건 옮기기가 느리고 걸으면서 제작할 수 없다" },
  clumsy: { tag: "ok", note: "움직일 때 소리가 커져 몰래 다니기 어렵다" },
  illiterate: { tag: "bad", note: "기술 서적을 못 읽는다. 우리 서버는 책이 빨리 읽혀 손해가 특히 크다" },
  deaf: { tag: "bad", note: "소리를 못 들어 다가오는 좀비를 놓친다" },
  hardofhearing: { tag: "bad", note: "들리는 범위가 줄어 기습을 당하기 쉽다" },
  thinskinned: { tag: "bad", note: "물리거나 긁힐 위험이 커진다" },
  weak: { tag: "bad", note: "근력이 크게 떨어져 전투와 운반이 모두 힘들다" },
  feeble: { tag: "bad", note: "근력이 떨어져 들 수 있는 무게가 줄어든다" },
  unfit: { tag: "bad", note: "지구력이 매우 낮아 금방 지친다" },
  asthmatic: { tag: "bad", note: "지구력이 빠르게 떨어진다" },
  slowlearner: { tag: "bad", note: "모든 경험치가 줄어든다" },
  hemophobic: { tag: "bad", note: "다른 사람을 치료할 수 없다. 멀티에서 특히 불리하다" },
  agoraphobic: { tag: "bad", note: "밖에 있으면 점점 공황 상태가 된다" },
  claustrophobic: { tag: "bad", note: "좁은 실내에서 점점 공황 상태가 된다" },
  conspicuous: { tag: "bad", note: "좀비 눈에 더 잘 띈다" },
  disorganized: { tag: "bad", note: "가방·상자 용량이 줄어든다" },
  shortsighted: { tag: "bad", note: "시야가 짧아져 위험을 늦게 본다" },
  weightgain: { tag: "bad", note: "과체중으로 시작해 달리기와 지구력이 떨어진다" },
  weightloss: { tag: "bad", note: "저체중으로 시작해 근력과 지구력이 떨어진다" },
  insomniac: { tag: "off", note: "우리 서버는 잠 설정이 꺼져 있어 고를 수 없다" },
  needsmoresleep: { tag: "off", note: "우리 서버는 잠 설정이 꺼져 있어 고를 수 없다" },
};

// 서버 스폰 지역(42.21 기본 11곳). 어려움 평은 흔히 쓰이는 평가다.
export const spawnTips = [
  "같이 하는 사람과 같은 지역을 고르면 금방 만난다. 호스트가 먼저 들어가서 지역을 알려 주면 좋다",
  "처음이면 리버사이드(Riverside)나 로즈우드(Rosewood)처럼 작은 마을이 흔히 무난하다고 평가된다",
  "멀드로(Muldraugh)와 웨스트포인트(West Point)는 건물이 많아 물자도 많지만 좀비도 많다",
];

// 시작 직후 할 일
export const firstDay = [
  { icon: "tools", title: "무기 먼저", text: "근처 집에서 망치, 쇠지렛대, 야구방망이 같은 근접 무기부터 찾는다" },
  { icon: "backpack-01", title: "가방 챙기기", text: "더플백이나 등산 가방을 메면 들 수 있는 양이 크게 늘어난다" },
  { icon: "droplet", title: "물 받아 두기", text: "단수는 서버 시작 후 0~30일 사이에 온다. 빈 병과 냄비에 미리 물을 채운다" },
  { icon: "bandage", title: "상처는 바로", text: "긁히거나 베이면 바로 소독하고 붕대를 감는다. 물린 상처는 치료할 수 없다" },
  { icon: "book-02", title: "책은 보이는 대로", text: "기술 서적은 거의 바로 읽힌다. 루팅하다 보이면 그 자리에서 읽는다" },
  { icon: "sticky-note-01", title: "스킬 보존 일지", text: "일지를 만들어 수시로 기록해 둔다. 기록해 둔 만큼만 죽은 뒤에 되찾는다" },
];
