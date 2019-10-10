FROM node:10-alpine as front
WORKDIR /app
COPY frontend .
RUN npm install
RUN npm run build

FROM python:3.7-alpine
WORKDIR /app
COPY backend .
COPY --from=front /app/dist /vue
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
