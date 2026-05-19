# ====================================
# EXEMPLO DE TESTE COM PYTHON
# ====================================
# Para usar este arquivo:
# 1. pip install pytest
# 2. pytest test_app.py -v

import pytest
from app import criar_app
from modelos import Musica, Playlist
from servico_musicas import ServicoMusicas


@pytest.fixture
def app():
    """Cria uma aplicação de teste."""
    app = criar_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Cria um cliente de teste."""
    return app.test_client()


class TestServicoMusicas:
    """Testes do serviço de músicas."""
    
    def setup_method(self):
        """Executado antes de cada teste."""
        self.servico = ServicoMusicas()
    
    def test_obter_todas_musicas(self):
        """Testa obter todas as músicas."""
        musicas = self.servico.obter_todas_musicas()
        assert musicas is not None
        assert 'titulo' in musicas
        assert 'total_musicas' in musicas
        assert musicas['total_musicas'] > 0
    
    def test_obter_musica_por_id(self):
        """Testa obter uma música específica."""
        musica = self.servico.obter_musica_por_id(0)
        assert musica is not None
        assert musica['id'] == 0
        assert 'nome' in musica
        assert 'arquivo' in musica
    
    def test_obter_musica_id_invalido(self):
        """Testa obter música com ID inválido."""
        musica = self.servico.obter_musica_por_id(999)
        assert musica is None
    
    def test_proxima_musica(self):
        """Testa obter próxima música."""
        proxima = self.servico.obter_proxima_musica(0)
        assert proxima is not None
        assert proxima['id'] == 1
    
    def test_proxima_musica_ultima(self):
        """Testa próxima música da última (ciclagem)."""
        total = self.servico.contar_musicas()
        proxima = self.servico.obter_proxima_musica(total - 1)
        assert proxima['id'] == 0
    
    def test_musica_anterior(self):
        """Testa obter música anterior."""
        anterior = self.servico.obter_musica_anterior(1)
        assert anterior is not None
        assert anterior['id'] == 0
    
    def test_musica_anterior_primeira(self):
        """Testa música anterior da primeira (ciclagem)."""
        anterior = self.servico.obter_musica_anterior(0)
        assert anterior is not None
        assert anterior['id'] == 20  # Última música (21 total)
    
    def test_contar_musicas(self):
        """Testa contar músicas."""
        total = self.servico.contar_musicas()
        assert total == 21


class TestModelos:
    """Testes dos modelos."""
    
    def test_criar_musica(self):
        """Testa criar uma música."""
        musica = Musica(
            nome="Teste",
            arquivo="musicas/teste.mp3",
            id=0
        )
        assert musica.nome == "Teste"
        assert musica.arquivo == "musicas/teste.mp3"
    
    def test_musica_para_dict(self):
        """Testa converter música para dicionário."""
        musica = Musica(
            nome="Teste",
            arquivo="musicas/teste.mp3",
            id=0
        )
        resultado = musica.para_dict()
        assert resultado['nome'] == "Teste"
        assert resultado['arquivo'] == "musicas/teste.mp3"
        assert resultado['id'] == 0
    
    def test_criar_playlist(self):
        """Testa criar uma playlist."""
        playlist = Playlist(titulo="Teste")
        assert playlist.titulo == "Teste"
        assert playlist.contar_musicas() == 0
    
    def test_adicionar_musica_playlist(self):
        """Testa adicionar música à playlist."""
        playlist = Playlist(titulo="Teste")
        musica = Musica(nome="Teste", arquivo="musicas/teste.mp3")
        
        playlist.adicionar_musica(musica)
        
        assert playlist.contar_musicas() == 1
        assert musica.id == 0


class TestRotas:
    """Testes dos endpoints da API."""
    
    def test_obter_musicas(self, client):
        """Testa endpoint GET /api/musicas."""
        response = client.get('/api/musicas')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['sucesso'] is True
        assert 'dados' in data
    
    def test_obter_musica_especifica(self, client):
        """Testa endpoint GET /api/musicas/<id>."""
        response = client.get('/api/musicas/0')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['sucesso'] is True
        assert data['dados']['id'] == 0
    
    def test_obter_proxima_musica_endpoint(self, client):
        """Testa endpoint GET /api/musicas/<id>/proxima."""
        response = client.get('/api/musicas/0/proxima')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['sucesso'] is True
        assert data['dados']['id'] == 1
    
    def test_obter_anterior_musica_endpoint(self, client):
        """Testa endpoint GET /api/musicas/<id>/anterior."""
        response = client.get('/api/musicas/1/anterior')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['sucesso'] is True
        assert data['dados']['id'] == 0
    
    def test_playlist_info(self, client):
        """Testa endpoint GET /api/playlist/info."""
        response = client.get('/api/playlist/info')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['sucesso'] is True
        assert 'total_musicas' in data['dados']
    
    def test_health_check(self, client):
        """Testa endpoint GET /api/health."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'online'
    
    def test_pagina_inicial(self, client):
        """Testa rota raiz /."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_rota_nao_existente(self, client):
        """Testa erro 404."""
        response = client.get('/rota-inexistente')
        assert response.status_code == 404


if __name__ == '__main__':
    # Executar com: python -m pytest test_app.py -v
    pytest.main([__file__, '-v'])
