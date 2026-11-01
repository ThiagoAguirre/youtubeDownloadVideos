# YouTube Download

Baixa vídeos do YouTube na melhor qualidade, a partir de uma lista de links num arquivo de texto.

## Instalação (só na primeira vez)

Precisa ter **Python 3** instalado. No terminal, dentro desta pasta:

```bash
# 1. Cria o ambiente e instala tudo (sem precisar de sudo)
python3 -m venv .venv
.venv/bin/pip install -U "yt-dlp[default]" deno imageio-ffmpeg

# 2. Dá permissão para rodar o script
chmod +x baixar.sh
```

> - **deno**: o YouTube exige um runtime JavaScript; sem ele dá erro
>   "Requested format is not available".
> - **imageio-ffmpeg**: traz o ffmpeg, que junta vídeo + áudio na melhor qualidade.
>   Se o ffmpeg já estiver instalado no sistema, ele é usado no lugar.

## Como baixar

1. Abra o arquivo **`links.txt`** e cole os links, **um por linha**:

   ```
   https://www.youtube.com/watch?v=XXXXXXXXXXX
   https://youtu.be/YYYYYYYYYYY
   https://www.youtube.com/playlist?list=ZZZZZZZZZZ
   ```

   Pode ser vídeo, playlist ou canal. Linhas começando com `#` são ignoradas.

2. Rode:

   ```bash
   ./baixar.sh
   ```

3. Os vídeos ficam na pasta **`videos/`**, em MP4.

## Arquivos

| Arquivo        | Para que serve                                                  |
|----------------|-----------------------------------------------------------------|
| `links.txt`    | Onde você cola os links                                         |
| `baixar.sh`    | Atalho: atualiza o yt-dlp e começa o download                   |
| `baixar.py`    | O programa que faz o download                                   |
| `videos/`      | Onde os vídeos são salvos                                       |

## Dicas

- **Rodar de novo é seguro:** vídeos que já estão na pasta `videos/` são pulados.
  Para baixar um vídeo de novo, é só apagar o arquivo dele de `videos/`.
- **Um link falhou?** Os outros continuam baixando. Veja a mensagem de erro no terminal.
- **Parou de funcionar?** O YouTube muda com frequência. O `baixar.sh` já atualiza o
  yt-dlp a cada uso, mas você também pode atualizar na mão:
  `.venv/bin/pip install -U yt-dlp`

## Aviso

Baixe só vídeos que são seus, que estão em domínio público ou cuja licença
permite o download (como Creative Commons), conforme os termos do YouTube.
