const express = require('express');
const mongoose = require('mongoose'); // for mongoDB
const router = express.Router();

// env value
const env = require('dotenv').config(); //add .env file 
const domainName = "dev-event-slack-bot.kro.kr"
const slackClientId = process.env.SLACK_CLIENT_ID

// db connect
mongoose
    .connect(process.env.MONGO_URL, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        dbName: "userInfo" // 이 이름으로 db가 생성됩니다.
    })
    .then(() => console.log(`mongoDB connected`))
    .catch((err) => console.error(err));


/**
 * On this page you display the Add to SLACK button.The user can click it to login with Slack.
 */
router.get('/auth/slack', async (_, res) => {
    const scopes = 'identity.basic,identity.email';
    const redirectUrl = `https://${domainName}/auth/slack/callback`;

    //Here you build the url. You could also copy and paste it from the Manage Distribution page of your app.
    // https://slack.com/oauth/v2/authorize?client_id=2844308222017.3909658800162&scope=calls:write,chat:write,channels:read,groups:read,mpim:read,im:read&user_scope=chat:write,im:read,identity.basic,calls:write,channels:read
    const oauthUrl = `https://slack.com/oauth/v2/authorize?client_id=${slackClientId}&user_scope=${scopes}&redirect_uri=${redirectUrl}`;
    return res.render('index', { oauthUrl });
});


/**
 * This is the callback page.
 */
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
