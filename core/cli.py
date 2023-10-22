from typing import Optional

import typer

from core import __app_name__, __version__
from core.transcript import YoutubeTranscriptDownloader

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

@app.command("transcript")
def transcript(
    url: str = typer.Argument(..., help="The URL of the YouTube video."),
    filename: str = typer.Option(
        None,
        "--filename",
        "-f",
        help="The filename of the transcript.",
    ),
    key_frame: bool = typer.Option(
        False,
        "--key-frame",
        "-k",
        help="Include the key frame of each sentence.",
    ),
    folder: str = typer.Option(
        "output",
        "--folder",
        "-d",
        help="The folder to save the transcript.",
    ),
    ) -> None:

    if not url:
        typer.echo("URL is required.")
        raise typer.Exit(code=1)
    
    if not filename:
        filename = f"{url.split('=')[1]}.txt"

    typer.echo(f"URL: {url} --> {filename}")

    downloader = YoutubeTranscriptDownloader(url)
    transcripts = downloader.get_transcript()
    joiner = ""
    if key_frame:
        joiner = "".join([f"{key}: {val}\n" for key, val in transcripts.items()])
    else:
        joiner = " ".join([val for _, val in transcripts.items()])
    with open(filename, "w") as f:
        f.write("From URL: " + url + "\n")
        f.write(joiner)