from .models import CustomUser
from django import forms
from .models import Avatar
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PetOwnerProfile, PetSitterProfile
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES, label="Register as")

    # Owner fields
    phone_number = forms.CharField(required=False)
    address = forms.CharField(required=False)

    # Sitter fields
    bio = forms.CharField(widget=forms.Textarea, required=False)
    experience_years = forms.IntegerField(required=False)
    hourly_rate = forms.DecimalField(
        max_digits=6, decimal_places=2, required=False)
    available = forms.BooleanField(required=False)

    photo = forms.ImageField(required=False)
    city = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2', 'user_type',
            'phone_number', 'address',  # Owner fields
            'bio', 'experience_years', 'hourly_rate', 'available',  # Sitter fields
            'photo', 'city'  # New sitter fields
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
            if user.user_type == 'owner':
                PetOwnerProfile.objects.create(
                    user=user,
                    phone_number=self.cleaned_data['phone_number'],
                    address=self.cleaned_data['address'],
                )
            elif user.user_type == 'sitter':
                PetSitterProfile.objects.create(
                    user=user,
                    bio=self.cleaned_data['bio'],
                    experience_years=self.cleaned_data['experience_years'],
                    hourly_rate=self.cleaned_data['hourly_rate'],
                    available=self.cleaned_data['available'] or False,
                    photo=self.cleaned_data['photo'],
                    city=self.cleaned_data['city']
                )
        return user


# class UserEditForm(UserChangeForm):
#     password = None  # to remove password field from the form
#     email = forms.EmailField(required=True)
#     bio = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     address = forms.CharField(required=True)
#     hourly_rate = forms.DecimalField(
#         required=True, max_digits=6, decimal_places=2)
#     experience_years = forms.IntegerField(required=True)

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'bio', 'phone_number',
#                   'address', 'hourly_rate', 'experience_years']


class AvatarForm(forms.ModelForm):
    imagen = forms.ImageField(required=True)

    class Meta:
        model = Avatar
        fields = ['imagen']


class UserEditForm(UserChangeForm):
    password = None  # remove password field
    email = forms.EmailField(required=True)

    # Owner fields
    phone_number = forms.CharField(required=False)
    address = forms.CharField(required=False)

    # Sitter fields
    bio = forms.CharField(widget=forms.Textarea, required=False)
    hourly_rate = forms.DecimalField(
        max_digits=6, decimal_places=2, required=False)
    experience_years = forms.IntegerField(required=False)
    photo = forms.ImageField(required=False)
    city = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'address', 'bio',
                  'hourly_rate', 'experience_years', 'photo', 'city']

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)

        # Hide sitter fields for owners
        if user_type == 'owner':
            for field in ['bio', 'hourly_rate', 'experience_years', 'photo', 'city']:
                self.fields[field].widget = forms.HiddenInput()

        # Hide owner fields for sitters
        elif user_type == 'sitter':
            for field in ['phone_number', 'address']:
                self.fields[field].widget = forms.HiddenInput()
