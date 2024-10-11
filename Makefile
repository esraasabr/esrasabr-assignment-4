# Install project dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run the Flask web application
run:
	@echo "Starting the Flask app..."
	flask run --host=0.0.0.0 --port=3000
