from rest_framework import serializers

# Worker
# GENERIC
from company.company.models import Company
from company.workers.models import Worker
from technologies.models import Technology


class WorkerSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Worker model
    """

    class Meta:
        model = Worker
        fields = "__all__"


# CREATE
class CreateWorkerSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of Workers
    """

    workers = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

    class Meta:
        model = Worker
        fields = ["company", "workers"]

    def validate(self, data):
        if not Company.objects.filter(id=data['company']).exists():
            raise serializers.ValidationError("There is no company created to associate these departments.")
        return True

    def create(self, validated_data):
        if isinstance(validated_data, dict):
            # Create a single worker
            workers = [validated_data['worker']]
        else:
            # Create a batch of workers
            workers = validated_data.pop("workers")
        for worker in workers:
            # Create a new worker
            company_worker = Worker(first_name=worker['first_name'], last_name=worker['last_name'],
                                    company=Company.objects.get(id=validated_data["company"]),
                                    time=worker['time'], level=worker['level'])
            company_worker.save()


# LIST
class ListWorkerSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list workers
    """

    class Meta:
        model = Worker
        fields = ["id", "first_name", "last_name", "time", "level"]


class UpdateWorkerSerializer(serializers.ModelSerializer):
    """
    Serializer to update workers
    """

    technologies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Technology.objects.all(),
        write_only=True
    )

    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "time", "level", "technologies"]

    def update(self, instance, validated_data):
        # Extrae las tecnologías del payload
        technologies = validated_data.pop('technologies', [])

        # Actualiza los campos del trabajador
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.time = validated_data.get('time', instance.time)
        instance.level = validated_data.get('level', instance.level)
        instance.save()

        # Asocia las tecnologías
        instance.technologies.set(technologies)
        return instance
