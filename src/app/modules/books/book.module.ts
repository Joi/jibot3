import {  NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BookService, BookServiceFactory } from './book.service';
import { FetcherService } from '@services/fetcher.service';
import { HttpClient } from '@angular/common/http';
import { BoltService } from '../slack/bolt/bolt.service';
import { tap } from 'rxjs/operators';
import * as nlp from 'compromise';
@NgModule({
	declarations: [	],
	exports: [
        RouterModule
    ],
	imports: [
		CommonModule,
        RouterModule,
	],
	providers: [
        FetcherService,
		{
			provide: BookService,
			useFactory: BookServiceFactory,
			deps: [HttpClient, FetcherService]
		}
	]
})
export class BookModule {
    constructor(
        private boltService:BoltService,
		private bookService: BookService,
    ) {
        this.favoriteBookGame();
    }
    private favoriteBookGame() {
        this.bookService.read().pipe(
			tap(books => {
				books.forEach(book => {
					let keywords = [];
					let normalizeOptions = {punctuation: true, quotations: true, whitespace:true, possessives:true};
					let doc;
                    let updateBook: boolean = false;
                    ['people', 'places', 'organizations'].forEach(noun => {
                        if (!book[noun]) {
                            if (!doc) {
                                doc = nlp.default(book.content).normalize(normalizeOptions);
                            }
                            book[noun] = JSON.stringify(doc[noun]().unique().normalize(normalizeOptions).json());
                        }
                        let nouns = JSON.parse(book[noun]);
                        Object.keys(nouns).forEach(i => {
                            let thing = nouns[i];
                            if (thing.text) {
                                let hint:any = {
                                    text:   thing.text.replace(/[^\w\s]$/g, ''),
                                    terms: 	thing.terms,
                                    noun: 	nlp.default(noun).nouns().toSingular().text()
                                }
                                let hintCallback = async ({ event, say }) => {
                                    hint.message = [
                                        `HI <@${event.user}>! You mentioned ${hint.text}!`,
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
                                        this.boltService.app.value.message(regex, hintCallback.bind(this));
                                    } else {
                                        keywords[hint.text] = { ...keywords[hint.text], ...thing.terms };
                                    }
                                } catch (e) {
                                    console.error(e);
                                }
                            }
                        });
                    });
                    // console.log(Object.keys(keywords));
                    if (updateBook) {
                        this.bookService.update(book).subscribe();
                    }
				})
			})
		).subscribe();
    }
}
