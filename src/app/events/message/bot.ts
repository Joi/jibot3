import { Injectable} from '@angular/core';
import { BoltMessage } from '@app/interfaces/bolt-message';
@Injectable()
export class Bot implements BoltMessage {
	private rot13 = (str) => str.split('').map(char => String.fromCharCode(char.charCodeAt(0) + (char.toLowerCase() < 'n' ? 13 : -13))).join('');
	public name =	'heybot';
	public regex =	/(bot).*/;
	public async callback({event, say}) {
		return await say(this.rot13(event.text));
	}
}
