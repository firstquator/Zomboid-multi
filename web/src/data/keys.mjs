// 플레이 팁 페이지의 단축키 가이드.
//
// 기본 키: 42.21 media/lua/shared/keyBinding.lua (탐색 모드는 client/Foraging/ISSearchManager.lua)
// 이름(name): Translate/KO/UI.json 의 UI_optionscreen_binding_* 그대로. 게임 설정 → 키 설정 화면과 같다.
// 인벤토리 클릭 동작: client/ISUI/ISInventoryPane.lua (onMouseDown, onMouseDoubleClick, Ctrl+A)
// 배속(F2~F6)과 PVP 안전 모드(G)는 우리 서버에서 쓰지 않아 뺐다.

// 키보드 그림과 목록에서 색으로 나누는 갈래. 순서대로 걸러 보기 버튼이 된다.
export const keyGroups = [
  { id: "move", label: "이동", icon: "running-shoes" },
  { id: "combat", label: "전투", icon: "sword-01" },
  { id: "item", label: "아이템", icon: "backpack-01" },
  { id: "ui", label: "창 열기", icon: "layout-01" },
  { id: "vehicle", label: "차량", icon: "steering" },
  { id: "chat", label: "채팅", icon: "bubble-chat" },
];

// keys: 키보드 그림의 키 이름. LMB/RMB/Wheel 은 마우스. when: 그 상황에서만 쓰는 키.
// alt: 어느 키든 된다(우클릭 또는 Ctrl). range: 첫 키~끝 키로 줄여 보여 준다.
export const keybinds = [
  // 이동
  { keys: ["W", "A", "S", "D"], name: "이동", group: "move", tip: "앞·뒤·왼쪽·오른쪽으로 걷는다" },
  { keys: ["Shift"], name: "달리기", group: "move", tip: "빨리 움직인다. 지구력이 조금씩 닳는다" },
  { keys: ["Alt"], name: "전력질주", group: "move", tip: "가장 빠르지만 지구력이 빨리 닳는다. 도망칠 때만" },
  { keys: ["C"], name: "웅크리기", group: "move", tip: "소리를 줄이고 몰래 움직인다" },
  { keys: ["E"], name: "상호작용", group: "move", tip: "문·창문 열고 닫기, 차 타고 내리기처럼 앞에 있는 물건을 쓴다" },
  { keys: ["Y"], name: "이곳으로 걸어가기", group: "move", tip: "마우스가 가리키는 곳까지 알아서 걸어간다" },
  { keys: ["End"], name: "탐색 모드 전환", group: "move", tip: "주변의 먹을거리·약초·재료를 찾는 채집 모드를 켜고 끈다" },
  { keys: ["Esc"], name: "취소 행동", group: "move", tip: "하던 행동을 멈춘다. 행동 중이 아니면 주 메뉴가 열린다" },

  // 전투
  { keys: ["RMB", "Ctrl"], alt: true, name: "조준하기", group: "combat", tip: "누르고 있는 동안 무기를 든다. 이 상태에서 좌클릭해야 공격한다" },
  { keys: ["LMB"], name: "공격/선택", group: "combat", tip: "조준한 채로 누르면 공격한다" },
  { keys: ["Space"], name: "밀치기/밟기", group: "combat", tip: "다가온 좀비를 밀쳐 넘어뜨리고, 쓰러진 좀비는 밟는다" },
  { keys: ["Alt"], name: "수동으로 바닥 공격", group: "combat", tip: "누른 채 공격하면 바닥에 쓰러진 좀비를 친다" },
  { keys: ["R"], name: "재장전", group: "combat", tip: "총에 탄창이나 총알을 넣는다" },
  { keys: ["X"], name: "총기 장전 손잡이 당김", group: "combat", tip: "총알을 약실에 넣는다. 장전 후 쏘기 전에" },
  { keys: ["R"], name: "무기 날 갈기", group: "combat", tip: "숫돌이 있으면 날붙이 무기를 간다" },

  // 아이템
  { keys: ["1", "2", "3", "4", "5", "6", "7", "8"], range: true, name: "단축키 칸 1~8", group: "item", tip: "허리·등에 매단 무기와 도구를 바로 손에 든다. 화면 아래 칸 순서" },
  { keys: ["F"], name: "조명 아이템 장착/켬/끔", group: "item", tip: "손전등을 들고 켠다. B42는 실내가 어두워서 자주 쓴다" },
  { keys: ["R"], name: "건축물 회전", group: "item", tip: "가구를 놓거나 지을 때 방향을 돌린다", when: "건축 중" },

  // 창 열기
  { keys: ["I"], name: "소지품 창 전환", group: "ui", tip: "내 가방과 주변 상자 창" },
  { keys: ["H"], name: "상태 창 전환", group: "ui", tip: "다친 곳을 보고 치료한다" },
  { keys: ["M"], name: "지도 열고 닫기", group: "ui", tip: "우리 서버는 같이 하는 사람 위치도 보인다" },
  { keys: ["B"], name: "제작 창 전환", group: "ui", tip: "만들 수 있는 것과 필요한 재료를 본다" },
  { keys: ["L"], name: "기술 창 전환", group: "ui", tip: "기술 레벨과 경험치를 본다" },
  { keys: ["J"], name: "정보 창 전환", group: "ui", tip: "캐릭터 정보, 특성, 몸 상태" },
  { keys: ["P"], name: "옷 방어도 창 전환", group: "ui", tip: "입은 옷이 부위별로 얼마나 막아 주는지 본다" },
  { keys: ["F1"], name: "생존 지침서 전환", group: "ui", tip: "게임에 들어 있는 그림 설명서" },
  { keys: ["=", "-", "Wheel"], alt: true, name: "화면 확대·축소", group: "ui", tip: "가까이 보거나 멀리 본다. 마우스 휠로도 된다" },
  { keys: ["F10"], name: "스크린샷 찍기", group: "ui", tip: "Zomboid\\Screenshots 폴더에 저장된다" },

  // 차량
  { keys: ["E"], name: "타기·내리기", group: "vehicle", tip: "차 문 옆에서 누른다", when: "차 옆에서" },
  { keys: ["N"], name: "시동 걸기", group: "vehicle", tip: "열쇠가 있거나 배선을 땄으면 시동이 걸린다", when: "운전석에서" },
  { keys: ["W", "S", "A", "D"], name: "운전", group: "vehicle", tip: "W 앞으로, A·D 방향. S 는 달리는 중엔 브레이크, 멈춘 뒤엔 후진", when: "운전석에서" },
  { keys: ["Space"], name: "브레이크", group: "vehicle", when: "운전 중" },
  { keys: ["Shift"], name: "정속 주행", group: "vehicle", tip: "Shift+W 로 켜고 설정 속도를 올리고, Shift+S 로 내린다. 브레이크를 밟으면 꺼진다", when: "운전 중" },
  { keys: ["F"], name: "전조등", group: "vehicle", when: "차 안에서" },
  { keys: ["Q"], name: "경적", group: "vehicle", tip: "운전자만 울린다(동승자가 누르면 외치기). 150칸 안의 좀비가 온다", when: "운전석에서" },
  { keys: ["V"], name: "차량 메뉴", group: "vehicle", tip: "원형 메뉴. 차 안에선 시동·배선 따기·문 잠그기, 차 밖에선 정비·주유·창문 부수기", when: "차 안·옆에서" },
  { keys: ["U"], name: "차량 정보", group: "vehicle", tip: "부품 상태를 보는 정비 화면. 차를 세워야 열린다", when: "차 안·옆에서" },
  { keys: ["O"], name: "히터/에어컨", group: "vehicle", when: "차 안에서" },
  { keys: ["Z"], name: "좌석 이동", group: "vehicle", when: "차 안에서" },

  // 채팅
  { keys: ["T", "Enter"], alt: true, name: "대화 창", group: "chat", tip: "채팅을 입력한다" },
  { keys: ["Tab"], name: "대화 표시 전환", group: "chat", tip: "대화 탭을 바꾼다", when: "채팅 중" },
  { keys: ["Q"], name: "외치기 · 감정표현", group: "chat", tip: "짧게 누르면 외치고(좀비가 온다), 길게 누르면 감정표현 원형 창이 열린다" },
  { keys: ["\\"], name: "한/영 전환", group: "chat", tip: "한글 채팅 입력 개선 모드의 키. 윈도우 입력기는 영문으로 두고 채팅창에서 바꾼다", mod: true },
];

