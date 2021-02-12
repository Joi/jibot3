import { Injectable} from '@angular/core';
import { Server } from 'http';
import { App, AppOptions, LogLevel } from '@slack/bolt';
import { environment } from '@env/environment';

import { ApiService } from '@services/api.service';
import { LoggerService } from '@services/logger.service';
import { MemberService } from '@app/components/members/member.service';
import { ConversationService } from '@app/components/conversations/conversation.service';
import { EventService } from '@app/events/event.service';
import { MessageService } from '@app/events/message/message.service';
@Injectable({
	providedIn: 'root'
})
export class BoltService {
	public collections:object = {};
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
	private services: any[] = [this.memberService, this.conversationService];
	constructor(
		private logger: LoggerService,
		private memberService: MemberService,
		private conversationService: ConversationService,
		private eventService: EventService,
		private messageService: MessageService,
		private apiService: ApiService,
	) {
	}
	public async init() {
		this.logger.log('Initializing Bolt...');
		return await this.connectToSlack()
			.then(this.startAppServer)
			.then(this.startServices.bind(this))
			.finally(() => {
				this.initEvents();
				this.initMessages();
				this.logger.log('Bolt initialized...');
				this.apiService
						.getApi("https://data.montgomerycountymd.gov/resource/98cc-bc7d.json")
						.subscribe(response => console.log(response));
			})
			.catch(err => console.warn(err));
	}
	private connectToSlack = async ():Promise<App> => await (!this.app) ? this.app = this.app = new App(this.boltOptions) : this.app;
	private startAppServer = async (app):Promise<Server> => await app.start({});
	private startServices = async ():Promise<any> => {
		return await Promise.all(this.services.map(async (service) => {
			let localName = service.collectionNames.collection;
			let response = await this.get(service.collectionNames.request);
			if (response.ok) this.collections[localName] = service[localName] = response[service.collectionNames.response];
			return service;
		}));
	}
	private get = async (objectName):Promise<any> => await this.app.client[objectName].list(this.clientConfig);
	private initMessages = ():void => this.messageService.messages.forEach(this.messageService.listen.bind(this));
	private initEvents = ():void => this.eventService.events.forEach(this.eventService.listen.bind(this));
	private getById = (id, collection):any => { return collection.find(i => i.id === id)};
}