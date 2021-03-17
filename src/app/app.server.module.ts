import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from '@app/app.component';
import { BoltService } from '@modules/slack/bolt/bolt.service';
import { AppMention } from '@modules/slack/events';
import { Rot13 } from '@modules/slack/messages';
import { SlackModule } from '@modules/slack/slack.module';
import { BookModule } from './modules/books/book.module';
@NgModule({
	bootstrap: [AppComponent],
	declarations: [ ],
	exports: [
		SlackModule,
        BookModule,
	],
	imports: [
		AppModule,
		ServerModule,
	],
	providers: [
		BoltService,
		AppMention,
		Rot13
	]
})
export class AppServerModule {}