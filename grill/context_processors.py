def asadmin(request):
    return {'asadmin':request.user.groups.filter(name='admin').exists()}

def asowner(request):
    return {'asowner':request.user.groups.filter(name='owner').exists()}