import { Injectable } from '@angular/core';
import { App, AppOptions, LogLevel } from '@slack/bolt';
import { Server } from 'http';

import { LoggerService } from '@services/logger.service';
import { EventService } from '../events/event.service';
import { MessageService } from '../messages/message.service';
import { MemberService } from '../members/member.service';

@Injectable({
	providedIn: 'root'
})
export class BoltService {
	constructor(
		private logger: LoggerService,
		private memberService: MemberService,
		private eventService: EventService,
		private messageService: MessageService,
	) { }

	public app:App;
	private appOptions: AppOptions = {
		logLevel:		LogLevel.ERROR,
		socketMode:		true,
		convoStore:		false,
	}
	private clientOptions = { token: null };
	private listenerServices = [
		this.eventService,
		this.messageService
	]
	public objects:Object = {};
	public init = async (options?:AppOptions) => {
		this.setOptions(options)
			.then(this.create.bind(this))
			.then(this.start.bind(this))
			.then(this.setupClientToken.bind(this))
			.then(() => {
				this.getMembers().then(this.setMembers.bind(this));
			})
			.then(this.startEventListeners.bind(this))
			.then(this.logger.init_done.bind(this))
			.catch(this.logger.error)
	}
	private setOptions  = async (options:AppOptions):Promise<AppOptions> => await {...this.appOptions, ...options};
	private create = async (options:AppOptions):Promise<App> => this.app = new App(options);
	private start = async (app:App):Promise<Server> => await app.start({});
	private setupClientToken = () => this.clientOptions.token = this.appOptions.token || null;

	private getMembers = async () => await this.app.client[this.memberService.collectionNames.request].list(this.clientOptions);
	private setMembers = (response) => this[this.memberService.collectionNames.local] = (response.ok) ? response[this.memberService.collectionNames.response] : null;
	private startEventListeners = ():void => this.listenerServices.forEach(service => service.events.forEach(service.listen.bind(this)));

	public getById(id:string, coll:any[]|string):any {
		let collection = (typeof coll === 'string') ? this.objects[coll] : coll;
		return collection.find(i => i.id === id);
	}
}