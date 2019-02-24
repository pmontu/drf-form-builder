from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import (
    Form, FormField, FormFieldOption, FormAttempt, FormFieldAttempt,
    FormFieldOptionAttempt,
)
from .serializers import (
    FormSerializer, FormFieldSerializer, FormFieldOptionSerializer,
    FormAttemptSerializer, FormFieldAttemptSerializer,
    FormFieldOptionAttemptSerializer,
)


class FormViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Form.objects.filter(user=user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk):
        form = self.get_object()
        form.is_published = not form.is_published
        form.save()
        serializer = FormSerializer(form)
        return Response(serializer.data)


class FormFieldViewSet(ModelViewSet):
    serializer_class = FormFieldSerializer

    def get_queryset(self):
        user = self.request.user
        return FormField.objects.filter(
            form__user=user,
            form=self.kwargs['form_pk']
        )

    def perform_create(self, serializer):
        form = get_object_or_404(Form, pk=self.kwargs['form_pk'])
        serializer.save(form=form)


class FormFieldOptionViewSet(ModelViewSet):
    serializer_class = FormFieldOptionSerializer

    def get_queryset(self):
        user = self.request.user
        return FormFieldOption.objects.filter(
            form__user=user,
            form_field__form=self.kwargs['form_pk'],
            form_field=self.kwargs['field_pk'],
        )

    def perform_create(self, serializer):
        field = get_object_or_404(
            FormField,
            pk=self.kwargs['field_pk'],
            form=self.kwargs['form_pk'],
        )
        serializer.save(field=field)


class FormAttemptViewSet(ModelViewSet):
    queryset = FormAttempt.objects.all()
    serializer_class = FormAttemptSerializer

    def get_queryset(self):
        user = self.request.user
        return FormAttempt.objects.filter(Q(user=user)|Q(form__user=user))

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class FormFieldAttemptViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = FormFieldAttemptSerializer

    def get_queryset(self):
        user = self.request.user
        return FormFieldAttempt.objects.filter(
            attempt__user=user,
            attempt=self.kwargs['attempt_pk'],
        )

    def perform_create(self, serializer):
        user = self.request.user
        attempt = get_object_or_404(
            FormFieldAttempt,
            pk=self.kwargs['attempt_pk'],
            attempt__user=user
        )
        serializer.save(attempt=attempt)


class FormFieldOptionAttemptViewSet(ModelViewSet):
    serializer_class = FormFieldOptionAttemptSerializer

    def get_queryset(self):
        user = self.request.user
        return FormFieldOptionAttempt.objects.filter(
            field__attempt__user=user,
            field__attempt=self.kwargs['attempt_pk'],
            field=self.kwargs['field_pk'],
        )

    def perform_create(self, serializer):
        user = self.request.user
        field = get_object_or_404(
            FormFieldAttempt,
            pk=self.kwargs['field_pk'],
            attempt=self.kwargs['attempt_pk'],
            attempt__user=user,
        )
        serializer.save(field=field)