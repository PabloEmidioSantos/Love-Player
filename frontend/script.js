

const musicas = [
  { nome: "Amor e Fé", arquivo: "musicas/amor-e-fe.mp3" },
  { nome: "Baby Se é Gata", arquivo: "musicas/baby-ce-e-gata.mp3" },
  { nome: "Canto da Sereia", arquivo: "musicas/canto-da-sereia.mp3" },
  { nome: "Set dos Casados", arquivo: "musicas/casado.mp3" },
  { nome: "Cupido", arquivo: "musicas/cupido.mp3" },
  { nome: "Doce Veneno", arquivo: "musicas/doce-veneno.mp3" },
  { nome: "Fala na Cara", arquivo: "musicas/fala-na-cara.mp3" },
  { nome: "Licor 43", arquivo: "musicas/licor-43.mp3" },
  { nome: "Nem Ligo pro Amor", arquivo: "musicas/nem-ligo-pro-amor.mp3" },
  { nome: "Opções", arquivo: "musicas/opcoes.mp3" },
  { nome: "Orgulho", arquivo: "musicas/orgulho.mp3" },
  { nome: "Poesia Acustica 7", arquivo: "musicas/poesia-7.mp3" },
  { nome: "Poesia Acustica 9", arquivo: "musicas/poesia-9.mp3" },
  { nome: "Poesia Acustica 12", arquivo: "musicas/poesia-12.mpeg" },
  { nome: "Poesia Acustica 13", arquivo: "musicas/poesia-13.mp3" },
  { nome: "Sal e Pimenta", arquivo: "musicas/sal-e-pimenta.mp3" },
  { nome: "Segredo", arquivo: "musicas/segredo.mp3" },
  { nome: "Tem Café", arquivo: "musicas/tem-cafe.mp3" },
  { nome: "Transei com a Morte", arquivo: "musicas/transei-com-a-morte.mp3" },
  { nome: "Vagalumes", arquivo: "musicas/vagalumes.mp3" },
  { nome: "Veterano", arquivo: "musicas/veterano.mp3" },
];

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

/* ================= PLAYLIST ================= */

playlist.innerHTML = "";

musicas.forEach((m, i) => {
  const li = document.createElement("li");
  li.textContent = m.nome;
  li.onclick = () => carregarMusica(i);
  playlist.appendChild(li);
});

/* ================= FUNÇÕES ================= */

function carregarMusica(i) {
  index = i;
  audio.src = musicas[i].arquivo;
  nome.textContent = musicas[i].nome;

  destacarMusica();

  audio.play().then(() => {
    btnPlay.textContent = "⏸";
  }).catch(() => {
    btnPlay.textContent = "▶️";
  });
}

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

function proxima() {
  index = (index + 1) % musicas.length;
  carregarMusica(index);
}

function anterior() {
  index = (index - 1 + musicas.length) % musicas.length;
  carregarMusica(index);
}

/* ================= REPEAT (SPOTIFY) ================= */

function alternarRepeat() {
  modoRepeat = (modoRepeat + 1) % 3;

  btnRepeat.classList.remove("ativo", "musica");

  if (modoRepeat === 1) {
    btnRepeat.classList.add("ativo");
    btnRepeat.textContent = "🔁";
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

