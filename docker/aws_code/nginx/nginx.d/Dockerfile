FROM nginx:latest

# Nginx 설정 파일 복사
COPY conf.d/nginx.conf /etc/nginx/nginx.conf

# Nginx 로그 디렉토리 생성 및 권한 설정
RUN mkdir -p /var/log/nginx && \
    chown -R www-data:www-data /var/log/nginx && \
    mkdir -p /var/www/html 


EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]

