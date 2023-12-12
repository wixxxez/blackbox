FROM ubuntu

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.5 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r req.txt  
 
CMD ["python3", "main.py"]

EXPOSE 8000