import { NgModule, APP_INITIALIZER, InjectionToken } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';
import { LoggerService } from '@services/logger.service';
//import { NlpjsModule } from 'nlpjs';
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
		//NlpjsModule,
	]
})
export class AppServerModule {
	// constructor() {
	// 	console.log(nlpjs);
	// }
}