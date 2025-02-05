FROM python:3.12
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /emneord.py
        COPY requirements.txt ./requirements.txt
        RUN pip3 install -r requirements.txt
        COPY . .
        CMD streamlit run emneord.py --server.port ${PORT} --server.baseUrlPath /emneord

