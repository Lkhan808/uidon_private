from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Skill, Language, Education, Contact, Portfolio
from .serializers import (
    SkillSerializer, LanguageSerializer, EducationSerializer,
    ContactSerializer, PortfolioSerializer
)


@api_view(["GET", "POST"])
def skill_list_create_view(request):
    """ Список навыков: Создание и список """
    if request.method == "GET":
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = SkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def skill_detail_view(request, pk):
    """ Детальный просмотр, обновление и удаление навыка """
    skill = Skill.objects.get(pk=pk)

    if request.method == "GET":
        serializer = SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = SkillSerializer(skill, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def language_list_create_view(request):
    if request.method == "GET":
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = LanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def language_detail_view(request, pk):
    language = Language.objects.get(pk=pk)
    if request.method == "GET":
        serializer = LanguageSerializer(language)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = LanguageSerializer(language, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def education_list_create_view(request):
    if request.method == "GET":
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = EducationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def education_detail_view(request, pk):
    education = Education.objects.get(pk=pk)

    if request.method == "GET":
        serializer = EducationSerializer(education)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = EducationSerializer(education, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def contact_list_create_view(request):
    if request.method == "GET":
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def contact_detail_view(request, pk):
    contact = Contact.objects.get(pk=pk)

    if request.method == "GET":
        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = ContactSerializer(contact, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def portfolio_list_create_view(request):
    if request.method == "GET":
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = PortfolioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def portfolio_detail_view(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)

    if request.method == "GET":
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = PortfolioSerializer(portfolio, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
