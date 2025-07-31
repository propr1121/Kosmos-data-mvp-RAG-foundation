setup:
	@echo "🔧 Installing Python deps..."
	pip install -r requirements.txt

ollama-install:
	@echo "📦 Installing Ollama (macOS)..."
	brew install ollama || true

ollama-serve:
	@echo "🚀 Starting Ollama server..."
	ollama serve

ollama-pull-mistral:
	@echo "⬇️  Downloading Mistral model..."
	ollama pull mistral

start-etl:
	@echo "🏁 Running ETL..."
	python main.py
