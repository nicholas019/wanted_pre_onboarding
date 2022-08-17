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
  - utils : access_token에 대한 인증 및 인가를 위한 login_decorator 정의( login_decorator는 User용, company용 두개로 정의)

2. 과제 1 : 채용공고를 등록합니다. ( RecruitmentView > post method )
  - 예시로 나온 회사아이디, 채용 포지션, 채용보상금, 채용내용, 사용기술 등록가능
  - Json형태의 데이터로 전달받아 DB에 저장
  - 회사아이디는 login_decorator를 통해 받은 company_id값을 사용
 
3. 과제 2. 채용공고를 수정합니다. ( RecruitmentView > PATCH method )
  - 등록되어있는 공고문을 path paramater로 받고 login_decorator로 인가된 id값으로 조회하여 가져온 데이터를 update하는 기능

3. 과제 3. 채용공고를 삭제합니다. ( RecruitmentView > delete method )
  - 과제 2와 마찬가지로 삭제할 공고문을 조회하여 삭제하는 기능
    
4. 과제 4-1. 채용공고의 목록을 가져옵니다. ( RecruitmentList > get method )
  - Django ORM의 object.all()을 사용하여 모든 공고를 가져와 List로 만들어 json 형식으로 반환하는 기능
  
5. 과제 4-2. 채용공고 검색기능 구현 ( RecruitmentList > get method )
  - 과제 4-1.의 클레스에 query parameter 로 자료를 받는다면 가져온 List에서 Q객체와 icontains를 활용하여 검색기능 구현
  - 검색 가능 대상 : skill(사용기술), position(채용포지션), compensation(채용보상), company_name(회사명), company_country(회사국가명), company_city(회사 지역명)
 
6. 과제 5. 채용 상세 페이지를 가져옵니다. ( RecruitmentDetailView > get method )
   - 보고싶은 상세페이지는 path parameter로 전달받으면 DB에서 가져와서 딕셔너리형태로 만들어 반환하는 기능 구현

7. 과제 5-1. 회사가올린 다른 채용공고 (id list)
  - 과제 5에 딕셔너리 안에 있는 id 값을 이용하여 Django ORM의 objects.filter를 이용하여 id값과 관련되어있는 모든 글을 가져와 list comprehension 을 이용하여 list로 만들어 
    과제 5의 딕셔너리와 포함하여 반환하는 기능 구현

8. 과제 6. 사용자는 채용공고에 지원합니다.(사용자는 1회만 지원 가능합니다)
  - User과 Recruitment와의 중간테이블인 UserRecruitment를 만들어 지원하는 부분을 구현 
  - 사용자는 1회만 지원이 가능함으로 login_decorator에서 받은 아이디값을 UserRecruitment 테이블에 데이터를 조회하여 존재하지 않을시 지원가능하게 구현
  - UserRecruitment 테이블에 존재할시 AlreadyExists 라는 메세지를 반환
    
    
