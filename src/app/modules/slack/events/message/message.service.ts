import { Injectable } from '@angular/core';
import { BoltMessage } from '@app/interfaces/bolt-message';
import * as  Messages from './';
@Injectable({
  	providedIn: 'root'
})
export class MessageService {
	public events: BoltMessage[] = [];
	constructor(
		public rot13: Messages.Rot13
	) {
		for (let arg of arguments) this.events.push(<BoltMessage>arg);
	}
	public listen(message:BoltMessage) {
		let bolt:any = this;
		bolt.app.message(message.regex, message.callback.bind(this));
	}
}
