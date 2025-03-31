FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /emneord.py

        COPY requirements.txt ./requirements.txt
        RUN uv pip install --system --compile-bytecode --only-binary=:all: --no-binary=python-louvain -r requirements.txt

        COPY ./emneord.py .

        # Warm up caches
        RUN python -c 'import streamlit, dhlab, pandas, requests'
        RUN timeout 5s streamlit hello; exit 0

        CMD streamlit run emneord.py \
            --server.port ${PORT} \
            --browser.gatherUsageStats=False \
            --server.baseUrlPath /emneord

