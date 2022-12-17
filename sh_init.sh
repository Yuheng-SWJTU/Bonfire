# This scripts is used to initialize the database and the tables
# It just needs to be run once
export FLASK_APP="app.py"
# shellcheck disable=SC2154
"$env":FLASK_APP = "app.py"

echo "[Bonfire] Initializing database and tables"
echo "WARNING: This scripts just needs to be run once"

echo "[Bonfire] We are running 'flask db init'..."
flask db init
echo "[Bonfire] We are running 'flask db migrate'..."
flask db migrate
echo "[Bonfire] We are running 'flask db upgrade'..."
flask db upgrade

# End of file