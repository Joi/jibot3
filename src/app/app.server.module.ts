import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from '@app/app.component';
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
	// providers: [
	// ]
})
export class AppServerModule {}