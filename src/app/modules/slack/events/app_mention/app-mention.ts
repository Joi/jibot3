import { Injectable} from '@angular/core';
import * as Bolt from '../../bolt/bolt.interface';
@Injectable()
export class AppMention implements Bolt.Event {
	public name: string = "app_mention";
	public async callback ({event, say}) {
		if (this.constructor.name.toLowerCase() === 'boltservice') {
			let bolt:any = this;
		} else {
			console.error(`Did you initialize your app thing  wrong? (${this.constructor.name})`);
		}
		//let member = bolt.getById(event.user, bolt.memberService.members);
		//let memberName = (member.real_name) ? member.real_name : member.name;
		//return await say(`Hello ${memberName}. I am ready to learn.`);
		return await say(`Hello! I am ready to learn.`);
	}
}
