"""Main entrypoint for OPI API."""

import argparse

import uvicorn


def parse_command() -> argparse.Namespace:
    """Parse API command line arguments."""
    parser = argparse.ArgumentParser(
        description=("Starts a web server that serves a REST API for the OPI project."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--host",
        help="The host to bind to.",
        type=str,
        default="0.0.0.0",  # noqa: S104
    )
    parser.add_argument(
        "--port",
        help="The port to bind to.",
        type=int,
        default=8080,
    )

    parser.add_argument(
        "--reload",
        help="Enable auto-reload of the server.",
        type=str,
        choices=["true", "false"],
        default="false",
    )

    return parser.parse_args()


def main() -> None:
    """Start the uvicorn server."""
    args = parse_command()
    uvicorn.run(
        "app.factory:app",
        reload=args.reload == "true",
        log_level="info",
        host=args.host,
        port=args.port,
        workers=1,
        headers=[
            ("Connection", "close"),
        ],
    )


if __name__ == "__main__":
    main()
