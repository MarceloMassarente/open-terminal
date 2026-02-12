import click
import uvicorn


@click.group()
def main():
    """open-terminal — terminal interaction API"""
    pass


@main.command()
@click.option("--host", default="0.0.0.0", help="Bind host")
@click.option("--port", default=8000, type=int, help="Bind port")
def run(host: str, port: int):
    """Start the sandbox API server."""
    uvicorn.run("open_terminal.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
