import { Injectable } from '@angular/core';
import { BoltEvent } from '@app/interfaces/bolt-event';
import * as Events  from './';
@Injectable({
  	providedIn: 'root'
})
export class EventService {
	public events: BoltEvent[] = [];
	constructor(
		public appMention: Events.AppMention,
	) {
		for (let arg of arguments) this.events.push(<BoltEvent>arg);
	}
	public listen(event:BoltEvent) {
		let bolt:any = this;
		bolt.app.event(event.name, event.callback.bind(bolt));
	}
}