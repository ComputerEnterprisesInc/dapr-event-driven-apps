dapr run -d ./components --app-id detection --app-port 5001 -- python detection/app.py &
dapr run -d ./components --app-id recognition --app-port 5002 -- python recognition/app.py &
dapr run -d ./components --app-id http-api --app-port 5000 -- python http-api/app.py
