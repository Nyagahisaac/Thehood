from django.test import TestCase
from .models import Neighbourhood,Business,User

# Create your tests here.

class NeighbourhoodTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.molly = Neighbourhood(name='Juja', location='Nairobi', no_occupant='500')

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.molly,Neighbourhood))
        
    # Testing save method
    def test_save_method(self):
        self.molly.save_neighbour()
        neighbour = Neighbourhood.objects.all()
        self.assertTrue(len(neighbour) > 0)