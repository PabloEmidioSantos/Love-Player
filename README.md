# Love Player - Python Edition 🎵❤️

Uma aplicação de reprodução de músicas moderna e bem estruturada, com **backend em Python** (Flask) e **frontend em HTML/CSS/JavaScript**.

## 📋 Visão Geral

Este projeto demonstra boas práticas de desenvolvimento:
- ✅ Backend bem estruturado e modular
- ✅ Separação clara de responsabilidades
- ✅ Fácil de entender e manter
- ✅ Documentação completa
- ✅ Código comentado para aprendizado

### Estrutura do Projeto

```
Love-Player/
├── app.py                      # 🚀 Arquivo principal (EXECUTE ESTE)
├── config.py                   # ⚙️ Configurações da aplicação
├── rotas.py                    # 🛣️ Rotas da API
├── modelos.py                  # 📊 Modelos de dados
├── servico_musicas.py          # 🎵 Lógica de negócio
├── requirements.txt            # 📦 Dependências Python
├── .env                        # 🔐 Variáveis de ambiente
├── README.md                   # 📚 Este arquivo
│
└── frontend/
    ├── index.html              # 🌐 HTML do player
    ├── script.js               # 🎮 Lógica do player
    ├── style.css               # 🎨 Estilos
    └── musicas/                # 🎶 Pasta com as músicas
        ├── amor-e-fe.mp3
        ├── baby-ce-e-gata.mp3
        └── ...
```

## 🚀 Como Executar

### 1️⃣ Preparar o Ambiente

#### No Windows:

```bash
# Abrir terminal na pasta do projeto
cd c:\Users\pablo.santos\Desktop\pablo_pessoal\EstudosGeral\python\Love-Player

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

#### No Linux/Mac:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Executar o Servidor

```bash
# Com ambiente virtual ativado:
python app.py
```

Você verá:
```
==================================================
❤️ Love Player - Backend Python ❤️
==================================================
🚀 Servidor iniciado em: http://localhost:1905
📁 Ambiente: development
🔧 Debug: True
==================================================
```

### 3️⃣ Acessar a Aplicação

Abra o navegador e acesse: **http://localhost:1905**

---

## 📚 Arquitetura e Conceitos

### 🏗️ Padrão MVC (Model-View-Controller)

Este projeto segue o padrão MVC para separação de responsabilidades:

- **Model** (`modelos.py`): Define as estruturas de dados
  - `Musica`: Representa uma música individual
  - `Playlist`: Representa uma coleção de músicas

- **View** (`frontend/`): Interface do usuário
  - HTML, CSS e JavaScript para o player

- **Controller** (`rotas.py`): Lógica de negócio
  - Endpoints da API que processam requisições

### 🔄 Fluxo de Dados

```
Frontend (HTML/JS)
    ↓
Requisição HTTP
    ↓
Rotas (rotas.py)
    ↓
Serviço (servico_musicas.py)
    ↓
Modelos (modelos.py)
    ↓
Resposta JSON
    ↓
