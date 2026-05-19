# ====================================
# CONFIGURAÇÕES DO APLICATIVO
# ====================================
# Este arquivo centraliza todas as configurações do projeto
# Facilita manutenção e reutilização em diferentes ambientes

import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

class Config:
    """
    Configurações gerais da aplicação.
    
    Atributos:
        SECRET_KEY: Chave secreta para sessões
        JSON_SORT_KEYS: Define se JSON será ordenado alfabeticamente
        STATIC_FOLDER: Pasta dos arquivos estáticos (HTML, CSS, JS)
        STATIC_URL_PATH: Caminho URL para arquivos estáticos
    """
    
    # Chave secreta (deve ser alterada em produção)
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')
    
    # JSON será ordenado alfabeticamente
    JSON_SORT_KEYS = False
    
    # Pasta dos arquivos estáticos (raiz do projeto)
    STATIC_FOLDER = '.'
    STATIC_URL_PATH = ''
    
    # Porta padrão
    PORT = int(os.getenv('PORT', 1905))
    
    # Host padrão
    HOST = os.getenv('HOST', 'localhost')
    
    # Debug mode
    DEBUG = os.getenv('DEBUG', 'True') == 'True'


class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    DEBUG = False
    TESTING = False
    # Em produção, a chave secreta deve vir de variável de ambiente
    SECRET_KEY = os.getenv('SECRET_KEY')


class TestingConfig(Config):
    """Configurações para testes."""
    DEBUG = True
    TESTING = True


# Seleciona a configuração baseado no ambiente
def obter_config():
    """
    Retorna a configuração apropriada baseado no ambiente.
    
    Returns:
        Config: Classe de configuração apropriada
    """
    ambiente = os.getenv('FLASK_ENV', 'development').lower()
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    return configs.get(ambiente, DevelopmentConfig)
