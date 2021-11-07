from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.http import Http404
from pet.models import Owner, Pet


class DemoTests(TestCase):
    items = [
        {"owner": 'Katie', "pet": ['Toto', 'Kitty']},
        {"owner": 'Sue', "pet": ['Bunny', 'Scott']},
        {"owner": 'Lynn', "pet": ['Skylar']},
    ]
    owner_names = [item["owner"] for item in items]
    # ['Katie', 'Sue', 'Lynn']
    pet_names = [name for item in items for name in item["pet"]]
    # ['Toto', 'Kitty', 'Bunny', 'Scott', 'Skylar']

    # Given an owner name, return their a list of pets or an empty list
    def pets_by_owner(self, owner):
        for item in self.items:
            if item["owner"] == owner:
                return item["pet"]
        return []

    # Create data in the database once
    def setUp(self):
        for item in self.items:
            owner = Owner.objects.create(name=item["owner"])
            for pet in item["pet"]:
                Pet.objects.create(name=pet, owner=owner)

        self.assertEqual(
            Owner.objects.all().count(),
            len(self.owner_names))
        self.assertEqual(
            Pet.objects.all().count(),
            len(self.pet_names))

    # Query for a non-existing owner
    def test_owner_not_found(self):
        print(f'\nRunning {self.id()}\n')
        names = list(self.owner_names)
        names.append('Lisa')
        for name in names:
            try:
                owner = get_object_or_404(Owner, name=name)
                self.assertEqual(owner.name, name)
            except Http404:
                print(f"Owner {name} not found")

    # Return the count of pet objects in database
    def test_pet_count(self):
        print(f'\nRunning {self.id()}\n')

        for name in self.owner_names:
            self.assertEqual(
                Pet.objects.filter(owner__name=name).count(),
                len(self.pets_by_owner(name)))

    # Query for a non-existing pet
    def test_pet_not_found(self):
        print(f'\nRunning {self.id()}\n')
        try:
            name = 'Sugar'
            get_object_or_404(Pet, name=name)
        except Http404:
            print(f"Pet {name} not found")

    # Delete an existing pet
    def test_delete_pet(self):
        print(f'\nRunning {self.id()}\n')
        name = 'Kitty'

        deleted_objects = Pet.objects.filter(name=name).delete()
        self.assertEqual(deleted_objects[0], self.pet_names.count(name))

        owner = Owner.objects.filter(pet__name=name)
        print(owner)
        self.assertEqual(owner.count(), 0)

    # Delete an existing owner
    def test_delete_owner(self):
        print(f'\nRunning {self.id()}\n')
        owner = 'Lynn'

        # Return Pet objects belonging to owner name
        pets = Pet.objects.filter(owner__name=owner)
        print(pets)

        # Delete owner by name
        try:
            deleted_owner = Owner.objects.get(name=owner).delete()
            # deleted_owner (2, {'pet.Pet': 1, 'pet.Owner': 1})
            self.assertEqual(deleted_owner[0], 2)
        except Http404:
            print(f"Owner '{owner}' not found!")

        # When an owner is deleted, so are their pets
        for p in pets:
            print(p)
            self.assertEqual(
                Pet.objects.filter(p__owner__name=owner).count(),
                0)

    # Add a pet to an existing owner
    def test_add_pet(self):
        print(f'\nRunning {self.id()}\n')
        pet = 'Liz'
        owner = 'Sue'

        try:
            sue = Owner.objects.get(name=owner)
            sue.pet_set.add(Pet.objects.create(name=pet, owner=sue))
        except Http404:
            print(f"Owner '{owner}' not found!")

        self.assertEqual(
            Pet.objects.filter(owner__name=owner).count(),
            len(self.pets_by_owner(owner))+1)

    # Update the name of an existing pet
    def test_update_pet_name(self):
        print(f'\nRunning {self.id()}\n')
        owner = 'Sue'
        old_name = 'Scott'
        new_name = 'Scoot'

        try:
            pet = get_object_or_404(Pet, owner__name=owner, name=old_name)
            pet.name = new_name
            pet.save()
        except Http404:
            print(f"Pet '{old_name}' for owner '{owner}' not found!")

        try:
            pet = get_object_or_404(Pet, owner__name=owner, name=old_name)
        except Http404:
            print(f"Pet '{old_name}' for owner '{owner}' not found!")
