# ====================================
# MODELOS DE DADOS
# ====================================
# Aqui definimos as estruturas de dados usadas no projeto
# Isso facilita o entendimento e reutilização

from dataclasses import dataclass
from typing import List


@dataclass
class Musica:
    """
    Representa uma música na playlist.
    
    Atributos:
        nome (str): Nome da música
        arquivo (str): Caminho do arquivo de áudio
        id (int): Identificador único (opcional)
    
    Exemplo:
        >>> musica = Musica(nome="Amor e Fé", arquivo="musicas/amor-e-fe.mp3", id=1)
        >>> print(musica.nome)
        Amor e Fé
    """
    nome: str
    arquivo: str
    id: int = None
    
    def para_dict(self) -> dict:
        """
        Converte a música em dicionário.
        
        Returns:
            dict: Dicionário com os dados da música
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'arquivo': self.arquivo
        }


@dataclass
class Playlist:
    """
    Representa uma playlist de músicas.
    
    Atributos:
        musicas (List[Musica]): Lista de músicas
        titulo (str): Título da playlist
    
    Exemplo:
        >>> playlist = Playlist(titulo="Melhores Músicas")
        >>> playlist.adicionar_musica(musica1)
    """
    titulo: str
    musicas: List[Musica] = None
    
    def __post_init__(self):
        """Inicializa a lista de músicas se não for fornecida."""
        if self.musicas is None:
            self.musicas = []
    
    def adicionar_musica(self, musica: Musica) -> None:
        """
        Adiciona uma música à playlist.
        
        Args:
            musica (Musica): A música a ser adicionada
        """
        musica.id = len(self.musicas)
        self.musicas.append(musica)
    
    def obter_musicas(self) -> List[dict]:
        """
        Retorna todas as músicas como dicionários.
        
        Returns:
            List[dict]: Lista de dicionários das músicas
        """
        return [musica.para_dict() for musica in self.musicas]
    
    def obter_musica_por_id(self, id: int) -> Musica or None:
        """
        Retorna uma música pelo ID.
        
        Args:
            id (int): ID da música
        
        Returns:
            Musica or None: A música encontrada ou None
        """
        for musica in self.musicas:
            if musica.id == id:
                return musica
        return None
    
    def contar_musicas(self) -> int:
        """
        Retorna a quantidade de músicas.
        
        Returns:
            int: Quantidade de músicas
        """
        return len(self.musicas)
    
    def para_dict(self) -> dict:
        """
        Converte a playlist em dicionário.
        
        Returns:
            dict: Dicionário com os dados da playlist
        """
        return {
            'titulo': self.titulo,
            'total_musicas': self.contar_musicas(),
            'musicas': self.obter_musicas()
        }
