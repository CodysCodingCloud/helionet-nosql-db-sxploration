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