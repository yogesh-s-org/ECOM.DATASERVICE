from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Wishlist
from .serializers import ProductSerializer, CategorySerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

@api_view(['GET'])
def get_products(request):
    """
    Retrieve a list of all products.
    """
    try:
        if not request.user.has_perm('ecom.view_product'):
            return Response(
                {'error': 'You do not have permission to view products'},
                status=status.HTTP_403_FORBIDDEN
            )
        limit = "end"
        offset = 0
        reqlimit = request.GET.get('limit')
        if reqlimit is not None:
            limit = int(reqlimit)
            requestedPage = int(request.GET.get('page') or 1)
            offset = (limit * (requestedPage - 1))
        products = Product.objects.all().select_related('stock').prefetch_related('images')[offset : offset + limit]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching products: {e}")
        return Response( 
            {'error': 'An error occurred while fetching products'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])   
def get_product_detail(request, product_id):
    """
    Retrieve detailed information about a specific product, including stock and images.
    """
    try:
        if not request.user.has_perm('ecom.view_product'):
            return Response(
                {'error': 'You do not have permission to view products'},
                status=status.HTTP_403_FORBIDDEN
            )       
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': 'An error occurred while fetching the product'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_categories(request):
    """
    Retrieve a list of all categories.
    """
    try:
        if not request.user.has_perm('ecom.view_category'):
            return Response(
                {'error': 'You do not have permission to view categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return Response(
            {'error': 'An error occurred while fetching categories'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def register(request):
    """
    Register a new user.
    """
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error during registration: {e}")
        return Response(
            {'error': 'An error occurred during registration'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def login(request):
    """
    Authenticate a user and provide a JWT token.
    """
    try:
        data = request.data
        username = data["username"]
        password = data["password"]
        user = User.objects.get(username=username)
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refreshToken': str(refresh),
                'accessToken': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        print(f"Error during login: {e}")
        return Response(
            {'error': 'An error occurred during login'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['POST'])
def add_product_to_wishlist(request):
    """
    Add a product to the user's wishlist.
    """
    try:
        if not request.user.has_perm('ecom.add_wishlist'):
            print(request.user)
            return Response(
                {'error': 'You do not have permission to add to wishlist'},
                status=status.HTTP_403_FORBIDDEN
            )
        user = request.user
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        print(f"Adding product {product_id} to wishlist for user {user}")
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            return Response(
                {'message': 'Product added to wishlist'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Product already in wishlist'},
                status=status.HTTP_200_OK
            )
    except Exception as e:
        print(f"Error adding product to wishlist: {e}")
        return Response(
            {'error': 'An error occurred while adding product to wishlist'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['GET'])
def get_wishlist(request):
    """
    Retrieve the user's wishlist.
    """
    try:
        if not request.user.has_perm('ecom.view_wishlist'):
            return Response(
                {'error': 'You do not have permission to view wishlist'},
                status=status.HTTP_403_FORBIDDEN
            )
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user).select_related('product')
        products = [item.product for item in wishlist_items]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching wishlist: {e}")
        return Response(
            {'error': 'An error occurred while fetching wishlist'},
            status=status.HTTP_400_BAD_REQUEST
        )