// 처음에 꼭 외울 것. keys 는 keybinds 의 키와 같아야 한다(테스트가 확인).
// combo: 앞의 키를 누른 채 뒤의 키. double: 두 번 누르기.
export const essentials = [
  { keys: ["E"], title: "상호작용", text: "문 열기, 차 타기, 물건 쓰기는 대부분 E" },
  { keys: ["RMB", "LMB"], combo: true, title: "조준 후 공격", text: "우클릭을 누른 채 좌클릭. 우클릭 없이 누르면 공격하지 않는다" },
  { keys: ["Space"], title: "밀치기·밟기", text: "붙은 좀비를 밀쳐 넘어뜨리고 쓰러지면 밟는다" },
  { keys: ["Shift"], title: "달리기", text: "Alt 는 전력질주. 둘 다 지구력이 닳는다" },
  { keys: ["C"], title: "웅크리기", text: "몰래 지나가거나 집에 조용히 들어갈 때" },
  { keys: ["I"], title: "소지품", text: "가방과 주변 상자를 한 번에 연다" },
  { keys: ["H"], title: "상태 창", text: "다치면 바로 열어서 붕대를 감는다" },
  { keys: ["M"], title: "지도", text: "같이 하는 사람 위치도 보인다" },
];

// 인벤토리 창에서 쓰는 마우스 동작
export const inventoryMoves = [
  { keys: ["RMB"], title: "할 수 있는 행동 보기", text: "아이템이나 물건에 우클릭하면 먹기, 읽기, 입기, 열기 같은 메뉴가 나온다" },
  { keys: ["LMB"], double: true, title: "더블클릭", text: "상자·바닥의 아이템은 내 가방으로 가져오고, 내 가방의 무기·옷·가방은 손에 들거나 입거나 멘다" },
  { keys: ["Drag"], title: "끌어서 옮기기", text: "아이템을 다른 창이나 상자 버튼 위로 끌어다 놓는다" },
  { keys: ["Ctrl", "LMB"], combo: true, title: "여러 개 고르기", text: "Ctrl 을 누른 채 클릭한 것만 골라진다. 고른 뒤 한 번에 끌어 옮긴다" },
  { keys: ["Shift", "LMB"], combo: true, title: "범위로 고르기", text: "처음 고른 것부터 클릭한 것까지 모두 골라진다" },
  { keys: ["Ctrl", "A"], combo: true, title: "모두 고르기", text: "마우스가 올라간 창의 아이템을 전부 고른다" },
];

