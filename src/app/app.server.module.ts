import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { App, LogLevel  } from '@slack/bolt';
import { environment } from '@env/environment';
import { AppModule } from '@app/app.module';
import { AppComponent } from '@app/app.component';
import { LoggerService } from '@app/services/logger.service';

@NgModule({
	bootstrap: [AppComponent],
	declarations: [],
	imports: [
		AppModule,
		ServerModule,
	],
	providers:	[]
})
export class AppServerModule {
	constructor(private loggerService: LoggerService) {
		this.loggerService.log(`${this.constructor.name} starting...`);
		this.create().catch(this.handleError.bind(this));
	}
	private handleError = (error) => this.loggerService.error(error);
	private rot13 = (str) => str.split('').map(char => String.fromCharCode(char.charCodeAt(0) + (char.toLowerCase() < 'n' ? 13 : -13))).join('');
	private getById = (id, collection) => collection.find(o => o.id === id);
	private interestingThings: string[] = ['users', 'conversations'];

	private app = new App({
		socketMode:		true,
		convoStore:		false,
		logLevel:		LogLevel.ERROR,
		clientId:		environment.SLACK_CLIENT_ID,
		clientSecret:	environment.SLACK_CLIENT_SECRET,
		token:			environment.SLACK_BOT_TOKEN,
		appToken:		environment.SLACK_APP_TOKEN,
		signingSecret:	environment.SLACK_SIGNING_SECRET,
	});
	private clientConfig: any = {
		token: environment.SLACK_BOT_TOKEN
	}
	public users:any[] = null;
	public conversations:any[] = null;

	private async create() {
		return await this.app.start({}).then(this.wakeup.bind(this));
	}
	private async wakeup(status) {
		if (status.ok) {
			this.loggerService.log(`Wakup complete...`)
			this.lookAround().then(this.listenToThings.bind(this));
		} else {
			this.loggerService.error(status);
		}
	}
	private async lookAround() {
		return this.interestingThings.forEach(async thing => await this.lookAt(thing).then(result => this.remember(thing, result)));
	}
	private async lookAt(something:string) {
		if (this.app.client[something]?.list) {
			return await this.app.client[something].list(this.clientConfig);
		}
	}
	private remember(something:string, data:any) {
		let collectionName:string = something;
		if (something == 'users') collectionName = 'members';
		this[something] = data[collectionName];
	}
	private listenToThings() {
		this.app.message(/(bot).*/, this.speakNonsense.bind(this));
		this.app.event('app_mention', this.introduceMyself.bind(this));
	}
	private async speakNonsense({ event, say }) {
		return await say(this.rot13(event.text));
	}
	private async introduceMyself({ event, say }) {
		if (this.users) {
			let user = this.getById(event.user, this.users);
			let userName = (user.real_name) ? user.real_name : user.name;
			return await say(`Hello ${userName}. I am ready to learn.`);
		} else {
			return await say(`Hello ${event.user}. I am ready to learn.`);
		}
	}
}