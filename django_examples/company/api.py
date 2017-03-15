import logging
from tastypie.authorization import Authorization
from tastypie.resources import Resource, ModelResource
from model import Client
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpCreated, HttpAccepted
from django.http.response import JsonResponse
from django_examples.company.cors import CSVSerializer

logger = logging.getLogger()


class ClientResource(ModelResource ):
    
    class Meta:
        allowed_methods = ['get', 'post', 'put', 'delete']
        queryset = queryset = Client.objects.all()
        resource_name = 'client'
        authorization = Authorization()
        
        """Campos excluidos na resposta"""
        excludes = ['id',]
        
        """Filtros disponiveis. ex: http://127.0.0.1:8080/sms-api/api/v1/sms/simulator?mail=contact@client1.com"""
        filtering = {
            'mail': ('exact',),
        }
        
    def get_object_list(self, bundle, **kwargs):
        logger.info('Method to GET log message.')
        return super(ClientResource, self).get_object_list(bundle, **kwargs)
    
    def obj_get(self, bundle, **kwargs):
        return super(ClientResource, self).obj_get(bundle=bundle, **kwargs)
    
    def obj_create(self, bundle, **kwargs):
        logger.info('Method to POST log message.')
        return super(ClientResource, self).obj_create(bundle, **kwargs)
    
    def obj_update(self, bundle, **kwargs):
        logger.info('Method to PUT log message.')
        return super(ClientResource, self).obj_update(bundle, **kwargs)
    
    def obj_delete(self, bundle, **kwargs):
        logger.info('Method to DELETE log message.')
        return super(ClientResource, self).obj_delete(bundle, **kwargs)

    
class ExemploResource(Resource):
    
    class Meta:
        allowed_methods = ['post']
        resource_name = 'exemplo'
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        
        logger.info('REQUEST: %s', bundle.data)
        
        try:
            mensagem = bundle.data['mensagem']
        except KeyError, e:
            logger.error('Faltando o parametro %s.' %str(e))
            raise ImmediateHttpResponse(HttpBadRequest(JsonResponse({'error':'Faltando o parametro %s.' %str(e)})))
        
        raise ImmediateHttpResponse(HttpCreated(JsonResponse({'success':'Mensagem recebida foi = %s' %str(mensagem)})))
    
    
class CsvResource(Resource):
    
    class Meta:
        allowed_methods = ['post']
        authorization = Authorization()
        resource_name = 'csv'
        serializer = CSVSerializer()
        always_return_data = True
        
    def obj_create(self, bundle, **kwargs):
        
        lines = bundle.data.get('lines')
        
        if len(lines) == 1:
            logger.error('error: Arquivo contem apenas a linha de cabecalho.')
            raise ImmediateHttpResponse(HttpBadRequest(JsonResponse({'error':'Arquivo contem apenas a linha de cabecalho.'})))
        elif len(lines) < 2:
            logger.error('error: Arquivo importado nao contem registros.')
            raise ImmediateHttpResponse(HttpBadRequest(JsonResponse({'error':'Arquivo importado nao contem registros.'})))
        
        ''' Pega cabecalho(linha 0) do CSV '''
        row_names = lines[0].split(";")
        logger.info('Cabecalho(linha 0) do arquivo CSV: {0}.'.format(row_names))
        
        ''' Retira o cabecalho(linha 0) do CSV '''
        lines = lines[1:len(lines)]
        
        ''' Cria lista de jsons(chave,valor) a partir das demais linhas do CSV '''
        jsons = []
        for line in lines:
            json_data = {}
            for x, row_name in enumerate(row_names):
                json_data[str(row_name)] = str(line.split(";")[x])
            jsons.append(json_data)
            
        for i, json in enumerate(jsons):
            logger.info('JSON gerado a partir da linha {0} do arquivo CSV: {1}.'.format(i+2, json))
            
        raise ImmediateHttpResponse(HttpAccepted(JsonResponse({'lines':jsons})))
    