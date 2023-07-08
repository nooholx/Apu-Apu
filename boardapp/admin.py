from django.contrib import admin
from .models import Board

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    # list_display : Admin 목록에 보여질 필드 목록
    list_display = ['b_no', 'b_title', 'b_writer', 'b_date']
    
    # list_display_links : 목록 내에서 링크로 지정할 필드 목록
    list_display_links = ['b_no', 'b_title']
    
    # list_per_page : 페이지 별로 보여질 개수(디폴트 100)
    list_per_page = 10