import { Injectable } from '@angular/core';
import { BoltService } from '@app/modules/slack/bolt.service';
import { LoggerService } from '@services/logger.service';
import { ApiService } from '@services/api.service';

import * as nlp from 'compromise';
@Injectable({
  	providedIn: 'root'
})
export class JibotService {
	private objNames: any = {
		members: this.boltService.memberService.collectionNames
	};
	constructor(
		private logger: LoggerService,
		private boltService: BoltService,
		private apiService: ApiService,
	) {	}
	public init = this.initialize;
	private async initialize() {
		this.logger.log(`Initializing ${this.constructor.name}...`);
		await this.boltService.init()
			.finally(this.favoriteBook.bind(this))
			.finally(async () => {
				this.logger.log(`${this.constructor.name} initialized...`);
			})
			.catch(this.logger.error);
		return;
	}
	private favoriteBook() {
		this.logger.log(`Loading favorite book routine...`);
		let bookTitles = Object.keys(this.apiService.books);
		let title = bookTitles[0];
		let book = this.apiService.books[title];
		let guess:any = { text:	title };
		let guessRegex = new RegExp(`.*(${guess.text}).*`);
		let guessCallback = async ({ event, say }) => {
			let user = this.boltService.getById(event.user, this.boltService.collections[this.objNames.members.local]);
			return await say(`*Congratulations* ${user.real_name}! You correctly guessed that I am reading ${guess.text}!`);
		};
		this.boltService.app.message(guessRegex, guessCallback.bind(this));
		book.get.subscribe(async (contents:string) => {
			book.contents = contents;
			this.readBook(book);
		});
	}

	private readBook(book) {
		this.logger.log(`Reading '${book.title}'...`);
		let keywords = [];
		let normalizeOptions = {
			punctuation: true,
			quotations: true,
			whitespace:true,
			possessives:true,
		}
		book.doc = nlp.default(book.contents).normalize(normalizeOptions);
		// .normalize({
		// 	// abbreviations: true,
		// 	// acronyms: true,
		// 	// honorifics: true,
		// 	// hyphenated:	true,
		// 	// punctuation: true,
		// 	// quotations: true,
		// 	// whitespace:true,
		// 	// possessives:true,
		// });
		// @TODO: We are going to want a nlp service or module
		// @TODO We are going to want to use CG natural language API for heavier thinking than this
		let nouns = ['people', 'places'];
		nouns.forEach(noun => {
			this.logger.log(`Saving ${noun}...`);
			book[noun] = book.doc[noun]().unique().normalize(normalizeOptions);
			book[noun].json().forEach(thing => {
				let hint:any = {
					text:	thing.text.replace(/[^\w\s]$/g, ''),
					terms: 	thing.terms,
					noun: 	nlp.default(noun).nouns().toSingular().text()
				};
				let hintCallback = async ({ event, say }) => {
					let user = this.boltService.getById(event.user, this.boltService.collections[this.objNames.members.local]);
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
}