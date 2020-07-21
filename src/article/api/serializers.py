from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from article.models import Article

class ArticleCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'title', 
            'content',
            'tags',
            'subject', 
            'draft',
            'publish',
            )
class ArticleDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    html_content= SerializerMethodField()
    image = SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            'id',
            'user', 
            'title', 
            'content',
            'html_content',
            'image',
            'tags',
            'slug', 
            'draft',
            'publish',
            )
    def get_user(self, obj):
        return str(obj.user.username)
    
    def get_html_content(self, obj):
        return obj.get_html()
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

class ArticleListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='article-api:detail',
        lookup_field='slug'
    )
    user = SerializerMethodField()
    html_content= SerializerMethodField()
    image = SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            # 'id',
            'url',
            'user', 
            'title', 
            'content',
            'html_content',
            'image',
            'tags', 
            'draft',
            'publish',
            )
    def get_user(self, obj):
        return str(obj.user.username)
    def get_html_content(self, obj):
        return obj.get_html()
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
