import { Injectable } from '@angular/core';
import * as Bolt from '@modules/slack/bolt.interface';
import * as Events from './index'
@Injectable({
  	providedIn: 'root'
})
export class EventService {
	public events: Bolt.Event[] = [];
	constructor(
		public appMention: Events.AppMention,
	) {
		for (let arg of arguments) this.events.push(<Bolt.Event>arg);
	}
	public listen(event:Bolt.Event) {
		let bolt:any = this;
		bolt.app.event(event.name, event.callback.bind(bolt));
	}
}