from django.core.management import BaseCommand

from app.models import Cliente


class Command(BaseCommand):

    def add_arguments(self, parser):
        # receive file csv to load
        parser.add_argument('file', type=str, help='file to load')

    def handle(self, *args, **options):
        # parse data and save model
        file = options['file']
        print(file)
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                data = line.split(',')
                print(data)
                cliente = Cliente()
                cliente.nome = data[-1]
                cliente.endereco = data[5]
                if len(data[6]) > 5:
                    cliente.numero = data[7]
                    cliente.phone = data[11]
                else:
                    cliente.numero = data[6]
                    cliente.bairro = data[3]
                    cliente.cidade = data[4]
                    cliente.phone = data[10]
                print(cliente.nome, cliente.endereco, cliente.numero, cliente.bairro, cliente.cidade, cliente.phone)
                cliente.save()
