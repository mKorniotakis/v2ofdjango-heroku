from allauth.account.forms import SignupForm


# class CustomSignupForm(SignupForm):
#
#     def __init__(self, *args, **kwargs):
#         super(CustomSignupForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'


class MyCustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user