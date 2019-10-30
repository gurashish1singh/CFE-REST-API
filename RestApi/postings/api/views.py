# We'll use generic views which are very convinient and shortcuts everything for us(DJANGO REST FRAMEWORK GENERIC VIEWS)

from rest_framework import generics,  mixins
from django.db.models import Q

from postings.models import BlogPost
from  .serializers import BlogPostSerializer
from .permissions import IsOwnerOrReadOnly


# Detail and Create view
class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = BlogPostSerializer

    # queryset = BlogPost.objects.all()

    # We could use this function to override the queryset
    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|Q
            (content__icontains=query))

        return qs

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    # This method is handled by the mixin
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {'request' : self.request}


# # Detail view
# class BlogPostListView(generics.ListAPIView):
#     lookup_field = 'pk'
#     serializer_class = BlogPostSerializer
#     # queryset = BlogPost.objects.all()

#     # We could use this function to override the queryset
#     def get_queryset(self):
#         return BlogPost.objects.all()


# RUD view
class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = BlogPost.objects.all()

    # We could use this function to override the queryset
    def get_queryset(self):
        return BlogPost.objects.all()

    
    def get_serializer_context(self, *args, **kwargs):
        return {'request':self.request}