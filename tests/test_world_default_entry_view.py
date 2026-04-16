import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.projects.models import Project
from apps.world.models import Location


@pytest.mark.django_db
def test_setting_default_entry_clears_entry_from_on_both_container_and_entry_loc():
    User = get_user_model()
    user = User.objects.create_user(username="owner", password="pw")
    project = Project.objects.create(name="Proj", owner=user)

    # Create locations
    container = Location.objects.create(project=project, name="Building", is_container=True)
    hallway = Location.objects.create(project=project, name="Hallway", parent_location=container)
    outside = Location.objects.create(project=project, name="Outside")

    # Pre-state: both container and hallway have entry_from set (valid before default entry is set)
    container.entry_from = outside
    container.save()
    hallway.entry_from = outside
    hallway.save()

    client = APIClient()
    client.force_authenticate(user)

    url = f"/api/v1/projects/{project.id}/world/locations/{container.id}/default-entry"
    res = client.put(url, {"entry_location_id": str(hallway.id)}, format="json")
    assert res.status_code == 200, res.content

    # Verify state after operation
    container.refresh_from_db()
    hallway.refresh_from_db()
    assert container.default_entry_location_id == hallway.id
    # Container keeps its entry_from under the new rule
    assert container.entry_from_id == outside.id
    # Default entry location itself must not have entry_from
    assert hallway.entry_from_id is None


@pytest.mark.django_db
def test_default_entry_requires_direct_child_and_returns_400_on_validation():
    User = get_user_model()
    user = User.objects.create_user(username="owner2", password="pw")
    project = Project.objects.create(name="Proj2", owner=user)

    container = Location.objects.create(project=project, name="Container", is_container=True)
    not_child = Location.objects.create(project=project, name="Elsewhere")

    client = APIClient()
    client.force_authenticate(user)
    url = f"/api/v1/projects/{project.id}/world/locations/{container.id}/default-entry"
    res = client.put(url, {"entry_location_id": str(not_child.id)}, format="json")
    assert res.status_code == 400
    assert "Default entry must be a direct child" in res.json().get("error", "") or "details" in res.json()
