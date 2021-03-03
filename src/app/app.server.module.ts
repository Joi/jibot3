import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';

import {
	ApiModule,
	SlackModule
} from './modules';


@NgModule({
	bootstrap: [AppComponent],
	declarations: [ ],
	exports: [
		SlackModule,
		ApiModule,
	],
	imports: [
		AppModule,
		ServerModule,
	],
	providers: [
		ApiModule,
	]
})
export class AppServerModule {
	constructor() {

	}
}