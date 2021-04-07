import { Injectable } from '@angular/core';
import { BoltService } from '@modules/slack/bolt/bolt.service';

@Injectable({
	providedIn: 'root'
})
export class NlpService   {
	constructor(
		private boltService: BoltService,
	) {
		console.error(this.boltService);
	}
}
