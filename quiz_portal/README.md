# notopened 1일 1상식 두뇌 퀴즈 포털 (Web Quiz Portal v1.1.0 RC)

> **notopened AI ENTERPRISE 신규사업개발실 비공개 출시 후보(RC) 패키지**  
> 모바일 퍼스트 경량 반응형 웹 퀴즈 포털 (추가 투입 비용: ₩0 | 테스트 통과율: 100%)

---

## 1. 프로젝트 개요
* **목적:** 하루(Haru)의 6대 SNS 퀴즈 숏폼 트래픽을 다운로드 허들 없는 웹 페이지로 즉시 전환하고, 구글 애드센스(Google AdSense) 웹 광고 및 패밀리 모바일 게임 3종(레오 #001, 노아 #002, 루카 #003) 다운로드 유입 창구로 활용하는 무자본 신규 사업 파이프라인.
* **담당 엔지니어:** 테오 (Theo | 신규사업 수석 소프트웨어 엔지니어 / Gemini)
* **협업:** 카이 (CBDO), 하이디 (CCO·CFO), 엘레노어 애쉬포드 (통합 CEO)
* **기술 스택:** Pure Vanilla HTML5, CSS3, ES6 JavaScript, Schema.org Quiz JSON-LD, Web Share API, Python Selenium E2E Automation.
* **규격:** 스마트폰(320px~480px) 모바일 퍼스트 레이아웃, WCAG 2.1 접근성 및 AdSense 정책 사전 준수.

---

## 2. 프로젝트 디렉터리 구조

```text
notopened-cbdo-mvp-v1.1.0/
├── quiz_portal/
│   ├── index.html                  # 메인 웹 진입점 (Semantic HTML5, Schema.org Quiz Rich Snippet)
│   ├── privacy.html                # 개인정보처리방침 (AdSense 심사 필수 문서, 비수집 원칙 명시)
│   ├── ads.txt                     # AdSense 공인 디지털 판매자 템플릿
│   ├── README.md                   # 프로젝트 및 테스트 가이드 (본 파일)
│   ├── TECHNICAL_HANDOFF_REPORT.md # 카이·하이디·엘리 협업용 공식 기술 인계서
│   ├── src/
│   │   ├── app.js                  # 퀴즈 상태 머신, 채점, 등급 산출, Web Share API 및 이벤트 로직
│   │   ├── data.js                 # 팩트 검증 완료된 5개 상식 퀴즈 문항 데이터 모듈
│   │   └── touchHandler.js         # 모바일 터치 이벤트, 고스트 클릭 방지, 터치 피드백 핸들러
│   ├── assets/
│   │   └── css/
│   │       └── style.css           # 모바일 반응형 스타일시트, .touch-active, :focus-visible, 320px 최적화
│   ├── tests/
│   │   ├── test_quiz_logic.py      # 파이썬 기반 데이터 무결성 및 단위 테스트 (6개 항목)
│   │   ├── test_browser_flow.py    # Headless Chromium 데스크톱 & 모바일 E2E 자동화 테스트 (23개 항목)
│   │   ├── daily_auto_check.py     # 일일 자동 점검 및 CEO 보고용 테이블 생성 스크립트
│   │   └── run_tests.sh            # 단위+스키마+브라우저 통합 원터치 테스트 스크립트
│   └── screenshots/                # E2E 브라우저 실행 검증 스크린샷 5종
├── haru_integration/
│   ├── quiz_schema.json            # 숏폼-웹 공용 JSON 스키마
│   ├── samples_for_haru.json       # 하루 연동용 3개 샘플 데이터
│   ├── test_schema.py              # 스키마 유효성 검증 테스트 (3개 항목)
│   └── haru_sync.py                # 하루 콘텐츠 자동 동기화 및 JS 변환 도구
├── heidi_monetization/
│   └── HEIDI_MONETIZATION_HANDOFF.md # 하이디 수익화·SEO 인계서
└── .github/workflows/
    └── ci.yml                      # GitHub Actions CI 파이프라인 (푸시/PR/일일 크론)
```

---

## 3. 로컬 실행 및 확인 방법

외부 빌드 도구나 유료 CDN 없이 표준 웹 브라우저 또는 로컬 경량 HTTP 서버로 구동됩니다.

```bash
cd quiz_portal
python3 -m http.server 8080
```
브라우저에서 `http://localhost:8080` 접속 시 퀴즈 인터랙션 구동.

---

## 4. 자동화 테스트 수행 방법

### 원터치 통합 테스트 (단위 + 스키마 + 브라우저 E2E)
```bash
bash quiz_portal/tests/run_tests.sh
```

### 일일 자동 점검 리포트 생성
```bash
python3 quiz_portal/tests/daily_auto_check.py
```

---

## 5. 거버넌스 및 운영 통제 원칙
* **비공개 원칙:** 회장 사전 서면 승인 전까지 외부 웹 호스팅 공개 배포 및 도메인 구매 일절 금지.
* **비용 0원 원칙:** 추가 유료 호스팅, 유료 폰트, 유료 CDN 배제, Cloudflare Pages / GitHub Pages 무료 티어 활용.
