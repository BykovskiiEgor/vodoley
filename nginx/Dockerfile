# nginx/Dockerfile
FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY vodoley-belebey.ru/fullchain.pem /etc/letsencrypt/live/vodoley-belebey.ru/fullchain.pem
COPY vodoley-belebey.ru/privkey.pem /etc/letsencrypt/live/vodoley-belebey.ru/privkey.pem

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
