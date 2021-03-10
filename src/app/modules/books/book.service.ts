import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DatabaseService } from '@app/services/database.service';
import { FetcherService } from '@services/fetcher.service';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
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
    public getContent(book):Observable<any> {
        console.log(`Retrieving ${book.title} from ${book.url}...`);
        let params = {...this.fetcher.presets.text};
		return this.fetcher.fetch(`/gutenberg/${book.url}`, params).pipe(
            map(content => {
				if(book.url.includes("gutenberg.org/")) content = this.trim(content);
				book.content = content;
				return content;
            })
        );
    }
	private trim(gutenberg) {
		let tab = `\\t`, space = '\\s', nonSpace = '\\S', newline = `[\\r\\n]`,
			trailingSpace = `[${tab}]*${newline}+[${tab}]*`,
			splats = '[\\*]{3}';
		let startRegex = `(${newline}${splats} START .*${splats}${trailingSpace})`,
			endRegex = `${newline}End of the Project Gutenberg EBook of .+${newline}`,
			contentRegex = new RegExp(`(${startRegex}(.[${space}${nonSpace}]*)${endRegex})`, 'g'),
			eightyCharLineRegex = new RegExp(`(${nonSpace}).${newline}{1}(${nonSpace})`, 'gs');
		let content = contentRegex.exec(gutenberg);
		return (content) ? content[3].replace(eightyCharLineRegex, '') : gutenberg;
	}
}

export function BookServiceFactory(http:HttpClient, fetcher: FetcherService) {
	return new BookService(http, fetcher);
}