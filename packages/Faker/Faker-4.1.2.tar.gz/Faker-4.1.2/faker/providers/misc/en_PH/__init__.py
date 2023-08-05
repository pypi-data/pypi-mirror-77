from .. import Provider as MiscProvider


class Provider(MiscProvider):
    """
    Provider for miscellaneous data for en_PH locale

    This class also houses all other provider methods that would have otherwise been weird to place in another provider.
    """

    gemstone_names = (
        'Agate', 'Amber', 'Amethyst', 'Aquamarine', 'Citrine', 'Diamond', 'Emerald', 'Garnet', 'Jade', 'Jasper',
        'Lapis Lazuli', 'Moonstone', 'Onyx', 'Opal', 'Peridot', 'Ruby', 'Sapphire', 'Sardonyx', 'Sunstone', 'Topaz',
        'Turquoise', 'Zircon',
    )
    mountain_names = (
        'Apo', 'Arayat', 'Atok', 'Banahaw', 'Bulusan', 'Caraballo', 'Cordillera', 'Cresta', 'Halcon', 'Hibok-Hibok',
        'Iriga', 'Kanlaon', 'Makiling', 'Malinao', 'Mariveles', 'Matumtum', 'Mayon', 'Palali', 'Palanan', 'Pao',
        'Pinatubo', 'Samat', 'Sicaba', 'Sierra Madre', 'Tabayoc',
    )
    plant_names = (
        'Acacia', 'Agoho', 'Akle', 'Anahaw', 'Anonas', 'Anubing', 'Aranga', 'Asparagus', 'Atis', 'Avocado', 'Azalea',
        'Azucena', 'Bagtikan', 'Bakawan', 'Balete', 'Balimbing', 'Banaba', 'Banuyo', 'Banyan', 'Baticulin', 'Batino',
        'Bauhinia', 'Bouganvilla', 'Caballero', 'Cabbage', 'Calantas', 'Calumpang', 'Camachile', 'Camia', 'Campanilla',
        'Carissa', 'Carrot', 'Catmon', 'Cattleya', 'Cauliflower', 'Celery', 'Champaca', 'Chico', 'Coconut', 'Cucumber',
        'Cypress', 'Dao', 'Dapdap', 'Dita', 'Duhat', 'Dungon', 'Gladiola', 'Gloriosa', 'Granada', 'Guijo', 'Gumamela',
        'Intsia', 'Ipil', 'Jacaranda', 'Jasmine', 'Kaimito', 'Kalachuchi', 'Kalamansi', 'Kamagong', 'Kamias',
        'Lanzones', 'Lawaan', 'Lily', 'Lumbayao', 'Mabolo', 'Macapuno', 'Macopa', 'Magnolia', 'Mahogany', 'Malugay',
        'Mayapis', 'Melon', 'Milflower', 'Molave', 'Mushroom', 'Mustard', 'Narra', 'Nipa', 'Oleander', 'Oliva',
        'Orchid', 'Palm', 'Pandan', 'Pepper', 'Piña', 'Raddish', 'Rosas', 'Sampaguita', 'Sampaloc', 'Santan', 'Santol',
        'Sineguelas', 'Squash', 'Supa', 'Talisay', 'Tamarind', 'Tanguile', 'Tindalo', 'Tulip', 'Yakal', 'Zinia',
    )
    space_object_names = (
        'Andromeda', 'Antares', 'Aquarius', 'Aries', 'Asteroid', 'Cancer', 'Canopus', 'Capricorn', 'Comet',
        'Constellation', 'Earth', 'Galaxy', 'Gemini', 'Hercules', 'Hydra', 'Juno', 'Jupiter', 'Leo', 'Libra', 'Mars',
        'Mercury', 'Milky Way', 'Neptune', 'Orion', 'Pisces', 'Planet', 'Pluto', 'Polaris', 'Sagittarius', 'Saturn',
        'Scorpio', 'Taurus', 'Uranus', 'Venus', 'Virgo', 'Zodiac',
    )
    random_object_names = gemstone_names + mountain_names + plant_names + space_object_names

    def gemstone_name(self):
        return self.random_element(self.gemstone_names)

    def mountain_name(self):
        return self.random_element(self.mountain_names)

    def plant_name(self):
        return self.random_element(self.plant_names)

    def space_object_name(self):
        return self.random_element(self.space_object_names)

    def random_object_name(self):
        return self.random_element(self.random_object_names)
