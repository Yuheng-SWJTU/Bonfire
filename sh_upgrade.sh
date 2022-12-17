# This script is used to upgrade the database and the tables
# It needs to be run every time the database is changed

export FLASK_APP="app.py"
# shellcheck disable=SC2154
"$env":FLASK_APP = "app.py"

echo "[Bonfire] Upgrading database and tables"
echo "WARNING: This scripts just needs to be run every time the database is changed"

echo "[Bonfire] We are running 'flask db migrate'..."
flask db migrate
echo "[Bonfire] We are running 'flask db upgrade'..."
flask db upgrade

# End of file