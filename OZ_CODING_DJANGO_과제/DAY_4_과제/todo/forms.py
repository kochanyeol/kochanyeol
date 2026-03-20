from django import forms
from .models import Todo

# Todo 생성 폼 - 사용자가 Todo 모델 기반으로 폼 생성
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo    # Todo 모델 기반으로 폼 생성
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Todo 수정 폼 - TodoForm을 상속받아 is_completed(완료 여부) 필드 추가
class TodoUpdateForm(TodoForm):
    class Meta(TodoForm.Meta):
        fields = TodoForm.Meta.fields + ['is_completed']