.PHONY: help airflow-up airflow-down kafka-test logs

help:
	@echo "AI Market Intelligence Hub - Commands"
	@echo "====================================="
	@echo "make airflow-up      - Start Airflow + Kafka"
	@echo "make airflow-down    - Stop all services"
	@echo "make kafka-test      - Test Kafka integration"
	@echo "make logs            - View Airflow logs"
	@echo "make kafka-topics    - List Kafka topics"
	@echo "make trigger-dag     - Trigger main pipeline"

airflow-up:
	cd orchestration && docker-compose up -d
	@echo "✅ Services started!"
	@echo "Airflow UI: http://localhost:8080 (admin/admin)"
	@echo "Kafka UI: http://localhost:8090"

airflow-down:
	cd orchestration && docker-compose down

kafka-test:
	python3 tests/test_kafka.py

logs:
	cd orchestration && docker-compose logs -f airflow-scheduler

kafka-topics:
	docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

trigger-dag:
	docker exec -it orchestration-airflow-scheduler-1 airflow dags trigger market_intelligence_pipeline
