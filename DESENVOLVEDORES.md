# ====================================
# GUIA DE DESENVOLVIMENTO
# ====================================
# Este arquivo contém informações importantes para desenvolvedores

## 📚 Estrutura do Projeto

```
Love-Player/
├── app.py                    # Aplicação principal - COMECE AQUI
├── config.py                 # Configurações
├── rotas.py                  # Endpoints da API
├── modelos.py                # Estruturas de dados
├── servico_musicas.py        # Lógica de negócio
├── __init__.py               # Marcador de pacote
├── requirements.txt          # Dependências
├── .env                      # Variáveis de ambiente
├── .gitignore                # Git ignore
├── README.md                 # Documentação geral
├── DESENVOLVEDORES.md        # Este arquivo
└── frontend/
    ├── index.html
    ├── script.js
    ├── style.css
    └── musicas/
```

## 🚀 Começar a Desenvolver

### 1. Entender a Estrutura

A estrutura segue o padrão **MVC (Model-View-Controller)**:

1. **Models** (`modelos.py`): Define os dados
   - `Musica`: Representa uma música
   - `Playlist`: Coleção de músicas

2. **Views** (`frontend/`): Interface do usuário
   - HTML, CSS, JavaScript

3. **Controllers** (`rotas.py`): Processa requisições
   - Endpoints da API

4. **Services** (`servico_musicas.py`): Lógica de negócio
   - Funções reutilizáveis

5. **Config** (`config.py`): Configurações
   - Diferentes ambientes

### 2. Fluxo de Requisição

```
Usuário clica no player (frontend/script.js)
    ↓
JavaScript faz fetch() para API
    ↓
Flask recebe em rotas.py
    ↓
rotas.py chama servico_musicas.py
    ↓
servico_musicas.py usa modelos.py
    ↓
Resposta JSON volta para frontend
    ↓
JavaScript renderiza na página
```

## 💻 Desenvolvendo Novas Features

### Exemplo 1: Adicionar Novo Endpoint

**Arquivo: `rotas.py`**

```python
@rotas_api.route('/musicas/pesquisar', methods=['POST'])
def pesquisar_musica():
    """
    Busca uma música pelo nome
    
    Returns:
        JSON com as músicas encontradas
    """
    from flask import request
    
    termo = request.json.get('termo', '')
    
    # Usa o serviço para buscar
    resultado = servico.buscar_musicas(termo)
    
    return jsonify({
        'sucesso': True,
        'dados': resultado
    }), 200
```

**Arquivo: `servico_musicas.py`**

```python
def buscar_musicas(self, termo: str) -> list:
    """Busca músicas pelo nome"""
    termo = termo.lower()
    return [
        m.para_dict() 
        for m in self.playlist.musicas 
        if termo in m.nome.lower()
    ]
```

### Exemplo 2: Integrar com Banco de Dados

**Instale SQLAlchemy:**
```bash
pip install flask-sqlalchemy
```

**Arquivo: `modelos.py`** (adaptado)

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Musica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    arquivo = db.Column(db.String(300), nullable=False)
    
    def para_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'arquivo': self.arquivo
        }
```

### Exemplo 3: Adicionar Sistema de Favoritos

**Arquivo: `modelos.py`**

```python
@dataclass
class Musica:
    # ... campos existentes ...
    favorita: bool = False
    
    def marcar_como_favorita(self):
        self.favorita = True
    
    def desmarcar_como_favorita(self):
        self.favorita = False
```

**Arquivo: `rotas.py`**

```python
@rotas_api.route('/musicas/<int:musica_id>/favoritar', methods=['POST'])
def favoritar_musica(musica_id):
    musica = servico.obter_musica_por_id(musica_id)
    musica.marcar_como_favorita()
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Marcada como favorita'
    }), 200
```

## 🧪 Testando a Aplicação

### Testar com cURL (terminal)

```bash
# Obter todas as músicas
curl http://localhost:1905/api/musicas

# Obter música específica
curl http://localhost:1905/api/musicas/0

# Próxima música
curl http://localhost:1905/api/musicas/0/proxima

# Health check
curl http://localhost:1905/api/health
```

### Testar no JavaScript (console do navegador)

```javascript
// Testar API
fetch('/api/musicas')
  .then(res => res.json())
  .then(data => console.log(data))

// Obter próxima música
fetch('/api/musicas/0/proxima')
  .then(res => res.json())
  .then(data => console.log(data.dados))
