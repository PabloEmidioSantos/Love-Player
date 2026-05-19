

// ====================================
// LOVE PLAYER - FRONTEND
// ====================================
// Script principal que controla o player de música
// Comunica com a API Python backend

let musicas = [];
let index = 0;
let modoRepeat = 1;
// 0 = desligado
// 1 = repetir playlist
// 2 = repetir música

const audio = document.getElementById("audio");
const nome = document.getElementById("musica-nome");
const progresso = document.getElementById("progresso");
const atual = document.getElementById("atual");
const duracao = document.getElementById("duracao");
const playlist = document.getElementById("playlist");
const btnPlay = document.getElementById("btnPlay");
const btnRepeat = document.getElementById("btnRepeat");

/* ================= INICIALIZAÇÃO ================= */

// Ao carregar a página, busca as músicas do backend
document.addEventListener('DOMContentLoaded', () => {
  carregarPlaylist();
  configurarAudio();
});

/* ================= FUNÇÕES DE API ================= */

/**
 * Carrega a playlist do backend (API Python)
 * 
 * Faz uma requisição GET para /api/musicas
 * Se bem-sucedida, popula o array de músicas
 * Se falhar, mostra erro no console
 */
async function carregarPlaylist() {
  try {
    const resposta = await fetch('/api/musicas');
    const dados = await resposta.json();
    
    if (dados.sucesso) {
      musicas = dados.dados.musicas;
      console.log(`✅ Playlist carregada: ${musicas.length} músicas`);
      renderizarPlaylist();
    } else {
      console.error('❌ Erro ao carregar playlist:', dados.erro);
      nome.textContent = 'Erro ao carregar músicas';
    }
  } catch (erro) {
    console.error('❌ Erro de conexão:', erro);
    nome.textContent = 'Erro de conexão com servidor';
  }
}

/**
 * Obtém a próxima música do backend
 * 
 * Usa a API para garantir consistência com o backend
 */
async function obterProximaMusica() {
  try {
    const resposta = await fetch(`/api/musicas/${index}/proxima`);
    const dados = await resposta.json();
    
    if (dados.sucesso) {
      return dados.dados;
    }
  } catch (erro) {
    console.error('❌ Erro ao obter próxima música:', erro);
  }
  return null;
}

/**
 * Obtém a música anterior do backend
 */
async function obterMusicaAnterior() {
  try {
    const resposta = await fetch(`/api/musicas/${index}/anterior`);
    const dados = await resposta.json();
    
    if (dados.sucesso) {
      return dados.dados;
    }
  } catch (erro) {
    console.error('❌ Erro ao obter música anterior:', erro);
  }
  return null;
}

/* ================= PLAYLIST ================= */

/**
 * Renderiza a lista de músicas no HTML
 * Cria elementos <li> clicáveis para cada música
 */
function renderizarPlaylist() {
  playlist.innerHTML = "";
  
  musicas.forEach((m) => {
    const li = document.createElement("li");
    li.textContent = m.nome;
    li.onclick = () => carregarMusica(m.id);
    playlist.appendChild(li);
  });
}

/* ================= FUNÇÕES DE CONTROLE DE ÁUDIO ================= */

/**
 * Configura os listeners do elemento <audio>
 * Atualiza a barra de progresso, tempo e posição da música
 */
function configurarAudio() {
  // Atualiza a barra de progresso enquanto a música toca
  audio.addEventListener('timeupdate', () => {
    if (audio.duration) {
      progresso.value = (audio.currentTime / audio.duration) * 100;
      atual.textContent = formatarTempo(audio.currentTime);
    }
  });
  
  // Atualiza duração total quando carrega metadata
  audio.addEventListener('loadedmetadata', () => {
    duracao.textContent = formatarTempo(audio.duration);
  });
  
  // Avança para próxima música quando termina (respeita repeat)
  audio.addEventListener('ended', () => {
    if (modoRepeat === 2) {
      // Repetir música atual
      carregarMusica(index);
    } else {
      // Próxima música
      proxima();
    }
  });
  
  // Permite que o usuário clique na barra para pular
  progresso.addEventListener('change', () => {
    audio.currentTime = (progresso.value / 100) * audio.duration;
  });
}

/**
 * Carrega e toca uma música específica
 * 
 * @param {number} i - Índice da música na lista
 */
