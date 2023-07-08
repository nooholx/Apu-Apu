from django.db import models

# Create your models here.


class User(models.Model):
    user_id=models.CharField(max_length=30,unique=True,verbose_name='유저아이디')
    user_email=models.EmailField(max_length=70,unique=True,verbose_name='유저 이메일')
    user_pw=models.CharField(max_length=50,verbose_name='유저비밀번호')
    
    
    def __str__(self):
        return self.user_id


    class Meta:
        
        db_table='user'
        verbose_name='유저'
        verbose_name_plural='유저'
# def __str__(self):는 생성된 객체의 이름을 지정하는 메서드입니다. 이름에서도 알 수 있듯이 str 타입을 리턴합니다. 이것을 등록하지 않으면 User 클래스로 생성된 object를 불러왔을 때 User object (1), User object (2), User object (3)와 같은 이름으로 표시가 되기 때문에 구분하기 어려우니 우리의 편의를 위해 등록해 주도록 합니다.

#return 값으로 self.user_name을 등록했기 때문에 object를 불러오면 object의 user_name 값으로 표시가 되게 됩니다.

#class Meta:는 DB 테이블명을 지정해주는 옵션입니다.

#db_table은 테이블명을 지정하는 옵션입니다.

#verbose_name은 해당 테이블의 닉네임을 말합니다.

#verbose_name_plural를 등록하지 않으면 '유저s'와 같이 복수형으로 표시될 때가 있으니 이것도 verbose_name과 똑같이 적어줍니다.