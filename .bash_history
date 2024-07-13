source venv/bin/activate
./ngrok http 5000
ls -l
rm ngrok
ls -l
ngrok --version
sudo apt uninstall ngrok
sudo rm /usr/local/bin/ngrok
ngrok --version
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
./ngrok http 5000
ls -l
ngrok config add-authtoken 2j9EeYHB81eDyAxHFANqErbWEEc_7dSwiMz279cMWwHd9nnwf
ngrok http 5000
