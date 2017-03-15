'''
Created on 14 de mar de 2017

@author: alirio
'''
from tastypie.serializers import Serializer

class CSVSerializer(Serializer):
    formats = Serializer.formats + ['csv']

    content_types = dict(Serializer.content_types.items() + [('csv', 'multipart/form-data')])

    def from_csv(self, content):
        dict = {}
        lines = content.splitlines()
        
        ''' Retira o cabecalho(4 primeiras linhas) e o rodape(2 ultimas linhas) do arquivo anexado(Content-Type: multipart/form-data) para so usar o conteudo do arquivo'''
        lines = lines[4: lines.__len__()-2]
        
        dict['lines'] = lines
        
        return dict
    