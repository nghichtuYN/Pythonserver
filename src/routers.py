from rest_framework_nested import routers
from src.product_category.viewsets import ProductCategoryViewSet
from src.products.viewsets import ProductViewSet
from src.product_image.viewsets import ProductImageViewSet
from src.colour.viewsets import ColourViewSet
from src.product_items.viewsets import ProductItemsViewSet
from src.product_variation.viewsets import ProductVariationViewSet
from src.size_option.viewsets import SizeOptionViewSet
from src.brand.viewsets import BrandViewSet
from src.auth.viewsets import RegisterViewSet,LoginViewSet,RefreshViewSet,GoogleLoginViewSet
from src.user.viewsets import UserViewSet
from src.size_category.viewsets import SizeCategoryViewSet
from src.orders.viewsets import OrderViewSet
from src.order_items.viewsets import OrderItemsViewSet
router = routers.SimpleRouter()
router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")
router.register(r'auth/google',GoogleLoginViewSet,basename="google-login")
router.register(r"user", UserViewSet, basename="user")
router.register(r"products", ProductViewSet, basename="products")
router.register(r'colour', ColourViewSet, basename="colour")
router.register(r'size_option', SizeOptionViewSet, basename="size_option")
router.register(r'product_category', ProductCategoryViewSet, basename="product_category")
router.register(r'brands',BrandViewSet,basename='brands')
router.register(r'size_category',SizeCategoryViewSet,basename='size_category')
router.register(r'product_items', ProductItemsViewSet, basename='product_items')
router.register(r'orders',OrderViewSet,basename='orders')
size_category_router=routers.NestedSimpleRouter(router,r"size_category",lookup="size_category")
size_category_router.register(r'size_option',SizeOptionViewSet,basename="size_category-size_option")
products_router = routers.NestedSimpleRouter(router, r"products", lookup="product")
products_router.register(r"product_items", ProductItemsViewSet, basename="product-product_items")
products_router.register(r'product_images', ProductImageViewSet, basename="product-images")
product_items_router = routers.NestedSimpleRouter(router, r'product_items', lookup="product_item")
product_items_router.register(r'product_variation', ProductVariationViewSet, basename='product_variation')
product_items_router.register(r'product_image', ProductImageViewSet, basename='product-item-product_image')
user_order_router=routers.NestedSimpleRouter(router,r'user',lookup="user")
user_order_router.register(r'orders',OrderViewSet,basename='orders')
order_router=routers.NestedSimpleRouter(router,r'orders',lookup="orders")
order_router.register(r'order_items',OrderItemsViewSet,basename='order_items')
urlpatterns = [
    *router.urls,
    *products_router.urls,
    *product_items_router.urls,
    *size_category_router.urls,
    *user_order_router.urls,
    *order_router.urls
]
