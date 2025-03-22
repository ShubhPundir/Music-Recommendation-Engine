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
