# ====================================
# SERVIÇO DE MÚSICAS
# ====================================
# Aqui fica toda a lógica relacionada a músicas
# Isso separa a lógica de negócio das rotas

from modelos import Musica, Playlist


class ServicoMusicas:
    """
    Serviço para gerenciar músicas e playlists.
    
    Esta classe centraliza toda a lógica relacionada a músicas,
    facilitando manutenção, testes e reutilização.
    
    Exemplo:
        >>> servico = ServicoMusicas()
        >>> musicas = servico.obter_todas_musicas()
    """
    
    def __init__(self):
        """Inicializa o serviço com a playlist padrão."""
        self.playlist = self._criar_playlist_padrao()
    
    def _criar_playlist_padrao(self) -> Playlist:
        """
        Cria a playlist padrão com as músicas do projeto.
        
        Esta é uma lista hardcoded das músicas disponíveis.
        Em um projeto real, isso viria de um banco de dados.
        
        Returns:
            Playlist: Playlist com todas as músicas
        """
        playlist = Playlist(titulo="Love Player - Playlist Oficial")
        
        # Lista de músicas (hardcoded, mas fácil de migrar para BD)
        musicas_dados = [
            {"nome": "Amor e Fé", "arquivo": "musicas/amor-e-fe.mp3"},
            {"nome": "Baby Se é Gata", "arquivo": "musicas/baby-ce-e-gata.mp3"},
            {"nome": "Canto da Sereia", "arquivo": "musicas/canto-da-sereia.mp3"},
            {"nome": "Set dos Casados", "arquivo": "musicas/casado.mp3"},
            {"nome": "Cupido", "arquivo": "musicas/cupido.mp3"},
            {"nome": "Doce Veneno", "arquivo": "musicas/doce-veneno.mp3"},
            {"nome": "Fala na Cara", "arquivo": "musicas/fala-na-cara.mp3"},
            {"nome": "Licor 43", "arquivo": "musicas/licor-43.mp3"},
            {"nome": "Nem Ligo pro Amor", "arquivo": "musicas/nem-ligo-pro-amor.mp3"},
            {"nome": "Opções", "arquivo": "musicas/opcoes.mp3"},
            {"nome": "Orgulho", "arquivo": "musicas/orgulho.mp3"},
            {"nome": "Poesia Acustica 7", "arquivo": "musicas/poesia-7.mp3"},
            {"nome": "Poesia Acustica 9", "arquivo": "musicas/poesia-9.mp3"},
            {"nome": "Poesia Acustica 12", "arquivo": "musicas/poesia-12.mpeg"},
            {"nome": "Poesia Acustica 13", "arquivo": "musicas/poesia-13.mp3"},
            {"nome": "Sal e Pimenta", "arquivo": "musicas/sal-e-pimenta.mp3"},
            {"nome": "Segredo", "arquivo": "musicas/segredo.mp3"},
            {"nome": "Tem Café", "arquivo": "musicas/tem-cafe.mp3"},
            {"nome": "Transei com a Morte", "arquivo": "musicas/transei-com-a-morte.mp3"},
            {"nome": "Vagalumes", "arquivo": "musicas/vagalumes.mp3"},
            {"nome": "Veterano", "arquivo": "musicas/veterano.mp3"},
        ]
        
        # Adiciona as músicas à playlist
        for musica_data in musicas_dados:
            musica = Musica(
                nome=musica_data["nome"],
                arquivo=musica_data["arquivo"]
            )
            playlist.adicionar_musica(musica)
        
        return playlist
    
    def obter_todas_musicas(self) -> dict:
        """
        Retorna todas as músicas da playlist.
        
        Returns:
            dict: Dicionário com os dados da playlist
        
        Exemplo de resposta:
            {
                "titulo": "Love Player - Playlist Oficial",
                "total_musicas": 21,
                "musicas": [...]
            }
        """
        return self.playlist.para_dict()
    
    def obter_musica_por_id(self, id: int) -> dict or None:
        """
        Retorna uma música específica pelo ID.
        
        Args:
            id (int): ID da música
        
        Returns:
            dict or None: Dicionário da música ou None se não encontrada
        
        Exemplo:
            >>> servico.obter_musica_por_id(0)
            {
                'id': 0,
                'nome': 'Amor e Fé',
                'arquivo': 'musicas/amor-e-fe.mp3'
            }
        """
        musica = self.playlist.obter_musica_por_id(id)
        return musica.para_dict() if musica else None
    
    def contar_musicas(self) -> int:
        """
        Retorna o total de músicas na playlist.
        
        Returns:
            int: Total de músicas
        """
        return self.playlist.contar_musicas()
    
    def obter_proxima_musica(self, id_atual: int) -> dict or None:
        """
        Retorna a próxima música na playlist.
        
        Usa lógica cíclica (ao final, volta para o início).
        
        Args:
            id_atual (int): ID da música atual
        
        Returns:
            dict or None: Dicionário da próxima música
        """
        total = self.contar_musicas()
        proximo_id = (id_atual + 1) % total
        return self.obter_musica_por_id(proximo_id)
    
    def obter_musica_anterior(self, id_atual: int) -> dict or None:
        """
        Retorna a música anterior na playlist.
        
        Usa lógica cíclica (antes do início, vai para o final).
        
        Args:
            id_atual (int): ID da música atual
        
        Returns:
            dict or None: Dicionário da música anterior
        """
        total = self.contar_musicas()
        anterior_id = (id_atual - 1 + total) % total
        return self.obter_musica_por_id(anterior_id)
