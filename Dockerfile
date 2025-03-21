FROM python:3.12-slim-bookworm
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /emneord.py

        COPY requirements.txt ./requirements.txt
        RUN pip install -r requirements.txt

        COPY ./emneord.py .

        # Warm up caches
        RUN python -c 'import streamlit, dhlab, pandas, requests'
        RUN timeout 5s streamlit run emneord.py; exit 0

        CMD streamlit run emneord.py --server.port ${PORT} --server.baseUrlPath /emneord-test-fast-pip

