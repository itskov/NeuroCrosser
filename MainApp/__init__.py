from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_beaker')
    config.add_route('home', '/')
    config.add_route('overlappingGenes','/overlap')
    config.add_route('fetchGO','/fetchGO')
    config.add_route('hello', '/howdy/{first}/{last}')
    config.scan('.views')
    return config.make_wsgi_app()
