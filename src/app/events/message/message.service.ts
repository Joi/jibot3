import { Injectable } from '@angular/core';
import { BoltMessage } from '@app/interfaces/bolt-message';
import * as  Messages from './';
@Injectable({
  	providedIn: 'root'
})
export class MessageService {
	public messages: BoltMessage[] = [];
	constructor() {
		Object.keys(Messages).forEach(i => this.messages.push(<BoltMessage>Messages[i]))
	}
	public listen(message:BoltMessage) {
		let bolt:any = this;
	}
}
