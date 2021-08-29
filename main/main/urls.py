from django.contrib import admin
from django.urls import path, include
from main.doc_urls import doc_urls
from main.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/api/', include('polls.urls')),
    path('drfauth/', LoginView.as_view(), name='drfauth'),
]

urlpatterns += doc_urls