from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Plant
from .forms import PlantForm


def all_plants(request):
    plants = Plant.objects.all()
    category = request.GET.get('category', '')
    is_edible = request.GET.get('is_edible', '')

    if category:
        plants = plants.filter(category=category)
    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    categories = Plant.Category.choices
    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': categories,
        'selected_category': category,
        'selected_edible': is_edible,
    })


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant_id)[:3]
    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
    })


def new_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f'"{plant.name}" has been added successfully!')
            return redirect('plant_detail', plant_id=plant.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PlantForm()
    return render(request, 'plants/new_plant.html', {'form': form})


def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{plant.name}" has been updated successfully!')
            return redirect('plant_detail', plant_id=plant.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/update_plant.html', {'form': form, 'plant': plant})


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    name = plant.name
    plant.delete()
    messages.success(request, f'"{name}" has been deleted.')
    return redirect('all_plants')


def search(request):
    query = request.GET.get('q', '').strip()
    plants = Plant.objects.none()
    if query:
        plants = (
            Plant.objects.filter(name__icontains=query) |
            Plant.objects.filter(about__icontains=query)
        ).distinct()
    return render(request, 'plants/search.html', {'plants': plants, 'query': query})
