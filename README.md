# United Tickets Monitoring

This is a collection of Python scripts that will notify you via email if a Manchester United ticket is being sold on Reddit.

It simply polls Reddit API on a periodic basis, for several subreddits and keywords. 
The collected submissions are saved into the database and sent via email.

Currently, it is not a web service, but only a script. You are free to host this yourself on a server. 
However, it is unlikely that this will be run as a web service. 
From a personal point of view, it will be disadvantageous to me if many people are using the service and being notified 
about tickets sale, thus minimise the chance of me to get the tickets myself.

## Future improvements
- Integrate Twitter
- Extract team we are playing against
- Extract price from text, and whether it is face value or not (NLP models can be used, but might be overkill)
- Extract stand and/or seats from text
- Extract quantity of tickets
- Notify if the ticket is sold
- Add mechanism to automatically contact seller (or by clicking on email)
- Make this as a web service (unlikely, see above)

## Requirements
- MongoDB 4.0.0+
- Python 3.5+

## Installation
1. Clone this repo
  ```
  git clone https://github.com/albertus-andito/united-tickets-monitoring.git
  ```
2. Create a virtual environment under this repo
  ```
  python3 -m venv ./united-tickets-monitoring-venv
  ```
  You can also use the `python3.7` command, depending on the version.
3. Install the required Python packages:
  ```
  source ./united-tickets-monitoring-venv/bin/activate
  pip install -r ./requirements.txt
  deactivate
  ```
4. Set MongoDB as a replica set (required for watch operation)
  - Your `/etc/mongod.conf` must look like this:
    ```
    ...
    # network interfaces
    net:
      port: 27017
      bindIp: 127.0.0.1,mongo0.replset.member
    ...
    replication:
      replSetName: "rs0"
    ```
  - Go to mongo shell.
    ```
    sudo systemctl start mongo #(this is if you haven't started the service)
    mongo
    ```
  - Inside the mongo shell, initiate the replica set
    ```
    $(mongo) rs.initiate({_id: "rs0", members: [{_id: 0, host: "127.0.0.1"}]})
    ```
5. Create .env file based on .env.default and populate its values

## Run the script
``` 
./run.sh
```