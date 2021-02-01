require('dotenv').config();
const { WebClient, LogLevel } = require('@slack/web-api');
const { App } = require('@slack/bolt');

const appToken      = process.env.SLACK_APP_TOKEN;
const botToken      = process.env.SLACK_BOT_TOKEN;
const signingSecret = process.env.SLACK_SIGNING_SECRET;
const webClient     = new WebClient(process.env.SLACK_BOT_TOKEN, { LogLevel: LogLevel.DEBUG });
const app = new App({
  token:            botToken, 
  appToken:         appToken,
  signingSecret:    signingSecret,
  socketMode:       true,
  LogLevel:         LogLevel.DEBUG,
});

let users, channels;

const initializeApp = (async () => await app.start(process.env.PORT || 3000).then(initializeBot))();
async function initializeBot(started) {
  if (started.ok) {
    await webClient.users.list({ token: botToken }).then(saveMembers);
    await webClient.conversations.list({ token: botToken }).then(saveChannels);
    app.message(/(bot).*/, ingestMessage);
    app.event('app_mention', introduceMyself);
  }
}

const rot13 = (str) => str.split('').map(char => String.fromCharCode(char.charCodeAt(0) + (char.toLowerCase() < 'n' ? 13 : -13))).join('');
const saveMembers = (result) => users = (result.ok) ? result.members : null;
const saveChannels = (result) => channels = (result.ok) ? result.channels : null;
const getById = (id, collection) => collection.find(o => o.id === id);
const ingestMessage = async ({ event, say }) => await say(rot13(event.text));

async function introduceMyself({ event, say })  {
  let message = event.text;
  let user = getById(event.user, users);
  if (user) {
   let userName = (user.real_name) ? user.real_name : user.name;
   await say(`Hello ${userName}. I am ready to learn.`);
 }
}