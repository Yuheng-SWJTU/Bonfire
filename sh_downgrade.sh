# This script is used to downgrade the database and the tables

export FLASK_APP="app.py"
# shellcheck disable=SC2154
"$env":FLASK_APP = "app.py"

echo "[Bonfire] Downgrading database and tables"

echo "[Bonfire] The database migration history list:"
flask db history
echo "[Bonfire] We are running 'flask db downgrade'..."
flask db downgrade

# End of file