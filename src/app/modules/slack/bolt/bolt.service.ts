import { Injectable } from '@angular/core';
import { App, AppOptions, LogLevel } from '@slack/bolt';
import { WebClient } from '@slack/web-api';

import { Server } from 'http';
import { LoggerService } from '@services/logger.service';
import { EventService } from '../events/event.service';
import { MessageService } from '../messages/message.service';
import { MemberService } from '../members/member.service';
import { BehaviorSubject } from 'rxjs';

import * as Messages from '@modules/slack/messages';
import * as Events from '@modules/slack/events';
import { FetcherService } from '@app/services/fetcher.service';
import { async } from '@angular/core/testing';

@Injectable({
	providedIn: 'root'
})
export class BoltService {
	constructor(
		private logger: LoggerService,
		private memberService: MemberService,
		public fetcher: FetcherService,
		public events: EventService,
		public messages: MessageService,
	) { }
	public app:BehaviorSubject<App> = new BehaviorSubject(null);
	public client: BehaviorSubject<WebClient> = new BehaviorSubject(null);

	private appOptions: AppOptions = {
		logLevel:		LogLevel.ERROR,
		socketMode:		true,
		convoStore:		false,
	}
	public clientOptions = { token: null };
	public objects:Object = {};
	public async init(options?:AppOptions) {
		this.setOptions(options)
			.then(this.create.bind(this))
			.then(this.start.bind(this))
			.then(this.setupClientToken.bind(this))
			.then(this.startClient.bind(this))
			.then(() => {
				this.getMembers().then(this.setMembers.bind(this));
			})
			.then(this.startEventListeners.bind(this))
			.then(this.logger.init_done.bind(this))
			.catch(this.logger.error)
	}
	private setOptions  = async (options:AppOptions):Promise<AppOptions> => this.appOptions = {...this.appOptions, ...options};
	private create = async (options:AppOptions):Promise<App> => {
		let app = new App(options);
		this.app.next(app);
		return app;
	}
	private start = async (app:App):Promise<Server> => await app.start({});
	private setupClientToken = async () => this.clientOptions.token = this.appOptions.token || null;
	private startClient = async(token:string) => this.client.next(new WebClient(token));
	private getMembers = async () => await this.client.value[this.memberService.collectionNames.request].list();
	private setMembers = (response) => this.objects[this.memberService.collectionNames.local] = (response.ok) ? response[this.memberService.collectionNames.response] : null;
	private startEventListeners = ():void => {
		let messages = [];
		let events = [];
		Object.values(Messages).forEach(msgClass => messages.push(new msgClass));
		Object.values(Events).forEach(eventClass => events.push(new eventClass));
		messages.forEach(this.messages.listen.bind(this));
		events.forEach(this.events.listen.bind(this));
	};

	public getById(id:string, coll:any[]|string):any {
		let collection = (typeof coll === 'string') ? this.objects[coll] : coll;
		return collection.find(i => i.id === id);
	}
}