RESP=$1

if [[ ${RESP} -eq 500 ]]; then
    echo "[ERROR] Looks like the Flask app has crashed!"
    # TODO - Call a shell script to rerun the app
else
    echo "Health Status: ✅"
fi