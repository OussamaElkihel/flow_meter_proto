
<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Install Docker and Docker Compose

* Update packages:
  ```sh
  sudo apt update && sudo apt upgrade -y
  ```

* Install Docker:
  ```sh
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER
  ```

  -->reboot raspberry pi

* Install Docker Compose plugin:
  ```sh
  sudo apt install -y docker-compose-plugin
  ocker compose version
  ```

* Create a project folder
  ```sh
  mkdir -p ~/mongo-setup
  cd ~/mongo-setup
  ```

* Create docker-compose.yml
  ```sh
  nano docker-compose.yml
  ```

* Yaml script
  ```yaml
  version: "3.8"
  services:
    mongo:
      image: mongo:4.4.18
      container_name: mongo
      restart: unless-stopped
      ports:
        - "27017:27017"
      environment:
        MONGO_INITDB_ROOT_USERNAME: admin
        MONGO_INITDB_ROOT_PASSWORD: examplepassword
      volumes:
        - mongo-data:/data/db

  volumes:
    mongo-data:
  ```

* Start MongoDB:
  ```sh
  docker compose up -d
  ```

* Connect to MongoDB after boot:
  ```sh
  docker exec -it mongo mongosh
  ```

<!-- USAGE EXAMPLES -->
## Usage

### Wiring between STM32 and nRF24L01

| nRF24L01 Pin | STM32 Pin  | 
|--------------|------------|
| VCC          | 3.3 V      | 
| GND          | GND        |
| CE           | PF13       | 
| CSN          | PF12       |
| SCK          | PA1        | 
| MOSI         | PA7        | 
| MISO         | PA6        | 
| IRQ          | Not Used ! | 

### Wiring between STM32 and YF-S401

| nRF24L01 Pin | STM32 Pin  | 
|--------------|------------|
| VCC          | 3.3 V      | 
| GND          | GND        |
| Signal       | PD12       | 

### Power the STM32

### Start python scripts

Start in this order:
1/receive_flow_vol.py
2/json_to_mongo.py

### Json files will be saved in "received_json" directory

* List json files:
  ```sh
  cd received_json
  ls
  ```