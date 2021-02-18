import { Injectable } from '@angular/core';
import { environment } from '@env/environment';
import { App, AppOptions, LogLevel } from '@slack/bolt';
import { LoggerService } from '@services/logger.service';
import { EventService } from './events/event.service';
import { MessageService } from './events/message/message.service';
import { MemberService } from '@app/components/members/member.service';
import { ConversationService } from '@app/components/conversations/conversation.service';

@Injectable({
  providedIn: 'root'
})
export class BoltService {
	public collections:Object = {};
	private boltOptions: AppOptions = {
		socketMode:		true,
		convoStore:		false,
		logLevel:		LogLevel.ERROR,
		clientId:		environment.SLACK_CLIENT_ID,
		clientSecret:	environment.SLACK_CLIENT_SECRET,
		token:			environment.SLACK_BOT_TOKEN,
		appToken:		environment.SLACK_APP_TOKEN,
		signingSecret:	environment.SLACK_SIGNING_SECRET,
	};
	private app: App;
	private clientConfig = {
		token: environment.SLACK_BOT_TOKEN
	};
	private objectServices: any[] = [
		this.memberService,
		this.conversationService
	];
	private listenerServices: any[] = [
		this.eventService,
		this.messageService
	];
  	constructor(
		private logger: LoggerService,
		private eventService: EventService,
		private messageService: MessageService,
		public memberService: MemberService,
		public conversationService: ConversationService,
	) {	}
	public init = () => this.initialize();
	private async initialize() {
		await this.connectToSlack()
			.then(this.startAppServer)
			.then(this.getSlackObjects.bind(this))
			.finally(this.startEventListeners.bind(this))
			.finally(this.boltIsInitizated.bind(this))
			.catch(this.logger.error);
		return this.app;
	}
	private connectToSlack = async ():Promise<App> => await (!this.app) ? this.app = this.app = new App(this.boltOptions) : this.app;
	private startAppServer = async (app):Promise<any> => await app.start({});
	private  async getSlackObjects():Promise<any> {
		return await Promise.all(this.objectServices.map(async (service) => {
			let localName = service.collectionNames.local;
			let response = await this.get(service.collectionNames.request);
			if (response.ok) this.collections[localName] = service[localName] = response[service.collectionNames.response];
		}));
	};
	private startEventListeners():void {
		this.listenerServices.forEach(service => service.events.forEach(service.listen.bind(this)));
		return;
	}
	private boltIsInitizated():void {
		this.logger.log(`${this.constructor.name} initialized...`);
		return;
	}
	private async get(objectName):Promise<any> {
		return await this.app.client[objectName].list(this.clientConfig);
	}
	public getById(id, collection):any {
		return collection.find(i => i.id === id);
	}
}
