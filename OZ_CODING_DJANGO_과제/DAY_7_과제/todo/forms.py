from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Comment, Todo

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

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'description' : SummernoteWidget(),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'start_date' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class TodoUpdateForm(TodoForm):
    class Meta(TodoForm.Meta):
        fields = TodoForm.Meta.fields + ['completed_image', 'is_completed',]
        widgets = {
            **TodoForm.Meta.widgets,
            'is_completed' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'completed_image' : forms.FileInput(attrs={'class':'form-control'}),
        }