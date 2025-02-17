# Cuomputer ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

The bot for my Discord server.  
[Join the Discord Server](https://discord.gg/mr-rivers-neighborhood)

> **Note:** This repository does not include sensitive tokens and secrets. To use or contribute to this project, you'll need to set up your own credentials.

## Table of Contents

- [Setup](#setup)
  - [Installation](#installation)
    - [Python Virtual Environment](#python-virtual-environment)
    - [Install Dependencies](#install-dependencies)
  - [Environment Variables](#environment-variables)
    - [Discord Credentials](#discord-credentials)
    - [API Keys](#api-keys)
    - [Service Account Credentials](#service-account-credentials)
- [Running the Bot](#running-the-bot)
- [Debugging](#debugging)
- [Testing](#testing)
  - [Unit Tests](#unit-tests)
- [Contributing](#contributing)
- [Owner Setup](#owner-setup)
  - [Heroku Deployment](#heroku-deployment)
    - [Environment Variables on Heroku](#environment-variables-on-heroku)
    - [Deploy to Heroku](#deploy-to-heroku)
  - [Discord Bot Setup](#discord-bot-setup)

## Setup

### Installation

#### Python Virtual Environment

It's recommended to use a virtual environment to manage dependencies. For detailed instructions, refer to the [official Python venv documentation](https://docs.python.org/3/library/venv.html).

1. **Create Virtual Environment:**

   ```bash
   python -m venv venv_name
   ```

   Replace `venv_name` with a name appropriate for your machine (e.g., `desktop`, `laptop`).

2. **Activate Virtual Environment:**

   - **Windows:**
     ```bash
     venv_name\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv_name/bin/activate
     ```

#### Install Dependencies

1. **Activate Virtual Environment:**
   
   Ensure your virtual environment is activated (see above).

2. **Install Required Packages:**
   
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Environment variables need to be set locally using a `.env` file. Heroku configurations are handled separately in the **Owner Setup** section.

#### Discord Credentials

Create a `.env` file in the root directory of your project and add the following:

```env
CLIENT_ID=your_discord_client_id
CLIENT_SECRET=your_discord_client_secret
TOKEN=your_discord_bot_token
```

#### API Keys

Add your API keys to the `.env` file:

```env
REPLICATE_API_TOKEN=your_replicate_api_token
OPENAI_API_KEY=your_openai_api_key
```

#### Service Account Credentials

##### gspreader [Service Account]

- **Local Setup (`.env`):**

  If your project requires a path to a credentials JSON file, add the following to your `.env` file:

  ```env
  GSPREADER_GOOGLE_CREDS_PATH=path/to/your/gspreader_credentials.json
  ```

  *Ensure that the JSON file is **not** committed to version control.*

##### Firestore and Google Drive [Service Account]

- **Local Setup (`.env`):**

  Add the path to your Firestore credentials JSON file:

  ```env
  GOOGLE_CREDENTIALS_PATH=path/to/your/google_credentials.json
  ```

## Running the Bot

Execute the following command in the root directory:

```bash
python main.py
```

## Debugging

To debug the bot using VSCode:

1. Open `main.py` in VSCode.
2. Press the **Run** button or use the shortcut `F5` to start the debugger.

## Testing

### Unit Tests

Unit tests are located in the `tests/unit_tests` directory.

1. **Set Up Environment Variables for Testing:**

   Ensure that `PYTHONPATH` is set to the root directory. This allows `pytest` to locate your modules correctly.

   - **Windows:**
     ```bash
     set PYTHONPATH=%cd%
     ```
   - **macOS/Linux:**
     ```bash
     export PYTHONPATH=.
     ```

2. **Run Unit Tests:**

   ```bash
   pytest tests/unit_tests
   ```

   *If you do not have `pytest` installed, you can install it using:*
   ```bash
   pip install pytest
   ```

   For more information, refer to the [pytest documentation](https://docs.pytest.org/en/stable/getting-started.html).

## Contributing

Contributions are welcome! Here's how you can help:

- **Areas of Interest:**
  - `bot/on_message` folder
  - `bot/scripts` folder

- **Steps to Contribute:**
  1. Fork the repository.
  2. Create a new branch for your feature or bugfix.
  3. Commit your changes with clear messages.
  4. Push to your fork and submit a Pull Request.

*Please ensure that you adhere to the project's coding standards and include tests for your contributions.*

## Owner Setup

*This section is intended for the project owner only.*

### Heroku Deployment

#### Environment Variables on Heroku

Environment variables need to be set on Heroku to ensure the bot functions correctly in the production environment.

1. **Navigate to Heroku Dashboard:**
   - Go to your [Heroku Dashboard](https://dashboard.heroku.com/) and select your app.

2. **Set Config Vars:**
   - Navigate to the **Settings** tab.
   - Click on **"Reveal Config Vars"**.
   - Add the following variables:

     ##### Discord Credentials
     ```
     CLIENT_ID=your_discord_client_id
     CLIENT_SECRET=your_discord_client_secret
     TOKEN=your_discord_bot_token
     ```

     ##### API Keys
     ```
     REPLICATE_API_TOKEN=your_replicate_api_token
     OPENAI_API_KEY=your_openai_api_key
     ```

     ##### Service Account Credentials

     - **gspreader [Service Account]:**
       ```
       GSPREADER_GOOGLE_CREDS={"your": "json_content"}
       ```
     
     - **Firestore and Google Drive [Service Account]:**
       ```
       GOOGLE_CREDENTIALS={"your": "json_content"}
       ```

     *Ensure that the JSON content is properly formatted as a single-line string.*

#### Deploy to Heroku

This project is configured to automatically deploy to Heroku when you push to the `main` branch.

1. **Ensure Heroku Remote is Set:**
   ```bash
   git remote add heroku https://git.heroku.com/your-heroku-app.git
   ```

2. **Push to Heroku:**
   ```bash
   git push heroku main
   ```

*Note: Replace `your-heroku-app` with your actual Heroku app name.*

### Discord Bot Setup

1. **Create a Discord Application:**
   - Go to the [Discord Developer Portal](https://discord.com/developers).
   - Click on **"New Application"** and follow the prompts to create your bot.

2. **Authorize the Bot:**
   - Use the following URL template to authorize your bot:
     ```
     https://discord.com/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&scope=bot&permissions=PERMISSIONS_INT
     ```
   - Replace `YOUR_BOT_CLIENT_ID` with your bot's client ID.
   - Set `PERMISSIONS_INT` to the desired permissions integer (e.g., `8` for admin).

*Ensure that sensitive information such as `CLIENT_ID`, `CLIENT_SECRET`, and `TOKEN` are securely stored and **never** committed to version control.*

---

**Happy Coding!** 🚀

---
