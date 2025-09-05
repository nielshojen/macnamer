from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib import messages
from rest_framework_api_key.models import APIKey
import inspect
import json as simplejson
import re

from .models import *
from .forms import *

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def next_name(group):
    counter = 1
    if group.prefix:
        while True:
            try:
                computer = get_object_or_404(Computer, name=counter, computergroup=group.id)
                counter += 1
            except Http404:
                break
        return_name = counter
    else:
        return_name = ""

    return return_name

@login_required
def index(request):
    groups = ComputerGroup.objects.all()
    context = {'user': request.user, 'groups':groups, }
    return render(request, 'namer/index.html', context)

#new computer group
@login_required
@csrf_protect
@permission_required('namer.add_computergroup', login_url='/login/')
def new_computer_group(request):
    context = {}
    if request.method == 'POST':
        form = ComputerGroupForm(request.POST)
        if form.is_valid():
            new_computer_group = form.save(commit=False)
            new_computer_group.save()
            return redirect('show_group', new_computer_group.id)
    else:
        form = ComputerGroupForm()
    context = {'form': form,}
    return render(request, 'forms/new_computer_group.html', context)

#edit computer group
@login_required
@csrf_protect
@permission_required('namer.change_computergroup', login_url='/login/')
def edit_computer_group(request, group_id):
    group = get_object_or_404(ComputerGroup, pk=group_id)
    context = {}
    if request.method == 'POST':
        form = ComputerGroupForm(request.POST, instance=group)
        if form.is_valid():
            the_group = form.save()
            return redirect('show_group', the_group.id)
    else:
        form = ComputerGroupForm(instance=group)
    context = {'form': form, 'group':group, }
    return render(request, 'forms/edit_computer_group.html', context)

#new computer
@login_required
@csrf_protect
@permission_required('namer.add_computer', login_url='/login/')
def new_computer(request, group_id):
    group = get_object_or_404(ComputerGroup, pk=group_id)
    context = {}
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            the_computer = form.save(commit=False)
            the_computer.name = re.sub("^0+","",the_computer.name)
            the_computer.computergroup = group
            the_computer.save()
            return redirect('show_group', group.id)
    else:
        initial_name = next_name(group)
        form = ComputerForm(initial={'name': initial_name})
    context = {'form': form, 'group':group, }
    return render(request, 'forms/new_computer.html', context)

#edit computer
@login_required
@csrf_protect
@permission_required('namer.change_computer', login_url='/login/')
def edit_computer(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)

    context = {}
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            the_computer = form.save(commit=False)
            the_computer.name = re.sub("^0+","",the_computer.name)
            the_computer.save()
            return redirect('show_group', computer.computergroup.id)
    else:
        form = ComputerForm(instance=computer)
    context = {'form': form, 'group':computer.computergroup, 'computer':computer, }
    return render(request, 'forms/edit_computer.html', context)

#show computer group
@login_required
def show_group(request, group_id):
    group = get_object_or_404(ComputerGroup, pk=group_id)
    computers = group.computer_set.all()
    length = 0
    for computer in computers:
        this_length = len(computer.name)
        if this_length > length:
            length = this_length
    context = { 'user': request.user, 'group':group, 'computers':computers, 'length':length, }
    return render(request, 'namer/show_group.html', context)

