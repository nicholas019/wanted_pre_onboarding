import jwt

from django.test import TestCase, Client
from django.conf import settings

from company.models import Company
from job.models     import Recruitment, UserRecruitment
from users.models   import User

class RecruitmentViewTest(TestCase):
    def setUp(self):
        Company.objects.bulk_create([
            Company(id = 1, name = "Fake 1 Company", country="Fake 1 Country", city="Fake 1 City"),
            Company(id = 2, name = "Fake 2 Company", country="Fake 2 Country", city="Fake 2 City"),
            Company(id = 3, name = "Fake 3 Company", country="Fake 3 Country", city="Fake 3 City"),
        ])
        User.objects.bulk_create([
            User(id = 1, name = "Fake 1 User"),
            User(id = 2, name = "Fake 2 User"),
            User(id = 3, name = "Fake 3 User"),
        ])
        Recruitment.objects.create(
            id           = 1,
            position     = "Fake Position",
            compensation = 100000,
            content      = "Fake Content",
            skill        = "Fake Skill",
            company_id   = 1
        )

    def tearDown(self):
        Company.objects.all().delete()
        User.objects.all().delete()
        Recruitment.objects.all().delete()
    
    def test_success_recruitment(self):
        client = Client()   

        self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers    = {"HTTP_Authorization":self.token}
        data = {
            "position"    : "fake position",
            "compensation": 1300000,
            "content"     : "fake content",
            "skill"       : "fake skill "
        }

        response = client.post('/recruitment', data, **headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_success_recruitment_update(self):
            client = Client()    

            self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
            headers    = {"HTTP_Authorization":self.token}
            data = {
                "skill"       : "change fake skill "
            }

            response = client.patch('/recruitment/1', data, **headers, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_fail_recruitment_update(self):
            client = Client()    

            self.token = jwt.encode({'id':3}, settings.SECRET_KEY, settings.ALGORITHM)
            headers    = {"HTTP_Authorization":self.token}
            data = {
                "skill"       : "change fake skill "
            }

            response = client.patch('/recruitment/1', data, **headers, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"message": "DoesNotExist"})

    def test_success_recruitment_delete(self):
            client = Client()    

            self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
            headers    = {"HTTP_Authorization":self.token}
            response = client.delete('/recruitment/1', **headers, content_type='application/json',follow=False, secure=False)
            self.assertEqual(response.status_code, 204)

    def test_fail_recruitment_delete(self):
            client = Client()    

            self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
            headers    = {"HTTP_Authorization":self.token}
            response = client.delete('/recruitment/3', **headers, content_type='application/json',follow=False, secure=False)
            self.assertEqual(response.status_code, 400)

class RecruitmentListViewTest(TestCase):
    def setUp(self):
        Company.objects.bulk_create([
            Company(id = 1, name = "Fake 1 Company", country="Fake 1 Country", city="Fake 1 City"),
            Company(id = 2, name = "Fake 2 Company", country="Fake 2 Country", city="Fake 2 City"),
            Company(id = 3, name = "Fake 3 Company", country="Fake 3 Country", city="Fake 3 City"),
        ])
        User.objects.bulk_create([
            User(id = 1, name = "Fake 1 User"),
            User(id = 2, name = "Fake 2 User"),
            User(id = 3, name = "Fake 3 User"),
        ])
        Recruitment.objects.bulk_create([
            Recruitment(
                id           = 1,
                position     = "Fake 1 Position",
                compensation = 100000,
                content      = "Fake 1 Content",
                skill        = "Fake 1 Skill",
                company_id   = 1),
            Recruitment(
                id           = 2,
                position     = "Fake 2 Position",
                compensation = 200000,
                content      = "Fake 2 Content",
                skill        = "Fake 2 Skill",
                company_id   = 2),
            Recruitment(
                id           = 3,
                position     = "Fake 3 Position",
                compensation = 300000,
                content      = "Fake 3 Content",
                skill        = "Fake 3 Skill",
                company_id   = 1),
        ])

    def tearDown(self):
        Company.objects.all().delete()
        User.objects.all().delete()
        Recruitment.objects.all().delete()
    
    def test_success_recruitment_list(self):
        client = Client()   

        response = client.get('/recruitment/list', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": [{
                "id"          : 1,
                "company_name": "Fake 1 Company",
                "country"     : "Fake 1 Country",
                "city"        : "Fake 1 City",
                "position"    : "Fake 1 Position",
                "compensation": 100000,
                "skill"       : "Fake 1 Skill"},
                {
                "id"          : 2,
                "company_name": "Fake 2 Company",
                "country"     : "Fake 2 Country",
                "city"        : "Fake 2 City",
                "position"    : "Fake 2 Position",
                "compensation": 200000,
                "skill"       : "Fake 2 Skill"},
                {
                "id"          : 3,
                "company_name": "Fake 1 Company",
                "country"     : "Fake 1 Country",
                "city"        : "Fake 1 City",
                "position"    : "Fake 3 Position",
                "compensation": 300000,
                "skill"       : "Fake 3 Skill"}
                ]})

    def test_success_recruitment_search(self):
        client = Client()   

        response = client.get('/recruitment/list?search=200000', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": [
                {
                "id"          : 2,
                "company_name": "Fake 2 Company",
                "country"     : "Fake 2 Country",
                "city"        : "Fake 2 City",
                "position"    : "Fake 2 Position",
                "compensation": 200000,
                "skill"       : "Fake 2 Skill"}
                ]})

