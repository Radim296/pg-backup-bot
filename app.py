import asyncio

from app.main import start_bot


def main():
    """
    The main function sets up an event loop and runs it indefinitely.
    """
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
