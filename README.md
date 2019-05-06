# trump_tweet_generator

This project uses the Twitter API to stream tweets of US President Donald Trump, through oauth2 authentication. A Python script is run to authenticate and stream tweets from Jan 1, 2016 through Jan 1, 2019 in batches of 100 tweets. These tweets are then compiled into a text document.

A second Python script is then used to read this compilation of tweets where the data is cleaned before being processed into a Markov Chain. The Markov Chain is built by tokenizing each tweet and determining the probabilities of each subsequent word appearing in the generated text, until the algorithm hits a 'stop' word. The Markov Chain is then exported in a JSON file and is read by a JavaScript file to display results in the browser.

The current Markov Chain is built by a collection of 1136 tweets.
