# Telegram + Openai Chatbot to answer audio messages...

#### YouTube
I have recorded a quick video tutorial on this repository, you can watch it [here](https://youtu.be/v2Wjje8BT-Q).

#### Steps
* create a `.env` file in the root directory and copy the content from the `.env.example` file and provide all the values
* create GCP account, and get the service account credentials, then create a Cloud Storage Buckate, and **make it public**.
* in the `.env` file replace the `CREDENTIALS` with your service account file path
* replace the `GCP_CLOUD_STORAGE_BUCKET_NAME` with your bucket name

#### Virtual environment
* create a virtual environment using `python3 -m venv venv`
* activate the virtual environment using `source venv/bin/activate`, for Windows `.\venv\Scripts\activate`

#### install packages
* install all the packages using `pip install -r requirements.txt`

#### Run the code
* for server
`uvicorn run:app --host 0.0.0.0 --port 5000`
* for local
`uvicorn run:app --reload`
* test the application `curl -X GET "http://127.0.0.1:8000"`

#### Set the Telegram webhook
* call the endpoint `/set-telegram-webhook`, it will set the webhook `curl -X GET "https://c7dc-2405-201-2027-501a-3b82-e1d-bbce-79e4.ngrok-free.app/set-telegram-webhook"` make sure you change the NGROK URL

