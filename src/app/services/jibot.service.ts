import { Injectable } from '@angular/core';
import { BoltService } from '@app/modules/slack/bolt.service';
import { LoggerService } from '@services/logger.service';
import { ApiService } from '@services/api.service';

import * as language from '@google-cloud/language';
// import * as nlp from 'compromise';
// import * as ngrams from 'compromise-ngrams';
// import * as paragraphs from 'compromise-paragraphs';
// import * as scan from 'compromise-scan';

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

	private async thing(contents) {
		let languageClient = new language.LanguageServiceClient({fallback: true});

		let text = "There was once a dog born in Spain, and his name was Gordo, and he was a very good and silly dog.";
		let document:any = {
			content: contents,
			type: "PLAIN_TEXT"
		};
		let [result] = await languageClient.analyzeSentiment({document: document});
		return result.documentSentiment;
	}

	private readBook(book) {
		// nlp.default.extend(ngrams);
		// nlp.default.extend(paragraphs);
		// nlp.default.extend(scan);
		this.logger.log(`Reading '${book.title}'...`);
		//console.log(book.contents);

		this.thing(book.contents).then(r => {
			console.log("ALSKJDLAKSJDLKASJD");
		});




		//let nouns = ['places'];
		//let keywords = [];
		// book.doc = nlp.default(book.contents).normalize({
		// 	abbreviations: true,
		// 	acronyms: true,
		// 	honorifics: true,
		// 	hyphenated:	true,
		// 	punctuation: true,
		// 	quotations: true,
		// 	whitespace:true,
		// 	possessives:true,
		// });
		// @TODO: We are going to want a nlp service or module
		// @TODO We are going to want to use CG natural language API for heavier thinking than this
		// nouns.forEach(noun => {
		// 	this.logger.log(`Saving ${noun}...`);
		// 	book[noun] = book.doc[noun]().unique().normalize({
		// 		punctuation: false,
		// 		whitespace:true,
		// 	}).sort('freq');
		// 	book[noun].json().forEach(thing => {
		// 		let hint:any = {
		// 			text:	thing.text.replace(/[^\w\s]$/g, ''),
		// 			terms: 	thing.terms,
		// 			noun: 	nlp.default(noun).nouns().toSingular().text()
		// 		};
		// 		let hintCallback = async ({ event, say }) => {
		// 			let user = this.boltService.getById(event.user, this.boltService.collections[this.objNames.members.local]);
		// 			hint.message = [
		// 				`HI ${user.real_name}! You mentioned ${hint.text}!`,
		// 				`I am reading a book related to this ${hint.noun}.`,
		// 				`Can you guess what book I am reading?`,
		// 			];


		// 			// ref.forEach(r => {
		// 			// 	let ref = r;
		// 			// 	console.log(ref.text);
		// 			// 	console.log(ref.terms.tags.first());
		// 			// });
		// 			// console.log("!!");
		// 			return await say(hint.message.join(' '));
		// 		}
		// 		let textRegex, regex;
		// 		try {
		// 			textRegex = hint.text.replace(/([.\*])/,'\$1');
		// 			regex = new RegExp(`.*(${textRegex}).*`, 'i');
		// 			if (!keywords[hint.text]) {
		// 				keywords[hint.text] = thing.terms;
		// 				this.boltService.app.message(regex, hintCallback.bind(this));
		// 			} else {
		// 				keywords[hint.text] = { ...keywords[hint.text], ...thing.terms };
		// 			}
		// 		} catch (e) {
		// 			console.error(e);
		// 		}
		// 	});
		// });

		// let paras = book.doc.paragraphs();
		// console.log(paras.json().length);


		//console.log(book.nouns.if("bag").json());
		//console.log(book.doc.lookup(keywords));
		// let refs = book.doc.lookup("Chicago").json();
		// let tagArray = [];
		// refs.forEach(ref => {
		// 	ref.terms.forEach(term => tagArray.push(term.tags));
		// });
		// //let b = new Set(tagsArray).values();
		// console.log();
		//this.logger.log(Object.keys(keywords).join(', '));
		return;
	}
}
