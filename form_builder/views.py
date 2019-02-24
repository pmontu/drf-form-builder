from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from .models import (
    Form, FormField, FormFieldOption, FormAttempt, FormFieldAttempt
)
from .serializers import (
    FormSerializer, FormFieldSerializer, FormFieldOptionSerializer,
    FormAttemptSerializer, FormFieldAttemptSerializer
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
        return FormAttempt.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class FormFieldAttemptViewSet(ModelViewSet):
    serializer_class = FormFieldAttemptSerializer

    def get_queryset(self):
        user = self.request.user
        return FormFieldAttempt.objects.filter(
            attempt__user=user,
            attempt=self.kwargs['attempt_pk'],
            field__form=self.kwargs['form_pk'],
        )

    def perform_create(self, serializer):
        attempt = get_object_or_404(FormAttempt, pk=self.kwargs['attempt_pk'])
        serializer.save(user=user, form=form)

