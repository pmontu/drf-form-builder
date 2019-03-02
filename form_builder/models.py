from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=200, unique=True)


class FormField(models.Model):
    TEXT = "T"
    RADIO = "R"
    FIELD_CHOCIES = (
        (TEXT, "Text"),
        (RADIO, "Radio"),
    )

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="fields",
    )
    field = models.CharField(
        max_length=1,
        choices=FIELD_CHOCIES,
        default=TEXT,
    )
    text = models.TextField()


class FormFieldOption(models.Model):
    """Store options for radio button"""
    field = models.ForeignKey(
        FormField,
        on_delete=models.CASCADE,
        related_name="options",
    )
    value = models.TextField(unique=True)


class FormFieldAttempt(models.Model):
    attempt = models.ForeignKey(
        "FormAttempt",
        on_delete=models.CASCADE,
        related_name="fields",
    )
    field = models.ForeignKey(
        FormField,
        on_delete=models.CASCADE,
    )
    text = models.TextField(default="", blank=True)


class FormAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    def create_fields(self):
        for field in self.form.fields.all():
            self.fields.create(attempt=self, field=field)


class FormFieldOptionAttempt(models.Model):
    field = models.ForeignKey(
        FormFieldAttempt,
        on_delete=models.CASCADE,
        related_name="options",
    )
    option = models.ForeignKey(
        FormFieldOption,
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ("field", "option")
