import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from palliatives.models import Category, Item


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "items")


class ItemsType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_items = graphene.List(ItemsType)
    category_by_name = graphene.Field(
        CategoryType, name=graphene.String(required=True))

    def resolve_all_items(root, into):
        return Item.objects.select_related('category').all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
