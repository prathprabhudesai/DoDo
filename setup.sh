touch /tmp/.todo.json
echo '[]' > /tmp/.todo.json
cp todo.py ~/
echo "alias todo='sudo python todo.py'" >> ~/.bashrc
source ~/.bashrc
