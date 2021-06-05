import requests
import json
import pprint

def get_ids(info):
    ids_particulares = list()
    for element in info:
        ids_ = element.get('contentIds')
        if ids_ : 
            ids_particulares += ids_
    return ids_particulares

def get_generos(data_content):
    Generos=[]
    for genre in data_content:
        try:
            gen=genre['description']
            Generos.append(gen)
        except Exception:
            Generos.append('none')             
    return Generos

def get_cast(data_content):
    credits_ = list()
    for credit in data_content:
        if credit['keyedRoles'][0]['key'] == 'C':
            credits_.append(credit['name'])
    return credits_

#Devuelvo int con la cantidad de episodios de una serie // Podría devolver toda la info de las temporadas porque lo tengo en la info recuperada
def get_temporadas(data_content):
    if data_content:
        cantTemp=0
        for season in data_content:
            cantTemp=cantTemp+1
    return cantTemp 

def get_catalogo(id_):
    url = "https://playdata.starz.com/metadata-service/play/partner/Web_ES/v8/content?lang=es-ES&contentIds={}&includes=title,logLine,contentType,contentId,ratingName,genres,properCaseTitle,topContentId,releaseYear,runtime,images,credits,episodeCount,seasonNumber,childContent,orderapi".format(id_)
    
    page = requests.get(url)
    page = page.json()

    try:
        data_content = page['playContentArray']['playContents'][0]
    except Exception:
        return None

    info = dict()
    
    info['Título'] = data_content.get('title',None)
    #info['Id'] = id_    
    if data_content.get('contentType').upper() != 'MOVIE':
        info['Cantidad de episodios']= data_content.get('episodeCount',None)
        info['Cantidad de temporadas'] = get_temporadas(data_content.get('childContent',None))
    else:
        duracion = data_content.get('runtime',None)
        if  duracion:
            duracion = int(duracion / 60)
        info['Duración'] = duracion
        info['Géneros']=get_generos(data_content['genres'])
        info['Año'] = data_content.get('releaseYear',None)

    info['Sinopsis'] = data_content.get('logLine',None)
    info['Actores'] = get_cast(data_content['credits'])

    return info

#MAIN
if __name__ == '__main__':

    api_para_conseguir_ids = "https://playdata.starz.com/metadata-service/play/partner/Web_ES/v8/blocks?playContents=map&lang=es-ES&pages=MOVIES,SERIES&includes=contentId,contentType,title,product,seriesName,seasonNumber,free,comingSoon,newContent,topContentId,properCaseTitle,categoryKeys,runtime,popularity,original,firstEpisodeRuntime,releaseYear,images,minReleaseYear,maxReleaseYear,episodeCount,detail"

    response = requests.get(api_para_conseguir_ids)
    response = response.json()

    info_1= response['blocks'][0]['blocks']
    info_2= response['blocks'][1]['blocks']

    ids = list()
    ids+= get_ids(info_1)
    ids+= get_ids(info_2)

    #Me borra los id repetidos
    setIds=set(ids)
    
    catalogoFull = list()
    for id_ in setIds:
        content = get_catalogo(id_)
        if content:
            catalogoFull.append(content)
            
    pprint.pprint(catalogoFull, sort_dicts=False)

    
    
