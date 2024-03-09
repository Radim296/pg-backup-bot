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

1. **Clone the repository**

    First, clone this repository to your local machine or server where you wish to run the backup service.

2. **Configure Environment Variables**

    Create a `.env` file in the project root directory. Populate it with the necessary environment variables:

    ```
    DB_HOST=your_database_host
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_NAME=your_database_name
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    CHAT_ID=your_telegram_chat_id
    ```

    Make sure to replace the placeholders with your actual database details and Telegram bot information.

3. **Setup Docker Compose**

    Within the project's root, create a `docker-compose.yml` file with the following content:

    ```yaml
    version: '3.8'
    services:
      backup_bot:
        build: .
        environment:
          - DB_HOST=${DB_HOST}
          - DB_USER=${DB_USER}
          - DB_PASSWORD=${DB_PASSWORD}
          - DB_NAME=${DB_NAME}
          - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
          - CHAT_ID=${CHAT_ID}
        volumes:
          - ./backup_script.sh:/usr/src/app/backup_script.sh
    ```

    This file instructs Docker Compose on how to build and run the service, passing in the necessary environment variables and mapping the backup script into the container.

4. **Build and Run**

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
