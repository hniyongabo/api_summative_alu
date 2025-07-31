FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Python3, pip, and venv
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv curl openssh-server sudo iputils-ping ca-certificates nginx && \
    mkdir /run/sshd && \
    if ! id -u ubuntu >/dev/null 2>&1; then \
        useradd --create-home --uid 1000 --shell /bin/bash ubuntu; \
    fi && \
    echo 'ubuntu:pass123' | chpasswd && \
    usermod -aG sudo ubuntu && \
    sed -ri 's/#?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -ri 's/#?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN chown -R ubuntu:ubuntu /app

# Set up Python virtual environment and install requirements
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# Nginx config
RUN echo 'server {\n\
    listen 80;\n\
    location / {\n\
        proxy_pass http://localhost:5002;\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
    }\n\
}' > /etc/nginx/sites-available/default

EXPOSE 5002 22 80

RUN ssh-keygen -A

# Startup script: start nginx, Flask app, and SSH
RUN echo '#!/bin/bash\n\
echo " Starting nginx..."\n\
service nginx start\n\
echo " Starting Flask application..."\n\
source /app/venv/bin/activate\n\
python3 /app/api.py &\n\
echo " Starting SSH daemon..."\n\
/usr/sbin/sshd -D' > /startup.sh && \
    chmod +x /startup.sh

CMD ["/startup.sh"]
