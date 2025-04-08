# LLM_text-to-sql

## Initalization

### Python Environment Setup 

#### Package Manager Setup

This project uses `uv` as the package manager.<br>Install it following the instructions at https://github.com/astral-sh/uv

```
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Database Setup

Download the Chinook database using the following command:

```
curl -s https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql | sqlite3 Chinook.db
```