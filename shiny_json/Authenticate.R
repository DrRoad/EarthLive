library(twitteR)
4377815library(ROAuth)
library(plyr)
library(dplyr)
library(stringr)
library(ggplot2)
#connect to API
download.file(url='http://curl.haxx.se/ca/cacert.pem', destfile='cacert.pem')
reqURL <- 'https://api.twitter.com/oauth/request_token'
accessURL <- 'https://api.twitter.com/oauth/access_token'
authURL <- 'https://api.twitter.com/oauth/authorize'
consumerKey <- 'yiHz2vJPQmHRIZ3WcAZcbhloY' #put the Consumer Key from Twitter Application
consumerSecret <- 'N1kGE6Y46z1KETOpUdMD1wqWQLGI35smz4f48k0wa4C4h9kUYv'  #put the Consumer Secret from Twitter Application
Cred <- OAuthFactory$new(consumerKey=consumerKey,
                         consumerSecret=consumerSecret,
                         requestURL=reqURL,
                         accessURL=accessURL,
                         authURL=authURL)
Cred$handshake(cainfo = system.file('CurlSSL', 'cacert.pem', package = 'RCurl'))