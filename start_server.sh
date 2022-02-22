if [[ "$APP_DEV_MODE" =~ ^(True|true|1)$ ]]; then
    EXTRA_ARGS="--reload --reload-dir=app"
    echo "Server: Using reloader"
fi

uvicorn \
    --host 0.0.0.0 \
    --port ${APP_PORT:-80} \
    --log-level info \
    ${EXTRA_ARGS} app.main:app
