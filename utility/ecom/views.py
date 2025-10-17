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
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_product(request):
    """
    Create a new product with stock and images.
    Expected request format:
    {
        "product": {
            "name": "Product Name",
            "description": "Description",
            "sellingPrice": "100.00",
            "maxRetailPrice": "120.00",
            "category": "category_id"
        },
        "stock": {
            "quantity": 10,
            "unit": "pieces"
        },
        "images": [
            {"url": "image_url1"},
            {"url": "image_url2"}
        ]
    }
    """
    try:
        with transaction.atomic():
            # Create product
            product_serializer = ProductSerializer(data=request.data.get('product'))
            if not product_serializer.is_valid():
                return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            product = product_serializer.save()

            # Create stock
            stock_data = request.data.get('stock')
            if stock_data:
                stock_data['product'] = product.id
                stock_serializer = StockSerializer(data=stock_data)
                if not stock_serializer.is_valid():
                    raise ValueError(stock_serializer.errors)
                stock_serializer.save()

            # Create images
            images_data = request.data.get('images', [])
            for image_data in images_data:
                image_data['product'] = product.id
                image_serializer = ImageSerializer(data=image_data)
                if not image_serializer.is_valid():
                    raise ValueError(image_serializer.errors)
                image_serializer.save()

            # Return the created product with all related data
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': 'An error occurred while creating the product'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_categories(request):
    """
    Retrieve a list of all categories.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_category(request):
    """
    Create a new category.
    Expected request format:
    {
        "name": "Category Name",
        "description": "Description"
    }
    """
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.save()
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)