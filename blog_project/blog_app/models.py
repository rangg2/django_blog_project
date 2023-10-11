from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Board(models.Model):
    user_id=models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, default='전체')
    views = models.IntegerField(default=0)
    # 게시글 임시 관련 데이터베이스 모델 정의 (임시저장 기능 포함)
    title =models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True,null=True)
    publish = models.CharField(max_length=1, default='Y')  # 게시글이 임시 저장인지 여부를 나타내는 필드
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='images/', null=True, default='')

    def __str__(self):
        return self.title
