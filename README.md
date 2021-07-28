# Heroku to Discord webhook middleware

Webhooks are a very powerful tool that allows you to send notifications from events in a service (for server webhooks) or receive notifications from events in a service (for client webhooks). For example:  
Discord is a client webhook, meaning you can send messages to a channel without even needing a bot. ([Discord-webhooks](https://discordapp.com/developers/docs/resources/webhook))  
Github and Heroku are webhook servers, meaning they will send notifications of certain events. ([Github-webhooks](https://developer.github.com/webhooks/)) ([Heroku-webhooks](https://devcenter.heroku.com/categories/app-webhooks))  

This also means you can 'connect' a webhook server with a webhook client to send notifications, however the data sent by the server can be (and in almost all cases is) different, meaning if you directly connect both it will probably not work. For this you need a middleware, a server that converts the server message into the client format.  
Discord has [built-in middlewares for Github](https://support.discordapp.com/hc/es/articles/228383668-Usando-Webhooks) and a few others, so you don't need any special treatment to connect Github and discord; however for other services, in this case Heroku, this middleware isn't available (or I couldn't find one) so I created my own. This app is just a middle server that converts Heroku webhook events into Discord webhook events, to be notified of Heroku changes directly from Discord. The app is also hosted on Heroku if you want to test it directly.

## Usage:
* Create a discord webhook (from a channel: edit channel->Webhooks->create). You should get a url with this format: `https://discordapp.com/api/webhooks/<id>/<key>` 
* Now go to Heroku and add the following webhook, changing the two last paths to the ones in your previously created webhook: `https://webhook-discord.herokuapp.com/<id>/<key>`.

For example, if your Discord webhook was  
`https://discordapp.com/api/webhooks/123456789012345678/qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfgh`  
you should write  
`https://webhook-discord.herokuapp.com/123456789012345678/qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfgh`  
This will use my deployed server as a middleware (details in 'Sample server'). If you want to deploy your own server check 'Deploy custom server'.

New: If you access the url from your browser, a button will be displayed to send a 'test' message and check if the url is valid. Please note that once configured you don't need to access the browser for anything, Heroku is the one sending the messages.

## Sample server
This app is hosted on Heroku, meaning you can follow the steps in 'Usage' to test directly. However note that the app is hosted on a free account, so it may take a few seconds to wake up, and also it may be abused in which case I will turn it off. Also note that although the app doesn't save/record any data (and I promise I will never do it), Heroku might save and keep a log of the petitions, so better not use it for sensible data. The sample server is: `https://webhook-discord.herokuapp.com/`

## Deploy custom server
If you want to deploy your own copy for personal use, just:
1) Fork the project (or copy/paste it, but forking is nicer and it will automatically comply with the license, otherwise you need to mention me).
1) Deploy your fork to Heroku or any other web service. The app is ready-to-deploy on Heroku, but it is just a Flask one-file app so other services should be fine.
1) Use your own url for the webhooks. In the second step of 'Usage' simply use your deployment url instead of mine.

## Contributions
Although this project was made for personal use, if you want to send pull requests or make/suggest changes I'll be happy to discuss them. The conversion was manually made so it may not have all type of events into consideration.

## Disclaimer
This app is not affiliated with nor endorsed by [Heroku](https://www.heroku.com/home) nor [Discord](https://discordapp.com/). The names, logos and services belongs to their respective owners.
