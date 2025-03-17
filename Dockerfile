FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /emneord.py
        COPY requirements.txt ./requirements.txt
        RUN uv pip install --system -r requirements.txt
        COPY . .
        CMD streamlit run emneord.py --server.port ${PORT} --server.baseUrlPath /emneord-test-fast

