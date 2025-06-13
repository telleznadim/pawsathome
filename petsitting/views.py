from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import PetOwnerProfile, PetSitterProfile
from .forms import PetForm
from .models import Pet, JobRequest
from django.urls import reverse_lazy, reverse
from .forms import JobRequestForm


def home(request):
    return render(request, 'petsitting/home.html')


def about(request):
    return render(request, 'petsitting/about.html')


@login_required
def pet_list(request):
    if hasattr(request.user, 'petownerprofile'):
        pets = Pet.objects.filter(owner=request.user.petownerprofile)
        return render(request, 'petsitting/pet_list.html', {'pets': pets})
    return redirect('home')  # Or show an error


@login_required
def add_pet(request):
    try:
        pet_owner = request.user.petownerprofile
    except PetOwnerProfile.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = pet_owner
            pet.save()
            return redirect('pet_list')
    else:
        form = PetForm()

    return render(request, 'petsitting/add_pet.html', {'form': form})


@login_required
def edit_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user.petownerprofile)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PetForm(instance=pet)
    return render(request, 'petsitting/edit_pet.html', {'form': form})


@login_required
def delete_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user.petownerprofile)
    if request.method == 'POST':
        pet.delete()
        return redirect('pet_list')
    return render(request, 'petsitting/delete_pet.html', {'pet': pet})


@login_required
def sitter_list(request):
    query = request.GET.get('city', '')  # Get city from search input
    sitters = PetSitterProfile.objects.select_related('user').all()

    if query:  # If a city is provided, filter sitters
        sitters = sitters.filter(city__icontains=query)

    return render(request, 'petsitting/sitter_list.html', {'sitters': sitters, 'query': query})


class JobRequestCreateView(LoginRequiredMixin, CreateView):
    model = JobRequest
    form_class = JobRequestForm
    template_name = 'petsitting/request_job.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        owner_profile = get_object_or_404(
            PetOwnerProfile, user=self.request.user)
        kwargs['owner'] = owner_profile
        return kwargs

    def form_valid(self, form):
        sitter_profile = get_object_or_404(
            PetSitterProfile, pk=self.kwargs['sitter_id'])
        owner_profile = get_object_or_404(
            PetOwnerProfile, user=self.request.user)
        form.instance.sitter = sitter_profile
        form.instance.owner = owner_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sitter_list')


class JobRequestInboxView(LoginRequiredMixin, ListView):
    model = JobRequest
    template_name = 'petsitting/job_inbox.html'
    context_object_name = 'job_requests'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'sitter':
            return redirect('home')  # Redirect if not an sitter
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        sitter = PetSitterProfile.objects.get(user=self.request.user)
        return JobRequest.objects.filter(sitter=sitter).order_by('-created_at')


class JobRequestOutboxView(LoginRequiredMixin, ListView):
    model = JobRequest
    template_name = 'petsitting/job_outbox.html'
    context_object_name = 'job_requests'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'owner':
            return redirect('home')  # Redirect if not an owner
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        owner = PetOwnerProfile.objects.get(user=self.request.user)
        return JobRequest.objects.filter(owner=owner).order_by('-created_at')


class JobRequestStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = JobRequest
    fields = ['status', 'message']
    template_name = 'petsitting/update_job_status.html'
    context_object_name = 'job_request'

    def dispatch(self, request, *args, **kwargs):
        job = self.get_object()
        user = request.user

        # Allow only the assigned sitter or owner to access the update form
        if job.sitter.user != user and job.owner.user != user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect to appropriate dashboard
        if self.request.user.user_type == 'sitter':
            return reverse_lazy('job_inbox')
        else:
            return reverse_lazy('job_outbox')
