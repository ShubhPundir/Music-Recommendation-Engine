# Project Setup with `uv`

This guide explains how to install `uv` and sync dependencies for your project.

## Prerequisites

Ensure you have Python installed. You can check by running:

```sh
python --version
```

or

```sh
python3 --version
```

## 1. Installing `uv`

`uv` is a fast Python package manager. To install it, run:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternatively, you can install `uv` via `pipx`:

```sh
pipx install uv
```

or using `cargo` (if you have Rust installed):

```sh
cargo install --locked uv
```

## 2. Syncing Dependencies

Once `uv` is installed, navigate to your project directory and run:

```sh
uv venv
uv sync
```

This will create a virtual environment and install dependencies from `pyproject.toml` or `requirements.txt`.

## 3. Activating the Virtual Environment

After syncing dependencies, activate the virtual environment:

- **Linux/macOS**:

  ```sh
  source .venv/bin/activate
  ```

- **Windows (PowerShell)**:

  ```sh
  .venv\Scripts\Activate.ps1
  ```

- **Windows (CMD)**:

  ```sh
  .venv\Scripts\activate.bat
  ```

## 4. Running the Project

Once activated, you can run your Python scripts as usual:

```sh
python your_script.py
```

## 5. Deactivating the Virtual Environment

To deactivate the virtual environment, simply run:

```sh
deactivate
```

## Additional Commands

- To install a new package:

  ```sh
  uv pip install package_name
  ```

- To update dependencies:

  ```sh
  uv pip upgrade
  ```

- To remove a package:

  ```sh
  uv pip uninstall package_name
  ```

---

Now your project is set up with `uv`, and dependencies are managed efficiently!


## Environment Variable Setup

Create a `.env` file in the root of your project directory with the following content:

```dotenv
LASTFM_API_KEY="your_lastfm_api_key"
GENIUS_ACCESS_TOKEN="your_genius_access_token"
MUSICBRAINZ_USER_AGENT="your_user_agent_string"

MONGO_ATLAS_URI="your_mongodb_connection_uri"

COCKROACH_USER="your_cockroach_user"
COCKROACH_PASS="your_cockroach_password"
COCKROACH_HOST="your_cockroach_host"
COCKROACH_PORT="your_cockroach_port"
```

---

### Get .env keys

🔑 How to Obtain API Keys
- Last.fm API Key:
Sign up or log in at https://www.last.fm/api, then create an API account to get your API key.

- Genius Access Token:
Register as a developer at https://genius.com/developers, create a new API client, and use the generated access token.

- MusicBrainz User Agent:
This is a custom string used to identify your application when making requests to the MusicBrainz API. Format:
"YourAppName/Version (your-email@example.com)"
MusicBrainz API Guidelines

- MongoDB Atlas URI:
Create a free cluster at https://www.mongodb.com/cloud/atlas, then click on "Connect" → "Connect your application" to get the URI.

- CockroachDB Credentials:
Sign up at https://www.cockroachlabs.com/get-started-cockroachdb/, create a serverless instance, and find your connection details under the "Connect" tab.