from rest_framework import serializers

from .models import (
	Form, FormField, FormFieldOption, FormAttempt, FormFieldAttempt,
	FormFieldOptionAttempt,
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("password",)


class FormFieldOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = FormFieldOption
		fields = "__all__"
		read_only_fields = ("field",)


class FormFieldSerializer(serializers.ModelSerializer):
	options = FormFieldOptionSerializer(read_only=True, many=True)

	class Meta:
		model = FormField
		fields = "__all__"
		read_only_fields = ("form",)


class FormSerializer(serializers.ModelSerializer):
	fields = FormFieldSerializer(many=True, read_only=True)
	username = serializers.CharField(source="user.username", read_only=True)

	class Meta:
		model = Form
		fields = "__all__"
		read_only_fields = ("user",)


class FormFieldOptionAttemptSerializer(serializers.ModelSerializer):
	value = serializers.CharField(source="option.value", read_only=True)

	class Meta:
		model = FormFieldOptionAttempt
		fields = "__all__"
		read_only_fields = ("field", )

	def create(self, validated_data):
		obj, created = FormFieldOptionAttempt.objects.get_or_create(
			**validated_data
		)
		return obj


class FormFieldAttemptSerializer(serializers.ModelSerializer):
	field = FormFieldSerializer(read_only=True)
	options = FormFieldOptionAttemptSerializer(read_only=True, many=True)

	class Meta:
		model = FormFieldAttempt
		fields = "__all__"
		read_only_fields = ("attempt",)


class FormAttemptSerializer(serializers.ModelSerializer):
	fields = FormFieldAttemptSerializer(many=True, read_only=True)
	form_name = serializers.CharField(source="form.name", read_only=True)
	username = serializers.CharField(source="user.username", read_only=True)

	class Meta:
		model = FormAttempt
		fields = "__all__"
		read_only_fields = ("user", "created_at", "updated_at",)

	def create(self, validated_data):
		attempt = FormAttempt.objects.create(**validated_data)
		attempt.create_fields()
		return attempt