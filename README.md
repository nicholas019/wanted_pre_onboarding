# wanted_pre_onboarding 백엔드 코스 과제 


## ERD
![원티드 프리온보딩](https://user-images.githubusercontent.com/103249222/185066359-f69dc1b5-f58a-40ed-af76-4bf9cbe745ef.png)


## 기능설명

1. django를 활용하여 개발 진행
  - 4개의 APP 생성 (users, company, job, core) 및 1개 디렉토리(utils) 생성
  - users : 사용자관련 모델 정의
  - company : 회사 관련 모델 정의
  - job : 채용공고와 채용지원 관련하여 모델 및 뷰 정의
  - core : 사측의 채용공고 등록일 및 수정일, 사용자의 채용지원 등록일 및 수정일자를 위한 TimeStamp 모델 정의 
  - utils : access_token에 대한 인증 및 인가를 위한 login_decorator 정의

2. 과제 1 : 채용공고를 등록합니다. ( RecruitmentView > post method )
  - 예시로 나온 회사아이디, 채용 포지션, 채용보상금, 채용내용, 사용기술 등록가능
  - Json형태의 데이터로 전달받아 DB에 저장
  - 회사아이디는 login_decorator를 통해 받은 company_id값을 사용
 
3. 과제 2. 채용공고를 수정합니다. ( RecruitmentView > PATCH method )
  - 등록되어있는 
    
