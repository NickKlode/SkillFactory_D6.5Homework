from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'postAuthor__authorUser__first_name':['icontains'],
            'dateCreation':['gt'],
            'postTitle':['icontains'],
        }