import { NgModule, APP_INITIALIZER, InjectionToken } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';
// import * as sqlite from 'sqlite';
// import * as sqlite3 from 'sqlite3';
import {
	ApiModule,
	SlackModule
} from './modules';

@NgModule({
	bootstrap: [AppComponent],
	declarations: [ ],
	exports: [
		SlackModule,
		ApiModule
	],
	imports: [
		AppModule,
		ServerModule,
	],
	providers: [
		ApiModule,
		// {
		// 	provide: APP_INITIALIZER,
		// 	useClass: sqlite3.Database,
		// }
		// {
		// 	provide: NlpjsModule,
		// 	useFactory: (nlpjs:NlpjsModule) => () => {

		// 	}
		// }
	]
})
export class AppServerModule {
	constructor() {}
}