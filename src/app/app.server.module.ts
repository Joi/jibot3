import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';
import { SlackModule } from './modules/slack/slack.module';
@NgModule({
	bootstrap: [AppComponent],
	declarations: [ ],
	exports: [
		SlackModule,
	],
	imports: [
		AppModule,
		ServerModule,
	],
	providers: []
})
export class AppServerModule {
	constructor() { }
}