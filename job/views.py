import json

from django.views          import View
from django.http           import JsonResponse
from django.db.models      import Q

from job.models        import Recruitment, UserRecruitment
from utils.login_decorator import company_login_decorator, user_login_decorator


class RecruitmentView(View):
    @company_login_decorator
    def post(self, request):
        data = json.loads(request.body)
        
        position     = data["position"]
        compensation = data["compensation"]
        content      = data["content"]
        skill        = data["skill"]
        company_id   = request.user.id
        
        Recruitment.objects.create(
            position     = position,
            compensation = compensation,
            content      = content,
            skill        = skill,
            company_id   = company_id
        )
        
        return JsonResponse({"message": "SUCCESS"}, status = 201)

    @company_login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body) 
            recruitment = Recruitment.objects.get(company_id = request.user.id)

            position     = data.get("position", recruitment.position)
            compensation = data.get("compensation", recruitment.compensation)
            content      = data.get("content", recruitment.content)
            skill        = data.get("skill", recruitment.skill)
            
            Recruitment.objects.filter(company_id = request.user.id).update(
                position     = position,
                compensation = compensation,
                content      = content,
                skill        = skill,
            )

            return JsonResponse({"message": "SUCCESS"}, status = 200)

        except Recruitment.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status = 400)
    
    @company_login_decorator
    def delete(self, request, recruitment_id):
        try: 
            Recruitment.objects.get(id = recruitment_id, company_id = request.user.id).delete()
            
            return JsonResponse({"message": "SUCCESS"}, status = 204)
        except Recruitment.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status = 400)

class RecruitmentListView(View):
    def get(self, request):
        search = request.GET.get('search')
        
        recruitments = Recruitment.objects.all().select_related("company")
        
        if search:  
            recruitments= recruitments.filter(
                Q(skill__icontains = search) |\
                Q(position__icontains=search)|\
                Q(compensation__icontains=search)|\
                Q(company__name__icontains=search)|\
                Q(company__country__icontains=search)|\
                Q(company__city__icontains=search) )
                        

        result = [{
            "id"          : recruitment.id,
            "company_name": recruitment.company.name,
            "country"     : recruitment.company.country,
            "city"        : recruitment.company.city,
            "position"    : recruitment.position,
            "compensation": recruitment.compensation,
            "skill"       : recruitment.skill
            }for recruitment in recruitments]

        return JsonResponse({"result" : result}, status =200)    

class RecruitmentDetailView(View):
    def get(self, request, id):
        try:
            recruitment = Recruitment.objects.select_related("company").get(id = id)
            others = Recruitment.objects.filter(company_id = recruitment.company_id)

            result = {
                "id"             : recruitment.id,
                "company_name"   : recruitment.company.name,
                "country"        : recruitment.company.country,
                "city"           : recruitment.company.city,
                "position"       : recruitment.position,
                "compensation"   : recruitment.compensation,
                "content"        : recruitment.content,
                "skill"          : recruitment.skill,
                "otherRecuitment": [other.id for other in others]
            }
            return JsonResponse({"result" : result}, status = 200)
        except Recruitment.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status = 400)

class ApplicationView(View):
    @user_login_decorator
    def post(self, request, recruitment_id):
        if UserRecruitment.objects.filter(user = request.user.id).exists():
            return JsonResponse({"message": "AlreadyExists"}, status = 400)
        
        UserRecruitment.objects.create(
            user_id        = request.user.id,
            recruitment_id = recruitment_id
        )
        return JsonResponse({"message": "SUCCESS"}, status = 200) 
