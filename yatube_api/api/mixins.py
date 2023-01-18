from rest_framework import viewsets, mixins


class GetPostMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass
