FROM apache/spark-py
USER root
RUN pip install --no-cache-dir --break-system-packages numpy pandas scipy
USER 1001