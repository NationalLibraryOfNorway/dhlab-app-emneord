FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /emneord.py

        COPY requirements.txt ./requirements.txt
        RUN uv pip install --system --compile-bytecode --only-binary=:all: --no-binary=python-louvain -r requirements.txt

        COPY ./emneord.py .

        # Warm up caches
        RUN timeout 5s streamlit run emneord.py; exit 0
        RUN python -c 'import dhlab, pandas'

        CMD streamlit run emneord.py \
            --server.port ${PORT} \
            --browser.gatherUsageStats=False \
            --server.baseUrlPath /emneord-test-fast

