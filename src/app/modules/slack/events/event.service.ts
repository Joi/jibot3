import { Injectable } from '@angular/core';
import * as Bolt from '../bolt/bolt.interface';
@Injectable({
  	providedIn: 'root'
})
export class EventService {
	public listen(event:Bolt.Event) {
		if (this.constructor.name.toLowerCase() === 'boltservice') {
			let bolt:any = this;
			bolt.app.value.event(event.name, event.callback.bind(bolt));
		} else {
			console.error(`Did you initialize your event listener function wrong? (${this.constructor.name})`);
		}
	}
}