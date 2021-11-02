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

    def tearDown(self):
        '''
        Function to delete every test instance after it runs
        '''
        Neighbourhood.objects.all().delete()

    def create_hood_test(self):
        '''
        Tests that a new hood is saved 
        '''
        self.hood.create_hood()
        hoodlist = Neighbourhood.objects.all()
        self.assertTrue(len(hoodlist)==1)

    def delete_hood_test(self):
        '''
        Tests that a Neighborhood instance can be deleted
        '''
        self.hood.save()
        Neighbourhood.delete(self.hood)
        hoodlist = Neighbourhood.objects.all()
        self.assertEqual(len(hoodlist,0))