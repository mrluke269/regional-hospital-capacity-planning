## Windows vs macOS Basics

| Task | Windows | macOS |
|-----|--------|-------|
| Activate virtual environment | `venv\Scripts\activate` | `source venv/bin/activate` |
| Path separator | `\` | `/` |
| Home folder | `C:\Users\Admin\` | `/Users/lukesm/` or `~` |
| SSH keys location | `C:\Users\Admin\.ssh` | `~/.ssh` |
| Terminal | PowerShell | Terminal (zsh) |


if platform.system() == "Windows":
    SNOWFLAKE_KEY_PATH = r"C:\Users\Admin\.ssh\snowflake_key.p8"
elif platform.system() == "Darwin":
    SNOWFLAKE_KEY_PATH = os.path.expanduser("~/.ssh/snowflake_key.p8")
else:
    SNOWFLAKE_KEY_PATH = "/opt/airflow/keys/snowflake_key.p8"

with open(SNOWFLAKE_KEY_PATH, 'rb') as key_file:
    private_key_pem = key_file.read()