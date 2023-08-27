from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FeedbackOnExecutor, FeedbackOnCustomer
from .serializers import FeedbackOnCustomerSerializer, FeedbackOnExecutorSerializer



@api_view(["POST"])
def create_feedback_on_executor(request):
    serializer = FeedbackOnExecutorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def create_feedback_on_customer(request):
    serializer = FeedbackOnCustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view(["GET", "POST"])
# def review_list_create_view(request):
#     if request.method == "GET":
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         serializer = ReviewSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
# @api_view(["GET"])
# def review_detail_view(request, pk):
#     review = Review.objects.get(pk=pk)
#     serializer = ReviewSerializer(review)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# @api_view(["GET", "POST"])
# def rating_list_create_view(request):
#     if request.method == "GET":
#         ratings = Rating.objects.all()
#         serializer = RatingSerializer(ratings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         serializer = RatingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
# @api_view(["GET"])
# def rating_detail_view(request, pk):
#     rating = Rating.objects.get(pk=pk)
#     serializer = RatingSerializer(rating)
#     return Response(serializer.data, status=status.HTTP_200_OK)
