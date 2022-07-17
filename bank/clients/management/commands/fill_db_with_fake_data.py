from django.core.management import BaseCommand

from clients.models import (
    ClientJob,
    ClientService,
    Client,
    ClientDetail,
)

NAME_FIELD = "name"
PRICE_FIELD = "price"
DESCRIPTION_FIELD = "description"
FIRST_NAME_FIELD = "first_name"
MIDDLE_NAME_FIELD = "middle_name"


def fill_jobs():
    """
    Fill jobs with fake data.
    :return:
    """

    jobs_names = [
        "developer",
        "potter",
        "realtor",
        "sales manager",
        "businessman",
    ]
    jobs = []

    for name in jobs_names:
        job, created = ClientJob.objects.get_or_create(name=name)
        if created:
            jobs.append(job)

    return jobs


def fill_services():
    """
    Fill services with fake data.
    :return:
    """
    services_data = [
        {
            "name": "sms",
            "price": 100,
            "description": "Fee for sms sending",
        },
        {
            "name": "insurance",
            "price": 1000,
            "description": "Subscription provides insurance",
        },
        {
            "name": "priority",
            "price": 3000,
            "description": "Subscription provides priority services",
        },
        {
            "name": "assistance",
            "price": 500,
            "description": "Subscription provides assistance services",
        },
    ]
    services = []

    for data in services_data:
        service, created = ClientService.objects.get_or_create(**data)
        if created:
            services.append(service)
    return services


def fill_clients():
    """
    Fill clients with fake data.
    :return:
    """
    services = ClientService.objects.all()
    clients_data = [
        {
            "first_name": "Jack",
            "middle_name": "Michael",
            "last_name": "Johns",
            "birthday": "1985-03-19",
            "job_id": 1,
        },
        {
            "first_name": "Calla",
            "middle_name": "Harlow",
            "last_name": "Johns",
            "birthday": "2000-06-01",
            "job_id": 4,
        },
        {
            "first_name": "Tom",
            "middle_name": "",
            "last_name": "Black",
            "birthday": "1978-04-29",
            "job_id": 2,
        },
        {
            "first_name": "Jerry",
            "middle_name": "Elliot",
            "last_name": "Smith",
            "birthday": "1988-08-08",
            "job_id": 3,
        },
        {
            "first_name": "Mike",
            "middle_name": "Louise",
            "last_name": "Parker",
            "birthday": "2004-01-16",
            "job_id": 1,
        },
    ]
    clients = []

    for data in clients_data:
        client, created = Client.objects.get_or_create(**data)
        if created:
            clients.append(client)
    return clients


def fill_clients_services():
    """
    Fill clients services with fake data.
    :return:
    """
    services = ClientService.objects.all()
    clients = Client.objects.all()
    services_ids = [
        [0, 2],
        [0],
        [1, 3],
        [1, 2, 3],
        [0, 3],
        [0, 3, 2],
        [0, 3, 2, 1],
        [0, 1],
    ]
    ids_len = len(services_ids)
    i = 0
    for client in clients:
        i = (i + 1) % ids_len
        for service_id in services_ids[i]:
            service = services[service_id]
            client.services.add(service)

    return clients


def fill_details():
    """
    Fill details with fake data.
    :return:
    """
    details_data = [
        {
            "client_id": 1,
            "bio": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet delectus, enim facere fugiat ipsa nobis odit omnis optio perferendis possimus quas, quasi quia reprehenderit, soluta voluptate. Assumenda beatae excepturi ullam.",
        },
        {
            "client_id": 2,
            "bio": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquam animi aspernatur at atque commodi corporis deleniti harum illo ipsam itaque laboriosam nesciunt nulla placeat quisquam recusandae repellendus repudiandae unde, velit. Eos fugiat nam quo vero. Accusantium ad aliquid animi commodi consectetur corporis cupiditate dolor doloremque ducimus error, ex exercitationem expedita facere fuga hic illo inventore ipsa iste laboriosam molestias natus nihil nostrum nulla obcaecati officiis provident quasi, quia quis quod rem similique sit sunt suscipit temporibus tenetur ut vitae? Accusantium atque aut cumque, dolorem laboriosam molestias mollitia non recusandae similique voluptas! Dicta ducimus eius fugit officia optio reiciendis reprehenderit soluta!",
            "income": 100000,
        },
        {
            "client_id": 3,
            "bio": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. A aperiam dolorem ex exercitationem placeat sapiente tempora tempore. Aperiam blanditiis consectetur doloremque eligendi id iste iusto labore mollitia pariatur porro possimus reiciendis rem soluta suscipit tempore unde, voluptates. Illum possimus ratione repellat repellendus voluptatem? Delectus harum itaque nulla quam rerum voluptatum?",
            "income": 150000,
        },
        {
            "client_id": 4,
            "bio": "Lorem ipsum dolor sit amet.",
            "income": 300000,
        },
        {
            "client_id": 5,
            "bio": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut, quisquam?",
            "income": 220000,
        },
    ]
    details = []

    for data in details_data:
        detail, created = ClientDetail.objects.get_or_create(**data)
        if created:
            details.append(detail)
    return details


class Command(BaseCommand):
    """
    Fill db with fake data
    """

    def handle(self, *args, **options):
        # Jobs
        self.stdout.write("Create some jobs")
        jobs = fill_jobs()
        self.stdout.write(f"Created jobs: {jobs}")

        # Services
        self.stdout.write("Create some services")
        services = fill_services()
        self.stdout.write(f"Created services: {services}")

        # Clients
        self.stdout.write("Create some clients")
        clients = fill_clients()
        self.stdout.write(f"Created clients: {clients}")

        # Services for clients
        self.stdout.write("Create some services to clients")
        clients = fill_clients_services()
        self.stdout.write(f"Updated clients: {clients}")

        # Details for clients
        self.stdout.write("Create some details for clients")
        details = fill_details()
        self.stdout.write(f"Created details: {details}")