function carregarMusica(i) {
  if (i < 0 || i >= musicas.length) {
    console.error('❌ Índice inválido');
    return;
  }
  
  index = i;
  const musica = musicas[i];
  
  audio.src = musica.arquivo;
  nome.textContent = musica.nome;
  
  destacarMusica();
  
  // Tenta tocar a música
  audio.play().then(() => {
    btnPlay.textContent = "⏸";
  }).catch(() => {
    btnPlay.textContent = "▶️";
    console.error('❌ Erro ao tocar áudio');
  });
}

/**
 * Alterna entre play e pause
 */
function playPause() {
  if (audio.paused) {
    audio.play().then(() => {
      btnPlay.textContent = "⏸";
    });
  } else {
    audio.pause();
    btnPlay.textContent = "▶️";
  }
}

/**
 * Vai para a próxima música
 */
async function proxima() {
  const proximaMusica = await obterProximaMusica();
  if (proximaMusica) {
    index = proximaMusica.id;
    carregarMusica(index);
  }
}

/**
 * Vai para a música anterior
 */
async function anterior() {
  const musicaAnterior = await obterMusicaAnterior();
  if (musicaAnterior) {
    index = musicaAnterior.id;
    carregarMusica(index);
  }
}

/* ================= REPEAT (SPOTIFY) ================= */

/**
 * Alterna entre os 3 modos de repetição
 * 0 = desligado
 * 1 = repetir playlist
 * 2 = repetir música individual
 */
function alternarRepeat() {
  modoRepeat = (modoRepeat + 1) % 3;
  
  btnRepeat.classList.remove("ativo", "musica");
  
  if (modoRepeat === 1) {
    // Repetir playlist
    btnRepeat.classList.add("ativo");
    btnRepeat.textContent = "🔁";
  } else if (modoRepeat === 2) {
    // Repetir música
    btnRepeat.classList.add("ativo", "musica");
    btnRepeat.textContent = "🔂";
  } else {
    // Desligado
    btnRepeat.textContent = "🔁";
  }
}

/* ================= UTILITÁRIOS ================= */

/**
 * Formata segundos para formato MM:SS
 * 
 * @param {number} segundos - Tempo em segundos
 * @returns {string} Tempo formatado (ex: "1:23")
 */
function formatarTempo(segundos) {
  if (!segundos || isNaN(segundos)) return "0:00";
  
  const minutos = Math.floor(segundos / 60);
  const secs = Math.floor(segundos % 60);
  
  return `${minutos}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Destaca a música atual na playlist
 * Remove highlight de todas as músicas e destaca a atual
 */
function destacarMusica() {
  document.querySelectorAll('#playlist li').forEach((li, i) => {
    li.style.color = i === index ? '#a855f7' : '#fff';
    li.style.fontWeight = i === index ? 'bold' : 'normal';
  });
}

  if (modoRepeat === 2) {
    btnRepeat.classList.add("ativo", "musica");
    btnRepeat.textContent = "🔂";
  }

  if (modoRepeat === 0) {
    btnRepeat.textContent = "🔁";
  }
}

audio.addEventListener("ended", () => {
  if (modoRepeat === 2) {
    audio.currentTime = 0;
    audio.play();
  } else if (modoRepeat === 1) {
    proxima();
  }
});

/* ================= PROGRESSO ================= */

audio.addEventListener("timeupdate", () => {
  progresso.value = (audio.currentTime / audio.duration) * 100 || 0;
  atual.textContent = formatarTempo(audio.currentTime);
  duracao.textContent = formatarTempo(audio.duration);
});

progresso.addEventListener("input", () => {
  audio.currentTime = (progresso.value / 100) * audio.duration;
});

/* ================= AUXILIARES ================= */

function formatarTempo(seg) {
  if (isNaN(seg)) return "0:00";
  const min = Math.floor(seg / 60);
  const sec = Math.floor(seg % 60).toString().padStart(2, "0");
  return `${min}:${sec}`;
}

function destacarMusica() {
  const itens = playlist.querySelectorAll("li");
  itens.forEach((li, i) => {
    li.style.color = i === index ? "#a855f7" : "#fff";
    li.style.fontWeight = i === index ? "bold" : "normal";
  });
}

