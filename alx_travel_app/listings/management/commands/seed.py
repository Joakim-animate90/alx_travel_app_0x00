from django.core.management.base import BaseCommand
from listings.models import Listing, CustomUser
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with sample listings data'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Create a host user if none exists
        host, created = CustomUser.objects.get_or_create(
            email='host@example.com',
            defaults={
                'username': 'host',
                'is_host': True,
                'first_name': 'Sample',
                'last_name': 'Host'
            }
        )
        
        # Sample travel locations
        locations = [
            'Nairobi, Kenya',
            'Mombasa, Kenya',
            'Zanzibar, Tanzania',
            'Cape Town, South Africa',
            'Marrakech, Morocco',
            'Victoria Falls, Zimbabwe',
            'Serengeti, Tanzania',
            'Maasai Mara, Kenya',
            'Lamu, Kenya',
            'Diani, Kenya'
        ]
        
        # Sample property types
        property_types = [
            'Beachfront Villa',     
            'Mountain Cabin',
            'City Apartment',
            'Safari Lodge',
            'Desert Camp',
            'Luxury Penthouse',
            'Countryside Cottage',
            'Treehouse Retreat',
            'Boutique Hotel',
            'Private Island',    
        ]
        
        # Create sample listings
        listings = []
        for i in range(20):
            title = f"{random.choice(property_types)} in {random.choice(locations)}"
            listings.append(Listing(
                title=title,
                description=fake.paragraph(nb_sentences=5),
                location=title.split(' in ')[1],
                price_per_night=round(random.uniform(50, 500), 2),
                max_guests=random.randint(1, 10),
                host=host
            ))
        
        # Bulk create listings
        Listing.objects.bulk_create(listings)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded 20 sample listings'))
