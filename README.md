# United Tickets Monitoring

This is a collection of Python scripts that will notify you via email if a Manchester United ticket is being sold on Reddit.

It simply polls Reddit API on a periodic basis, for several subreddits and keywords. 
The collected submissions are saved into the database and sent via email.

Currently, it is not a web service, but only a script. You are free to host this yourself on a server. 
(Don't forget to change the environment variables.) However, it is unlikely that this will be run as a web service. 
From a personal point of view, it will be disadvantageous to me if many people are using the service and being notified 
about tickets sale, thus minimise the chance of me to get the tickets myself.

## Future improvements
- Integrate Twitter
- Extract price from text, and whether it is face value or not (NLP models can be used, but might be over the top)
- Make this as a web service (unlikely, see above)

## Requirements
- MongoDB 4.0.0+
- Python 3.5+


