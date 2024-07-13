# PostgreSQL Backup Bot 📦🔐

This project provides a robust solution for automating PostgreSQL database backups and delivering those backups directly via Telegram. It utilizes Docker to encapsulate the backup process and Telegram API for a convenient backup delivery method.

## Description 📖

Using a combination of PostgreSQL client tools, cron jobs for scheduling, and a Telegram bot for notifications and file delivery, this solution is perfect for those seeking an automated, secure, and straightforward way to handle database backups.

## Features 🌟

- Automated database backups scheduled via cron.
- Direct delivery of backup files to your Telegram chat.
- Easy setup with Docker and Docker Compose.
- Utilizes environment variables for secure handling of sensitive information.

## Prerequisites 🛠️

Before you begin, ensure you have installed:

- Docker
- Docker Compose

Also, you will need:

- PostgreSQL database access details.
- A Telegram bot token and chat ID to receive the backup files.

## Setup Instructions 🚀

1. **Setup Docker Compose**

    Within the project's root, create a `docker-compose.yml` file with the following content:

    ```yaml
    version: '3.8'
    services:
      backup_bot:
        build: https://github.com/Radim296/pg-backup-bot.git
        environment:
          - DB_HOST=
          - DB_USER=
          - DB_PASSWORD=
          - DB_NAME=
          - CHAT_ID=
          - TELEGRAM_BOT_TOKEN=

          # configuring the time (you can set one of the following options)
          - TIME_TO_SEND=00:00 # hour:minute in 24h format
          - INTERVAL=100 # minutes

          # optional variables
          - MESSAGE_THREAD_ID=
    ```

    This file instructs Docker Compose on how to build and run the service, passing in the necessary environment variables and mapping the backup script into the container.

2. **Build and Run**

    Execute the following command to build and start the backup bot:

    ```
    docker-compose up --build
    ```

    To run it in detached mode (in the background), use:

    ```
    docker-compose up -d --build
    ```

## Usage 📋

With the service running, it will execute the backup script according to the schedule defined in the crontab within the Dockerfile (default is midnight daily). The script dumps the PostgreSQL database and sends the resulting file to the specified Telegram chat.

## Contributing 🤝

Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit your contributions via pull requests.

## License 📄

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgments 💡

- This project was inspired by the need for a simple, automated backup solution with notifications and delivery via Telegram.
- Thanks to all contributors and the open-source community for the tools and libraries that made this project possible.

Let this 🚢 sail smoothly with your backups secured and delivered straight to your 📱!
