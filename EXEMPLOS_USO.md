# 📚 DOCUMENTAÇÃO - EXEMPLO DE USO

## 🎯 Objetivo

Este documento mostra como usar a API Love Player com exemplos práticos para nível Junior/Pleno.

---

## 📋 Índice

1. [Usar via cURL](#usar-via-curl)
2. [Usar via JavaScript](#usar-via-javascript)
3. [Usar via Python](#usar-via-python)
4. [Entender as Respostas](#entender-as-respostas)

---

## 🔌 Usar via cURL

### Terminal Windows (PowerShell)

```powershell
# Obter todas as músicas
curl http://localhost:1905/api/musicas

# Obter música específica
curl http://localhost:1905/api/musicas/0

# Obter próxima música
curl http://localhost:1905/api/musicas/0/proxima

# Obter música anterior
curl http://localhost:1905/api/musicas/5/anterior

# Informações da playlist
curl http://localhost:1905/api/playlist/info

# Health check
curl http://localhost:1905/api/health
```

### Terminal Linux/Mac

```bash
# Mesmo que acima, mas use bash ao invés de PowerShell
curl http://localhost:1905/api/musicas
```

---

## 🌐 Usar via JavaScript

### No Console do Navegador (F12)

#### 1. Obter todas as músicas

```javascript
fetch('/api/musicas')
  .then(resposta => resposta.json())
  .then(dados => {
    console.log('Total de músicas:', dados.dados.total_musicas);
    console.log('Primeira música:', dados.dados.musicas[0]);
  })
  .catch(erro => console.error('Erro:', erro));
```

#### 2. Obter música específica

```javascript
fetch('/api/musicas/0')
  .then(res => res.json())
  .then(dados => console.log(dados.dados))
  .catch(erro => console.error('Erro:', erro));
```

#### 3. Navegar entre músicas

```javascript
// Próxima música
fetch('/api/musicas/0/proxima')
  .then(res => res.json())
  .then(dados => console.log('Próxima:', dados.dados.nome));

// Música anterior
fetch('/api/musicas/5/anterior')
  .then(res => res.json())
  .then(dados => console.log('Anterior:', dados.dados.nome));
```

#### 4. Função auxiliar para usar na página

```javascript
// Adicione isto no console para usar depois

// Função para obter uma música
async function pegarMusica(id) {
  const res = await fetch(`/api/musicas/${id}`);
  const dados = await res.json();
  return dados.dados;
}

// Função para listar todas
async function listarTodasMusicas() {
  const res = await fetch('/api/musicas');
  const dados = await res.json();
  return dados.dados.musicas;
}

// Uso:
pegarMusica(0).then(m => console.log(m.nome));
```

---

## 🐍 Usar via Python

### Script Python para testar a API

#### Criar arquivo `teste_api.py`:

```python
"""
Script para testar a API do Love Player
Execute com: python teste_api.py
"""

import requests
import json

# URL base da API
BASE_URL = "http://localhost:1905/api"

def obter_musicas():
    """Obtém todas as músicas"""
    resposta = requests.get(f"{BASE_URL}/musicas")
    dados = resposta.json()
    
    if dados['sucesso']:
        musicas = dados['dados']['musicas']
        print(f"✅ {len(musicas)} músicas encontradas:\n")
        
        for m in musicas:
            print(f"  [{m['id']:2d}] {m['nome']:<30} - {m['arquivo']}")
    else:
        print(f"❌ Erro: {dados['erro']}")

def obter_musica_especifica(id_musica):
    """Obtém uma música específica"""
    resposta = requests.get(f"{BASE_URL}/musicas/{id_musica}")
    dados = resposta.json()
    
    if dados['sucesso']:
        m = dados['dados']
        print(f"\n📀 Música #{m['id']}")
        print(f"   Nome: {m['nome']}")
        print(f"   Arquivo: {m['arquivo']}")
    else:
        print(f"❌ {dados['erro']}")

def navegar_playlist():
    """Exemplo de navegação pela playlist"""
    print("\n🎵 Navegação pela Playlist:")
    print("-" * 40)
    
    # Comença na música 0
    id_atual = 0
    
    for i in range(3):
        # Obtém música atual
        res = requests.get(f"{BASE_URL}/musicas/{id_atual}")
        m = res.json()['dados']
        print(f"Atual: {m['nome']}")
        
        # Próxima
        res = requests.get(f"{BASE_URL}/musicas/{id_atual}/proxima")
        proxima = res.json()['dados']
        print(f"  → Próxima: {proxima['nome']}")
        
        id_atual = proxima['id']
        print()

def info_playlist():
    """Obtém informações da playlist"""
    resposta = requests.get(f"{BASE_URL}/playlist/info")
    dados = resposta.json()['dados']
    
    print(f"\n📊 Informações da Playlist:")
    print(f"   Título: {dados['titulo']}")
    print(f"   Total: {dados['total_musicas']} músicas")

def health_check():
    """Verifica se o servidor está online"""
    try:
        resposta = requests.get(f"{BASE_URL}/health")
        dados = resposta.json()
        print(f"✅ {dados['mensagem']}")
        return True
    except:
        print("❌ Servidor offline")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🎵 Testador da API Love Player")
    print("=" * 50)
    
    # Verifica se servidor está online
    if not health_check():
        print("\n⚠️  Inicie o servidor primeiro!")
        print("   python app.py")
        exit()
    
    # Executa testes
    obter_musicas()
    obter_musica_especifica(0)
    navegar_playlist()
    info_playlist()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("=" * 50)
```

#### Instalar dependência:

```bash
pip install requests
```

#### Executar:

```bash
python teste_api.py
```

---

## 📊 Entender as Respostas

### Formato Padrão

```json
{
  "sucesso": true,
  "dados": { ... }
}
```

ou em caso de erro:

```json
{
  "sucesso": false,
  "erro": "Mensagem de erro"
}
```

### Resposta: Obter Todas as Músicas

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
      {
        "id": 1,
        "nome": "Baby Se é Gata",
        "arquivo": "musicas/baby-ce-e-gata.mp3"
      }
      // ... mais músicas
    ]
  }
}
```

### Resposta: Obter Uma Música

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

### Resposta: Health Check

```json
{
  "status": "online",
  "mensagem": "Love Player está funcionando! ❤️"
}
```

### Resposta: Erro 404

```json
{
  "sucesso": false,
  "erro": "Música com ID 999 não encontrada"
}
```

---

## 🎓 Exemplos Práticos

### Exemplo 1: Listar Todas as Músicas (JavaScript)

```javascript
async function listarMusicas() {
  try {
    const res = await fetch('/api/musicas');
    const dados = await res.json();
    
    if (dados.sucesso) {
      dados.dados.musicas.forEach(musica => {
        console.log(`${musica.id} - ${musica.nome}`);
      });
    }
  } catch (erro) {
    console.error('Erro:', erro);
  }
}

listarMusicas();
```

### Exemplo 2: Criar Um Sistema de Favoritos (JavaScript)

```javascript
// Armazenar favoritos no localStorage
const favoritos = new Set(JSON.parse(localStorage.getItem('favoritos') || '[]'));

function marcarComoFavorito(musicaId) {
  favoritos.add(musicaId);
  localStorage.setItem('favoritos', JSON.stringify([...favoritos]));
  console.log('❤️ Adicionado aos favoritos');
}

function desfavoritar(musicaId) {
  favoritos.delete(musicaId);
  localStorage.setItem('favoritos', JSON.stringify([...favoritos]));
  console.log('💔 Removido dos favoritos');
}

function isFavorito(musicaId) {
  return favoritos.has(musicaId);
}
```

### Exemplo 3: Buscar Música (Python)

```python
import requests

def buscar_musica(termo):
    """Busca uma música pelo nome"""
    res = requests.get('http://localhost:1905/api/musicas')
    dados = res.json()['dados']['musicas']
    
    termo = termo.lower()
    resultados = [m for m in dados if termo in m['nome'].lower()]
    
    return resultados

# Usar:
resultados = buscar_musica('poesia')
for m in resultados:
    print(f"{m['nome']} - {m['arquivo']}")
```

### Exemplo 4: Contador de Reproduções (JavaScript)

```javascript
// Armazenar quantas vezes cada música foi tocada
const contagemReproduzidas = {};

function registrarReproducao(musicaId) {
  contagemReproduzidas[musicaId] = 
    (contagemReproduzidas[musicaId] || 0) + 1;
  
  console.log(`Tocada ${contagemReproduzidas[musicaId]} vezes`);
}

function obterMusicasMaisTocadas() {
  return Object.entries(contagemReproduzidas)
    .sort((a, b) => b[1] - a[1]);
}
```

---

## 🚀 Próximas Features

Ao entender estes exemplos, você pode implementar:

- [ ] Sistema de favoritos
- [ ] Histórico de reprodução
- [ ] Busca de músicas
- [ ] Gêneros/categorias
- [ ] Rating das músicas
- [ ] Temas/Dark mode
- [ ] Seleção de múltiplas
- [ ] Atalhos de teclado

---

## 💡 Dicas

1. **Use DevTools (F12)** para debugar
2. **Procure por erros no console** se algo não funcionar
3. **Teste com cURL primeiro** para validar API
4. **Use Postman** para testes mais avançados
5. **Consulte o README.md** para mais informações

---

**Boa sorte! 🎵❤️**
