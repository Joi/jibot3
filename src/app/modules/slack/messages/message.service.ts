import { Injectable } from '@angular/core';
import * as Messages from './index'
import * as Bolt from '../bolt/bolt.interface';
@Injectable({
  	providedIn: 'root'
})
export class MessageService {
	constructor(
		public rot13: Messages.Rot13
	) {
		for (let arg of arguments) this.events.push(<Bolt.Message>arg);
	}
	public events  = [];
	public listen(message) {
		let bolt:any = this;
		bolt.app.message(message.regex, message.callback.bind(this));
	}
}