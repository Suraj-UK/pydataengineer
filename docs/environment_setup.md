# Local Environment Setup Guide

This guide summarizes the required tooling and verification steps for running the
`pydataengineer` exercises locally.

## 1. Prerequisites

Install the following system dependencies before creating the Python
environment.  Each step includes platform-specific commands and a quick
verification so you can confirm everything is wired up correctly.

1. **Python 3.11.x** – the project is pinned to Python 3.11 via Poetry.
   Choose the method that best matches your operating system:

   **Windows** – install [Python 3.11](https://www.python.org/downloads/windows/)
     using the official installer (check **“Add python.exe to PATH”**). Verify the runtime with:
   ```bash
   python --version  # should print 3.11.x
   ```

2. **Poetry** – manages dependencies and the virtual environment.  Poetry’s
   recommended installer works across platforms:
   
   On Windows PowerShell:
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content |
       python -
   ```
   Restart your shell and confirm installation:
   ```bash
   poetry --version
   ```

3. **Java 11 (OpenJDK)** – PySpark uses the JVM.  Install the LTS release that
   matches CI:
   - **Windows**: download and install [Zulu OpenJDK 11](https://www.azul.com/downloads/)
     or another OpenJDK 11 build, then set the `JAVA_HOME` environment variable.

   Verify Java is available:
   ```bash
   java -version  # should report version 11
   ```

4. **Windows-only Hadoop tooling**
   ```powershell
   choco install vcredist2010
   git clone --depth 1 -b master https://github.com/cdarlint/winutils.git
   $env:HADOOP_HOME = "$PWD\winutils\hadoop-3.3.5"
   $env:Path += ";$env:HADOOP_HOME\bin"
   winutils.exe chmod 777 C:\path\to\project
   ```

## 2. Create and Activate the Poetry Environment

```bash
poetry lock
poetry install
poetry run jupyter notebook
```

## 3. Configure Spark / PySpark

PySpark 3.5.1 is pinned to align with the remote Gitpod image and CI runners.
On macOS/Linux, installing Java 11 is sufficient—PySpark bundles its own Spark
binaries.

On native Windows (without WSL), download the Hadoop `winutils` package that
matches the Spark Hadoop version (3.3.x) and set the following environment
variables before launching VS Code or Jupyter:

```powershell
$env:HADOOP_HOME = "C:\\path\\to\\winutils\\hadoop-3.3.5"
$env:PATH += ";$env:HADOOP_HOME\\bin"
```

Run `winutils.exe chmod 777 <project_path>` once to confirm the Hadoop tooling
works, mirroring the CI check.

## 4. (Optional) VS Code Integration

1. Install the Python, Jupyter, and PySpark extensions.
2. Open the folder in VS Code and allow it to detect the Poetry virtual
   environment.
3. Configure any linters/formatters to use the Poetry environment so imports
   resolve correctly.

## 5. Verify the Setup

Run the full suite of project checks from the repository root:

```bash
poetry run pytest tests/unit
poetry run pytest tests/integration
poetry run mypy --ignore-missing-imports --disallow-untyped-calls \
               --disallow-untyped-defs --disallow-incomplete-defs \
               data_transformations tests
poetry run pylint data_transformations tests
```

All commands should pass without errors.  If any command fails, address the
reported issue before the pairing session.

## 6. Working with the Data

The raw datasets live under `resources/` and are small enough to run locally.
The Spark jobs write outputs to your filesystem, so ensure you have permission
in the target directories you plan to use during the interview.

## 7. Troubleshooting Tips

- If PySpark cannot find Java, confirm `JAVA_HOME` points to a Java 11
  installation and that `java -version` reports 11.x.
- For Windows path issues, prefer WSL 2 or follow the `winutils` setup above.
- When using Jupyter notebooks, start kernels through Poetry to ensure the
  correct interpreter: `poetry run python -m ipykernel install --user \
  --name pydataengineer --display-name "Python (pydataengineer)"`.

With these steps completed, your environment matches the project’s
expectations and should be ready for the code pairing interview.