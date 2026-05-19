# ====================================
# APLICAÇÃO PRINCIPAL - LOVE PLAYER
# ====================================
# Arquivo principal que inicializa e executa o servidor
# Este é o arquivo que você deve executar para iniciar o projeto

from flask import Flask, render_template
from config import obter_config
from rotas import rotas_api
import os


def criar_app():
    """
    Factory function para criar a aplicação Flask.
    
    Esta função cria e configura a aplicação de forma profissional,
    permitindo fácil reutilização e testes.
    
    Returns:
        Flask: Aplicação Flask configurada
    
    Exemplo:
        >>> app = criar_app()
        >>> app.run()
    """
    
    # Obtém a configuração apropriada baseado no ambiente
    config = obter_config()
    
    # Cria a aplicação Flask
    app = Flask(
        __name__,
        static_folder=config.STATIC_FOLDER,
        static_url_path=config.STATIC_URL_PATH
    )
    
    # Aplica as configurações
    app.config.from_object(config)
    
    # Registra os blueprints (rotas)
    app.register_blueprint(rotas_api)
    
    # ====== ROTAS PRINCIPAIS ======
    
    @app.route('/')
    def pagina_inicial():
        """
        Rota raiz - servir o arquivo index.html
        
        Quando o usuário acessa localhost:1905, ele recebe o index.html
        que contém o player de música.
        """
        return render_template('index.html')
    
    @app.errorhandler(404)
    def nao_encontrado(erro):
        """
        Handler para erro 404 (página não encontrada)
        
        Quando uma rota não existe, retorna um erro JSON legível.
        """
        return {
            'sucesso': False,
            'erro': 'Rota não encontrada',
            'status_code': 404
        }, 404
    
    @app.errorhandler(500)
    def erro_interno(erro):
        """
        Handler para erro 500 (erro interno do servidor)
        
        Quando ocorre um erro não tratado, retorna um erro JSON legível.
        """
        return {
            'sucesso': False,
            'erro': 'Erro interno do servidor',
            'status_code': 500
        }, 500
    
    return app


# Se este arquivo for executado diretamente, inicia o servidor
if __name__ == '__main__':
    # Cria a aplicação
    app = criar_app()
    
    # Obtém as configurações
    config = obter_config()
    
    # Exibe mensagem de boas-vindas
    print("=" * 50)
    print("❤️ Love Player - Backend Python ❤️")
    print("=" * 50)
    print(f"🚀 Servidor iniciado em: http://{config.HOST}:{config.PORT}")
    print(f"📁 Ambiente: {app.config.get('ENV', 'production')}")
    print(f"🔧 Debug: {app.debug}")
    print("=" * 50)
    
    # Inicia o servidor
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
