import { Injectable} from '@angular/core';
import { BoltEvent } from '@app/interfaces/bolt-event';
@Injectable()
export class AppMention implements BoltEvent {
	constructor() { }
	public name: string = "app_mention";
	public async callback({event, say}) {
		let bolt:any = this;
		let member = bolt.getById(event.user, bolt.memberService.members);
		let memberName = (member.real_name) ? member.real_name : member.name;
		return await say(`Hello ${memberName}. I am ready to learn.`);
	}
}
