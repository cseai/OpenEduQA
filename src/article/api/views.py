from django.db.models import Q
# from rest_framework.filters import (
#     SearchFilter,
#     OrderingFilter
# )
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView, 
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .permissions import IsOwnerOrReadOnly

from .pagination import (
    ArticleLimitOffsetPagination,
    ArticlePageNumberPagination,
) 

from article.models import Article
from .serializers import (
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer, 
)
 
class ArticleCreateAPIView(CreateAPIView):
    queryset = Article.objects.active()
    serializer_class = ArticleCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleDeleteAPIView(DestroyAPIView):
    queryset = Article.objects.active()
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    

class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.objects.active()
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'

class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListSerializer
    # queryset = Article.objects.active()
    # It's not working !!!
    # filter_bacends = (SearchFilter) # , OrderingFilter
    # search_fields = ('title', 'content')
    # ordering_fields = ('title', 'content')

    pagination_class = ArticlePageNumberPagination # ArticleLimitOffsetPagination 

    def get_queryset(self, *args, **kwargs):
        queryset_list = Article.objects.active()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__name__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        return queryset_list

class ArticleUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Article.objects.active()
    serializer_class = ArticleCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