@login_required
@permission_required('namer.delete_computer', login_url='/login/')
def delete_computer(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    group = get_object_or_404(ComputerGroup, pk=computer.computergroup.id)
    computer.delete()
    return redirect('show_group', group_id=group.id)

#new network
@login_required
@csrf_protect
@permission_required('namer.add_network', login_url='/login/')
def new_network(request, group_id):
    group = get_object_or_404(ComputerGroup, pk=group_id)
    context = {}
    #context.update(csrf(request))
    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
            the_network = form.save(commit=False)
            the_network.computergroup = group
            the_network.save()
            return redirect('show_network', group.id)
    else:
        form = NetworkForm()
    context = {'form': form, 'group':group, }
    return render(request, 'forms/new_network.html', context)

#edit network
@login_required
@csrf_protect
@permission_required('namer.change_network', login_url='/login/')
def edit_network(request, network_id):
    network = get_object_or_404(Network, pk=network_id)

    context = {}
    #context.update(csrf(request))
    if request.method == 'POST':
        form = NetworkForm(request.POST, instance=network)
        if form.is_valid():
            the_network = form.save(commit=False)
            the_network.save()
            return redirect('show_network', network.computergroup.id)
    else:
        form = NetworkForm(instance=network)
    context = {'form': form, 'group':network.computergroup, 'network':network, }
    return render(request, 'forms/edit_network.html', context)

#show network
@login_required
def show_network(request, group_id):
    group = get_object_or_404(ComputerGroup, pk=group_id)
    networks = group.network_set.all()
    context = { 'user': request.user, 'group':group, 'networks':networks, }
    return render(request, 'namer/show_network.html', context)

@login_required
@permission_required('namer.delete_network', login_url='/login/')
def delete_network(request, network_id):
    network = get_object_or_404(Network, pk=network_id)
    group = get_object_or_404(ComputerGroup, pk=network.computergroup.id)
    network.delete()
    return redirect('show_network', group_id=group.id)

# client checkin
@csrf_exempt
def checkin(request):
    try:
        serial_num = request.POST['serial']
    except:
        raise Http404
    try:
        ip = request.POST['ip']
    except:
        raise Http404

    try:
        key = request.POST['key']
    except:
        raise Http404
    try:
        #try to find the computer
        computer = get_object_or_404(Computer, serial__iexact=serial_num)
    except:
        wan_ip = get_client_ip(request)
        ##we couldn't find the computer, get it's subnet out of the passed ip
        subnet = ip.rpartition('.')[0] + ".0"
        ##find if there are any subnets with this IP address
        try:
            computergroup = get_object_or_404(ComputerGroup, key=key)
        except:
            raise Http404
        ##get the next name of from the group - if it's not blank carry on
        new_name = next_name(computergroup)
        if new_name == "":
            raise Http404
        else:
            ##if there are, create a new computer in that group with the serial
            computer = Computer(name=new_name, serial=serial_num, computergroup=computergroup)
            computer.save()

    computer.last_checkin = timezone.now()
    computer.save()
    group = computer.computergroup

    computers = group.computer_set.all()
    ##need to get the longest number.
    length = 0
    for the_computer in computers:
        this_length = len(the_computer.name)
        if this_length > length:
            length = this_length
    c ={'name':computer.name, 'prefix':group.prefix,  'divider':group.divider, 'domain':group.domain, 'length':length, }
    return HttpResponse(simplejson.dumps(c), content_type="application/json")

# api key management
@staff_member_required
def api_key_list(request):
    qs = APIKey.objects.order_by("-created")
    return render(request, "api_keys/list.html", {"keys": qs})

@staff_member_required
@require_http_methods(["GET", "POST"])
def api_key_create(request):
    if request.method == "POST":
        form = APIKeyCreateForm(request.POST)
        if form.is_valid():
            kwargs = {"name": form.cleaned_data["name"]}
            expires_value = form.cleaned_data.get("expires_at")
            model_has_field = any(f.name == "expires_at" for f in APIKey._meta.get_fields())
            create_key_params = inspect.signature(APIKey.objects.create_key).parameters
            create_accepts_param = "expires_at" in create_key_params

            if expires_value is not None and model_has_field and create_accepts_param:
                kwargs["expires_at"] = expires_value

            # Always use create_key(), never APIKey(...)
            key, obj = APIKey.objects.create_key(**kwargs)
            return render(request, "api_keys/create_done.html", {"key": key, "obj": obj})
    else:
        form = APIKeyCreateForm()

    return render(request, "api_keys/create.html", {"form": form})

@staff_member_required
@require_POST
def api_key_revoke(request, pk):
    obj = get_object_or_404(APIKey, pk=pk)
    if not obj.revoked:
        obj.revoked = True
        obj.save(update_fields=["revoked"])
        messages.success(request, f"API key '{obj.name}' has been revoked.")
    else:
        messages.info(request, f"API key '{obj.name}' was already revoked.")
    return redirect("api_keys_list")

@staff_member_required
@require_POST
def api_key_delete(request, prefix):
    obj = get_object_or_404(APIKey, prefix=prefix)
    obj.delete()
    messages.success(request, f"API key “{obj.name}” was deleted.")
    return redirect("api_keys_list")