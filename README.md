# Helionet nosql dbs and usage example

## Required Environment
- for convenience the following is a sample of an .env file that you may use for a local installation of the project:
```env
    NEO_URI="bolt://localhost:7687"
    NEO_USERNAME="neo4j"
    NEO_PASSWORD="your_password"
    REDIS_PORT=6379
    REDIS_HOST="localhost"
    REDIS_PASSWORD="yourpassword"
    DB_USAGE_TYPE=1
    DEBUG=1
```
- DEBUG
    - 1 : more print statements
    - 0 : minimizes print statements
- DB_USAGE_TYPE
    - 1 : uses neo4j implementation only
    - 2 : uses redis implementation only
    - 3 : uses both databases together for what each are best for


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


## Issues with tkinter
- if you get a module not found error for `_tkinter`, follow the following steps
- mac instructions
    1. brew install tcl-tk@8 pkgconf
    2. pyenv uninstall 3.13.2
    3. env \
        PATH="$(brew --prefix tcl-tk@8)/bin:$PATH" \
        LDFLAGS="-L$(brew --prefix tcl-tk@8)/lib" \
        CPPFLAGS="-I$(brew --prefix tcl-tk@8)/include" \
        PKG_CONFIG_PATH="$(brew --prefix tcl-tk@8)/lib/pkgconfig" \
        PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk@8)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk@8)/lib -ltcl8.6 -ltk8.6'" \
        pyenv install 3.13.2
    4. pyenv global 3.13.2
    5. recreate your .venv