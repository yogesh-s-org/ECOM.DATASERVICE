from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Wishlist, OTP
from .serializers import ProductSerializer, CategorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_otp_email, add_user_to_group
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

#Fetch custom model
User = get_user_model()

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
        start_index = None
        end_index = None
        reqlimit = request.GET.get('limit')
        if reqlimit is not None:
            limit = int(reqlimit)
            requestedPage = int(request.GET.get('page') or 1)
            start_index = (limit * (requestedPage - 1))
            end_index = start_index + limit
        products = Product.objects.all().select_related('stock').prefetch_related('images', 'ratings')[start_index:end_index]
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
def authenticate(request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        if not email or not otp_code:
            return Response({'error': 'Email address and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email) 
            latest_otp = OTP.objects.filter(user=user).order_by('-created_at').first()

            if not latest_otp or not latest_otp.is_valid() or latest_otp.otp_code != otp_code:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful.',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An internal error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
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
        
@api_view(['POST'])
def request_otp(request):
    email = request.data.get('email')

    if not email:
        return Response({'error': 'email is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user, created = User.objects.get_or_create(email=email)
    if created:
        add_user_to_group(user, 'buyer')
    otp_code = OTP.generate_code()
    OTP.objects.create(user=user, otp_code=otp_code)
    sms_success = send_otp_email(email, otp_code)

    if sms_success:
        return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)
    else:
        # Handle SMS failure (e.g., temporary service outage)
        return Response({'error': 'Failed to send OTP.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)