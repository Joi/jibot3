import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { AppModule } from '@app/app.module';
import { AppComponent } from '@app/app.component';
import { BoltService } from './modules/server/slack/bolt/bolt.service';
import { AppMention } from './modules/server/slack/events';
import { Rot13 } from './modules/server/slack/messages';
import { SlackModule } from '@modules/server/slack/slack.module';
import { BookService } from './modules/server/books/book.service';
import * as nlp from 'compromise';
import { tap } from 'rxjs/operators';
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
	providers: [
		BookService,
		BoltService,
		AppMention,
		Rot13
	]
})
export class AppServerModule {
	private favoriteBookGame() {
		this.bookService.read().pipe(
			tap(books => {
				books.forEach(book => {
					let keywords = [];
					let normalizeOptions = {punctuation: true, quotations: true, whitespace:true, possessives:true};
					book['doc'] = nlp.default(book.content).normalize(normalizeOptions);
					['people', 'places', 'organizations'].forEach(noun => {
						console.log(`Saving ${noun}...`);
						book[noun] = book.doc[noun]().unique().normalize(normalizeOptions);
						book[noun].json().forEach(thing => {
							let hint:any = {
								text:	thing.text.replace(/[^\w\s]$/g, ''),
								terms: 	thing.terms,
								noun: 	nlp.default(noun).nouns().toSingular().text()
							};
							let hintCallback = async ({ event, say }) => {
								let user = this.boltService.getById(event.user, 'members');
								hint.message = [
									`HI ${user.real_name}! You mentioned ${hint.text}!`,
									`I am reading a book related to this ${hint.noun}.`,
									`Can you guess what book I am reading?`,
								];
								return await say(hint.message.join(' '));
							}
							let textRegex, regex;
							try {
								textRegex = hint.text.replace(/([.\*])/,'\$1');
								regex = new RegExp(`\\b(${textRegex})\\b`, 'i');
								if (!keywords[hint.text]) {
									keywords[hint.text] = thing.terms;
									this.boltService.app.message(regex, hintCallback.bind(this));
								} else {
									keywords[hint.text] = { ...keywords[hint.text], ...thing.terms };
								}
							} catch (e) {
								console.error(e);
							}
						});
					});
				})
			})
		).subscribe();
	}
	constructor(
		private boltService:BoltService,
		private bookService: BookService,
	) {
		this.favoriteBookGame();
	}
}