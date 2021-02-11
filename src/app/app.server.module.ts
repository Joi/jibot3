import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from '@app/app.component';
import { BoltService } from '@services/bolt.service';
import { LoggerService } from './services/logger.service';
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
		Events.AppMention,
		Messages.Rot13,
	]
})
export class AppServerModule {
	constructor(
		private boltService: BoltService,
		private loggerService: LoggerService
	) {
		this.boltService.init().then((r) => this.loggerService.log(`Bolt initialized...`));
	}
}