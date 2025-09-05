from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey

from namer.models import *
from .serializers import *

def next_name(group):
    computers = Computer.objects.filter(computergroup=group).values_list('name', flat=True)
    max_num = 0
    for name in computers:
        try:
            num = int(name)
            max_num = max(max_num, num)
        except ValueError:
            continue
    return max_num + 1

class ComputerGroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAdminUser]
    queryset = ComputerGroup.objects.all()
    serializer_class = ComputerGroupSerializer

class NetworksViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAdminUser]
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

class ComputersViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAdminUser]
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "name"]
    ordering = ["id"]

    def create(self, request, *args, **kwargs):
        data = request.data
        single = isinstance(data, dict)
        if single:
            data = [data]

        instances = []

        posted_serials = [item.get("serial") for item in data if "serial" in item]
        existing_serials = set(
            Computer.objects.filter(serial__in=posted_serials).values_list("serial", flat=True)
        )

        seen_serials = set()

        name_counters = {}

        for instance in data:
            serial = instance.get("serial")
            if not serial or serial in existing_serials or serial in seen_serials:
                continue
            seen_serials.add(serial)

            group = get_object_or_404(ComputerGroup, pk=instance["computergroup"])

            provided_name = instance.get("name")
            if provided_name is None or str(provided_name).strip() == "":
                if group.id not in name_counters:
                    name_counters[group.id] = next_name(group)
                instance["name"] = str(name_counters[group.id])
                name_counters[group.id] += 1
            instances.append(instance)

        serializer = self.get_serializer(data=instances, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        if single and serializer.data:
            return Response(serializer.data[0], status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)