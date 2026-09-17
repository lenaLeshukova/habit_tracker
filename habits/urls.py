from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits.views import HabitViewSet, PublicHabitListAPIView

app_name = 'habits'

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [
    path('public/', PublicHabitListAPIView.as_view(), name='public_habits'),
    path('', include(router.urls)),
]
