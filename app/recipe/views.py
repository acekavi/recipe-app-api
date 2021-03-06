from rest_framework import viewsets, mixins
#  from rest_framework import authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    # Base viewset for the app
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Return objects for the current authenticated user
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        # Create a new tag
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeViewSet):
    # Manage tags in the database
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeViewSet):
    # Manage tags in the database
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    # Manage recipes in the database
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # retrieve the recipes for the auth user
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        # Return appropriate classes
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        # Create a  new recipe
        serializer.save(user=self.request.user)
