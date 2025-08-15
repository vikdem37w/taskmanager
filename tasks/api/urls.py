from rest_framework.routers import SimpleRouter
# from django.urls import path, include
from .views import TaskViewSet

router = SimpleRouter()
router.register(r'api/tasks', TaskViewSet)

urlpatterns = router.urls