```

## 📝 Boas Práticas

### 1. Sempre Documente com Docstrings

```python
def minha_funcao(parametro: str) -> dict:
    """
    Descrição breve da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        parametro (str): Descrição do parâmetro
    
    Returns:
        dict: Descrição do retorno
    
    Raises:
        ValueError: Se parametro é inválido
    
    Example:
        >>> resultado = minha_funcao("teste")
        >>> print(resultado)
        {...}
    """
    pass
```

### 2. Use Type Hints

```python
# ✅ BOM
def processar_musica(id: int, nome: str) -> dict:
    pass

# ❌ RUIM
def processar_musica(id, nome):
    pass
```

### 3. Separe Responsabilidades

```
- `modelos.py`: Estrutura de dados
- `servico_musicas.py`: Lógica de negócio
- `rotas.py`: Endpoints da API
- `config.py`: Configurações
```

### 4. Trate Erros Apropriadamente

```python
try:
    # Tenta fazer algo
    resultado = servico.obter_musica(id)
    
    if not resultado:
        return jsonify({'erro': 'Não encontrada'}), 404
    
    return jsonify({'sucesso': True, 'dados': resultado}), 200

except ValueError as e:
    return jsonify({'erro': str(e)}), 400

except Exception as e:
    return jsonify({'erro': 'Erro interno'}), 500
```

### 5. Use Variáveis de Ambiente

```python
# ✅ BOM
PORT = os.getenv('PORT', 1905)

# ❌ RUIM
PORT = 1905  # Hardcoded
```

## 🔄 Workflow de Desenvolvimento

1. **Planeje**: O que precisa fazer?
2. **Crie o modelo** (`modelos.py`): Estruture os dados
3. **Crie o serviço** (`servico_musicas.py`): Implemente a lógica
4. **Crie a rota** (`rotas.py`): Exponha a API
5. **Atualize o frontend** (`script.js`): Consuma a API
6. **Teste**: Use curl, console do navegador
7. **Documente**: Adicione comentários e docstrings

## 📦 Dependências do Projeto

```
Flask==3.0.0          # Framework web
python-dotenv==1.0.0  # Variáveis de ambiente
Werkzeug==3.0.1       # WSGI utilities
```

### Para Expandir (Opcional)

```bash
# Banco de dados
pip install flask-sqlalchemy

# Validação de dados
pip install marshmallow

# Testes
pip install pytest

# Segurança
pip install flask-cors

# API documentation
pip install flask-swagger
```

## 🐛 Debug e Troubleshooting

### Ver Logs Detalhados

**Arquivo: `app.py`**

```python
import logging

# Ativa logging detalhado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Usar em funções
logger.debug("Mensagem de debug")
logger.info("Informação importante")
logger.error("Erro encontrado")
```

### Usar o Debugger do Flask

```python
# Em app.py
app.run(debug=True)  # Ativa recarregamento automático
```

### Inspecionar Requisições

```python
from flask import request

@rotas_api.route('/debug', methods=['GET', 'POST'])
def debug():
    print(f"Método: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Dados: {request.json}")
    return "OK", 200
```

## 🚀 Deploy para Produção

### 1. Alterar Variáveis de Ambiente

```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=sua-chave-super-segura-aqui
```

### 2. Usar Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 3. Usar Nginx como Proxy

```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

## 📚 Recursos Adicionais

- [Documentação Flask](https://flask.palletsprojects.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [REST API Best Practices](https://restfulapi.net/)
- [Flask Patterns](https://flask.palletsprojects.com/patterns/)

## 💬 Perguntas Comuns

### P: Como adicionar autenticação?

R: Use extensões como `Flask-Login` ou `Flask-JWT-Extended`:

```bash
pip install Flask-Login Flask-JWT-Extended
```

### P: Como habilitar CORS?

R: Use `Flask-CORS`:

```bash
pip install Flask-CORS
```

```python
from flask_cors import CORS
CORS(app)
```

### P: Como adicionar validação de dados?

R: Use `Marshmallow`:

```bash
pip install Marshmallow
```

### P: Como criar testes?

R: Use `pytest`:

```bash
pip install pytest

# Arquivo: test_app.py
def test_obter_musicas():
    response = client.get('/api/musicas')
    assert response.status_code == 200
```

---

**Boa sorte desenvolvendo! 🚀**

Dúvidas? Consulte a documentação no README.md ou explore o código!
