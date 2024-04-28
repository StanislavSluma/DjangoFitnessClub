from django.shortcuts import render
from .models import Client


def clients(request):
    clis = Client.objects.all()
    return render(request, 'clients.html', {'clis': clis})


def client(request, id):
    cli = Client.objects.filter(id=id)[0]
    groups = cli.group_set.all()
    return render(request, 'client.html', {'cli': cli, 'groups': groups})
