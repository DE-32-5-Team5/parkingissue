FROM nginx:latest

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY page /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
