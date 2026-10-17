// 문제 해결 목록. id 는 다른 화면에서 #id 로 바로 연결하므로 바꾸지 않는다.
// who: 누가 겪는 문제인지(host, join, all). 화면에서 걸러 볼 때 쓴다.
// 근거와 게임 문구 원문은 docs/research/hosting.md 9절.

export const troubles = [
  {
    id: "version",
    who: "all",
    icon: "game-controller-03",
    q: "버전 불일치로 접속 실패",
    steps: [
      "게임 문구: \"클라이언트 버전와 서버 버전이 일치하지 않습니다\"",
      "Steam 라이브러리 → Project Zomboid 우클릭 → 속성 → 게임 버전 및 베타 → <span class=\"ui\">Default Public Version</span>",
      "Steam 업데이트 완료 후 게임 재실행. 호스트와 참가자의 첫 화면 버전 표기가 같은지 확인",
    ],
  },
  {
    id: "invite",
    who: "join",
    icon: "user-add-01",
    q: "초대가 오지 않거나 수락해도 들어가지지 않음",
    steps: [
      "참가자는 게임 메인 메뉴에 있어야 함. 게임 중이면 \"게임 플레이 중에는 초대를 받을 수 없습니다\"",
      "호스트가 서버에 들어간 상태에서 Esc → 친구 초대 → 해당 친구 초대",
      "서버를 다시 열면 초대 허용 목록이 비므로 매번 다시 초대",
      "호스트와 Steam 친구인지 확인",
    ],
  },
  {
    id: "firewall",
    who: "host",
    icon: "shield-01",
    q: "방화벽 확인 창에서 취소를 누름",
    steps: [
      "Win → '방화벽' 검색 → 'Windows Defender 방화벽을 통해 앱 허용'",
      "'설정 변경' → 'Zulu Platform x64 Architecture'와 'Project Zomboid' 항목의 '개인' 칸 체크",
      "목록에 없으면 '다른 앱 허용' → 게임 폴더의 jre64\\bin\\java.exe 추가",
    ],
  },
  {
    id: "download",
    who: "all",
    icon: "cloud-download",
    q: "모드 다운로드가 진행되지 않음",
    steps: [
      "참가자: 게임 종료 → Steam 완전 종료(트레이 아이콘 → 나가기) → 재실행 후 다시 초대 수락",
      "호스트: 서버 시작 화면에서 멈추면 중단 → 다시 시작. 다른 모드에서 또 멈추면 반복",
      "호스트: Zomboid\\coop-console.txt 끝부분에 0/0 bytes로 남은 모드가 있는지 확인",
    ],
  },
  {
    id: "workshop-mismatch",
    who: "all",
    icon: "refresh",
    q: "창작마당 아이템 버전 불일치 오류",
    steps: [
      "게임 문구: \"창작마당 아이템의 버전이 서버와 다릅니다\". 모드가 방금 업데이트된 경우 발생",
      "호스트: 게임을 완전히 나갔다가 서버 만들기로 다시 시작 (서버가 새 버전을 받음)",
      "참가자: Steam 완전 종료 후 재실행, Steam 다운로드가 끝난 뒤 접속",
      "그래도 안 되면 해당 모드 구독 해지 → 재구독",
    ],
  },
  {
    id: "no-preset",
    who: "host",
    icon: "folder-open",
    q: "서버 이름 목록에 zomboid-multi가 없음",
    steps: [
      "설치 명령이 '설치 완료'로 끝났는지 확인. 빨간 오류가 있었다면 그 화면을 캡처해 공유",
      "게임이 켜진 상태에서 실행했다면 게임을 끄고 다시 실행",
      "C:\\Users\\(사용자 이름)\\Zomboid\\Server\\zomboid-multi.ini 파일이 있는지 확인",
    ],
  },
  {
    id: "server-stops",
    who: "host",
    icon: "stop-circle",
    q: "서버가 시작하자마자 꺼짐",
    steps: [
      "서버 메모리 설정이 PC 여유 메모리보다 크면 실패할 수 있음. 5GB로 낮춰 다시 시작",
      "Zomboid\\Server\\zomboid-multi_SandboxVars.lua를 지우고 설치 명령을 다시 실행 (파일이 깨지면 서버가 바로 종료됨)",
      "로그 위치: Zomboid\\coop-console.txt. 오류 화면과 함께 공유하면 원인을 찾기 쉬움",
    ],
  },
  {
    id: "powershell",
    who: "host",
    icon: "command-line",
    q: "PowerShell 명령 실행 시 빨간 오류",
    steps: [
      "명령 앞뒤에 다른 글자가 섞이지 않았는지 확인. 사이트의 복사 버튼 사용 권장",
      "회사·학교 PC처럼 관리되는 PC는 실행이 막혀 있을 수 있음. 모드 목록 화면의 '수동 설정' 사용",
    ],
  },
  {
    id: "korean-chat",
    who: "all",
    icon: "keyboard",
    q: "채팅 한글 입력 불가 / 캐릭터가 움직이지 않음",
    steps: [
      "윈도우 입력기를 영문 상태로 유지. 한글 상태에서는 이동 키가 입력되지 않음",
      "채팅창에서 \\ 키로 한/영 전환. 한글 입력 모드가 게임 안에서 글자를 조합",
    ],
  },
  {
    id: "ip-join",
    who: "join",
    icon: "router-01",
    q: "Steam 초대 대신 IP로 접속하고 싶음",
    steps: [
      "호스트 공유기에서 UDP 16261–16262 포트포워드 필요 (Steam 초대는 필요 없음)",
      "참가자: 여러 명이서 하기 → 서버 추가 → 호스트 공인 IP, 포트 16261",
      "IP로 들어와도 호스트가 친구 초대 창에서 해당 친구를 초대 또는 수락해 두어야 함",
    ],
  },
  {
    id: "backup",
    who: "host",
    icon: "archive",
    q: "월드 백업과 복구",
    steps: [
      "자동 백업: 서버를 켤 때마다 Zomboid\\backups\\startup에 최근 5개 저장",
      "수동 백업: 게임을 끈 상태에서 C:\\Users\\(사용자 이름)\\Zomboid 폴더 전체 압축",
      "월드만 옮길 때: Zomboid\\Saves\\Multiplayer\\zomboid-multi 폴더 복사 후 새 PC에서 설치 명령 실행",
    ],
  },
];
