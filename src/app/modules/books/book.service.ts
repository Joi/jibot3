import { Injectable } from '@angular/core';
import { environment } from '@env/environment';
import { BoltService } from '@modules/slack/bolt/bolt.service';
import { LoggerService } from '@app/services';
import { ApiService } from '../api/api.service';
import { first, map } from 'rxjs/operators';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BookService {
	constructor(
		private logger: LoggerService,
		private api:ApiService,
		private boltService: BoltService,
	) { }
	public books: any = {};
	private apiOptions:any = {
		...this.api.presets.text,
		params: new HttpParams().set('$$app_token', environment.GUTENBERG_TOKEN)
	};
	public init() {
		this.apiOptions.headers.set('$$app_token', environment.GUTENBERG_TOKEN);
		this.getBooks().then(books => {
			books.forEach(book => {
				this.logger.log(`Getting '${book.name}'...`);
				this.books[book.name] = this.api.get(book.url, this.apiOptions).pipe(
					map(this.trim.bind(this))
				);
				this.books[book.name].subscribe(
					(content) => {
						this.books[book.name].content = content;
						this.read(book);
					},
					console.error
				)
			})
		})

	}
	private read(book) {
		this.logger.log(`Reading '${book.name}'...`);
	}
	private guess(book) {

	}
	private async getBooks() {
		return await [
			{
				name: '2 B R 0 2 B',
				url: 'https://www.gutenberg.org/cache/epub/21279/pg21279.txt',
			},
			// {
			// 	name: 'The Mysterious Island',
			// 	url: "https://www.gutenberg.org/files/1268/1268-0.txt",
			// }
		]
		// @TODO: replace this with a getter

	}
	private trim(gutenberg) {
		this.logger.log(`Trimming gutenberg book...`);
		let tab = `\\t`, space = '\\s', nonSpace = '\\S', newline = `[\\r\\n]`,
			trailingSpace = `[${tab}]*${newline}+[${tab}]*`,
			splats = '[\\*]{3}';
		let startRegex = `(${newline}${splats} START .*${splats}${trailingSpace})`,
			endRegex = `${newline}End of the Project Gutenberg EBook of .+${newline}`,
			contentRegex = new RegExp(`(${startRegex}(.[${space}${nonSpace}]*)${endRegex})`, 'g'),
			eightyCharLineRegex = new RegExp(`(${nonSpace}).${newline}{1}(${nonSpace})`, 'gs');
		let contents = contentRegex.exec(gutenberg);
		//.replace(eightyCharLineRegex, '')
		return (contents) ? contents[3] : gutenberg;
	}
}
