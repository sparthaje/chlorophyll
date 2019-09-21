FROM node:lts

EXPOSE 5000

RUN mkdir /app
WORKDIR /app
COPY . .

RUN yarn
RUN yarn global add serve
RUN yarn build

CMD ["serve", "-s", "dist"]
