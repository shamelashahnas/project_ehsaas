from django.shortcuts import render

# Create your views here.
def home_admin_view(request):
    return render(request, 'admin/home.html')