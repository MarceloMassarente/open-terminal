import click
import uvicorn


@click.group()
def main():
    """open-terminal — terminal interaction API"""
    pass


BANNER = r"""
   ____                    _____                   _             _
  / __ \                  |_   _|                 (_)           | |
 | |  | |_ __   ___ _ __   | | ___ _ __ _ __ ___  _ _ __   __ _| |
 | |  | | '_ \ / _ | '_ \  | |/ _ | '__| '_ ` _ \| | '_ \ / _` | |
 | |__| | |_) |  __| | | | | |  __| |  | | | | | | | | | | (_| | |
  \____/| .__/ \___|_| |_| \_/\___|_|  |_| |_| |_|_|_| |_|\__,_|_|
        | |
        |_|
"""


@main.command()
@click.option("--host", default="0.0.0.0", help="Bind host")
@click.option("--port", default=8000, type=int, help="Bind port")
@click.option(
    "--api-key",
    default="",
    envvar="OPEN_TERMINAL_API_KEY",
    help="Bearer API key (or set OPEN_TERMINAL_API_KEY env var)",
)
def run(host: str, port: int, api_key: str):
    """Start the sandbox API server."""
    import os
    import secrets

    generated = not api_key
    if not api_key:
        api_key = secrets.token_urlsafe(24)

    os.environ["OPEN_TERMINAL_API_KEY"] = api_key

    click.echo(BANNER)
    if generated:
        click.echo("=" * 60)
        click.echo(f"  API Key: {api_key}")
        click.echo("=" * 60)
    click.echo()

    uvicorn.run("open_terminal.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
