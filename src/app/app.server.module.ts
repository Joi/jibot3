import { NgModule, APP_INITIALIZER, InjectionToken } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';
import { LoggerService } from '@services/logger.service';

import * as nlphs from 'nlpjs';
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
	providers: []
})
export class AppServerModule {
}