"""
Management command to seed the database with sample plant data.

Usage:
    python manage.py seed_plants

Clears all existing plants and inserts ~10 fresh samples with images
downloaded from Unsplash (free, no attribution required for seed use).

NOTE: pip install Pillow is required for ImageField support.
NOTE: An internet connection is needed on first run to fetch images.
"""
import os
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from plants.models import Plant


PLANTS_DATA = [
    {
        'name': 'Olive Tree',
        'about': (
            'The olive tree (Olea europaea) is one of the oldest cultivated trees in the world, '
            'native to the Mediterranean basin. It is an evergreen tree known for its gnarled trunk, '
            'silver-green leaves, and small, oval fruits. Olive trees can live for thousands of years '
            'and are a symbol of peace, wisdom, and longevity.'
        ),
        'used_for': (
            'Olive oil production, table olives, traditional medicine, woodworking, '
            'and as an ornamental landscape tree.'
        ),
        'category': Plant.Category.TREE,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1598512752271-33f913a5af13?w=800&q=80',
        'image_filename': 'olive_tree.jpg',
    },
    {
        'name': 'Date Palm',
        'about': (
            'The date palm (Phoenix dactylifera) is a flowering plant species in the palm family '
            'cultivated for its sweet, edible fruits. It thrives in hot, arid climates and has been '
            'a staple food source in the Middle East and North Africa for thousands of years. '
            'It can grow up to 30 metres tall.'
        ),
        'used_for': (
            'Fruit production (dates), sugar extraction, palm frond weaving, timber, '
            'and traditional medicine.'
        ),
        'category': Plant.Category.TREE,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&q=80',
        'image_filename': 'date_palm.jpg',
    },
    {
        'name': 'Rose',
        'about': (
            'The rose (Rosa) is a woody perennial flowering plant of the genus Rosa in the family '
            'Rosaceae. Roses are renowned for their beauty and fragrance. There are over 300 species '
            'and thousands of cultivars. They grow as shrubs, climbers, and trailing plants, with '
            'blooms in nearly every colour.'
        ),
        'used_for': (
            'Ornamental gardening, perfume and essential oil extraction (rose water, attar of roses), '
            'culinary decoration, and gift-giving.'
        ),
        'category': Plant.Category.FLOWER,
        'is_edible': False,
        'image_url': 'https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=800&q=80',
        'image_filename': 'rose.jpg',
    },
    {
        'name': 'Mint',
        'about': (
            'Mint (Mentha) is a genus of plants in the family Lamiaceae. It is an aromatic herb '
            'known for its refreshing, cool scent and flavour. Mint spreads rapidly via underground '
            'runners and is found in moist habitats worldwide. Common varieties include spearmint '
            'and peppermint.'
        ),
        'used_for': (
            'Culinary seasoning (teas, salads, sauces), digestive medicine, oral hygiene products, '
            'aromatherapy, and insect repellent.'
        ),
        'category': Plant.Category.HERB,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=800&q=80',
        'image_filename': 'mint.jpg',
    },
    {
        'name': 'Tomato',
        'about': (
            'The tomato (Solanum lycopersicum) is a plant in the nightshade family, native to South '
            'America. It produces edible, often red, berry-like fruits that are one of the most '
            'widely consumed vegetables (botanically a fruit) in the world. Tomatoes are rich in '
            'vitamins C and K, potassium, and lycopene.'
        ),
        'used_for': (
            'Fresh eating, sauces, soups, salads, ketchup, canning, juices, and as a base '
            'for countless cooked dishes worldwide.'
        ),
        'category': Plant.Category.VEGETABLE,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1582284540020-8acbe03f4924?w=800&q=80',
        'image_filename': 'tomato.jpg',
    },
    {
        'name': 'Watermelon',
        'about': (
            'Watermelon (Citrullus lanatus) is a flowering plant species native to tropical and '
            'subtropical Africa. It produces large, smooth, green-rinded fruits with sweet red or '
            'yellow flesh, packed with water (about 92%). Watermelons are one of the most popular '
            'summer fruits worldwide.'
        ),
        'used_for': (
            'Fresh fruit consumption, juices, smoothies, salads, and the seeds are edible when roasted.'
        ),
        'category': Plant.Category.FRUIT,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1563114773-84221bd62daa?w=800&q=80',
        'image_filename': 'watermelon.jpg',
    },
    {
        'name': 'Basil',
        'about': (
            'Basil (Ocimum basilicum) is a culinary herb of the family Lamiaceae, native to tropical '
            'regions from central Africa to Southeast Asia. It is a tender plant highly sensitive to '
            'cold. Sweet basil is the most commonly grown variety, with fragrant, bright-green leaves '
            'and small white flowers.'
        ),
        'used_for': (
            'Italian and Asian cuisine (pesto, pasta, salads), herbal teas, aromatherapy, '
            'and traditional medicine for digestive and anti-inflammatory purposes.'
        ),
        'category': Plant.Category.HERB,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
        'image_filename': 'basil.jpg',
    },
    {
        'name': 'Cactus',
        'about': (
            'Cacti (family Cactaceae) are succulent plants native to the Americas, adapted to '
            'survive in extremely dry environments. They store water in their thick, fleshy stems '
            'and are protected by sharp spines. There are over 1,700 species ranging from tiny '
            'ground-huggers to towering saguaro giants.'
        ),
        'used_for': (
            'Ornamental landscaping and indoor decoration, water storage research, some species '
            'used in fencing. Prickly pear cactus fruits are edible, though most species are not.'
        ),
        'category': Plant.Category.TREE,
        'is_edible': False,
        'image_url': 'https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=800&q=80',
        'image_filename': 'cactus.jpg',
    },
    {
        'name': 'Lavender',
        'about': (
            'Lavender (Lavandula) is a genus of 47 known species of flowering plants in the mint '
            'family. Native to the Old World, it is best known for its beautiful purple flowers and '
            'calming fragrance. Lavender thrives in sunny, well-drained conditions and is a favourite '
            'in herb gardens worldwide.'
        ),
        'used_for': (
            'Aromatherapy, essential oils, perfumery, culinary flavouring (baked goods, teas), '
            'sleep aids, and as an ornamental garden plant.'
        ),
        'category': Plant.Category.FLOWER,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800&q=80',
        'image_filename': 'lavender.jpg',
    },
    {
        'name': 'Sunflower',
        'about': (
            'The sunflower (Helianthus annuus) is a large annual forb native to North America. '
            'It is known for its large, daisy-like flower head up to 30 cm wide with bright yellow '
            'petals and a central brown disc. Sunflowers are notably heliotropic in their bud stage, '
            'tracking the sun across the sky.'
        ),
        'used_for': (
            'Sunflower oil production, edible seeds (snacks, baking), birdseed, '
            'ornamental gardening, and biofuel research.'
        ),
        'category': Plant.Category.FLOWER,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=800&q=80',
        'image_filename': 'sunflower.jpg',
    },
    {
        'name': 'Aloe Vera',
        'about': (
            'Aloe vera is a succulent plant species of the genus Aloe, originally from the Arabian '
            'Peninsula. It has thick, fleshy, green leaves edged with small teeth. The leaves contain '
            'a clear gel rich in vitamins, minerals, and antioxidants. It thrives in dry, tropical, '
            'and semi-tropical climates and is widely cultivated as an ornamental and medicinal plant.'
        ),
        'used_for': (
            'Skin care and cosmetics (gels, lotions, sunburn relief), traditional medicine, '
            'dietary supplements, and as an ornamental houseplant.'
        ),
        'category': Plant.Category.HERB,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1567331711402-509c12c41959?w=800&q=80',
        'image_filename': 'aloe_vera.jpg',
    },
    {
        'name': 'Mango',
        'about': (
            'The mango (Mangifera indica) is a tropical tree native to South Asia and one of the most '
            'widely cultivated fruits in the world. It belongs to the cashew family Anacardiaceae. '
            'Mango trees can grow up to 40 metres tall and live for over 300 years. The fruit ranges '
            'from green to yellow, orange, or red and has juicy, sweet, aromatic flesh.'
        ),
        'used_for': (
            'Fresh fruit consumption, juices, smoothies, pickles, chutneys, dried fruit snacks, '
            'and traditional Ayurvedic medicine.'
        ),
        'category': Plant.Category.FRUIT,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=800&q=80',
        'image_filename': 'mango.jpg',
    },
    {
        'name': 'Tulip',
        'about': (
            'Tulips (Tulipa) are a genus of spring-blooming perennial herbaceous bulbiferous geophytes '
            'in the lily family Liliaceae. Native to Central Asia, they were brought to Europe in the '
            '16th century and sparked the famous "Tulip Mania" in the Netherlands. With over 3,000 '
            'registered cultivars, tulips come in nearly every colour and are one of the world\'s '
            'most recognised flowers.'
        ),
        'used_for': (
            'Ornamental gardening, cut flower industry, floral arrangements, and symbolic use '
            'in cultural celebrations and national identity (Netherlands).'
        ),
        'category': Plant.Category.FLOWER,
        'is_edible': False,
        'image_url': 'https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=800&q=80',
        'image_filename': 'tulip.jpg',
    },
    {
        'name': 'Garlic',
        'about': (
            'Garlic (Allium sativum) is a species of bulbous flowering plant in the genus Allium. '
            'Native to Central Asia, it has been used as both food and traditional medicine for '
            'thousands of years. The plant grows to about 1 metre in height and produces a bulb '
            'made up of individual cloves wrapped in papery skin. Its pungent flavour comes from '
            'organosulfur compounds, especially allicin.'
        ),
        'used_for': (
            'Culinary seasoning worldwide, antibacterial and antifungal medicine, '
            'cardiovascular health supplements, and as a natural insect repellent in gardens.'
        ),
        'category': Plant.Category.VEGETABLE,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?w=800&q=80',
        'image_filename': 'garlic.jpg',
    },
    {
        'name': 'Bamboo',
        'about': (
            'Bamboo is a subfamily of flowering perennial evergreen plants in the grass family Poaceae. '
            'It is one of the fastest-growing plants on Earth, with some species growing up to 91 cm '
            'per day. There are over 1,400 bamboo species found across Asia, Africa, and the Americas. '
            'Despite its grass classification, bamboo can reach heights of over 30 metres.'
        ),
        'used_for': (
            'Construction and flooring, furniture, paper production, edible shoots (bamboo shoots), '
            'musical instruments, and sustainable packaging material.'
        ),
        'category': Plant.Category.TREE,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1509909756405-be0199881695?w=800&q=80',
        'image_filename': 'bamboo.jpg',
    },
    {
        'name': 'Strawberry',
        'about': (
            'The garden strawberry (Fragaria × ananassa) is a widely grown hybrid species of the '
            'genus Fragaria, first bred in Brittany, France, in the 1750s. It is cultivated worldwide '
            'for its heart-shaped, bright red, juicy fruit. The plant is a low-growing perennial '
            'that spreads via runners, producing small white flowers before fruiting.'
        ),
        'used_for': (
            'Fresh eating, jams, jellies, juices, desserts, ice cream, and as a flavouring '
            'in confectionery and cosmetics.'
        ),
        'category': Plant.Category.FRUIT,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=800&q=80',
        'image_filename': 'strawberry.jpg',
    },
    {
        'name': 'Rosemary',
        'about': (
            'Rosemary (Salvia rosmarinus, formerly Rosmarinus officinalis) is a fragrant evergreen '
            'herb native to the Mediterranean region. It belongs to the mint family Lamiaceae and '
            'grows as a woody shrub with needle-like leaves and small blue, pink, or white flowers. '
            'It has been used in cooking and medicine since ancient times.'
        ),
        'used_for': (
            'Culinary seasoning for meats, breads, and soups; herbal medicine for memory and '
            'circulation; aromatherapy; and as a garden ornamental.'
        ),
        'category': Plant.Category.HERB,
        'is_edible': True,
        'image_url': 'https://images.unsplash.com/photo-1604480133435-25b86862d276?w=800&q=80',
        'image_filename': 'rosemary.jpg',
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample plant data (clears existing plants first).'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing plants...')
        Plant.objects.all().delete()

        media_plants_dir = os.path.join('media', 'plants')
        os.makedirs(media_plants_dir, exist_ok=True)

        for data in PLANTS_DATA:
            self.stdout.write(f"  Adding {data['name']}...")
            filename = data['image_filename']
            local_path = os.path.join(media_plants_dir, filename)

            # Download image if not already cached
            if not os.path.exists(local_path):
                try:
                    req = urllib.request.Request(
                        data['image_url'],
                        headers={'User-Agent': 'Mozilla/5.0 (PlanteerSeeder/1.0)'}
                    )
                    with urllib.request.urlopen(req, timeout=15) as response:
                        img_data = response.read()
                    with open(local_path, 'wb') as f:
                        f.write(img_data)
                    self.stdout.write(f"    Downloaded image for {data['name']}")
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"    Could not download image for {data['name']}: {e}")
                    )
                    img_data = None

            plant = Plant(
                name=data['name'],
                about=data['about'],
                used_for=data['used_for'],
                category=data['category'],
                is_edible=data['is_edible'],
            )

            if os.path.exists(local_path):
                with open(local_path, 'rb') as f:
                    plant.image.save(filename, ContentFile(f.read()), save=False)

            plant.save()

        count = Plant.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nDone! {count} plants seeded successfully.'))
