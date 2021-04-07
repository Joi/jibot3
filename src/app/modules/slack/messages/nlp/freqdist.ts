
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
			let urlRegex = new RegExp(/url:<(.*)>/);
			let urlParam;
			let extension = 'png';
			console.log(event);
			if (urlRegex.test(event.text)) {
				urlParam = event.text.match(urlRegex)[1];
				let url = `http://localhost:4200/freqdist.${extension}?url=${urlParam}`
				let params = {...bolt.fetcher.presets[extension] };
				bolt.fetcher.fetch(url, params)
					.subscribe(
						async (response) => {
							return await bolt.client.value.files.upload({
								channels: event.channel,
								title: "Frequency Distribution Graph",
								initial_comment: urlParam,
								file: Readable.from(Buffer.from(response)),
							})
						},
						(error) => console.log(error)
					)
			}
		}
	}

	public png(response:HttpResponse<any>) {
		console.log(response);
	}
}
