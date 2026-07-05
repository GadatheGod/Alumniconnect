import random
from django.core.management.base import BaseCommand
from alumni.models import User, AlumniProfile


FIRST_NAMES = ['Arun', 'Balu', 'Cyrus', 'Deepak', 'Elango', 'Feroz', 'Ganesh', 'Harish', 'Irfan', 'Jegan', 'Karthik', 'Lakshmi', 'Mohan', 'Naveen', 'Omar', 'Prakash', 'Rajan', 'Senthil', 'Thamizhan', 'Uma', 'Amutha', 'Bhama', 'Chitra', 'Divya', 'Elavarasi', 'Farha', 'Gayathri', 'Hemalatha', 'Indira', 'Janani', 'Kavitha', 'Meena', 'Nalini', 'Priya', 'Renuka', 'Saranya', 'Thulasi', 'Usha']
LAST_NAMES = ['Balakrishnan', 'Murugan', 'Subramanian', 'Rajamanickam', 'Gnanasekar', 'Thangavelu', 'Krishnasamy', 'Pandian', 'Sundaram', 'Velayudham', 'Anbarasan', 'Chellappan', 'Devarajan', 'Easwaran', 'Fathima', 'Gobi', 'Hemanth', 'Iyappan', 'Jeyaraman', 'Kannan']
NATIVE_LOCATIONS = ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Thoothukudi', 'Dindigul', 'Thanjavur', 'Ramanathapuram', 'Tiruppur', 'Nagercoil', 'Karur']
COMPANIES = ['TCS', 'Infosys', 'Wipro', 'HCL', 'Tech Mahindra', 'Cognizant', 'Accenture', 'Deloitte', 'Flipkart', 'Amazon', 'Google', 'Microsoft', 'Adobe', 'Oracle', 'SAP', 'IBM', 'Capgemini', 'Zoho', 'Freshworks', 'Ramco']
ROLES = ['Software Engineer', 'Developer', 'Analyst', 'Manager', 'Lead', 'Architect', 'Designer', 'Consultant', 'Team Lead', 'Director']
CITIES = ['Chennai', 'Coimbatore', 'Bangalore', 'Hyderabad', 'Pune', 'Mumbai', 'Delhi', 'Singapore', 'Dubai', 'USA', 'UK', 'Australia']
DEPARTMENTS = ['CSE', 'ECE', 'MECH', 'CE', 'EEE', 'IT', 'AIME', 'BTECH', 'MBA', 'MCA', 'MTECH']
SUPPORT_MODES = ['online', 'offline', 'both', 'not_possible']
VISIT_FREQS = ['monthly', 'quarterly', 'yearly', 'rarely', 'never']
SUPPORT_OFFERINGS = [
    'Hiring in IT, connections in software companies',
    'Banking sector network, finance mentorship',
    'Manufacturing industry contacts, plant visits',
    'Startup ecosystem, funding connections',
    'Higher education guidance, PhD recommendations',
    'Real estate investments, property connections',
    'Healthcare sector network, hospital contacts',
    '',
]


class Command(BaseCommand):
    help = 'Seed the database with sample alumni data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=20, help='Number of sample alumni to create')

    def handle(self, *args, **options):
        count = options['count']
        created = 0

        for i in range(count):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = f'seed{i+1}@alumniconnect.org'
            phone = '9' + str(random.randint(1000000000, 9999999999))
            department = random.choice(DEPARTMENTS)
            year = random.randint(2000, 2024)
            company = random.choice(COMPANIES) if random.random() > 0.2 else ''
            role = random.choice(ROLES) if company else ''
            city = random.choice(CITIES) if random.random() > 0.3 else ''
            native_location = random.choice(NATIVE_LOCATIONS)
            support_mode = random.choice(SUPPORT_MODES)
            visit_freq = random.choice(VISIT_FREQS)
            free_days = random.choice(['Weekends', 'Monday-Friday evenings', 'Anytime', 'Saturday only', ''])
            willing = random.random() > 0.3
            support = random.choice(SUPPORT_OFFERINGS)

            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name,
                    password='testpass123',
                )

                AlumniProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    department=department,
                    year_of_passing=year,
                    current_company=company,
                    current_role=role,
                    current_city=city,
                    native_location=native_location,
                    support_mode=support_mode,
                    visit_frequency_coimbatore=visit_freq,
                    free_to_talk_days=free_days,
                    willing_to_mentor=willing,
                    support_offered=support,
                )
                created += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipped {email}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Created {created} sample alumni records. Password for all: testpass123'))
