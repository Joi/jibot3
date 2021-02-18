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
		private apiService: ApiService
	) {	}
	public init = this.initialize;
	private async initialize() {
		this.logger.log(`Initializing ${this.constructor.name}...`);
		await this.apiService.init()
			.then(this.boltService.init)
			.finally(this.favoriteBook.bind(this))
			.finally(() => {
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
		book.get.subscribe(contents => {
			book.contents = contents;
		 	this.readBook(book);
		});
	}

	private readBook(book) {
		this.logger.log(`Reading '${book.title}'...`);
		let keywords = [];
		let nouns = ['people','places','topics'];
		book.doc = nlp.default(book.contents);
		nouns.forEach(noun => {
			book[noun] = book.doc[noun]().json();
			book[noun].forEach(thing => {
				let hint:any = {
					text:	thing.text.replace(/[^\w\s]+$/g, ''),
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
				let textRegex = hint.text.replace('.','\.');
				let regex = new RegExp(`.*(${textRegex}).*`, 'i');
				if (!keywords[hint.text]) {
					keywords[hint.text] = thing.terms;
					this.boltService.app.message(regex, hintCallback.bind(this));
				} else {
					//@TODO: Should we merge terms from different nouns?
				}
			});
		});
		this.logger.log(Object.keys(keywords).join(', '));
		return;
	}
}