class RecruitmentDetailViewTest(TestCase):
    def setUp(self):
        Company.objects.bulk_create([
            Company(id = 1, name = "Fake 1 Company", country="Fake 1 Country", city="Fake 1 City"),
            Company(id = 2, name = "Fake 2 Company", country="Fake 2 Country", city="Fake 2 City"),
            Company(id = 3, name = "Fake 3 Company", country="Fake 3 Country", city="Fake 3 City"),
        ])
        User.objects.bulk_create([
            User(id = 1, name = "Fake 1 User"),
            User(id = 2, name = "Fake 2 User"),
        ])
        Recruitment.objects.bulk_create([
            Recruitment(
                id           = 1,
                position     = "Fake 1 Position",
                compensation = 100000,
                content      = "Fake 1 Content",
                skill        = "Fake 1 Skill",
                company_id   = 1),
            Recruitment(
                id           = 2,
                position     = "Fake 2 Position",
                compensation = 200000,
                content      = "Fake 2 Content",
                skill        = "Fake 2 Skill",
                company_id   = 2),
            Recruitment(
                id           = 3,
                position     = "Fake 3 Position",
                compensation = 300000,
                content      = "Fake 3 Content",
                skill        = "Fake 3 Skill",
                company_id   = 1),
        ])

    def tearDown(self):
        Company.objects.all().delete()
        User.objects.all().delete()
        Recruitment.objects.all().delete()
    
    def test_success_recruitment_detail(self):
        client = Client()   

        response = client.get('/recruitment/1/detail', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": {
                "id"             : 1,
                "company_name"   : "Fake 1 Company",
                "country"        : "Fake 1 Country",
                "city"           : "Fake 1 City",
                "position"       : "Fake 1 Position",
                "compensation"   : 100000,
                "content"        : "Fake 1 Content",
                "skill"          : "Fake 1 Skill",
                "otherRecuitment":[1, 3]}})
    
    def test_fail_recruitment_detail(self):
        client = Client()   

        response = client.get('/recruitment/4/detail', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "DoesNotExist"})

class ApplicationViewTest(TestCase):
    def setUp(self):
        Company.objects.bulk_create([
            Company(id = 1, name = "Fake 1 Company", country="Fake 1 Country", city="Fake 1 City"),
            Company(id = 2, name = "Fake 2 Company", country="Fake 2 Country", city="Fake 2 City"),
            Company(id = 3, name = "Fake 3 Company", country="Fake 3 Country", city="Fake 3 City"),
        ])
        User.objects.bulk_create([
            User(id = 1, name = "Fake 1 User"),
            User(id = 2, name = "Fake 2 User"),
        ])
        Recruitment.objects.bulk_create([
            Recruitment(
                id           = 1,
                position     = "Fake 1 Position",
                compensation = 100000,
                content      = "Fake 1 Content",
                skill        = "Fake 1 Skill",
                company_id   = 1),
            Recruitment(
                id           = 2,
                position     = "Fake 2 Position",
                compensation = 200000,
                content      = "Fake 2 Content",
                skill        = "Fake 2 Skill",
                company_id   = 2),
            Recruitment(
                id           = 3,
                position     = "Fake 3 Position",
                compensation = 300000,
                content      = "Fake 3 Content",
                skill        = "Fake 3 Skill",
                company_id   = 1),
        ])

    def tearDown(self):
        Company.objects.all().delete()
        User.objects.all().delete()
        Recruitment.objects.all().delete()
    
    def test_success_application(self):
        client = Client()   

        self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers    = {"HTTP_Authorization":self.token}
        response = client.post('/application/1', **headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_fail_application(self):
        client = Client()   

        UserRecruitment.objects.create(user_id = 1, recruitment_id = 1)
        self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers    = {"HTTP_Authorization":self.token}
        response = client.post('/application/1', **headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "AlreadyExists"})    