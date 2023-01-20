from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Perk, Experience
from categories.models import Category
from . import serializers
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExperienceSerializer


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            return exceptions.NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            update_perk = serializer.save()
            return Response(
                serializers.PerkSerializer(update_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(all_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceListSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            perks_pks = request.data.get("perks")
            if not category_pk:
                raise exceptions.ParseError
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    raise exceptions.ParseError(
                        "The category's kind should be 'experience'."
                    )
            except Category.DoesNotExist:
                raise exceptions.NotFound

            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    if perks_pks:
                        for perk_pk in perks_pks:
                            perk = Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise exceptions.NotFound

            experience = serializer.save()
            serializer = serializers.ExperienceSerializer(
                experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")
            perks_pks = request.data.get("perks")
            if not category_pk:
                raise exceptions.ParseError
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    raise exceptions.ParseError(
                        "The category's kind should be 'experience'."
                    )
            except Category.DoesNotExist:
                raise exceptions.NotFound

            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    if perks_pks:
                        for perk_pk in perks_pks:
                            perk = Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise exceptions.NotFound

            experience = serializer.save()
            serializer = serializers.ExperienceSerializer(
                experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = Experience.objects.get(pk=pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        perk = experience.perk.all()
        serializer = serializers.PerkSerializer(perk, many=True)
        return Response(serializer.data)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            check_in__gte=now,
        )

        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceSerializer(
            data=request.data,
            context={"experience": experience},
            partial=True,
        )

        if serializer.is_valid():
            new_booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )

            serializer = PublicBookingSerializer(new_booking)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
