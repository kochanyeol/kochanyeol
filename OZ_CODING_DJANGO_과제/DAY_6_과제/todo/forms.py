from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {'message': '댓글'}
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,      # 세로 줄 수 지정
                'cols': 40,     # 가로 글자 수 지정
                'class': 'form-control',    # CSS 클래스
                'placeholder': '댓글을 입력하세요.' # 입력칸에 안내문구
            })
        }
