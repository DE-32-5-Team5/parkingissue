FROM nginx:latest

COPY conf.d/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/log/nginx && \
    chown -R www-data:www-data /var/log/nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
