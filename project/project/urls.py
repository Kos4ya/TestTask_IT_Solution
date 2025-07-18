from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('quotes/', include('quotes.urls')),
    path('admin/', admin.site.urls),
]
