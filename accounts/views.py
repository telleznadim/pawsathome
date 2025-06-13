
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from .forms import UserEditForm
from .models import PetOwnerProfile, PetSitterProfile
from .models import Avatar
from .forms import AvatarForm
from django.contrib.auth import get_user_model


# Register View


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                avatar = Avatar.objects.get(user=request.user.id).image.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar

            return redirect('home')
        else:
            # Form has errors, will be displayed in the template
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# @login_required
# def editprofile_view(request):
#     user = request.user
#     profile = None

#     if user.user_type == 'owner':
#         profile = PetOwnerProfile.objects.get(user=user)
#     elif user.user_type == 'sitter':
#         profile = PetSitterProfile.objects.get(user=user)

#     if request.method == 'POST':
#         form = UserEditForm(request.POST, instance=user)
#         if form.is_valid():
#             user = form.save()
#             # Update profile fields manually
#             if user.user_type == 'owner':
#                 profile.phone_number = form.cleaned_data['phone_number']
#                 profile.address = form.cleaned_data['address']
#             elif user.user_type == 'sitter':
#                 profile.bio = form.cleaned_data['bio']
#                 profile.hourly_rate = form.cleaned_data['hourly_rate']
#                 profile.experience_years = form.cleaned_data['experience_years']
#             profile.save()

#             return redirect('home')
#     else:
#         initial_data = {
#             'email': user.email,
#         }
#         if user.user_type == 'owner':
#             initial_data.update({
#                 'phone_number': profile.phone_number,
#                 'address': profile.address,
#             })
#         elif user.user_type == 'sitter':
#             initial_data.update({
#                 'bio': profile.bio,
#                 'hourly_rate': profile.hourly_rate,
#                 'experience_years': profile.experience_years,
#             })

#         form = UserEditForm(instance=user, initial=initial_data)

#     return render(request, 'accounts/editprofile.html', {'form': form})


# @login_required
# def agregarAvatar(request):
#     if request.method == "POST":
#         miForm = AvatarForm(request.POST, request.FILES)
#         if miForm.is_valid():
#             usuario = request.user
#             imagen = miForm.cleaned_data["imagen"]

#             # ________ Borrar avatares viejos
#             avatarViejo = Avatar.objects.filter(user=usuario)
#             if len(avatarViejo) > 0:
#                 for i in range(len(avatarViejo)):
#                     avatarViejo[i].delete()

#             avatar = Avatar(user=usuario, imagen=imagen)
#             avatar.save()

#             # ________ Enviar la imagen al home
#             imagen = Avatar.objects.get(user=usuario).imagen.url
#             request.session["avatars"] = imagen

#             return redirect(reverse_lazy("home"))
#     else:
#         miForm = AvatarForm()
#     return render(request, "accounts/agregar_Avatar.html", {"form": miForm})


# @login_required
# def agregarAvatar(request):
#     if request.method == "POST":
#         miForm = AvatarForm(request.POST, request.FILES)
#         if miForm.is_valid():
#             usuario = request.user
#             imagen = miForm.cleaned_data["imagen"]

#             # Remove old avatars
#             Avatar.objects.filter(user=usuario).delete()

#             # Save new one
#             Avatar.objects.create(user=usuario, imagen=imagen)

#             return redirect(reverse_lazy("home"))
#     else:
#         miForm = AvatarForm()
#     return render(request, "accounts/agregar_Avatar.html", {"form": miForm})


@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)
        if miForm.is_valid():
            usuario = request.user
            imagen = miForm.cleaned_data["imagen"]

            avatar = Avatar(user=usuario, imagen=imagen)
            avatar.save()

            request.session["avatars"] = avatar.imagen.url
            return redirect(reverse_lazy("home"))
    else:
        miForm = AvatarForm()
    return render(request, "accounts/agregar_Avatar.html", {"form": miForm})


@login_required
def editprofile_view(request):
    user = request.user
    user_type = user.user_type

    profile = None
    if user_type == 'owner':
        profile = PetOwnerProfile.objects.get(user=user)
    elif user_type == 'sitter':
        profile = PetSitterProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES,
                            instance=user, user_type=user_type)
        if form.is_valid():
            user = form.save()
            if user_type == 'owner':
                profile.phone_number = form.cleaned_data['phone_number']
                profile.address = form.cleaned_data['address']
            elif user_type == 'sitter':
                profile.bio = form.cleaned_data['bio']
                profile.hourly_rate = form.cleaned_data['hourly_rate']
                profile.experience_years = form.cleaned_data['experience_years']
                profile.city = form.cleaned_data['city']
                if form.cleaned_data['photo']:
                    profile.photo = form.cleaned_data['photo']
            profile.save()
            return redirect('home')
    else:
        initial_data = {
            'email': user.email,
        }
        if user_type == 'owner':
            initial_data.update({
                'phone_number': profile.phone_number,
                'address': profile.address,
            })
        elif user_type == 'sitter':
            initial_data.update({
                'bio': profile.bio,
                'hourly_rate': profile.hourly_rate,
                'experience_years': profile.experience_years,
                'city': profile.city,
            })

        form = UserEditForm(
            instance=user, initial=initial_data, user_type=user_type)

    return render(request, 'accounts/editprofile.html', {'form': form})
