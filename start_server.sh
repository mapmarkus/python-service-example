if [[ "$WEB_RELOADER" =~ ^(True|true|1)$ ]]; then
    EXTRA_ARGS="--reload --reload-dir=app"
    echo "Server: Using reloader"
fi

uvicorn \
    --host 0.0.0.0 \
    --port 7030 \
    --log-level info \
    ${EXTRA_ARGS} app.main:app
