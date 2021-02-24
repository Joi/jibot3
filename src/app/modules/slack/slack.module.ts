import { APP_INITIALIZER, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { environment } from '@env/environment';

import { BooksModule } from '@modules/books/books.module';
import { BoltService } from './bolt/bolt.service';

//import { ApiService } from '@modules/api/api.service';

import { AppOptions } from '@slack/bolt';
import * as Events from './events';
import * as Messages from './messages';

//import { ApiService } from '../api/api.service';
@NgModule({
	declarations: [ ],
	exports: [BooksModule],
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
		Events.AppMention,
		Messages.Rot13,
	]
})
export class SlackModule { }