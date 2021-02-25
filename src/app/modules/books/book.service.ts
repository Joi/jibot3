import { Injectable } from '@angular/core';
import { BoltService } from '@modules/slack/bolt/bolt.service';
import { LoggerService } from '@app/services';
import { ApiService } from '../api/api.service';
import { map } from 'rxjs/operators';
import * as nlp from 'compromise';
import { threadId } from 'worker_threads';

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
	public favoriteBook: any;
	private apiOptions:any = {
		...this.api.presets.text,
	};
	public init() {
		this.getBooks().then(books => {
			books.forEach(book => {
				this.logger.log(`Getting '${book.name}'...`);
				this.books[book.name] = {
					name: book.name,
					sub: this.api.get(book.url, this.apiOptions).pipe(
						map(this.trim.bind(this))
					).toPromise()
					.then(content => this.books[book.name].content = content)
					.then(() => this.read(this.books[book.name]))
					.then(() => (books.indexOf(book) === 0) ? this.guess(this.favoriteBook = this.books[book.name]): null)
					.catch(console.error)
				};
			})
		})
	}
	private getBooks = async () => [
		// {
		// 	name: '2 B R 0 2 B',
		// 	url: 'https://www.gutenberg.org/cache/epub/21279/pg21279.txt',
		// },
		{
			name: 'The Mysterious Island',
			url: "https://www.gutenberg.org/files/1268/1268-0.txt",
		},
		// {
		// 	name: 'The Time Machine',
		// 	url: 'https://www.gutenberg.org/files/35/35-0.txt',
		// }
	];
	private read(book) {
		this.logger.log(`Reading '${book.name}'...`);
		let normalizeOptions = {
			punctuation: true,
			quotations: true,
			whitespace:true,
			possessives:true,
		}
		let keywords = [];
		book.doc = nlp.default(book.content).normalize(normalizeOptions);
		['people', 'places', 'organizations'].forEach(noun => {
			this.logger.log(`Saving ${noun}...`);
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
		this.logger.log(Object.keys(keywords).join(', '));
		return;
	}
	public guess(book) {
		this.logger.log(`Loading favorite book routine...`);
		let guess:any = { text:	book.name };
		let guessRegex = new RegExp(`.*(${guess.text}).*`);
		let guessCallback = async ({ event, say }) => {
			let user = this.boltService.getById(event.user, 'members');
			return await say(`*Congratulations* ${user.real_name}! You correctly guessed that I am reading ${guess.text}!`);
		};
		//this.boltService.app.message(guessRegex, guessCallback.bind(this));
		// book.get.subscribe(async (contents:string) => {
		// 	book.contents = contents;
		// 	this.readBook(book);
		// });
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
