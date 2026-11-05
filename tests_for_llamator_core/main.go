package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/google/uuid"
	"github.com/segmentio/kafka-go"
)

const (
	producerTopic = "core_attack_topic"
	consumerTopic = "attack_result_topic"
	brokerAddress = "kafka:9092"
)

type ConsumerMessage struct {
	AttackID string         `json:"attack_id"`
	Result   map[string]any `json:"result"`
	Error    *string        `json:"error"`
	TaskID   *string        `json:"task_id"`
}

type ProducerMessage struct {
	TargetURL       string         `json:"target_url"`
	TargetAuthToken string         `json:"target_auth_token"`
	TargetModel     string         `json:"target_model"`
	RequestId       string         `json:"request_id"`
	AttackID        string         `json:"attack_id"`
	ToolName        string         `json:"tool_name"`
	Attrs           map[string]any `json:"attrs"`
}

func main() {
	go func() {
		log.Println("Консьюмер запущен и слушает Kafka...")
		consumeMessages()
	}()

	http.HandleFunc("/trigger", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Метод не поддерживается. Используйте POST", http.StatusMethodNotAllowed)
			return
		}

		produceMessage()

		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Сообщение успешно отправлено в Kafka по вашему запросу!")
	})

	log.Println("Go Core Service запущен на порту 8081...")
	
	if err := http.ListenAndServe(":8081", nil); err != nil {
		log.Fatalf("Ошибка запуска HTTP сервера: %v", err)
	}
}

func produceMessage() {
	writer := &kafka.Writer{
		Addr:     kafka.TCP(brokerAddress),
		Topic:    producerTopic,
		Balancer: &kafka.LeastBytes{}}
	defer writer.Close()

	targetUrl := os.Getenv("DeepseekUrl")	
	token := os.Getenv("DeepseekKey")
	nameModel := os.Getenv("Deepseek")

	message := &ProducerMessage{
		TargetURL:       targetUrl,
		TargetAuthToken: token,
		TargetModel:     nameModel,
		RequestId:       uuid.New().String(),
		AttackID:        uuid.New().String(),
		ToolName:        "llamator",
		Attrs:           nil,
	}

	messageBytes, err := json.Marshal(message)

	if err != nil {
		log.Fatalf("Ошибка конвертации в JSON: %v", err)
	}

	kafkaMsg := kafka.Message{
		Value: messageBytes}

	err = writer.WriteMessages(context.Background(), kafkaMsg)

	if err != nil {
		log.Printf("Ошибка записи сообщения: %v", err)
	} else {
		log.Println("Сообщение успешно отправлено в Kafka!")
	}
}

func consumeMessages() {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers: []string{brokerAddress},
		Topic:   consumerTopic,
		GroupID: "red-ai-core-results-consumer",
		StartOffset: kafka.FirstOffset,
	})
	defer reader.Close()

	for {
		data, err := reader.ReadMessage(context.Background())
		if err != nil {
			log.Printf("Ошибка чтения из Kafka: %v\n", err)
			continue
		}

		log.Printf("--- Сырое сообщение Kafka ---\n%+v\n", data)

		msg := &ConsumerMessage{}

		err = json.Unmarshal(data.Value, &msg)
		if err != nil {
			log.Println(err)
			continue
		}

		log.Printf("--- Распакованный объект ---\n%+v\n", msg)
	}
}
