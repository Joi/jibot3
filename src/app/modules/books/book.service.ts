import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DatabaseService } from '@app/services/database.service';
import { FetcherService } from '@services/fetcher.service';
import * as nlp from 'compromise';
import { tap } from 'rxjs/operators';
@Injectable({
  providedIn: 'root'
})
export class BookService extends DatabaseService {
    constructor(
        http: HttpClient,
        private fetcher: FetcherService
    ) {
        super(http, "books");
    }
    public getContent(book) {
        console.log(`Retrieving ${book.title} from ${book.url}...`);
        let params = { ...this.fetcher.presets.text };
        return this.fetcher.fetch(book.url, params)
        // .pipe(
        //     tap(content => {
        //         book.content = content;
        //         //console.log(typeof content);
        //         //book.content = content;
        //         this.update(book);
        //     })
        // )
    }
    public nlp(book) {
        let normalizeOptions = {
			punctuation: true,
			quotations: true,
			whitespace:true,
			possessives:true,
		}
		let keywords = [];
		// book.doc = nlp.default(book.content).normalize(normalizeOptions);
		// ['people', 'places', 'organizations'].forEach(noun => {
		// 	book[noun] = book.doc[noun]().unique().normalize(normalizeOptions);
		// });
		return;
    }
}

export function BookServiceFactory(http:HttpClient, fetcher: FetcherService) {
	return new BookService(http, fetcher);
}