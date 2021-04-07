import { Injectable} from '@angular/core';
import * as Bolt from '../../bolt/bolt.interface';
@Injectable()
export class AppMention implements Bolt.Event {
	public name: string = "app_mention";
	public async callback ({event, say}) {
		return await say(`Hello <@${event.user}>. I am ready to learn.`);
	}
}