Frontend renderiza
```

---

## 🔌 API REST

### Endpoints Disponíveis

#### 📋 Obter Todas as Músicas

```http
GET /api/musicas
```

**Resposta (200):**
```json
{
  "sucesso": true,
  "dados": {
    "titulo": "Love Player - Playlist Oficial",
    "total_musicas": 21,
    "musicas": [
      {
        "id": 0,
        "nome": "Amor e Fé",
        "arquivo": "musicas/amor-e-fe.mp3"
      },
      ...
    ]
  }
}
```

#### 🎵 Obter Música Específica

```http
GET /api/musicas/:id
```

**Resposta (200):**
```json
{
  "sucesso": true,
  "dados": {
    "id": 0,
    "nome": "Amor e Fé",
    "arquivo": "musicas/amor-e-fe.mp3"
  }
}
```

#### ⏭️ Obter Próxima Música

```http
GET /api/musicas/:id/proxima
```

Retorna a próxima música na playlist (com navegação cíclica).

#### ⏮️ Obter Música Anterior

```http
GET /api/musicas/:id/anterior
```

Retorna a música anterior na playlist (com navegação cíclica).

#### 📊 Informações da Playlist

```http
GET /api/playlist/info
```

**Resposta (200):**
```json
{
  "sucesso": true,
  "dados": {
    "total_musicas": 21,
    "titulo": "Love Player - Playlist Oficial"
  }
}
```

#### 🏥 Health Check

```http
GET /api/health
```

**Resposta (200):**
```json
{
  "status": "online",
  "mensagem": "Love Player está funcionando! ❤️"
}
```

---

## 🎓 Como Entender o Código

### Para Iniciantes (Junior)

1. **Comece por `app.py`**
   - Veja como a aplicação é criada
   - Entenda a função `criar_app()`

2. **Depois, explore `config.py`**
   - Entenda como as configurações funcionam
   - Veja como usar variáveis de ambiente

3. **Estude `modelos.py`**
   - Aprenda sobre dataclasses
   - Veja como estruturar dados

4. **Olhe `servico_musicas.py`**
   - Entenda a lógica de negócio
   - Veja como usar os modelos

5. **Finalmente, `rotas.py`**
   - Entenda como criar endpoints
   - Veja como retornar JSON

### Para Desenvolvedores Plenos

- Explore a documentação inline (docstrings)
- Veja exemplos de boas práticas
- Considere extensões:
  - Integração com banco de dados
  - Autenticação de usuários
  - Sistema de favoritos
  - Busca de músicas
  - Histórico de reprodução

---

## 🔧 Configuração e Variáveis de Ambiente

### Arquivo `.env`

```env
FLASK_ENV=development    # development, production, testing
PORT=1905                # Porta do servidor
DEBUG=True               # Ativar modo debug
HOST=localhost           # Host do servidor
SECRET_KEY=...           # Chave secreta (mude em produção)
```

### Classes de Configuração

- `DevelopmentConfig`: Ambiente de desenvolvimento
- `ProductionConfig`: Ambiente de produção
- `TestingConfig`: Ambiente de testes

---

## 💡 Exemplos de Uso do Frontend

### Carregar Playlist

```javascript
// Fetch automático ao carregar a página
async function carregarPlaylist() {
  const resposta = await fetch('/api/musicas');
  const dados = await resposta.json();
  musicas = dados.dados.musicas;
}
```

### Tocar uma Música

```javascript
function carregarMusica(id) {
  const musica = musicas[id];
  audio.src = musica.arquivo;
  audio.play();
}
```

### Navegar para Próxima

```javascript
async function proxima() {
  const proximaMusica = await fetch(`/api/musicas/${index}/proxima`);
  const dados = await proximaMusica.json();
  index = dados.dados.id;
  carregarMusica(index);
}
```

---

## 🎨 Personalização

### Adicionar Novas Músicas

Edite `servico_musicas.py`, na função `_criar_playlist_padrao()`:

```python
musicas_dados = [
    {"nome": "Minha Nova Música", "arquivo": "musicas/minha-musica.mp3"},
    ...
]
```

### Mudar Cores

Edite `frontend/style.css`:

```css
.player {
  background: #seu-color;
  box-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
}

.player h1 {
  color: #sua-cor;
}
```

### Adicionar Novos Endpoints

Em `rotas.py`:

```python
@rotas_api.route('/novo-endpoint', methods=['GET'])
def novo_endpoint():
    return jsonify({
        'sucesso': True,
        'dados': {...}
    }), 200
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:** Ative o ambiente virtual e instale as dependências:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Erro: "Port 1905 already in use"

**Solução:** Mude a porta no `.env`:
```env
PORT=1906
```

### Frontend não carrega as músicas

**Solução:** 
1. Verifique se o servidor está rodando
2. Abra o console do navegador (F12) e veja erros
3. Confirme que `/api/musicas` retorna dados

---

## 📈 Próximos Passos

Ideias para expandir o projeto:

- [ ] Banco de dados (SQLite, PostgreSQL)
- [ ] Sistema de usuários e login
- [ ] Playlist customizáveis
- [ ] Favoritos/Likes
- [ ] Histórico de reprodução
- [ ] Busca e filtros
- [ ] Sistema de recomendações
- [ ] Upload de músicas
- [ ] Sincronização com Spotify
- [ ] Testes automatizados

---

## 📞 Suporte

Dúvidas sobre Python? Confira:
- [Documentação Flask](https://flask.palletsprojects.com/)
- [Documentação Python](https://docs.python.org/3/)
- [REST API Best Practices](https://restfulapi.net/)

---

## 👨‍💻 Autor Original

**Pablo Emidio dos Santos** - Dev Junior
- [LinkedIn](https://www.linkedin.com/in/pabloemidiodossantos/)

---

## 📄 Licença

ISC License

---

**Feito com ❤️ e muito código Python 🐍**
