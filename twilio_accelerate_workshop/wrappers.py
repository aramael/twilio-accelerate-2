
def twilio(func):
    def authenticate_and_call(*args, **kwargs):
        if not Account.is_authentic(request):
            raise Exception('Authentication Failed.')
        return func(*args, **kwargs)
    return authenticate_and_call