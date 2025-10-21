from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, StockSerializer, ImageSerializer, CategorySerializer
from django.db import transaction

@api_view(['GET'])
def get_products(request):
    """
    Retrieve a list of all products.
    """
    try:
        limit = int(request.GET.get('limit'))
        requestedPage = int(request.GET.get('page'))
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
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
