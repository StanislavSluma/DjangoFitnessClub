from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms


class ReviewForm(forms.Form):
    grade = forms.IntegerField(label='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = forms.CharField(label='Отзыв', widget=forms.Textarea)
