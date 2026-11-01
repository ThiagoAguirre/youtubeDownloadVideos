import shutil
import sys
from pathlib import Path

from yt_dlp import YoutubeDL

PASTA = Path(__file__).resolve().parent
ARQUIVO_LINKS = PASTA / "links.txt"
PASTA_VIDEOS = PASTA / "videos"


def ler_links():
    if not ARQUIVO_LINKS.exists():
        ARQUIVO_LINKS.write_text("# Cole um link do YouTube por linha\n", encoding="utf-8")
        print(f"Criei {ARQUIVO_LINKS.name}. Cole os links nele e rode de novo.")
        sys.exit(0)
    links = []
    for linha in ARQUIVO_LINKS.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            links.append(linha)
    return links


def achar_ffmpeg():
    """ffmpeg do sistema, ou o que vem no pacote imageio-ffmpeg do .venv."""
    caminho = shutil.which("ffmpeg")
    if caminho:
        return caminho
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def achar_deno():
    """deno do .venv (pacote pip 'deno') ou do sistema; o YouTube exige um runtime JS."""
    local = Path(sys.executable).parent / "deno"
    if local.exists():
        return str(local)
    return shutil.which("deno")


def opcoes():
    ffmpeg = achar_ffmpeg()
    tem_ffmpeg = ffmpeg is not None
    if tem_ffmpeg:
        formato = "bestvideo*+bestaudio/best"
    else:
        formato = "best[acodec!=none][vcodec!=none]/best"
        print("AVISO: ffmpeg não encontrado. A qualidade fica limitada (geralmente 720p).")
        print("       Para a melhor qualidade, instale: sudo apt install ffmpeg\n")

    opts = {
        "format": formato,
        "outtmpl": str(PASTA_VIDEOS / "%(title)s [%(id)s].%(ext)s"),
        "ignoreerrors": True,
        "windowsfilenames": True,
    }
    if tem_ffmpeg:
        opts["merge_output_format"] = "mp4"
        opts["ffmpeg_location"] = ffmpeg
        opts["format_sort"] = ["res", "fps", "vcodec:h264", "acodec:aac"]
        opts["postprocessors"] = [{"key": "FFmpegCopyStream"}]
        opts["postprocessor_args"] = {"copystream": ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]}
    deno = achar_deno()
    if deno:
        opts["js_runtimes"] = {"deno": {"path": deno}}
    else:
        print("AVISO: deno não encontrado; rode: .venv/bin/pip install deno\n")
    return opts


def main():
    links = ler_links()
    if not links:
        print(f"Nenhum link em {ARQUIVO_LINKS.name}. Cole um link por linha e rode de novo.")
        return
    PASTA_VIDEOS.mkdir(exist_ok=True)
    print(f"{len(links)} link(s) encontrado(s).\n")
    with YoutubeDL(opcoes()) as ydl:
        erro = ydl.download(links)
    print(f"\nPronto! Vídeos em: {PASTA_VIDEOS}")
    if erro:
        print("Alguns links falharam; veja as mensagens acima.")


if __name__ == "__main__":
    main()
