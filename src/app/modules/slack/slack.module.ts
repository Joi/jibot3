import { APP_INITIALIZER, InjectionToken, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { App, AppOptions } from '@slack/bolt';
import { environment } from '@env/environment';
import { BoltService } from './bolt/bolt.service';
import * as Events from './events';
import * as Messages from './messages';
import { MessageService } from './messages/message.service';
import { BehaviorSubject } from 'rxjs';
@NgModule({
	declarations: [ ],
	exports: [],
	imports: [CommonModule],
	providers: [
		{
			provide:APP_INITIALIZER,
			deps: [BoltService],
			multi: true,
			useFactory: (bolt: BoltService) => () => bolt.init(<AppOptions>{
				clientId:		environment.SLACK_CLIENT_ID,
				clientSecret:	environment.SLACK_CLIENT_SECRET,
				token:			environment.SLACK_BOT_TOKEN,
				appToken:		environment.SLACK_APP_TOKEN,
				signingSecret:	environment.SLACK_SIGNING_SECRET,
			}),
		},
		BoltService,
		// MessageService,
		// Events.AppMention,
		// Messages.Rot13,
	]
})
export class SlackModule  {
	// private boltApp: BehaviorSubject<App> = this.bolt.app;
	// private messageListeners: any[] = [
	// 	new Messages.Rot13(),
	// ];
	// private eventListeners: any[] = [
	// 	new Events.AppMention()
	// ]
	constructor(
		// private bolt: BoltService
	) {
		// this.boltApp.subscribe(app => {
		// 	if (app) {
		// 		this.messageListeners.forEach(this.bolt.messages.listen.bind(this.bolt));
		// 		//this.eventListeners.forEach(this.bolt.events.listen.bind(this.bolt));
		// 		this.eventListeners.forEach(console.log);
		// 	}
		// });
		//this.boltService.eventService.listen(Events.AppMention)
	}
}