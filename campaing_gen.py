import pyrebase,os,json,random
from google.cloud import pubsub_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_key.json"

firebaseConfig = {
  "apiKey": "AIzaSyBnz6wws3EjTRnFOG7NvefKSr9CsaOlcxY",
  "authDomain": "flick-it-users-storage.firebaseapp.com",
  "databaseURL": "https://flick-it-users-storage-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "flick-it-users-storage",
  "storageBucket": "flick-it-users-storage.appspot.com",
  "messagingSenderId": "1046722019798",
  "appId": "1:1046722019798:web:905b021820e1922f95a477",
  "measurementId": "G-J3T9K8WPV2",
  "serviceAccount": "serviceAccountCredentials.json"
}
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

file = open("word.json")
data = json.load(file)
file.close()

subscriber = pubsub_v1.SubscriberClient()

def callback(message: pubsub_v1.subscriber.message.Message):
    message.ack()
    print("Receive")
    rd = random.randint(0,len(data["data"]))
    newWord = data["data"][rd]["word"]
    point = data["data"][rd]["point"]
    db.child("word").update({"point":point,"word":newWord})
    return 0

streaming_pull_future = subscriber.subscribe("projects/third-essence-365119/subscriptions/launch-campaign-sub", callback=callback)
print(f"Listening for messages on projects/third-essence-365119/subscriptions/launch-campaign-sub..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.


