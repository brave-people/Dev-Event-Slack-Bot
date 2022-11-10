const express = require('express');
const mongoose = require('mongoose'); // for mongoDB
const router = express.Router();
const { WebClient } = require('@slack/web-api');
const client = new WebClient();

// env value
const env = require('dotenv').config(); //add .env file 
const domainName = "dev-event-slack-bot.kro.kr"

// db connect
mongoose
    .connect(process.env.MONGO_URL, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        dbName: "userInfo" // 이 이름으로 db가 생성됩니다.
    })
    .then(() => console.log(`mongoDB connected`))
    .catch((err) => console.error(err));


router.get('/auth/slack', async (_, res) => {
    const botScopes = 'calls:write,chat:write,channels:read,groups:read,mpim:read,im:read';
    const userScopes = '';
    const clientId = process.env.SLACK_CLIENT_ID;
    const oauthUrl = `https://slack.com/oauth/v2/authorize?client_id=${clientId}&scope=${botScopes}&user_scope=${userScopes}`;
    return res.render('index', { oauthUrl });
});


router.get('/auth/slack/callback', async (req, res) => {
    try {
        const response = await client.oauth.v2.access({
            client_id: process.env.SLACK_CLIENT_ID,
            client_secret: process.env.SLACK_CLIENT_SECRET,
            code: req.query.code,
        });

        const identity = await client.users.identity({
            token: response.authed_user.access_token
        });

        // At this point you can assume the user has logged in successfully with their account.
        return res.status(200).send(`<html><body><p>You have successfully logged in with your slack account! Here are the details:</p><p>Response: ${JSON.stringify(response)}</p><p>Identity: ${JSON.stringify(identity)}</p></body></html>`);
    } catch (eek) {
        console.log(eek);
        return res.status(500).send(`<html><body><p>Something went wrong!</p><p>${JSON.stringify(eek)}</p>`);
    }
});

module.exports = router;
