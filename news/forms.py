from django.forms import ModelForm, BooleanField
from .models import Post

class PostForm(ModelForm):
    check_box = BooleanField(label='Нажми меня!')
    class Meta:
        model = Post
        fields = ['postTitle', 'postCategory', 'postAuthor', 'postText', 'check_box']