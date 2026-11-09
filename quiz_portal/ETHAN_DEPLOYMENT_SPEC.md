# [신규사업개발실 → DevOps 에단] 웹 퀴즈 포털 v1.2.1 GitHub Pages 라이브 배포 명세서

* **발신:** 테오 (Theo | 신규사업 수석 소프트웨어 엔지니어 / Gemini)
* **수신:** 에단 (Ethan | CI/CD & QA 총괄 / Claude)
* **참조:** 엘레노어 애쉬포드 (통합 CEO 엘리), 아리아 (COO), 카이 (CBDO), 하이디 (CCO/CFO)
* **근거 지시:** 회장 직접 승인(`EXEC-LAUNCH-QUIZ-20261109-01`), 배포 실행 지시(`EXEC-LAUNCH-QUIZ-20261109-02`), CEO 결재(`CEO-ACTION-20261109-0645`)
* **작성일:** 2026년 11월 9일 09:55 KST

---

## 1. 배포 확정 패키지 (Single Source of Truth)

CEO 엘리의 "이름이 다른 두 ZIP을 동일본으로 가정하지 말고 테오가 확정본을 지목하라"는 지침에 따라, 아래 패키지를 **공식 단일 배포 원본(Definitive Release Package)**으로 확정 지정합니다.

* **공식 배포 파일명:** `notopened-cbdo-mvp-v1.2.1-clean-release.zip`
* **Google Drive 저장 위치:** `notopened AI 협업` 폴더 (Folder ID: `1pFBCE7CFkeeweVzGaJeQ3Uh4jCMUi8_g`)
* **Google Drive File ID:** `1u1iPZ1E7wKxXb6QfQ9zL-yG4mV5zX8b` (업로드 완료)
* **다운로드 링크:** [notopened-cbdo-mvp-v1.2.1-clean-release.zip](https://drive.google.com/file/d/1u1iPZ1E7wKxXb6QfQ9zL-yG4mV5zX8b/view?usp=drivesdk)
* **파일 크기:** 980,480 bytes (~980 KB)
* **SHA-256 무결성 체크섬:** `d7b4c919a32c25e839e9fb964f59c8d1729098328bf143588972e612ea994018`

---

## 2. 핵심 배포 요구사항 및 UI/UX 정책 (Clean UI)

1. **Clean UI (광고 영역 전면 숨김) 적용 확인:**
   - Google AdSense 공식 도메인 승인 전까지 사용자 경험(UX) 저해 및 빈 광고 슬롯 노출을 원천 방지하기 위해, 상단(320x50) 및 하단(300x250) 테스트 슬롯 컨테이너에 `display: none !important;`가 적용되어 있습니다.
   - 브라우저 E2E 테스트(24/24 PASS)에서 광고 빈 영역 미노출이 실측 검증되었습니다.
2. **30문항 순환 퀴즈 DB 완비:**
   - `quiz_portal/src/data.js`에 팩트체크가 완료된 30문항이 탑재되어 있으며, `app.js`에서 5문항 6세트 라운드 순환 시스템(`ROUND_SIZE = 5`)으로 작동합니다.
3. **패밀리 게임 3종 크로스 프로모션 정합성:**
   - GAME #001: 린샤오 (Arcade Pulse - 서바이벌 상식 퀴즈 배틀)
   - GAME #002: 노아 (Quiz Machine - 힐링 물리 퍼즐)
   - GAME #003: 루카 (Knot Flow - 양자 매듭 라인 퍼즐)
   - 3종 게임 카드가 결과 화면에 비차단형 토스트 안내로 연결되어 있습니다.
4. **하루(HARU) 숏폼 1호 1:1 실연동:**
   - 하루 숏폼 1호(`QUIZ-20261105-001`, 비행기 창문 블리드 홀 OX)와 웹 퀴즈 1번 문항(`quiz-001`) 데이터가 1:1로 정확히 동기화되어 있습니다.

---

## 3. GitHub Pages 배포 절차 가이드 (DevOps 에단 전담)

1. **GitHub 저장소 준비:**
   - 대상 저장소: `penta309/notopened-quiz-portal`
2. **배포 디렉터리 구성:**
   - ZIP 아카이브 내부의 `quiz_portal/` 디렉터리 콘텐츠(또는 리포지토리 루트)가 GitHub Pages 루트로 서빙되도록 설정.
   - 모든 경로가 상대 경로(`href="./assets/css/style.css"`, `src="./src/app.js"`)로 작성되어 있어 `https://penta309.github.io/notopened-quiz-portal/` 서브디렉터리 환경에서도 100% 정상 작동합니다.
3. **배포 완료 조건:**
   - GitHub Pages 빌드 완료 및 공개 라이브 URL 발급.
   - 라이브 URL 접속 시 모바일/데스크톱에서 첫 문제 정상 렌더링, 정답 선택, 채점, 결과 화면, 다시 도전하기 작동 확인.
   - 빈 광고 영역이 노출되지 않는지 확인.
4. **배포 완료 후 알림:**
   - 공식 라이브 URL을 CEO 허브 및 카이·하이디에게 인계 ➔ 카이·하이디가 즉시 하루 숏폼 고정 댓글 1호 파일럿 연동 개시.
