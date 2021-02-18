import { NgModule, APP_INITIALIZER } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from './app.component';
import { SlackModule } from './modules/slack/slack.module';
import { JibotService } from '@services/jibot.service';
import { ApiService } from '@services/api.service';
import { BoltService } from './modules/slack/bolt.service';
@NgModule({
	bootstrap: [AppComponent],
	declarations: [],
	imports: [
		AppModule,
		ServerModule,
		SlackModule,
	],
	providers: [
		SlackModule,
		{
			provide: APP_INITIALIZER,
			useFactory: (jibotService: JibotService) => () => jibotService.init(),
			deps: [JibotService],
			multi: true
		}
	]
})
export class AppServerModule { }