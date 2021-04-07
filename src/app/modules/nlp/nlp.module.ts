import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NlpService } from './nlp.service';
import { BoltService } from '../slack/bolt/bolt.service';
@NgModule({
	declarations: [],
	exports: [],
	imports: [
		CommonModule
	],
	providers: [
		NlpService
	]
})
export class NlpModule {
	private map: any = {
		freqdist: this.freqdist
	}
	constructor(
		private boltService:BoltService,
	) {
		Object.keys(this.map).forEach(m => {
			let regex = new RegExp(`${m}`);
			//this.boltService.messageService.listen(regex, this.freqdist.bind(this))
			//this.boltService.app.message(regex, this.freqdist.bind(this))
			//console.log(this.boltService);
		})

	}
	public freqdist({ event, say }) {
		console.log(event);
	}
}
