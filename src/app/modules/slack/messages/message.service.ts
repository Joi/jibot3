import { Inject, Injectable } from '@angular/core';
import * as Messages from './index';

@Injectable({
  	providedIn: 'root'
})
export class MessageService {
	constructor(
	) {	}
	public listen(message) {
		if (this.constructor.name.toLowerCase() === 'boltservice') {
			let bolt:any = this;
			bolt.app.value.message(message.regex, message.callback.bind(bolt));
		} else {
			console.error(`Did you initialize your message listener function wrong? (${this.constructor.name})`);
		}
	}
}