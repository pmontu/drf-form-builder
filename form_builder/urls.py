from django.urls import re_path, include
from rest_framework_nested import routers

from .views import (
	FormViewSet, FormFieldViewSet, FormFieldOptionViewSet,
	FormAttemptViewSet, FormFieldAttemptViewSet,
	FormFieldOptionAttemptViewSet,
)

router = routers.SimpleRouter()
router.register("forms", FormViewSet)

form_field_router = routers.NestedSimpleRouter(router, r'forms', lookup='form')
form_field_router.register(r'fields', FormFieldViewSet, base_name='form-fields')

form_field_option_router = routers.NestedSimpleRouter(form_field_router, r'fields', lookup='field')
form_field_option_router.register(r'options', FormFieldOptionViewSet, base_name='form-field-options')

attempt_router = routers.SimpleRouter()
attempt_router.register("attempts", FormAttemptViewSet)

field_attempt_router = routers.NestedSimpleRouter(attempt_router, r'attempts', lookup='attempt')
field_attempt_router.register(r'fields', FormFieldAttemptViewSet, base_name='attempt-fields')

option_attempt_router = routers.NestedSimpleRouter(field_attempt_router, r'fields', lookup='field')
option_attempt_router.register(r'options', FormFieldOptionAttemptViewSet, base_name='attempt-field-options')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^', include(form_field_router.urls)),
    re_path(r'^', include(form_field_option_router.urls)),
    re_path(r'^', include(attempt_router.urls)),
    re_path(r'^', include(field_attempt_router.urls)),
    re_path(r'^', include(option_attempt_router.urls)),
]