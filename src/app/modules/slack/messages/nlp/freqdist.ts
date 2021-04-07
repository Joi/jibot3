
import { HttpResponse } from '@angular/common/http';
import { Injectable} from '@angular/core';
import { Readable } from 'stream';
import * as Bolt from '../../bolt/bolt.interface';

@Injectable()
export class FreqDist  implements Bolt.Message {
	public name	=	'freqdist';
	public regex =	/(freqdist).*/;
	public async callback({event, say}) {
		if (this.constructor.name.toLowerCase() === "boltservice") {
			let bolt:any = this;
			let paramName, paramValue;
			let params: any = {
				url: new RegExp(/url:<(.*)>/),
				text: new RegExp(/text:\s*`(.*)`/),
			}
			Object.keys(params).forEach(name => {
				let regex = params[name];
				if (regex.test(event.text)) {
					paramName = name;
					paramValue = event.text.match(regex)[1];
				}
			});
			let extension = 'png';
			let url = `http://localhost:4200/freqdist.${extension}?${paramName}=${paramValue}`;
			bolt.fetcher
				.fetch(url, {...bolt.fetcher.presets[extension] })
				.subscribe(
					async (response) => {
						return await bolt.client.value.files.upload({
							channels: event.channel,
							title: (paramName == 'url') ? `From URL: ${paramValue}` : `From your provided text`,
							initial_comment: `<@${event.user}>, here is your frequency distribution graph:`,
							file: Readable.from(Buffer.from(response)),
						})
					},
					(error) => console.log(error)
				);
		}
	}
}
