from django.shortcuts import render


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        description = request.data['description']

        if Project.objects.filter(name=name).exists():
            raise ValidationError(f"Project with name: {name} already exists")

        project = Project.objects.create(name=name, description=description)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=request.data['id'])
        project.name = request.data['name']
        project.description = request.data['description']
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
