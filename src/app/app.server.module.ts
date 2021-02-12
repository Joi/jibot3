import { NgModule, APP_INITIALIZER } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';

import { BoltService } from '@services/bolt.service';
import { ApiService } from '@services/api.service';

import * as Events from '@app/events'
import * as Messages from '@app/events/message';
@NgModule({
	bootstrap: [AppComponent],
	declarations: [],
	imports: [
		AppModule,
		ServerModule,
	],
	providers: [
		{
			provide: APP_INITIALIZER,
			useFactory: (boltService: BoltService) => () => boltService.init(),
			deps: [BoltService],
			multi: true
		},
		Events.AppMention,
		Messages.Rot13,
	]
})
export class AppServerModule { }