// Love Player - Frontend Estático
// Este arquivo foi convertido para funcionar sem dependência de backend

const musicas = [
  { nome: 'Amor e Fé', arquivo: 'musicas/amor-e-fe.mp3' },
  { nome: 'Baby, Cé e Gata', arquivo: 'musicas/baby-ce-e-gata.mp3' },
  { nome: 'Canto da Sereia', arquivo: 'musicas/canto-da-sereia.mp3' },
  { nome: 'Casado', arquivo: 'musicas/casado.mp3' },
  { nome: 'Cupido', arquivo: 'musicas/cupido.mp3' },
  { nome: 'Doce Veneno', arquivo: 'musicas/doce-veneno.mp3' },
  { nome: 'Fala na Cara', arquivo: 'musicas/fala-na-cara.mp3' },
  { nome: 'Licor 43', arquivo: 'musicas/licor-43.mp3' },
  { nome: 'Nem Ligo pro Amor', arquivo: 'musicas/nem-ligo-pro-amor.mp3' },
  { nome: 'Opções', arquivo: 'musicas/opcoes.mp3' },
  { nome: 'Orgulho', arquivo: 'musicas/orgulho.mp3' },
  { nome: 'Poesia 12', arquivo: 'musicas/poesia-12.mpeg' },
  { nome: 'Poesia 13', arquivo: 'musicas/poesia-13.mp3' },
  { nome: 'Poesia 7', arquivo: 'musicas/poesia-7.mp3' },
  { nome: 'Poesia 9', arquivo: 'musicas/poesia-9.mp3' },
  { nome: 'Sal e Pimenta', arquivo: 'musicas/sal-e-pimenta.mp3' },
  { nome: 'Segredo', arquivo: 'musicas/segredo.mp3' },
  { nome: 'Tem Café', arquivo: 'musicas/tem-cafe.mp3' },
  { nome: 'Transei com a Morte', arquivo: 'musicas/transei-com-a-morte.mp3' },
  { nome: 'Vagalumes', arquivo: 'musicas/vagalumes.mp3' },
  { nome: 'Veterano', arquivo: 'musicas/veterano.mp3' }
];

let musicaAtual = null;
let indexMusica = 0;
let modoRepeat = 1;

const audio = document.getElementById('audio');
const musicaNome = document.getElementById('musica-nome');
const progresso = document.getElementById('progresso');
const tempoAtual = document.getElementById('atual');
const duracaoTotal = document.getElementById('duracao');
const btnPlay = document.getElementById('btnPlay');
const btnRepeat = document.getElementById('btnRepeat');
const playlistElement = document.getElementById('playlist');

window.addEventListener('DOMContentLoaded', () => {
  renderizarPlaylist();
  configurarAudio();
});

function renderizarPlaylist() {
  playlistElement.innerHTML = '';

  musicas.forEach((musica, index) => {
    const item = document.createElement('li');
    item.textContent = musica.nome;
    item.className = 'playlist-item';
    item.tabIndex = 0;
    item.addEventListener('click', () => carregarMusica(index));
    item.addEventListener('keypress', (event) => {
      if (event.key === 'Enter') {
        carregarMusica(index);
      }
    });

    playlistElement.appendChild(item);
  });

  destaqueSelecao();
}

function carregarMusica(index) {
  if (!musicas[index]) {
    return;
  }

  indexMusica = index;
  musicaAtual = musicas[index];

  audio.src = musicaAtual.arquivo;
  musicaNome.textContent = musicaAtual.nome;
  audio.load();
  btnPlay.textContent = '▶️';

  destaqueSelecao();
}

function playPause() {
  if (!audio.src) {
    return;
  }

  if (audio.paused) {
    audio.play();
    btnPlay.textContent = '⏸️';
  } else {
    audio.pause();
    btnPlay.textContent = '▶️';
  }
}

function proxima() {
  if (musicas.length === 0) {
    return;
  }

  indexMusica = (indexMusica + 1) % musicas.length;
  carregarMusica(indexMusica);
  audio.play();
}

function anterior() {
  if (musicas.length === 0) {
    return;
  }

  indexMusica = (indexMusica - 1 + musicas.length) % musicas.length;
  carregarMusica(indexMusica);
  audio.play();
}

function alternarRepeat() {
  modoRepeat = modoRepeat === 1 ? 2 : 1;
  btnRepeat.textContent = modoRepeat === 1 ? '🔁' : '🔂';
}

function configurarAudio() {
  audio.addEventListener('timeupdate', () => {
    if (audio.duration) {
      const progressoAtual = (audio.currentTime / audio.duration) * 100;
      progresso.value = progressoAtual;
      tempoAtual.textContent = formatarTempo(audio.currentTime);
    }
  });

  audio.addEventListener('loadedmetadata', () => {
    duracaoTotal.textContent = formatarTempo(audio.duration);
  });

  audio.addEventListener('ended', () => {
    if (modoRepeat === 2) {
      audio.currentTime = 0;
      audio.play();
    } else {
      proxima();
    }
  });

  progresso.addEventListener('input', () => {
    if (!audio.duration) {
      return;
    }

    const tempo = (progresso.value / 100) * audio.duration;
    audio.currentTime = tempo;
  });
}

function destaqueSelecao() {
  const itens = document.querySelectorAll('.playlist-item');
  itens.forEach((item, index) => {
    item.classList.toggle('selecionado', index === indexMusica);
  });
}

function formatarTempo(segundos) {
  const minutos = Math.floor(segundos / 60);
  const segundosRestantes = Math.floor(segundos % 60);
  return `${minutos}:${segundosRestantes.toString().padStart(2, '0')}`;
}
