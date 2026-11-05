# Этап 1: Сборка
FROM golang:1.26-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# Компилируем бинарник с именем core-app
RUN go build -o core-app .

# Этап 2: Финальный образ
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/core-app .

# Запускаем скомпилированное ядро
CMD ["./core-app"]