import { NgModule, APP_INITIALIZER, InjectionToken } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';

import { LoggerService } from '@services/logger.service';
import {
	//ApiModule,
	SlackModule
} from './modules';

const Logger = new InjectionToken('logger');
const factory = () => new LoggerService().init()
@NgModule({
	bootstrap: [AppComponent],
	declarations: [ ],
	exports: [
		SlackModule,
		//ApiModule
	],
	imports: [
		AppModule,
		ServerModule,
	],
	providers: [
		{
			provide: APP_INITIALIZER,
			deps: [LoggerService],
			useFactory: (logger:LoggerService) => () => logger.init(),
			multi: true,
		},
		// { provide: Location, useValue: 'https://angular.io/#someLocation' },
		// {
		// 	provide: Hash,
		// 	useFactory: (location: string) => location.split('#')[1],
		// 	deps: [Location]
		// }
	]
})
export class AppServerModule {
}