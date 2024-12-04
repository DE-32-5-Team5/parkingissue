FROM nginx:latest

RUN apt-get update && \
    apt-get install -y iputils-ping

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY page/test.html /usr/share/nginx/html
COPY page/clear.html /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
