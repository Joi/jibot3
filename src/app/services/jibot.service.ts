import { Injectable } from '@angular/core';
import { BoltService } from '@app/modules/slack/bolt.service';
import { LoggerService } from '@services/logger.service';
import { ApiService } from '@services/api.service';
import * as nlp from 'compromise';
import { App } from '@slack/bolt';

@Injectable({
  	providedIn: 'root'
})
export class JibotService {
	private boltApp: App;
	private objNames: any;
	constructor(
		private logger: LoggerService,
		private boltService: BoltService,
		private apiService: ApiService
	) {
		this.objNames = {
			members: this.boltService.memberService.collectionNames
		}
	}
	public init = this.initialize;
	private async initialize() {
		this.logger.log(`Initializing ${this.constructor.name}...`);
		return await this.apiService.init()
			.then(this.boltService.init)
			.then(app => (this.boltApp = app))
			.then(this.favoriteBook.bind(this))
			.finally(() => {
				this.logger.log(`${this.constructor.name} initialized...`);
			});
	}
	private favoriteBook() {
		this.logger.log(`Loading favorite book routine...`);
		Object.keys(this.apiService.books).forEach(title => {
			let book:any = this.apiService.books[title];
			let guess:any = { text:	title };
			let guessRegex = new RegExp(`.*(${guess.text}).*`);
			let guessCallback = async({ event, say }) => {
				let user = this.boltService.getById(event.user, this.boltService.collections[this.objNames.members.local]);
				return await say(`*Congratulations* ${user.real_name}! You correctly guessed that I am reading ${guess.text}!`);
			};
			this.boltApp.message(guessRegex, guessCallback.bind(this));
			if (!book.contents) book.get.subscribe(contents => {
				book.contents = contents;
				book.doc = nlp.default(book.contents);
				this.readBook(book);
			});
		});
		return;
	}
	private readBook(book) {
		let keywords = {};
		let nouns = ['people','places'];
		nouns.forEach(noun => {
			book[noun] = book.doc[noun]().json();
			book[noun].forEach(thing => {
				let hint:any = {
					text:	thing.text.replace(/[^\w\s]+$/g, ''),
					terms: 	thing.terms,
					noun: 	nlp.default(noun).nouns().toSingular().text()
				};
				let hintCallback = ({ event, say }) => {
					let user = this.boltService.getById(event.user, this.boltService.collections[this.objNames.members.local]);
					hint.message = [
						`HI ${user.real_name}! You mentioned ${hint.text}!`,
						`I am reading a book related to this ${hint.noun}.`,
						`Can you guess what book I am reading?`,
					];
					return say(hint.message.join(' '));
				}
				let keyword = hint.text.replace('.','\.');
				let regex = new RegExp(`.*(${keyword}).*`, 'i');
				if (!keywords[hint.text]) {
					keywords[hint.text] = thing.terms;
					this.boltApp.message(regex, hintCallback.bind(this));
				} else {
					//@TODO: Should we merge terms from different nouns?
				}
			});
		});
	}
}
