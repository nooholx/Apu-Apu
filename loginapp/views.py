from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib import messages
from django.db.utils import IntegrityError

# Create your views here.

def login1(request):
    return render(request,
                "loginapp/indexkakaonaver.html",
                {})
    


# 로그인 만들기 
def MemberInsert(request):
    
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
    
    rs = mem.setMemberInsert(mem_id, mem_pass, mem_name, mem_email )

    if mem_id == '' :
        msg="""
            <script type='text/javascript'>
                alert('아이디는 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 
    
    if mem_pass == '':
        msg="""
            <script type='text/javascript'>
                alert('비밀번호는 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """        
        return HttpResponse(msg) 


    if mem_email == '':
        msg="""
            <script type='text/javascript'>
                alert('이메일은 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """               
        return HttpResponse(msg)        
    
    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('아이디 비밀번호를 확인하세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
        
        
    msg="""
        <script type='text/javascript'>
            alert('회원가입이 완료되었습니다.');
            location.href='loginapp/memberup.html';
        </script>
    """
    return HttpResponse(msg)



# 로그아웃 
def login_logout(request):
    return render(request,
                "loginapp/memberup.html",
                {})
    
def login(request):
    try :
        if request.method == "POST" :
            mem_id = request.POST["mem_id"]
            mem_pass = request.POST["mem_pass"]
                    
        elif request.method == "GET" :        
            mem_id = request.GET["mem_id"]
            mem_pass = request.GET["mem_pass"]
            
    except :
        url = "경로"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    ## DB
    dict_col = mem.getLogin(mem_id, mem_pass)
# return HttpResponse(dict_col["rs"])
    # return HttpResponse(mem_pass)
    
    ### 성공여부
    if dict_col["rs"] == "no" :
        msg="""
            <script type="text/javascript">
                alert('아이디 또는 비밀번호가 일치하지 않습니다.');
                history.go(-1);
            </script>
        """
        
        return HttpResponse(msg)
        
    request.session["ses_mem_id"]=mem_id
    request.session["ses_mem_name"] = dict_col["mem_name"]
    
    return render(request,
                "경로",
                    {})
    
def logout(request):
    if request.session.get("ses_mem_id"):
        ### 세션 정보 비우기
        request.session.flush()
        
        msg="""
            <script type='text/javascript'>
                alert('로그아웃 되었습니다.');
                location.href ='/index';
            </script>
        """
    else :
        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요!!!');
                location.href ='/index';
            </script>
        """
    return HttpResponse(msg)

def mypage(request):
    try :
        dict_col = mem.getmypage(request.session["ses_mem_id"])
                
    except :
        url = "경로"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    return render(request,
            "경로",
            {"dict_col":dict_col})

    
    

# def signup(request):
    # return render(request,
                # "loginapp/memberup.html",
                # {})
    
    
# def signup(request):
#     if request.method == 'POST':
#         if request.POST["password1"] == request.POST["password2"]:
#             try:
#                 user = User.objects.create_user(username=request.POST["username"],
#                                                password=request.POST["password1"],
#                                                email=request.POST["email"])
                
#             except IntegrityError:
#                 return render(request,"loginapp/memberup.html",{"date":"id_overlap"})
#             messages.info(request,"회원가입이 완료되었습니다.!")
#             auth.login(request,user)
#             return redirect("loginapp/memberup.html")    
                    
#     else : 
#         return render(request ,"loginapp/memberup.html")        