FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

# This ensures dist is preserved in the final image
CMD ["sh", "-c", "cp -r /app/dist /output"]
