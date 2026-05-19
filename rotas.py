# ====================================
# ROTAS DA APLICAÇÃO
# ====================================
# Aqui definimos todos os endpoints da API
# Cada rota cuida de uma responsabilidade específica

from flask import Blueprint, render_template, jsonify
from servico_musicas import ServicoMusicas

# Cria um blueprint para organizar as rotas
# Blueprints são uma forma profissional de organizar rotas em Flask
rotas_api = Blueprint('api', __name__, url_prefix='/api')

# Instancia o serviço de músicas (em produção, seria injetado)
servico = ServicoMusicas()


# ====== ROTAS DE MÚSICAS ======

@rotas_api.route('/musicas', methods=['GET'])
def obter_musicas():
    """
    Endpoint para obter todas as músicas.
    
    Retorna a lista completa de músicas da playlist.
    
    Returns:
        JSON com a estrutura:
        {
            "sucesso": true,
            "dados": {
                "titulo": "Love Player - Playlist Oficial",
                "total_musicas": 21,
                "musicas": [...]
            }
        }
    
    Exemplo de uso (frontend):
        fetch('/api/musicas')
            .then(res => res.json())
            .then(data => console.log(data.dados.musicas))
    """
    try:
        dados = servico.obter_todas_musicas()
        return jsonify({
            'sucesso': True,
            'dados': dados
        }), 200
    
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter músicas: {str(e)}'
        }), 500


@rotas_api.route('/musicas/<int:musica_id>', methods=['GET'])
def obter_musica(musica_id):
    """
    Endpoint para obter uma música específica.
    
    Args:
        musica_id (int): ID da música (deve estar entre 0 e total-1)
    
    Returns:
        JSON com a música encontrada ou erro 404
    
    Exemplo de uso (frontend):
        fetch('/api/musicas/0')
            .then(res => res.json())
            .then(data => console.log(data.dados))
    """
    try:
        musica = servico.obter_musica_por_id(musica_id)
        
        if not musica:
            return jsonify({
                'sucesso': False,
                'erro': f'Música com ID {musica_id} não encontrada'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'dados': musica
        }), 200
    
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter música: {str(e)}'
        }), 500


@rotas_api.route('/musicas/<int:musica_id>/proxima', methods=['GET'])
def obter_proxima_musica(musica_id):
    """
    Endpoint para obter a próxima música.
    
    Implementa a navegação cíclica (ao final, volta ao início).
    
    Args:
        musica_id (int): ID da música atual
    
    Returns:
        JSON com a próxima música
    
    Exemplo de uso (frontend):
        fetch('/api/musicas/5/proxima')
            .then(res => res.json())
            .then(data => console.log(data.dados))
    """
    try:
        proxima = servico.obter_proxima_musica(musica_id)
        
        if not proxima:
            return jsonify({
                'sucesso': False,
                'erro': 'Erro ao obter próxima música'
            }), 500
        
        return jsonify({
            'sucesso': True,
            'dados': proxima
        }), 200
    
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter próxima música: {str(e)}'
        }), 500


@rotas_api.route('/musicas/<int:musica_id>/anterior', methods=['GET'])
def obter_musica_anterior(musica_id):
    """
    Endpoint para obter a música anterior.
    
    Implementa a navegação cíclica reversa (antes do início, vai ao final).
    
    Args:
        musica_id (int): ID da música atual
    
    Returns:
        JSON com a música anterior
    
    Exemplo de uso (frontend):
        fetch('/api/musicas/0/anterior')
            .then(res => res.json())
            .then(data => console.log(data.dados))
    """
    try:
        anterior = servico.obter_musica_anterior(musica_id)
        
        if not anterior:
            return jsonify({
                'sucesso': False,
                'erro': 'Erro ao obter música anterior'
            }), 500
        
        return jsonify({
            'sucesso': True,
            'dados': anterior
        }), 200
    
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter música anterior: {str(e)}'
        }), 500


@rotas_api.route('/playlist/info', methods=['GET'])
def obter_info_playlist():
    """
    Endpoint para obter informações gerais da playlist.
    
    Returns:
        JSON com total de músicas e outras informações
    
    Exemplo de uso (frontend):
        fetch('/api/playlist/info')
            .then(res => res.json())
            .then(data => console.log(`Total: ${data.dados.total_musicas}`))
    """
    try:
        total = servico.contar_musicas()
        return jsonify({
            'sucesso': True,
            'dados': {
                'total_musicas': total,
                'titulo': 'Love Player - Playlist Oficial'
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter informações: {str(e)}'
        }), 500


# ====== ROTA DE HEALTH CHECK ======

@rotas_api.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar se o servidor está funcionando.
    
    Útil para monitoramento e testes.
    
    Returns:
        JSON com status da aplicação
    
    Exemplo de uso (frontend):
        fetch('/api/health')
            .then(res => res.json())
            .then(data => console.log(data.status))
    """
    return jsonify({
        'status': 'online',
        'mensagem': 'Love Player está funcionando! ❤️'
    }), 200
