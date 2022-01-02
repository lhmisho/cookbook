import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from ingredients.models import Category, Ingredient


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (graphene.relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (graphene.relay.Node, )


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    category = graphene.relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = graphene.relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    # all_ingredients = graphene.List(IngredientType)
    # category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    # def resolve_all_ingredients(root, info):
    #     # We can easily optimize query count in the resolve method
    #     return Ingredient.objects.select_related("category").all()
    #
    # def resolve_category_by_name(root, info, name):
    #     try:
    #         return Category.objects.get(name=name)
    #     except Category.DoesNotExist:
    #         return None


schema = graphene.Schema(query=Query)
