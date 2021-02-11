import { Injectable} from '@angular/core';
import { BoltMessage } from '@app/interfaces/bolt-message';
@Injectable()
export class Rot13 implements BoltMessage {
	public name =	'rot13';
	public regex =	/(bot).*/;
	public async callback({event, say}) {
		let rot13 = (str) => str.split('').map(char => String.fromCharCode(char.charCodeAt(0) + (char.toLowerCase() < 'n' ? 13 : -13))).join('');
		return await say(rot13(event.text));
	}
}