from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ComponentForm
from .models import Component


def component_list(request):
    query = request.GET.get("q", "").strip()
    components = Component.objects.all()
    if query:
        components = components.filter(
            Q(name__icontains=query)
            | Q(value__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        )
    return render(
        request,
        "inventory/component_list.html",
        {"components": components, "query": query},
    )


def component_create(request):
    form = ComponentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Component added to inventory.")
        return redirect("inventory:component_list")
    return render(
        request,
        "inventory/component_form.html",
        {"form": form, "page_title": "Add a component"},
    )


def component_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = ComponentForm(request.POST or None, instance=component)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Component updated.")
        return redirect("inventory:component_list")
    return render(
        request,
        "inventory/component_form.html",
        {"form": form, "page_title": "Edit component"},
    )


def component_delete(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == "POST":
        component.delete()
        messages.success(request, "Component deleted.")
        return redirect("inventory:component_list")
    return render(
        request,
        "inventory/component_confirm_delete.html",
        {"component": component},
    )
