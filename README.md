# Telegram Bot with MongoDB Aggregation

This project is a Telegram bot that aggregates salary data from MongoDB based on user input.

## Prerequisites

Before you start, make sure you have Docker and Poetry installed on your machine.

## Setup and Installation

1. **Clone the Repository**
   Create an Environment Configuration File

2. Create a file named .env in the root directory of the project with the following content 

(see .env.example):


      TELEGRAM_TOKEN=your_telegram_bot_token



      MONGO_URI=mongodb://localhost:27017


3. Ensure Configuration Files Exist
   Make sure that metadata.json and collection.bson files are present in the data directory.


4. Run MongoDB on Docker. 

Use the following command to start MongoDB in a Docker container:


      docker run --name mongodb -d -p 27017:27017 mongo




5. Install Dependencies

Use Poetry to install project dependencies:

      poetry install

Use Poetry to run the bot:


      poetry run python ./src/__main__.py or 
or

      poetry run python3.X ./src/__main__.py

where X the version of Python
