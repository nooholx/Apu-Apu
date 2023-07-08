from django import template

register = template.Library()

# 에너테이션 적용
@register.filter 

# 템플릿 필터 함수 sub는 기존 값 value에서 입력으로 받은 값 arg를 빼서 반환함
def sub(value, arg):
    return value - arg
