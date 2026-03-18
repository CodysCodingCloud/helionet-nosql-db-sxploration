# Helionet nosql dbs and usage example

## Running the Docker Containers

The current version makes use of a local neo4j and redis db. to install and run it complete the following

1. Install docker desktop
2. download and run the dbs
    - `bash rundb.sh 0`
3. Shut down the dbs when you are done working with the dbs
    - `bash rundb.sh 666`
4. subsequent runs of the db can use the following unless there are update to the dbs
    - `bash rundb.sh 1`

## Redis Installation

sudo apt-get install lsb-release curl gpg
curl -fsSL <https://packages.redis.io/gpg> | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] <https://packages.redis.io/deb> $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis

docker run -d --name redis -p 6379:6379 redis:<version>

<!-- Installin ttkbootstrap for UI -->
python -m pip install ttkbootstrap