// 키보드 그림의 배열. w 는 키 너비(1 = 보통 키). gap 은 빈칸.
export const keyboardRows = [
  [{ k: "Esc" }, { gap: 0.6 }, { k: "F1" }, { k: "F2" }, { k: "F3" }, { k: "F4" }, { gap: 0.3 }, { k: "F5" }, { k: "F6" }, { k: "F7" }, { k: "F8" }, { gap: 0.3 }, { k: "F9" }, { k: "F10" }, { k: "F11" }, { k: "F12" }, { gap: 0.4 }, { k: "End" }],
  [{ k: "`" }, { k: "1" }, { k: "2" }, { k: "3" }, { k: "4" }, { k: "5" }, { k: "6" }, { k: "7" }, { k: "8" }, { k: "9" }, { k: "0" }, { k: "-" }, { k: "=" }, { k: "Back", w: 2 }],
  [{ k: "Tab", w: 1.5 }, { k: "Q" }, { k: "W" }, { k: "E" }, { k: "R" }, { k: "T" }, { k: "Y" }, { k: "U" }, { k: "I" }, { k: "O" }, { k: "P" }, { k: "[" }, { k: "]" }, { k: "\\", w: 1.5 }],
  [{ k: "Caps", w: 1.75 }, { k: "A" }, { k: "S" }, { k: "D" }, { k: "F" }, { k: "G" }, { k: "H" }, { k: "J" }, { k: "K" }, { k: "L" }, { k: ";" }, { k: "'" }, { k: "Enter", w: 2.25 }],
  [{ k: "Shift", w: 2.25 }, { k: "Z" }, { k: "X" }, { k: "C" }, { k: "V" }, { k: "B" }, { k: "N" }, { k: "M" }, { k: "," }, { k: "." }, { k: "/" }, { k: "RShift", label: "Shift", w: 2.75 }],
  [{ k: "Ctrl", w: 1.5 }, { k: "Win", w: 1.25 }, { k: "Alt", w: 1.25 }, { k: "Space", w: 6.25 }, { k: "RAlt", label: "한/영", w: 1.25 }, { k: "Menu", w: 1.25 }, { k: "RCtrl", label: "한자", w: 1.5 }],
];

// 화면에 보여 줄 키 이름
export const keyLabel = (k) =>
  ({ LMB: "좌클릭", RMB: "우클릭", Wheel: "휠", Drag: "끌기", Space: "Space", Back: "←" })[k] ?? k;
