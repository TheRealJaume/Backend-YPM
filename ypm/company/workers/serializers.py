from rest_framework import serializers

# Worker
# GENERIC
from company.company.models import Company
from company.workers.models import Worker


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
        workers = validated_data.pop("workers")
        for worker in workers:
            # Divide the string to extract the first name and the last name
            name_parts = worker.split(" ")

            # Save the first name on a variable
            first_name = name_parts[0]

            # If there's more than one last name, save both on the last name variable
            if len(name_parts) > 1:
                last_name = " ".join(name_parts[1:])
            else:
                last_name = ''

            # Create a new worker
            company_worker = Worker(first_name=first_name, last_name=last_name,
                                    company=Company.objects.get(id=validated_data["company"]))
            company_worker.save()

# LIST
class ListWorkerSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list workers
    """

    class Meta:
        model = Worker
        fields = ["id", "first_name", "last_name", "company"]