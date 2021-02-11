import { Injectable } from '@angular/core';
import { BoltMessage } from '@app/interfaces/bolt-message';
import * as  Messages from './';
@Injectable({
  	providedIn: 'root'
})
export class MessageService {
	public messages: BoltMessage[] = [];
	constructor(
		public bot: Messages.Bot
	) {
		for (let message of arguments) this.messages.push(<BoltMessage>message);
	}
	public listen(message:BoltMessage) {
		let bolt:any = this;
		bolt.app.message(message.regex, message.callback.bind(this));

	}
}
