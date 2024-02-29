<div align="center">
    <img width="300" alt="Python logo" src="https://www.python.org/static/community_logos/python-logo.png">
</div>

<div align="center">
    <h1>  620-1 Locker </h1>
</div>

## ✒️ : 목차
- ✍️ [프로젝트 개요](#프로젝트-개요)
- 🛠 [기능](#-기능)


## 프로젝트 개요

- 연구실 인원들의 출/퇴근 상태를 체크함으로써 연구실 참여에 동기부여 및 연구 개발 시간을 체크 할 수 있습니다.
- 작품 동작을 위한 개발이 아닌 실제로 적용했을때 발생하는 문제점 및 디버깅을 해보면서 실력을 향상시킨다.

## **🔍 동작영상**

<details>
    <summary><h3>620-1 Locker(23-10-03)</summary>
    <div align="center">
        <img src="https://github.com/KIM2C1/620-1-Locker/assets/119794073/778f3e0a-ea64-4380-be92-621bc7d8786f">
    </div>
</details>

## **🛠 기능**

### CMOS QR코드 스캐너 모듈을 이용하여 사용자 태그 인식
<div align="left">
        <img width="250" src="https://github.com/KIM2C1/MPPT/assets/76949032/8404c6e0-9e5a-4e79-9d32-c94edb51b7d5">
</div>
 - 라즈베리파이4와 USB 연결 및 [USB모드, Add CR, 9600] 바코드 스캐너 설정
 - Key Mapping을 통해 디코드 진행

### 23:50 자동 퇴근처리
 - 퇴근을 찍지 못 하였으면 자동 퇴근 처리 진행

### 매달 데이터 추출
 - 한달치 출퇴근 데이터 엑셀로 추출 진행

### 매달 DB 초기화
 - DB 용량을 고려하여 매달 MySQL 초기화

### 실시간 웹 모니터링
 - 서버 및 포트포워딩을 설정하여 외부에서도 출퇴근 기록 확인 가
