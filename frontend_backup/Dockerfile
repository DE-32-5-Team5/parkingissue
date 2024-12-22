FROM httpd:2.4

# docker build --build-arg REPO_URL=.....
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./page /usr/local/apache2/blog/

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

# /usr/local/apache2/blog
