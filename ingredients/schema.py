import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from ingredients.models import Category, Ingredient, Product


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

    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return "hello!"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        # fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    category = graphene.relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = graphene.relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    product = graphene.Field(ProductType, id=graphene.ID())
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)

    # all_ingredients = graphene.List(IngredientType)
    # category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    #
    # def resolve_all_ingredients(root, info):
    #     # We can easily optimize query count in the resolve method
    #     return Ingredient.objects.select_related("category").all()
    #
    # def resolve_category_by_name(root, info, name):
    #     try:
    #         return Category.objects.get(name=name)
    #     except Category.DoesNotExist:
    #         return None


#******************* 😎 PRODUCT-MUTATIONS 😎 *************************#
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category = Category.objects.create(
            name=name
        )

        return CreateCategory(category=category)



#******************* 😎 PRODUCT-MUTATIONS 😎 *************************#
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        price = graphene.Float()
        category = graphene.List(graphene.ID)
        in_stock = graphene.Boolean()
        date_created = graphene.types.datetime.DateTime()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price=None, category=None, in_stock=True, date_created=None):
        product = Product.objects.create(
            name=name,
            price=price,
            in_stock=in_stock,
            date_created=date_created
        )
        # This is how we deal with ManyToMany
        # Loop through and add categories for our product. Simple right? 😉
        if category is not None:
            category_set = []
            for cat_id in category:
                cat_obj = Category.objects.get(pk=cat_id)
                category_set.append(cat_obj)
            product.category.set(category_set)

        product.save()
        # return an instance of the Mutation 🤷‍♀️
        return CreateProduct(
            product=product
        )


#***************** 🔥🔥🔥 Wiring up the mutations 🔥🔥🔥 *******************#
class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_category = CreateCategory.Field()

# schema = graphene.Schema(query=Query)
