import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BoltService } from './bolt.service';
import { EventService } from './events/event.service'
import * as Events from './events';
import * as Messages from './messages';
@NgModule({
	declarations: [ ],
	exports: [ ],
	imports: [
		CommonModule
	],
	providers: [
		BoltService,
		EventService,
		Events.AppMention,
		Messages.Rot13,
	]
})
export class SlackModule { }
