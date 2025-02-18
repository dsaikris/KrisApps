# KrisApps

> Some apps built using Streamlit. 
> Visit https://krisapps.streamlit.app/ or https://krisapps-386486290258.us-west4.run.app to try out the apps.

> For developers: Here are the instructions to locally run Stremlint

## Run locally
```
python3 -m venv ./venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run Home.py --server.port 8080
```

## Run in docker
```
docker build -t krisapps .
docker run -p 8080:8080 krisapps
```


> These are my personal pages. Please contact me for any questions or suggestions. Thank you.
