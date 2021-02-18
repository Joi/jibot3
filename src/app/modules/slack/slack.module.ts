import { APP_INITIALIZER, NgModule, Provider } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BoltService } from './bolt.service';
import { EventService } from './events/event.service'
import * as Events from './events';
import * as Messages from './events/message';

@NgModule({
	declarations: [],
	imports: [
		CommonModule
	],
	providers: [
		EventService,
		// {
		// 	provide: APP_INITIALIZER,
		// 	useFactory: (boltService: BoltService) => () => boltService.init(),
		// 	deps: [BoltService],
		// 	multi: true
		// },
		Events.AppMention,
		Messages.Rot13,
	]
})
export class SlackModule { }
