import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from apps.projects.models import Project
from apps.world.models import Location


@pytest.mark.django_db
def test_container_with_default_entry_forbids_descendant_entry_from():
    User = get_user_model()
    user = User.objects.create_user(username="u1", password="pw")
    project = Project.objects.create(name="P", owner=user)

    home = Location.objects.create(
        project=project, name="Home", is_container=True
    )
    living_room = Location.objects.create(
        project=project, name="Living Room", parent_location=home
    )
    # set default entry for the container
    home.default_entry_location = living_room
    home.save()

    kitchen = Location.objects.create(
        project=project, name="Kitchen", parent_location=home
    )

    # Attempt to set entry_from to its ancestor container that has a default entry
    kitchen.entry_from = home
    with pytest.raises(ValidationError):
        kitchen.save()


@pytest.mark.django_db
def test_container_with_default_entry_allows_outer_entry_from():
    User = get_user_model()
    user = User.objects.create_user(username="u2", password="pw")
    project = Project.objects.create(name="P2", owner=user)

    # Container A with default entry
    a = Location.objects.create(project=project, name="A", is_container=True)
    a_hub = Location.objects.create(project=project, name="A-Hub", parent_location=a)
    a.default_entry_location = a_hub
    a.save()

    # Inner under A (to confirm inner is blocked separately)
    a_room = Location.objects.create(project=project, name="A-Room", parent_location=a)

    # Outer location B (not a descendant of A)
    b = Location.objects.create(project=project, name="B")

    # Outer is allowed to use container A as entry_from
    b.entry_from = a
    b.save()  # should not raise
    b.refresh_from_db()
    assert b.entry_from_id == a.id

    # Inner remains forbidden
    a_room.entry_from = a
    with pytest.raises(ValidationError):
        a_room.save()


@pytest.mark.django_db
def test_container_with_default_entry_can_have_entry_from():
    """A container that has a default entry may itself have entry_from set."""
    User = get_user_model()
    user = User.objects.create_user(username="u2b", password="pw")
    project = Project.objects.create(name="P2b", owner=user)

    container = Location.objects.create(project=project, name="Container", is_container=True)
    hub = Location.objects.create(project=project, name="Hub", parent_location=container)
    container.default_entry_location = hub
    container.save()

    outside = Location.objects.create(project=project, name="Outside")

    # Under the new rule, this is allowed
    container.entry_from = outside
    container.save()
    container.refresh_from_db()
    assert container.entry_from_id == outside.id


@pytest.mark.django_db
def test_cross_container_boundary_outer_allowed_inner_blocked():
    User = get_user_model()
    user = User.objects.create_user(username="u3", password="pw")
    project = Project.objects.create(name="P3", owner=user)

    # Two top-level containers
    left = Location.objects.create(project=project, name="Left", is_container=True)
    left_hub = Location.objects.create(project=project, name="Left-Hub", parent_location=left)
    left.default_entry_location = left_hub
    left.save()

    right = Location.objects.create(project=project, name="Right", is_container=True)
    right_room = Location.objects.create(project=project, name="Right-Room", parent_location=right)

    # Outer connection from Right-Room to Left container is allowed
    right_room.entry_from = left
    right_room.save()
    right_room.refresh_from_db()
    assert right_room.entry_from_id == left.id

    # Inner descendant of Left is still blocked
    left_child = Location.objects.create(project=project, name="Left-Child", parent_location=left)
    left_child.entry_from = left
    with pytest.raises(ValidationError):
        left_child.save()
