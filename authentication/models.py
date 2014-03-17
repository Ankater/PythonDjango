from django.db import models

# Create your models here.
def index(request):
    if ('username' in request.REQUEST) and ('password' in request.REQUEST):
        username = request.REQUEST['username']
        password = request.REQUEST['password']
        user = authenticate(username=username, password=password)
        print(user)
    return render_to_response('login.html')
