# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from pagedown.widgets import PagedownWidget

from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()
# from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'is_student', 'is_teacher')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = User
        fields = ('name', 'bio', 'current_address', 'parmanent_address', 'is_student', 'is_teacher', 'image', 'follows')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['follows'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["follows"].queryset = User.objects.all()

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        # user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    # email = forms.EmailField(label='Email address')
    query = forms.CharField(label='Username / Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        # email = self.cleaned_data.get("email")
        # password = self.cleaned_data.get("password")

        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        # if email and password:
        #     user = authenticate(username=email, password=password)
        #     if not user:
        #         raise forms.ValidationError("This user does not exist")
        #     if not user.check_password(password):
        #         raise forms.ValidationError("Incorrect passsword")
        #     if not user.is_active:
        #         raise forms.ValidationError("This user is not longer active.")
        # return super(LoginForm, self).clean(*args, **kwargs)

        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()

        # print('user_qs_final', user_qs_final)

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does note exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("credentials are not correct")
        if not user_obj.is_active:
            raise forms.ValidationError("This user is not longer active.")
        self.cleaned_data["user_obj"] = user_obj

        # print('self.cleaned_data', self.cleaned_data)

        return super(LoginForm, self).clean(*args, **kwargs)


class UserFollowForm(forms.Form):
    # follow = forms.BooleanField(label="Follow", type="hidden")
    pass


class UserUnfollowForm(forms.Form):
    # follow = forms.BooleanField(label="Unfollow")
    pass
