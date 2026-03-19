from django.db import models

class Blog(models.Model):
    CATAGORY_CHOICES = (
        ('', '선택하세요'),
        ('free', '자유'),
        ('travel', '여행'),
        ('food', '음식'),
        ('life', '일상'),
    )

    category = models.CharField('카테고리', max_length=20, choices=CATAGORY_CHOICES, default='')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')                            # 본문은 길이가 길 수 있기 때문에 TextField로 설정
    # author = models.CharField(max_length=50) 추후 업데이트
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

# 블로그에 필요한 것
# 제목, 내용, 작성자, 작성일자, 수정일자, 카테고리

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:20]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'